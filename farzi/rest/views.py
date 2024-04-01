
from datetime import date as _Date, timezone
import json
import time
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from html5lib import serialize
from sympy import Q
from accounts.models import Category, CustomUser, Product
from accounts.views import User
from main.models import OrderItem, Payment
from rest.forms import AppointmentForm
from .models import Addressuser, Appointment, DeliveryAgentProfile, FurniturePrediction, Furniturerent, Rent, ServiceBooking, deliveryagent
import os
from twilio.rest import Client
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
from tensorflow import keras

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((376, 339))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def predict(image_path):
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    return prediction

def seminar2(request):
    predicted_label = None
    latest_prediction = None

    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        image_path = os.path.join('media', filename)

        prediction = predict(image_path)

        class_labels = {0: 'Bed', 1: 'Chair', 2: 'Sofa', 3: 'Swivel chair', 4: 'Table'}
        predicted_class = np.argmax(prediction)
        predicted_label = class_labels[predicted_class]

        FurniturePrediction.objects.create(image=filename, prediction=predicted_label)
        latest_prediction = FurniturePrediction.objects.latest('id')

    return render(request, 'seminar2.html', {'predicted_label': predicted_label, 'latest_prediction': latest_prediction})

# model = keras.models.load_model('models/furniture_model.h5')
def send_whatsapp_message(to, body):
    # Your Twilio account SID and auth token
    account_sid = 'ACdd73defbb24e5f653611d4906eafff25'
    auth_token = 'cf333437aa65df405dbbb2b9c4d6c719'
    twilio_number = '+916282519724'  # Should be your WhatsApp sandbox number

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=f'whatsapp:{twilio_number}',
            body=body,
            to=f'whatsapp:{to}'
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# Usage example
success, message_id = send_whatsapp_message('recipient_number', 'Your message here')
if success:
    print(f'Message sent successfully. Message SID: {message_id}')
else:
    print(f'Failed to send message: {message_id}')

def result(request):
    # Retrieve the latest prediction from the database
    latest_prediction = FurniturePrediction.objects.latest('id')
    print("hai")
    print(latest_prediction)

    context = {
        'image_path': latest_prediction.image,
        'prediction': latest_prediction.prediction,
    }

    return render(request, 'result.html', context)

def check_availability(request):
    if request.method == 'POST' and request.is_ajax():
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Furniturerent, id=product_id)
        is_available = product.is_available(start_date, end_date, quantity)
        return JsonResponse({'available': is_available})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def rentuser(request,t_id):
    user=request.user
    error_message=''
    app = get_object_or_404(Furniturerent, id=t_id)
    furniture = Furniturerent.objects.all()
    add = Addressuser.objects.filter(user=user)
    max_quantity = int(app.stock)
    print(max_quantity)
    if request.method == 'POST':
        print("Testing")
        # Retrieve form data from POST request
        selected_address_id = request.POST.get('selected_address')
        quantity = int(request.POST.get('quantity-chair'))
        start_date = request.POST.get('startdate-chair')
        end_date = request.POST.get('enddate-chair')
        product_id = t_id  # Assuming it's hardcoded for now, you may need to modify this
        product_price = app.rental_price  # Assuming it's hardcoded for now, you may need to modify this
        existing_booking = Rent.objects.filter(
                product_id=product_id,
                start_date__range=(start_date, end_date),
                end_date__range=(start_date, end_date),
            )
        
        count = 0  # Initialize count before the loop
        for existing_booking in existing_booking:  # Assuming 'existing_bookings' is the list of bookings
            count += existing_booking.quantity  # Increment count by the quantity of each booking
            print(existing_booking.quantity)
            
        print("Total sum:", count)  # Print the total sum after the loop completes
        availablestock=max_quantity - count
        print("Total sum:",availablestock)
        # print("Heloo errro")
        # print(existing_booking)
        # print("Heloo errro")

        if availablestock < quantity:
            error_message = f"Only {availablestock} slots are available"
            
        # Retrieve the selected address
        else:
            selected_address = Addressuser.objects.get(id=selected_address_id)
            
            # Calculate price
            # Assuming product price is hardcoded for now, you may need to modify this
            price_per_day = product_price
            days_difference = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
            total_price = price_per_day * days_difference * quantity
            print("hai")
            print(total_price)
            # Create Rent object
            rent = Rent.objects.create(
                user=user,  # Assuming the user is logged in and you have a way to retrieve the user
                address=selected_address,
                product_id=product_id,
                quantity=quantity,
                price=total_price,
                start_date=start_date,
                end_date=end_date,
                status=False,  # Assuming the initial status is False
                paid=False  # Assuming the initial paid status is False
            )
            rent.save()
            return redirect('userrentsttaus')
    return render(request, "rentuser.html",{'furniture': furniture,'app':app,'add':add,'max_quantity':max_quantity,'error_message':error_message})



