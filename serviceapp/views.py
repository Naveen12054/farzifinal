from decimal import Decimal
from email import message
from pyexpat.errors import messages
from anyio import current_time
from django.shortcuts import redirect, render
from datetime import date as _Date, datetime, timezone
import time
from django.conf import settings
from django.urls import reverse
import razorpay
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from html5lib import serialize
from requests import request
from sympy import Q
from accounts.models import Category, CustomUser, Product
from accounts.views import User
from serviceapp.models import CompareProduct, Delivery, Feedback, Paymentrent, Paymentservice
from main.models import OrderItem, Payment
from rest.forms import AppointmentForm
from rest.models import Addressuser, Appointment, DeliveryAgentProfile, FurniturePrediction, Furniturerent, Rent, ServiceBooking,deliveryagent
import os
from twilio.rest import Client
from razorpay import Client

# Create your views here.
from django.http import JsonResponse

def update_status_accept(request,t_id):
    app = get_object_or_404(DeliveryAgentProfile, id=t_id)
    app.status = 1
    app.save()
    return redirect('admindeliveryagentviews')
def update_status_reject(request,t_id):
    app = get_object_or_404(DeliveryAgentProfile, id=t_id)
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
from twilio.rest import Client
def adminrentdashboard(request):
    # Retrieve the latest prediction from the database
    latest_prediction = FurniturePrediction.objects.latest('id')
    message_body = f"❌ Your booking for 🏨 from  📅 to  📅 has been canceled. We apologize for any inconvenience caused."


    # Send cancellation message via Twilio WhatsApp
    client = Client("ACdd73defbb24e5f653611d4906eafff25", "cf333437aa65df405dbbb2b9c4d6c719")
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message_body,
        to='whatsapp:+916282519724'  # Replace with the user's WhatsApp number
        )

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
    
    user_appointments = Rent.objects.filter(paid=1).order_by('start_date')
    user_appointment = Rent.objects.filter(paid=0).order_by('start_date')

    context = {
        'user_appointments': user_appointments,
        'user_appointment':user_appointment,
    }

    return render(request, 'adminrentrequest.html', context)

def userrentsttaus(request):
    current_time = timezone.now()
    user_appointments = Rent.objects.filter(user=request.user,
                                             paid=1).order_by('start_date')
    done = Rent.objects.filter(user=request.user,
                                paid=0).order_by('start_date')

    context = {
        'user_appointments': user_appointments,
        'done':done,
    }

    return render(request, 'userrentsttaus.html', context)

def adminservicedashboard(request):
    user_appointments = Rent.objects.filter(user=request.user).order_by('start_date')
    context = {
        'user_appointments': user_appointments,
    }

    return render(request, 'adminservicedashboard.html', context)


def adminserviceprovider(request):
    user_appointments = Rent.objects.filter(user=request.user).order_by('start_date')
    user=CustomUser.objects.filter(role=5)
    context = {
        'user_appointments': user_appointments,
        'user':user
    }

    return render(request, 'adminserviceprovider.html', context)

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
from django.views.decorators.csrf import csrf_exempt
def rentpayment(request, rent_id):
    user = request.user
    cart_items=get_object_or_404(Rent, id=rent_id)

    try:
        
        product = get_object_or_404(Rent, id=rent_id)
        total_price = Decimal(product.price * 1)
        print(total_price)
        amount = int(total_price * 100)
        # Convert total price to paise and round to 2 decimal places
        # amount_in_paise = int(total_price * 100)
        # rounded_amount = Decimal(amount_in_paise).quantize(Decimal('1.00'))

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency='INR',
            payment_capture='0',
        ))

        razorpay_order_id = razorpay_order['id']
        callback_url = '/serviceapp/paymenthandlerrent/'

        order = Paymentrent.objects.create(
            user=request.user,
            amount=amount/100,
            razorpay_order_id=razorpay_order_id,
            payment_status=Payment.PaymentStatusChoices.PENDING,
            rent=product
        )
        

        # Add the product to the order
        
        
        # payment.products.add(product)  # Add the product to the Payment object

        # # Save the Payment to generate a Payment ID
        # payment.save()
        
        # Save the order to generate an order ID
        order.save()
        
        context = {
            'total_price': total_price,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': 'INR',
            'callback_url': callback_url,
            'product': cart_items,


        }

        return render(request, 'rentconfirmuser.html', context=context)

    except (Product.DoesNotExist, ) as e:
        # Handle cases where product or seller does not exist
        return HttpResponseBadRequest("Product or Seller does not exist.")
