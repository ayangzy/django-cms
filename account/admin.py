from django.contrib import admin
from account.models import *

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')
    
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)

