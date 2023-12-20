from django.contrib import admin
from solo.admin import SingletonModelAdmin

from app_tropipay.models import TropipayConfig


# Register your models here.
@admin.register(TropipayConfig)
class TropipayConfigAdmin(SingletonModelAdmin):
    pass