@csrf_exempt
def paymenthandlerrent(request):
    print("Outsideif")
    # only accept POST request.
    if request.method == "POST":
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        payment = Paymentrent.objects.get(razorpay_order_id=razorpay_order_id)
        
        if result is not None:
            payment = Paymentrent.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.amount * 100)  # Convert Decimal to paise

            # capture the payment
            razorpay_client.payment.capture(payment_id, amount)
            payment = Paymentrent.objects.get(razorpay_order_id=razorpay_order_id)

            # Update the order with payment ID and change status to "Successful"
            payment.payment_id = payment_id
            payment.payment_status = Paymentrent.PaymentStatusChoices.SUCCESSFUL
            
            payment.save()
            rent = Rent.objects.get(id=payment.rent_id)  # Assuming rent_id is the field that links Rent and Paymentrent
            rent.paid = True
            rent.save()
            # Send the welcome email with PDF invoice
            #send_welcome_email(payment.user.username, payment.sub_type, payment.amount, payment.user.email, payment,)
            
            # render success page on successful capture of payment
            return redirect( 'userrentsttaus')
        else:
            # if signature verification fails.
            payment.payment_status = Paymentrent.PaymentStatusChoices.FAILED
            return render(request, 'paymentfail.html')
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
    
from django.contrib import messages
def add_to_compare(request, product_id):
    # Retrieve the property object
    property_obj = get_object_or_404(Product, pk=product_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create CompareProperty object for the user
        compare_property, created = CompareProduct.objects.get_or_create(user=request.user)

        # Check if the property is already in the compare list
        if property_obj in compare_property.products.all():
            messages.error(request, "This property is already in your compare list.")
        elif compare_property.products.count() >= 4:
            messages.error(request, "You can only compare up to 4 properties.")
        else:
            # Add the property to the compare list
            compare_property.products.add(property_obj)
            messages.success(request, "Property added to compare list successfully.")
    else:
        message.error(request, "You need to be logged in to add properties to compare list.")

    return redirect('singleview', product_id=product_id)

def compare_properties(request):
    # Get the CompareProperty objects for the logged-in user
    compare_properties = CompareProduct.objects.filter(user=request.user)

    context = {'compare_properties': compare_properties}

    return render(request, 'compareproduct.html', context)

def checkassignments(request):
    # Get the CompareProperty objects for the logged-in user
    compare_properties = OrderItem.objects.filter(deliverystatus=False)
    compare_propert = Rent.objects.filter(deliverystatus=False)


    context = {'compare_properties': compare_properties,'compare_propert':compare_propert}

    return render(request, 'checkassignments.html', context)

def remove_property(request, product_id):
    try:
        user = request.user
        compare_property = CompareProduct.objects.get(user=user)
        property_to_remove = compare_property.products.get(id=product_id)
        compare_property.products.remove(property_to_remove)
        return redirect(reverse('compare_properties'))  # Redirect to another view after removal
    except CompareProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'CompareProperty not found'})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Property not found'})
    
def servicepayment(request, service_id):
    user = request.user
    try:
        
        product = get_object_or_404(ServiceBooking, id=service_id)
        total_price = Decimal(product.estimatedcost * 1)
        print(total_price)
        amount = int(total_price * 100)
        # Convert total price to paise and round to 2 decimal places
        # amount_in_paise = int(total_price * 100)
        # rounded_amount = Decimal(amount_in_paise).quantize(Decimal('1.00'))

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency='INR',
            payment_capture='0',
        ))

        razorpay_order_id = razorpay_order['id']
        callback_url = '/serviceapp/paymenthandlerservice/'

        order = Paymentservice.objects.create(
            user=request.user,
            amount=amount/100,
            razorpay_order_id=razorpay_order_id,
            payment_status=Payment.PaymentStatusChoices.PENDING,
            service=product
        )
        

        # Add the product to the order
        
        
        # payment.products.add(product)  # Add the product to the Payment object

        # # Save the Payment to generate a Payment ID
        # payment.save()
        
        # Save the order to generate an order ID
        order.save()
        
        context = {
            'total_price': total_price,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': 'INR',
            'callback_url': callback_url,

        }

        return render(request, 'rentconfirmuser.html', context=context)

    except (Product.DoesNotExist, ) as e:
        # Handle cases where product or seller does not exist
        return HttpResponseBadRequest("Product or Seller does not exist.")
    

