from django.db import models
from solo.models import SingletonModel


class TropipayConfig(SingletonModel):
    tpp_client_id = models.CharField(max_length=255, null=True, blank=True)
    tpp_client_secret = models.CharField(max_length=255, null=True, blank=True)
    tpp_client_email = models.EmailField(null=True, blank=True)
    tpp_client_password = models.CharField(max_length=255, null=True, blank=True)
    tpp_url = models.CharField(null=True, blank=True, default='www.tropipay.com', max_length=255)
    tpp_success_url = models.URLField(null=True, blank=True)
    tpp_failed_url = models.URLField(null=True, blank=True)
    tpp_notification_url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = 'Configuración de Tropipay'

    def __str__(self): return 'Configuración de Tropipay'