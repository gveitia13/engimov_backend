import datetime
import http.client
import json
from hashlib import sha1, sha256

import pytz
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_cart.cart import Cart
from app_tropipay.models import TropipayConfig
from core.models import EnterpriseData, Orden, Product, ComponenteOrden
from core.serializers import OrdenSerializer


# Create your views here.
# @csrf_exempt
@api_view(['POST'])
def pay(request):
    if request.method == 'POST':
        print('llego')
        if EnterpriseData.objects.all()[0].checkout_allowed == True and TropipayConfig.objects.exists():
            print('llego2')
            tropipay_config: TropipayConfig = TropipayConfig.objects.first()
            purchase_data = json.loads(request.body.decode('utf-8'))
            purchase_data['cart_id'] = request.headers.get('Cart-Id')
            print(purchase_data)
            # try:
            orden: (Orden | None) = create_order(purchase_data, **{})
            if orden:
                print('llego3')
                mensaje = create_message_order(request, orden)
                conn = http.client.HTTPSConnection("" + tropipay_config.tpp_url + "")
                # genera un request json
                payload_tpp = {"grant_type": "client_credentials", "client_id": tropipay_config.tpp_client_id,
                               "client_secret": tropipay_config.tpp_client_secret}
                # hago la petition y capturo el response
                payload_tpp = json.dumps(payload_tpp)
                headers = {'Content-Type': "application/json"}
                # se hace el post
                conn.request("POST", "/api/v2/access/token", payload_tpp, headers)
                res = conn.getresponse()
                data = res.read()
                token = data.decode("utf-8")
                token = json.loads(token)['access_token']
                # Convertir total a 2 decimales
                address = 'Dirección: ' + orden.detalles_direccion
                client = {
                    'name': orden.nombre,
                    'lastName': orden.apellidos,
                    "address": address,
                    "phone": orden.telefono_comprador,
                    "email": orden.correo,
                    "countryId": 0,
                    "termsAndConditions": "true"
                }
                impuesto = orden.total * EnterpriseData.objects.first().tropipay_impuesto / 100
                if impuesto > 0:
                    orden_total = round((orden.total + impuesto + 0.5), 2) * 100
                else:
                    orden_total = round(orden.total, 2) * 100
                brazil_timezone = pytz.timezone("America/Sao_Paulo")
                brazil_time = datetime.datetime.now(brazil_timezone)
                payload_tpp = {
                    "reference": str(orden.uuid),
                    "concept": "Orden de Engimov a nombre de " + client['email'],
                    "favorite": "false",
                    "description": mensaje,
                    "amount": orden_total,  # para quitar decimales
                    "currency": 'USD',
                    "singleUse": "true",
                    "reasonId": 4,
                    "expirationDays": 0,
                    "lang": "es",
                    "urlSuccess": "" + tropipay_config.tpp_success_url + "",
                    "urlFailed": "" + tropipay_config.tpp_failed_url + "",
                    "urlNotification": "" + tropipay_config.tpp_notification_url + "",
                    "serviceDate": str(brazil_time.year) + '-' + str(brazil_time.month) + '-' + str(brazil_time.day),
                    "client": client,
                    "directPayment": "true",
                    "paymentMethods": ["EXT", "TPP"]
                }

                payload_tpp = json.dumps(payload_tpp)
                headers = {
                    'Content-Type': "application/json",
                    'Authorization': "Bearer " + token
                }
                conn.request("POST", "/api/v2/paymentcards", payload_tpp, headers)
                res = conn.getresponse()
                data = res.read()
                retorno = data.decode("utf-8")
                if 'error' in json.loads(retorno):
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    retorno = json.loads(retorno)['shortUrl']
                    orden.link_de_pago = retorno
                    orden.total = float('{:.2f}'.format(orden_total)) / 100
                    orden.save()
                    return Response(data={'payment_link': orden.link_de_pago}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt)
def tpp_success(request):
    uuid: str = request.GET.get('reference')
    uuid = uuid.replace('-', '')
    if Orden.objects.filter(pk=uuid).exists():
        orden = Orden.objects.get(pk=uuid)
        import time
        t_end = time.time() + 5
        while time.time() < t_end:
            if orden.status == '1':
                mensaje = create_message_order(request, orden)
                return redirect(
                    f'https://api.whatsapp.com/send/?phone=+{EnterpriseData.objects.all().first().tel}&text='
                    + mensaje.replace(" <br/> ", "\n") + '&app_absent=1')
        # Mandar pal fail
        return render(request, 'order_fail.html', {'uuid': uuid, 'business': EnterpriseData.objects.first()})
    return render(request, 'order_fail.html', {'uuid': uuid, 'business': EnterpriseData.objects.first()})


