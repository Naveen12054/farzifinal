from datetime import date, datetime
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from jsonschema import ValidationError
from accounts.models import Category, CustomUser


class FurniturePrediction(models.Model):
    image = models.ImageField(upload_to='uploads/')
    prediction = models.CharField(max_length=255)

class install(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_by_name', null=True)
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_by_email', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
    price = models.CharField(max_length=12)
    loacation = models.CharField(max_length=1000)
    loacation1 = models.CharField(max_length=1000)

    date = models.DateField()
    start_time = models.TimeField(null=True)
    status = models.BooleanField(default=False)
    del_status = models.BooleanField(default=False)


    def str(self):
            return str(self.name)


class Addressuser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    alternate_contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Address"

    def save(self, *args, **kwargs):
        max_addresses = 8
        existing_addresses = Addressuser.objects.filter(user=self.user).count()
        if existing_addresses >= max_addresses:
            raise ValidationError(f"A user can only have a maximum of {max_addresses} addresses.")
        super().save(*args, **kwargs)



class Furniturerent(models.Model):
    product_code = models.CharField(max_length=255)
    category = models.CharField(max_length=255,null=True)
    description = models.TextField()
    stock= models.CharField(max_length=100)
    product_images1 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    product_images2 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    product_images3 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    product_images4 = models.FileField(upload_to='sample/', null=True, blank=True, max_length=255)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    status=models.BooleanField(max_length=555,default=False)
    length = models.CharField(max_length=555,null=True)
    width = models.CharField(max_length=555,null=True)
    height = models.CharField(max_length=555,null=True)
    material = models.CharField(max_length=255)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    quality_standard = models.CharField(max_length=255)
    rentproduct=models.BooleanField(default=True)
    status1=models.BooleanField(default=True)
    def update_condition(self):
        today = timezone.now().date()
        if self.start_date <= today <= self.end_date:
            self.condition = "Renting"
        else:
            self.condition = "Not Available"
        self.save()

    
    def __str__(self):
        return self.product_code

class Rent(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    address=models.ForeignKey(Addressuser,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Furniturerent, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status=models.BooleanField(max_length=555,default=False)
    rejected=models.BooleanField(max_length=555,default=False)
    paid=models.BooleanField(max_length=555,default=False)
    deliverystatus=models.BooleanField(default=False)


class deliveryagent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    pin = models.CharField(max_length=6)
    mobile = models.CharField(max_length=10)
    status=models.BooleanField(default=False)
    rejected=models.BooleanField(default=False)



    def __str__(self):
        return self.name



class DeliveryAgentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='profile_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    insurance_expiry_date = models.DateField()
    longitude = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    banking_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    routing_number = models.CharField(max_length=20)
    max_delivery_distance = models.PositiveIntegerField()
    emergency_contact = models.CharField(max_length=15)
    status=models.BooleanField(default=False)
    rejected=models.BooleanField(default=False)
    accepted=models.BooleanField(default=False)
    pin = models.CharField(max_length=6, default='000000')  # Default pin value
    mobile = models.CharField(max_length=10, default='0000000000')


    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"
    


class Appointment(models.Model):
        TIME_CHOICES = [
            (datetime.strptime('09:00 AM', '%I:%M %p').time(), '09:00 AM'),
            (datetime.strptime('11:00 AM', '%I:%M %p').time(), '11:00 AM'),
            (datetime.strptime('01:00 PM', '%I:%M %p').time(), '01:00 PM'),
            (datetime.strptime('03:00 PM', '%I:%M %p').time(), '03:00 PM'),
            (datetime.strptime('05:00 PM', '%I:%M %p').time(), '05:00 PM'),
        ]

        

        date = models.DateField()
        client = models.ForeignKey(
            CustomUser, 
            on_delete=models.CASCADE, 
            related_name='client_appointments',
            limit_choices_to={'role': CustomUser.CUSTOMER}
        )
        
        time_slot = models.TimeField(choices=TIME_CHOICES,null=True)
        created_date = models.DateTimeField(auto_now_add=True, null=True)
        modified_date = models.DateTimeField(auto_now=True, null=True)
        cancelled_date = models.DateTimeField(null=True, blank=True)
        payment_status= models.BooleanField(default=False)
        status=models.BooleanField(default=False)
        status1=models.BooleanField(default=False)
        approved=models.BooleanField(default=False)
        viewed=models.BooleanField(default=False)
        rejected=models.BooleanField(default=False)
        user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        cost = models.CharField(max_length=10,default='0')
        totalcost = models.CharField(max_length=10,default='0')
        estimatedcost = models.CharField(max_length=10,default='0')
        mobile = models.CharField(max_length=10)
        location = models.CharField(max_length=1000)
        order_id = models.CharField(max_length=1000)
        desc = models.CharField(max_length=1000000)
        approved_timestamp = models.DateTimeField(null=True, blank=True)
        rejectionreason = models.CharField(max_length=100, null=True, default=None)

        def str(self):
            return f"Appointment with {self.client.name}  on {self.date} at {self.get_time_slot_display()}"
from django.db.models.signals import pre_save
class ServiceBooking(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    desc = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255, default='')
    mobile = models.IntegerField(default=0)
    pet_weight = models.FloatField(default=0.0)
    date = models.DateField(null=True)
    time_slot = models.CharField(max_length=50, default='')
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    rejectionreason = models.CharField(max_length=255, default='')
    estimatedcost = models.CharField(max_length=10,default='0')



        