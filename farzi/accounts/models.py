from datetime import timezone
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role=4
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    CUSTOMER = 1
    SELLER = 2
    DELIVERY = 3
    ADMIN = 4
    MAIN =5


    ROLE_CHOICE = (
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
        (DELIVERY, 'Delivery'),
        (ADMIN,'Admin'),
        (MAIN,'Main'),

    )

    username=None
    USERNAME_FIELD = 'email'
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True) 
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')

    # date_joined = models.DateTimeField(auto_now_add=True)
    # last_login = models.DateTimeField(auto_now_add=True)
    # created_date = models.DateTimeField(auto_now_add=True)
    # modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    district = models.CharField(max_length=15, blank=True, null=True)
    addressline1 = models.CharField(max_length=15, blank=True, null=True)
    addressline2 = models.CharField(max_length=15, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    aphone_no = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def str(self):
        if self.user:
            return self.user.email
        else:
            return "UserProfile with no associated user"
##############################################################################################################################################################3


class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    district = models.CharField(max_length=15, blank=True, null=True)
    addressline1 = models.CharField(max_length=15, blank=True, null=True)
    addressline2 = models.CharField(max_length=15, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    map = models.CharField(max_length=150, blank=True, null=True)
    gstno = models.CharField(max_length=15, blank=True, null=True)
    panno = models.CharField(max_length=15, blank=True, null=True)
    ownername = models.CharField(max_length=15, blank=True, null=True)
    aphone_no = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def str(self):
        if self.user:
            return self.user.email
        else:
            return "UserProfile with no associated user"
##############################################################################################################################################################3

class Category(models.Model):
    category_name = models.CharField(max_length=30, default='Unknown')
    category_image = models.ImageField(upload_to='pic', default='')
    descriptioncat = models.CharField(max_length=500, null=False, blank=False, default="Default category description")
    status=models.BooleanField(default=False)
    for_rent = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False, default="Default subcategory description")
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,related_name="user")
    brand_name = models.CharField(max_length=255, null=True)
    product_name = models.CharField(max_length=255, null=True,unique=True)
    material_description = models.TextField(max_length=555,null=True)
    product_description = models.TextField(max_length=555,null=True)
    price = models.DecimalField(max_digits=255,decimal_places=2, null=True)
    quantity = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE,related_name="cat1") # You can create a separate Category model if needed
    product_images1 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    product_images2 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    product_images3 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    product_images4 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    measurements = models.CharField(max_length=555,null=True)
    maintenance = models.CharField(max_length=555,null=True)
    color = models.CharField(max_length=255, null=True)
    status=models.BooleanField(max_length=555,default=False)
    admincontrol=models.BooleanField(max_length=555,default=False)

    

    def __str__(self):
        return self.product_name