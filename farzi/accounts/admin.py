from django.contrib import admin
from .models import CustomUser,UserProfile,Category,Product,Subcategory
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)