def rentuserlist(request):
    furniture = Furniturerent.objects.all()
    return render(request, "rentuserlist.html",{'furniture': furniture})
def services(request):
    user_appointments = Appointment.objects.filter(client=request.user).order_by('-date')
    return render(request, "services.html",{'user_appointments': user_appointments})
def installation(request):
    return render(request, "installation.html")


def manintenece(request):
    context = None
    appointments = Appointment.objects.all()

    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        # Check if the current user (client) has already booked an appointment for the same date and time slot
        existing_appointment = Appointment.objects.filter(client=request.user, date=date, time_slot=time_slot).exclude(time_slot__isnull=True).first()

        # Check if the current user (client) has already booked an appointment for the same date
        existing_appointment_same_date = Appointment.objects.filter(client=request.user, date=date).exclude(time_slot__isnull=True).first()

        if existing_appointment:
            apps = Appointment.objects.filter(date=date, time_slot=time_slot).exclude(time_slot__isnull=True)
            time_slots = {time(9, 0): 1, time(11, 0): 1, time(13, 0): 1, time(15, 0): 1, time(17, 0): 1}
            for app in apps:
                time_slots[app.time_slot] = 0

            available_slots = [time_slot.strftime('%I:%M %p') for time_slot, available in time_slots.items() if available]
            available_slots = ", ".join(available_slots)

            user = request.user
            initial_data = {
                'client': user,
                'client_name': user.name,
                
            }
        elif existing_appointment_same_date:
            user = request.user
            initial_data = {
                'client': user,
                'client_name': user.name,
                
            }
            appointment_form = AppointmentForm(initial=initial_data)
            context = {
                'error1': 'You have already scheduled an appointment for the selected Date',
                'appointment_form': appointment_form,
                
            }
        else:
            form = AppointmentForm(request.POST)
            form.instance.client = request.user
            if form.is_valid():
                existing_appointment_same_slot = Appointment.objects.filter(date=form.cleaned_data['date'], time_slot=form.cleaned_data['time_slot']).exclude(time_slot__isnull=True).first()
                if existing_appointment_same_slot:
                # The selected time slot is already booked, handle this case
                    context = {
                        'error': 'The selected time slot is already booked. Please choose another time slot.',
                        'appointment_form': form,
                    }
                    return render(request, 'manintenece.html', context)
                appointment1 = form.save(commit=False)  # Save the form data to the appointment instance but don't commit to the database yet
                appointment1.user= request.user
                appointment1.save()
                return redirect('services')
    else:
        user = request.user
        initial_data = {
            'client': user,
            'client_name': user.name,
        }
        appointment_form = AppointmentForm(initial=initial_data)

        context = {'appointment_form': appointment_form,
                   'appointments': appointments}

    return render(request, 'manintenece.html', context)
# def get_available_time_slots(request):
    
#     date = request.GET.get('date')

#     # Fetch existing appointments for the selected date and therapist
#     existing_appointments = Appointment.objects.filter(date=date)

#     # Create a list of all available time slots
#     all_time_slots = [time(9, 0), time(11, 0), time(13, 0), time(15, 0), time(17, 0)]

#     # Initialize a dictionary to store the availability of time slots
#     time_slot_availability = {time_slot: True for time_slot in all_time_slots}

#     # Mark time slots as unavailable if they are already booked
#     for appointment in existing_appointments:
#         if appointment.time_slot in time_slot_availability:
#             time_slot_availability[appointment.time_slot] = False

