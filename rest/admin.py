from django.contrib import admin

# Register your models here.
from .models import FurniturePrediction,deliveryagent,Appointment,DeliveryAgentProfile,Furniturerent,Addressuser,Rent,ServiceBooking
admin.site.register(FurniturePrediction)
admin.site.register(deliveryagent)
admin.site.register(Appointment)
admin.site.register(Addressuser)
admin.site.register(Furniturerent)
admin.site.register(DeliveryAgentProfile)
admin.site.register(Rent)
admin.site.register(ServiceBooking)










