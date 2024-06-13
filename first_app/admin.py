from django.contrib import admin
from .models import Vehicle, Client, VehicleType, ServiceVIN, Service


admin.site.register(Vehicle)
admin.site.register(Client)
admin.site.register(VehicleType)
admin.site.register(ServiceVIN)
admin.site.register(Service)