#     # Filter the available time slots
#     available_time_slots = [time_slot.strftime('%I:%M %p') for time_slot, is_available in time_slot_availability.items() if is_available]

#     return JsonResponse({'available_time_slots': available_time_slots})

from django.http import JsonResponse
from datetime import time, datetime

def get_available_time_slots(request):
    try:
        date_str = request.GET.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid date format or missing date parameter'})

    existing_appointments = Appointment.objects.filter(date=date)
    all_time_slots = [time(9, 0), time(11, 0), time(13, 0), time(15, 0), time(17, 0)]
    time_slot_availability = {time_slot: True for time_slot in all_time_slots}

    for appointment in existing_appointments:
        if appointment.time_slot in time_slot_availability:
            time_slot_availability[appointment.time_slot] = False

    available_time_slots = [time_slot.strftime('%I:%M %p') for time_slot, is_available in time_slot_availability.items() if is_available]

    return JsonResponse({'status': 'success', 'available_time_slots': available_time_slots})


from django.shortcuts import render, redirect
from .models import install
from django.contrib import messages

def install(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        date = request.POST.get('date')
        time_slot = request.POST.get('timeslot')
        contact_number = request.POST.get('contact_number')
        location_on_map = request.POST.get('location_on_map')

        # Assuming you have user information available in the request or session
        user = request.user  # Adjust this based on your authentication setup

        # Assuming you have set up the 'install' model correctly
        booking = install.objects.create(
            name=user,
            email=user.email,
            date=date,
            start_time=time_slot,
            loacation=location_on_map,
            loacation1=location_on_map,  # Update this field accordingly
            status=False,  # You can set the status based on your logic
            del_status=False,  # You can set the delivery status based on your logic
        )

        messages.success(request, 'Booking successful!')
        return redirect('success_page')  # Redirect to a success page or another page as needed

    return render(request, 'install.html')  # Adjust 'your_template_name.html' accordingly
def addrent(request):
    print("hello")
    
    if request.method == 'POST':
        # Extract data from the POST request
        product_code = request.POST['product_code']
        category = request.POST['category']  # Assuming 'category' is the name attribute of the category select field
        condition = request.POST['quantity']
        rental_price = request.POST['price']
        status = request.POST.get('status', False)  # If status is not provided, default to False
        length = request.POST['length']
        width = request.POST['breadth']
        height = request.POST['height']
        material = request.POST['material']
        security_deposit = request.POST['security_deposit']
        quality_standard = request.POST['quality_standard']
        product_images1 = request.FILES.get('product_images1')
        product_images2 = request.FILES.get('product_images2')
        product_images3 = request.FILES.get('product_images3')
        product_images4 = request.FILES.get('product_images4')
        print("hai")
        print(product_images1)

        # Create a new instance of the Furniturerent model
        new_product = Furniturerent(
            product_code=product_code,
            category=category,
            condition=condition,
            rental_price=rental_price,
            status=status,
            length=length,
            width=width,
            height=height,
            material=material,
            security_deposit=security_deposit,
            quality_standard=quality_standard,
            product_images4=product_images4,
            product_images3=product_images3,
            product_images2=product_images2,
            product_images1=product_images1,
        )

        # Save the instance to the database
        new_product.save()
        return redirect('adminrentdashboard')

    # If the request method is not POST, render the form
    return render(request, 'addrent.html')
import string
import secrets


        
def deliveryagentadmin(request,appointment_id):
    app = get_object_or_404(deliveryagentcantidates, id=appointment_id)
    users = CustomUser.objects.all()
    delivery_agents = deliveryagent.objects.all()
    delivery = DeliveryAgentProfile.objects.all()
    delivery12 = deliveryagentcantidates.objects.filter(status=False)
    common_users = []
    for agent in delivery_agents:
        # Check if there is a corresponding DeliveryAgentProfile
        if DeliveryAgentProfile.objects.filter(user=agent.user).exists():
            # If there is a corresponding profile, add the user to the list
            common_users.append(agent.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pin = request.POST.get('pin')
        mobile = request.POST.get('mobile')
        password = generate_random_password()

        try:
            custom_user = User.objects.create(
                name=name,
                first_name=name,
                email=email,
                password = password,
                role=User.DELIVERY  # Assuming DELIVERY corresponds to the 'Delivery' role
            )
            custom_user.set_password(password)
            custom_user.save()
            deliveryagent.objects.create(
                user=custom_user,
                name=custom_user.name,
                email=custom_user.email,
                pin=pin,
                mobile=mobile
            )
            recipient_number = mobile  # Replace with the recipient's phone number
            message_body = 'Sample message '     # Replace with the message body
            success, message_id = send_whatsapp_message(recipient_number, message_body)

            if success:
                print(f'Message sent successfully. Message SID: {message_id}')
            else:
                print(f'Failed to send message: {message_id}')


            return redirect('spage')
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=400)
    context = {
        'delivery_agents': delivery_agents,
        'delivery':delivery,
        'users':users,
        'common_users': common_users,
        'delivery12':delivery12,
        'app':app
    }

    return render(request, 'deliveryagentadmin.html',context)

def seller(request):
    if request.method == 'POST':
        name1 = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('pass', None)
        role = User.SELLER
        print(email)
        

        if name1 and email and role and password:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'login.html', {'error_message': error_message})
            
            else:
                user = User(name=name1, email=email, role=role)
                user.set_password(password)  # Set the password securely
                user.save()
                return redirect('login')  
            
    return render(request, 'seller.html')

