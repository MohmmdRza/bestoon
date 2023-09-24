from django.contrib import admin
from saffron.models import *


class PaymentAdmin(admin.ModelAdmin):
    pass


class SaffronAdmin(admin.ModelAdmin):
    pass


class SaffronCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Saffron, SaffronAdmin)
admin.site.register(SaffronCategory, SaffronCategoryAdmin)