@csrf_exempt
def paymenthandlerservice(request):
    print("Outsideif")
    # only accept POST request.
    if request.method == "POST":
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        payment = Paymentservice.objects.get(razorpay_order_id=razorpay_order_id)
        
        if result is not None:
            payment = Paymentservice.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.amount * 100)  # Convert Decimal to paise

            # capture the payment
            razorpay_client.payment.capture(payment_id, amount)
            payment = Paymentservice.objects.get(razorpay_order_id=razorpay_order_id)

            # Update the order with payment ID and change status to "Successful"
            payment.payment_id = payment_id
            payment.payment_status = Paymentservice.PaymentStatusChoices.SUCCESSFUL
            
            payment.save()
            service = ServiceBooking.objects.get(id=payment.service_id)
            s=service.time_slot  # Assuming rent_id is the field that links Rent and Paymentrent
            print(s)
            service.paid = 1
            service.save()
            s1=service.time_slot  # Assuming rent_id is the field that links Rent and Paymentrent
            print(s1)
            # Send the welcome email with PDF invoice
            #send_welcome_email(payment.user.username, payment.sub_type, payment.amount, payment.user.email, payment,)
            user_email = service.user.email
            
            # Sending email to the user
            email_subject = 'Appointment Confirmed'
            email_body = f'Greeting form Farzi Furniture Store.Your appointment has been confirmed.\n\n'
            email_body += f'The estimate of ₹ {service.estimatedcost} is paid succesfully.\n\n'
            email_body += f'Appointment Details has been mentioned below:\n'
            email_body += f'Date: {service.date}\n'
            email_body += f'Time: {service.time_slot}\n'
            email_body += f'Service provider name: Savio Jose, Contact: 6282519724" \n'

            
            send_mail(
                email_subject,
                email_body,
                'farzifurniturestore@gmail.com',  # Replace with your email address or the sender's email
                [user_email],  # Use the extracted user email as the recipient
                fail_silently=False,
            )
            # render success page on successful capture of payment
            return redirect( 'servicelanding')
        else:
            # if signature verification fails.
            payment.payment_status = Paymentrent.PaymentStatusChoices.FAILED
            return render(request, 'paymentfail.html')
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
def takedelivery(request,t_id):
    app = get_object_or_404(OrderItem, id=t_id)
    delivery = Delivery.objects.create(
        user=request.user,
        order=app,
        delivered_at=timezone.now()  # Assuming status should be set to True upon delivery
    )
    app.deliverystatus=1
    app.save()
    return redirect( 'checkassignments')


def myassignments(request):
    # Get the CompareProperty objects for the logged-in user
    compare_properties = Delivery.objects.filter(user=request.user)

    context = {'compare_properties': compare_properties}

    return render(request, 'myassignments.html', context)


def deliverydone(request,t_id):
    app = get_object_or_404(Delivery, id=t_id)
    app.status=1
    app.save()
    return redirect( 'myassignments')
def get_bookings_for_date(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        bookings = ServiceBooking.objects.filter(date=date).values('time_slot')
        return JsonResponse({'bookings': list(bookings)})
def servicebooking(request):
    user=request.user
    error_message=''
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')
        desc = request.POST.get('desc')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        existing_booking = ServiceBooking.objects.filter(
                date=date,
                paid=True,
                time_slot=time_slot,   # Check if the existing end time is greater than or equal to the new end time
            ).first()

        if existing_booking:
            error_message = "Slot already booked"
            print("error")
            print(error_message)
            print("error")
            

        else:
            print("error")
            print(error_message)
            print("error")

            
        # Create a new instance of the GroomingServiceBooking model
            booking = ServiceBooking(
                mobile=mobile,
                location=location,
                desc=desc,
                user=user,
                date=date,
                time_slot=time_slot,
            )
            booking.save()
            user = request.user
       
            return redirect('servicelanding')
    context = {
        
        'error_message':error_message,
        }
      # Redirect to a success page
    return render(request, 'servicebooking.html',context)


def feedback_page(request, ser_id):
    user_id = request.user.id
    selected_station = Product.objects.get(pk=ser_id)
    feedbacks = Feedback.objects.filter(product_id=ser_id,status=True).order_by("-date")
    # Check if the current user has already submitted feedback for the selected station
    feedback_exists = Feedback.objects.filter(product=selected_station, userprofile=request.user, status=True).exists()

    return render(request, 'feedback_page.html', {'product': ser_id,'feedbacks': feedbacks, 'user_id': user_id, 'feedback_exists': feedback_exists})


def add_comment(request, ser_id):
    user_id = request.user.id

    if request.method == 'POST':
        message = request.POST.get('messages')
        rating = request.POST.get('rating')        # Fetch the CustomUser object using the user ID
        user = CustomUser.objects.get(id=user_id)
        product = get_object_or_404(Product, id=ser_id)        # Create the Feedback object
        feedback = Feedback.objects.create(
            userprofile_id=user_id,
            product=product,
            first_name=user.name,
            message=message,
            rating=rating,  
            status=True,
            date=datetime.now(),
        )
        feedback.save()

    # Redirect to the feedback_page with the station_id
    return redirect('feedback_page', ser_id=ser_id)


def delete_feedback(request, feedback_id, ser_id):
    # Retrieve the feedback object
    user_id = request.user.id
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    
    # Set status to True to mark as deleted
    feedback.status = False
    feedback.save()  # Save the changes
    
    # Redirect to the feedback page with both station_id and user_id
    return redirect('feedback_page', ser_id=ser_id)

def servicelanding(request):
    # Retrieve the feedback object
    user_id = request.user.id
    current_date = timezone.now().date()
    user_appointments=ServiceBooking.objects.filter(user=request.user).order_by("-date")
    context={
        'user_appointments':user_appointments,
        'current_date':current_date,
    }
    
    # Redirect to the feedback page with both station_id and user_id
    return render(request,'servicelanding.html',context)