def deliveryagentprofile(request):
    user=request.user
    delivery_agents1=get_object_or_404(deliveryagent, user=user)
    delivery_agents = deliveryagent.objects.filter(user=user)
    pin1=delivery_agents1.pin
    mobile1=delivery_agents1.mobile
    print("hai")
    print(pin1)
    print("hello")

    if request.method == 'POST':
        # Extract data from the request.POST dictionary
        first_name = request.POST.get('first_name')
        last_name = 0   
        insurance_policy_number = request.POST.get('insurance_policy_number')
        longitude = request.POST.get('longitude')
        bank_name = request.POST.get('bank_name')
        banking_name = request.POST.get('banking_name')
        account_number = request.POST.get('account_number')
        routing_number = request.POST.get('routing_number')
        max_delivery_distance = request.POST.get('max_delivery_distance')
        emergency_contact = request.POST.get('emergency_contact')
        current_date = _Date.today()
        profile_photo = request.FILES.get('profile_photo')
        print(profile_photo)
        # Create DeliveryAgentProfile instance and save to the database
        profile = DeliveryAgentProfile.objects.create(
            user=request.user,  # Assuming you have a User model linked to the DeliveryAgentProfile
            first_name=first_name,
            last_name=last_name,
            latitude=insurance_policy_number,
            insurance_expiry_date=current_date,
            longitude=longitude,
            bank_name=bank_name,
            banking_name=banking_name,
            account_number=account_number,
            routing_number=routing_number,
            max_delivery_distance=max_delivery_distance,
            emergency_contact=emergency_contact,
            profile_photo=profile_photo,
            pin=pin1,
            mobile=mobile1
        )
        return redirect('deliveryagentdashboard')  # Redirect to a success page or any other desired page
    context = {
        'delivery_agents': delivery_agents
    }
    return render(request, 'deliveryagentprofile.html',context)
def spage(request):

    return render(request, "spage.html")
def deliveryagentdashboard(request):
    orders = Payment.objects.all()
    orders1 = OrderItem.objects.all()

    
    context = {
        'orders': orders,
        'orders1':orders1
    }
    return render(request, "deliveryagentdashboard.html",context)
from django.db.models import Count
from django.utils import timezone

# Get the current date
current_date = timezone.now().date()
def serviceadmin(request):
    paid = Appointment.objects.filter(payment_status = 1,
                                              approved=1
                                              ).order_by('date')
    current_date = timezone.now().date()
    print("Check")
    for appointment in paid:
        if appointment.date <= current_date:
            appointment.status = "Completed"
        else:
            appointment.status = "Pending"
    acceptedservice = Appointment.objects.filter(approved = 1,
                                                 payment_status=0
                                                 ).order_by('date')
    pending = Appointment.objects.filter(rejected = 0,
                                              payment_status=0,
                                              approved=0
                                              ).order_by('date')
    done = Appointment.objects.filter(payment_status=1, approved=1, date__lte=current_date).order_by('date')
    
    # Filtering out appointments already present in the 'paid' queryset
    doneservice = done.exclude(pk__in=paid.values_list('pk', flat=True))
    for appointment in doneservice:
        print(appointment.date, appointment.client)
    print("doneservice")
    reject = Appointment.objects.filter(rejected = 1).order_by('date')
    appointments_count_by_date = (
        Appointment.objects
        .values('date')
        .annotate(num_appointments=Count('id'))
        .order_by('date')
    )

