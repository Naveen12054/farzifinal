from django.contrib import admin

# Register your models here.
from .models import FurniturePrediction,deliveryagent,Appointment
admin.site.register(FurniturePrediction)
admin.site.register(deliveryagent)
admin.site.register(Appointment)