# TPP_Notification
@method_decorator(csrf_exempt)
def tpp_verificar(request: HttpRequest):
    if request.method == 'POST' and TropipayConfig.objects.exists():
        tropipay_config: TropipayConfig = TropipayConfig.objects.first()
        payload = json.loads(request.body)
        bankOrderCode = payload['data']['bankOrderCode']
        originalCurrencyAmount = payload['data']['originalCurrencyAmount']
        signature = payload['data']['signature']
        status = payload['status']
        referencia = payload['data']['reference']
        cadena = bankOrderCode + tropipay_config.tpp_client_email + sha1(
            tropipay_config.tpp_client_password.encode('utf-8')).hexdigest() \
                 + originalCurrencyAmount
        cadena = cadena.encode('utf-8')
        firma = sha256(cadena).hexdigest()
        if firma == signature:
            orden = get_object_or_404(Orden, pk=referencia)
            if status == 'OK':
                orden.status = '1'
                # Hice el descuento
                for i in orden.componente_orden.all():
                    prod = i.producto
                    prod.stock -= i.cantidad
                    prod.sales += i.cantidad
                    prod.save()
            else:
                orden.status = '2'
            orden.link_de_pago = "CONSUMIDO"
            orden.save()
            return HttpResponse('Verificando...')
    # fails alerta
    return render(request, 'order_fail.html',
                  {'uuid': request.session['last_order'], 'business': EnterpriseData.objects.first()})


def create_order(purchase_data, **kwargs):
    # Datos del formulario
    nombre = purchase_data['nombre']
    apellidos = purchase_data['apellidos']
    correo = purchase_data['correo']
    # municipio = Municipio.objects.get(pk=purchase_data['municipio'])
    detalles_direccion = purchase_data['detalles_direccion']
    telefono_comprador = purchase_data['telefono_comprador']
    # precio_envio = municipio.precio if moneda == 'CUP' else municipio.precio_euro
    # Calcular total
    cart = Cart()
    cart.session = purchase_data['cart_id']
    total = 0
    # taza_cambio = 1 if moneda == 'CUP' else EnterpriseData.objects.all().first().taza_cambio
    tiempo_de_entrega = 0
    if cart.get_all():
        print(cart.get_all())
        pks = [prod['sku'] for prod in cart.get_all()]
        products = Product.objects.filter(pk__in=pks)
        # Pastilla
        total += cart.get_total()
        for c in products:
            if int(c.delivery_time) > tiempo_de_entrega:
                tiempo_de_entrega = int(c.delivery_time)
        # Precio de envio
        # total += municipio.precio if moneda == 'CUP' else municipio.precio_euro
        orden = Orden(total=float(total), precio_envio=0, status='2', nombre=nombre, apellidos=apellidos,
                      detalles_direccion=detalles_direccion, tiempo_de_entrega=tiempo_de_entrega, correo=correo,
                      telefono_comprador=telefono_comprador)
        orden.save()
        for c in products:
            ComponenteOrden.objects.create(orden=orden, producto=c,
                                           respaldo=float(
                                               float(c.price) * int(cart.get(c.pk)['quantity'])),
                                           cantidad=int(cart.get(c.pk)['quantity']))
            # Aki se rebaja
            # if moneda == 'CUP':
            # c.stock = c.stock - int(cart.get(c.pk)['quantity'])
            # c.save()
        # Limpiar cart
        cart.clear()
        return orden
    return None


def create_message_order(request, orden: Orden):
    mensaje = 'Orden de compra:\n'
    mensaje += 'Ticket: ' + f'{str(orden.uuid)}\n'
    mensaje += 'Comprador: ' + orden.nombre + ' ' + orden.apellidos + '\n'
    mensaje += 'Teléfono del comprador: ' + orden.telefono_comprador + '\n'
    # mensaje += 'Precio de envío: ' + str(orden.precio_envio) + f' USD\n'
    mensaje += 'Precio total: ' + '{:.2f}'.format(orden.total) + f'USD\n'
    mensaje += 'Tiempo máximo de entrega: ' + str(orden.tiempo_de_entrega) + ' días\n\n'
    mensaje += 'Productos comprados: \n'
    for c in orden.componente_orden.all():
        mensaje += str(c) + '\n'
    mensaje += '\nDatos de entrega:\n'
    mensaje += f'Dirección: {orden.detalles_direccion}'
    return mensaje


def cancel_order(request, *args, **kwargs):
    orden = Orden.objects.get(pk=kwargs.get('pk'))
    orden.status = '3'
    orden.save()
    for c in orden.componente_orden.all():
        if c.producto:
            prod = c.producto
            prod.stock = prod.stock + c.cantidad
            prod.sales -= c.cantidad
            prod.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


def fail_order(request):
    if 'last_order' in request.session:
        return render(request, template_name='order_fail.html',
                      context={'uuid': request.session['last_order'], 'business': EnterpriseData.objects.first()})
    return redirect('index-euro')


class OrdenAPIList(generics.ListCreateAPIView):
    serializer_class = OrdenSerializer
    queryset = Orden.objects.all()


class OrdenAPIDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdenSerializer
    queryset = Orden.objects.all()
    lookup_field = 'uuid'