# Print appointments count for each date
    for appointment_count in appointments_count_by_date:
        print(f"Appointments on {appointment_count['date']}: {appointment_count['num_appointments']}")
    print("fufuufufu")
    appointments_count_by_date = (
        Appointment.objects
        .values('date')
        .annotate(num_appointments=Count('id'))
        .order_by('date')
    )

    # Prepare data for chart
    categories = [appointment['date'].strftime('%Y-%m-%d') for appointment in appointments_count_by_date]
    counts = [appointment['num_appointments'] for appointment in appointments_count_by_date]

    context = {
        'acceptedservice': acceptedservice,
        'reject':reject,
        'pending':pending,
        'paid':paid,
        'done':done,
        'doneservice':doneservice,
    }
    return render(request, "serviceadmin.html",context)

def listofservices(request):
    profiles = DeliveryAgentProfile.objects.all()
    appointments = ServiceBooking.objects.all().order_by("-date")
    current_date = timezone.now().date()
    return render(request, 'listofservices.html', {'appointments': appointments,'profiles':profiles,'current_date':current_date})


def requestpage(request,appointment_id):
    print("hai")

    app = get_object_or_404(ServiceBooking, id=appointment_id)
    if request.method == 'POST':
        # Check if the form is submitted
        if 'approve' in request.POST:
            # If the 'Approve' button is clicked, set the 'approved' field to True
            app.accepted = 1
            app.estimatedcost = request.POST.get('text') 
            app.save()
            user_email = app.user.email
            
            # Sending email to the user
            email_subject = 'Appointment Scheduled'
            email_body = f'Greeting form Farzi Furniture Store.Your appointment has been approved.\n\n'
            email_body += f'Thank you for choosing our service.Please complete the service charge of ₹ {app.estimatedcost} to confirm the request.\n\n'
            email_body += f'Appointment Details has been mentioned below:\n'
            email_body += f'Date: {app.date}\n'
            email_body += f'Time: {app.time_slot}\n'
            email_body += f'Complete the payment here: http://127.0.0.1:8000/rest/services/" \n'

            
            send_mail(
                email_subject,
                email_body,
                'farzifurniturestore@gmail.com',  # Replace with your email address or the sender's email
                [user_email],  # Use the extracted user email as the recipient
                fail_silently=False,
            )
            return redirect('listofservices')

        elif 'reject' in request.POST:
            # If the 'Reject' button is clicked, set the 'rejected' field to True
            app.rejected = True
            app.rejectionreason = "We regret to inform you that your appointment has been rejected. Unfortunately, that specific date maintenance is on an off. We appreciate your interest and hope to collaborate with you in the future when circumstances permit. Thank you for your understanding kindly schedule another appointment."
            app.save()


            user_email = app.user.email
            
            # Sending email to the user
            email_subject = 'Appointment Not Scheduled'
            email_body = f'Your appointment has not been approved.\n\n'
            email_body += f'We regret to inform you that your appointment has been rejected. Unfortunately, that specific date maintenance is on an off. We appreciate your interest and hope to collaborate with you in the future when circumstances permit. Thank you for your understanding kindly schedule another appointment.\n\n'
            
            send_mail(
                email_subject,
                email_body,
                'farzifurniturestore@gmail.com',  # Replace with your email address or the sender's email
                [user_email],  # Use the extracted user email as the recipient
                fail_silently=False,
            )

            return redirect('listofservices')

    return render(request, "requestpage.html",{'app': app})
from django.core import serializers
from django.core.serializers import serialize
def searchByName(request,name):
    print(name)
    # name=name.lower()
    users = Product.objects.filter(product_name__icontains=name)
    user_data = serializers.serialize('json', users)
    print(user_data)

    # Return the serialized data as JSON response
    return JsonResponse(user_data, safe=False)
