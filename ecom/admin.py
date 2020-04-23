from django.contrib import admin
from . models import product , contact , Orders

# Register your models here.
admin.site.register(product)
admin.site.register(contact)
admin.site.register(Orders)
