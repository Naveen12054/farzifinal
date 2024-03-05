from django.shortcuts import redirect, render
from datetime import date as _Date, timezone
import time
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from html5lib import serialize
from requests import request
from sympy import Q
from accounts.models import Category, CustomUser, Product
from accounts.views import User
from main.models import Payment
from rest.forms import AppointmentForm
from rest.models import Addressuser, Appointment, DeliveryAgentProfile, FurniturePrediction, Furniturerent, Rent, deliveryagent, deliveryagentcantidates,deliveryagent
import os
from twilio.rest import Client

# Create your views here.
from django.http import JsonResponse

def update_status_accept(request,t_id):
    app = get_object_or_404(deliveryagent, id=t_id)
    app.status = 1
    app.save()
    return redirect('admindeliveryagentviews')
def update_status_reject(request,t_id):
    app = get_object_or_404(deliveryagent, id=t_id)
    app.rejected = 1
    app.save()
    return redirect('admindeliveryagentviews')

def deliveryaddress(request,):
    user=request.user
    address_users = Addressuser.objects.filter(user=user)
    if request.method == 'POST':
        # Get the posted data from the form
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        contact_number = request.POST.get('contact_number')
        alternate_contact_number = request.POST.get('alternate_contact_number')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        print("hai")
        print(street_address)
        # Create a new Addressuser object with the posted data
        new_address = Addressuser(
            user=user,
            city=city,
            street_address=street_address,
            state=state,
            country=country,
            postal_code=postal_code,
            contact_number=contact_number,
            alternate_contact_number=alternate_contact_number,
            latitude=latitude,
            longitude=longitude
        )

        # Save the new Addressuser object to the database
        new_address.save()

        # Redirect to a success page or any other page after saving the data
        return redirect('deliveryaddress')
    # app = get_object_or_404(Furniturerent, id=t_id)
    return render(request, "deliveryaddress.html", {'address_users': address_users})
def addressedit(request,t_id):
    app = get_object_or_404(Addressuser, id=t_id)
    if request.method == 'POST':
        # Update the fields with the submitted values
        app.street_address = request.POST.get('street_address', app.street_address)
        app.city = request.POST.get('city', app.city)
        app.state = request.POST.get('state', app.state)
        app.country = request.POST.get('country', app.country)
        app.postal_code = request.POST.get('postal_code', app.postal_code)
        app.contact_number = request.POST.get('contact_number', app.contact_number)
        app.alternate_contact_number = request.POST.get('alternate_contact_number', app.alternate_contact_number)
        app.latitude = request.POST.get('latitude', app.latitude)
        app.longitude = request.POST.get('longitude', app.longitude)
        
        # Save the updated object
        app.save()
        
        # Redirect to a success page or any other page after updating
        return redirect('deliveryaddress')
    return render(request,'addressedit.html',{'app': app})

def adminrentdashboard(request):
    # Retrieve the latest prediction from the database
    latest_prediction = FurniturePrediction.objects.latest('id')
    

    context = {
        'image_path': latest_prediction.image,
        'prediction': latest_prediction.prediction,
    }

    return render(request, 'adminrentdashboard.html', context)
def adminrentviewproducts(request):
    furniture = Furniturerent.objects.all()
    

    context = {
        'furniture': furniture,
    }

    return render(request, 'adminrentviewproducts.html', context)

def rentadminsingleview(request,t_id):
    app = get_object_or_404(Furniturerent, id=t_id)
    

    context = {
        'app': app,
    }

    return render(request, 'rentadminsingleview.html', context)

def admindeliveryagentsdashboard(request):
    app = Furniturerent.objects.all()
    context = {
        'app': app,
    }

    return render(request, 'admindeliveryagentsdashboard.html', context)

def adminproductandcategorydashboard(request):
    app = Furniturerent.objects.all()
    user_count = CustomUser.objects.count()
    count = CustomUser.objects.filter(role=1).count()
    count1 = Payment.objects.filter(payment_status='successful').count()
    productcount = Product.objects.filter(status=False).count()
    context = {
        'app': app,
        'count': count,
        'user_count': user_count,
        'count1':count1,
        'productcount':productcount,
    }

    return render(request, 'adminproductandcategorydashboard.html', context)

def adminuserdashboard(request):
    app = Furniturerent.objects.all()
    user_count = CustomUser.objects.count()
    count = CustomUser.objects.filter(role=1).count()
    count1 = Payment.objects.filter(payment_status='successful').count()
    productcount = Product.objects.filter(status=False).count()
    context = {
        'app': app,
        'count': count,
        'user_count': user_count,
        'count1':count1,
        'productcount':productcount,
    }

    return render(request, 'adminuserdashboard.html', context)

def adminreports(request):
    app = Furniturerent.objects.all()
    user_count = CustomUser.objects.count()
    count = CustomUser.objects.filter(role=1).count()
    count1 = Payment.objects.filter(payment_status='successful').count()
    productcount = Product.objects.filter(status=False).count()
    context = {
        'app': app,
        'count': count,
        'user_count': user_count,
        'count1':count1,
        'productcount':productcount,
    }

    return render(request, 'adminreports.html', context)
def adminrentrequest(request):
    user_appointments = Rent.objects.all().order_by('start_date')
    context = {
        'user_appointments': user_appointments,
    }

    return render(request, 'adminrentrequest.html', context)

def userrentsttaus(request):
    user_appointments = Rent.objects.filter(user=request.user).order_by('start_date')
    context = {
        'user_appointments': user_appointments,
    }

    return render(request, 'userrentsttaus.html', context)