def generate_random_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password
def deliverybase(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pin = request.POST.get('pin')
        mobile = request.POST.get('mobile')
        password = generate_random_password()


        try:
            custom_user = User.objects.create(
                name=name,
                first_name=name,
                email=email,
                password = password,
                role=User.DELIVERY 
                 # Assuming DELIVERY corresponds to the 'Delivery' role
            )
            custom_user.set_password(password)
            custom_user.save()
            deliveryagent.objects.create(
                user=custom_user,
                name=custom_user.name,
                email=custom_user.email,
                pin=pin,
                mobile=mobile
            )
            
            email_subject = 'Registration Successful'
            email_body = f'Thank you for registering as a delivery agent. Your password is: {password}\n\n'
            email_body += f'Click on the following link to complete your profile:\nhttp://127.0.0.1:8000/rest/deliveryagentprofile/'

            send_mail(
                email_subject,
                email_body,
                email,  # Use the provided email address as the sender
                [email],
                fail_silently=False,
            )
            
            
            return redirect('spage')
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=400)
    return render(request, "deliverybase.html")
def admindeliveryagentviews(request):
    # this is for admin to view the cantidates for the job
    users = CustomUser.objects.all()
    delivery_agents = deliveryagent.objects.all()
    delivery = DeliveryAgentProfile.objects.all()
    common_users = []
    for agent in delivery_agents:
        # Check if there is a corresponding DeliveryAgentProfile
        if DeliveryAgentProfile.objects.filter(user=agent.user).exists():
            # If there is a corresponding profile, add the user to the list
            common_users.append(agent.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        pin = request.POST.get('pin')
        mobile = request.POST.get('mobile')

        try:
            custom_user = User.objects.create(
                name=name,
                email=email,
                password=password,
                role=User.DELIVERY  # Assuming DELIVERY corresponds to the 'Delivery' role
            )
            custom_user.set_password(password)
            custom_user.save()
            deliveryagent.objects.create(
                user=custom_user,
                name=custom_user.name,
                email=custom_user.email,
                pin=pin,
                mobile=mobile
            )
            
            email_subject = 'Registration Successful'
            email_body = f'Thank you for registering as a delivery agent. Your password is: {password}\n\n'
            email_body += f'Click on the following link to complete your profile:\nhttp://127.0.0.1:8000/accounts/login/'

            send_mail(
                email_subject,
                email_body,
                email,  # Use the provided email address as the sender
                [email],
                fail_silently=False,
            )
            return redirect('spage')
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=400)
    context = {
        'delivery_agents': delivery_agents,
        'delivery':delivery,
        'users':users,
        'common_users': common_users
    }

    return render(request, 'admindeliveryagentviews.html',context)
def adminsidecatidacydelivery(request):
    users = CustomUser.objects.all()
    delivery12 = DeliveryAgentProfile.objects.filter(status=False)
    
   
    context = {
        'users':users,
        'delivery12':delivery12
    }

    return render(request, 'adminsidecatidacydelivery.html',context)
def acceptrent(request,appointment_id):
    print(appointment_id)
    app = get_object_or_404(Rent, id=appointment_id)
    product=app.product.id
    app.status=1
    app.save()
    print(product)
    productdetails = get_object_or_404(Rent, id=product)
    print(productdetails)
    accepted_product = app.product
    accepted_product.update_condition()

    # Mark other appointments with overlapping dates as rejected if their conditions are not met
    overlapping_apps = Rent.objects.filter(
        Q(start_date__range=[app.start_date, app.end_date]) |
        Q(end_date__range=[app.start_date, app.end_date]) |
        Q(start_date__lte=app.start_date, end_date__gte=app.end_date)
    ).exclude(id=appointment_id)

    for overlapping_app in overlapping_apps:
        overlapping_product = overlapping_app.product
        overlapping_product.update_condition()
        if overlapping_product.condition != "Renting":
            overlapping_app.rejected = True
            overlapping_app.save()
    user_appointments = Rent.objects.all().order_by('start_date')
    context = {
        'user_appointments': user_appointments,
        'app':app,
    }
    return render(request, "adminrentrequest.html",context)