
from datetime import date as _Date, timezone
import time
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from accounts.models import Category, CustomUser
from accounts.views import User
from rest.forms import AppointmentForm
from .models import Appointment, DeliveryAgentProfile, FurniturePrediction, Furniturerent, deliveryagent
import os
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

model = keras.models.load_model('models/furniture_model.h5')

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



def rentuser(request):
    return render(request, "rentuser.html")
def services(request):
    user_appointments = Appointment.objects.filter(client=request.user)
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
    if request.method == 'POST':
        # Extract data from the POST request
        product_code = request.POST['product_code']
        category = request.POST['category']  # Assuming 'category' is the name attribute of the category select field

        description = request.POST['description']
        condition = request.POST['condition']
        rental_price = request.POST['price']
        status = request.POST.get('status', False)  # If status is not provided, default to False
        length = request.POST['length']
        width = request.POST['breadth']
        height = request.POST['height']
        material = request.POST['material']
        security_deposit = request.POST['security']
        quality_standard = request.POST['brand_name']

        # Create a new instance of the Furniturerent model
        new_product = Furniturerent(
            product_code=product_code,
            category=category,
            description=description,
            condition=condition,
            rental_price=rental_price,
            status=status,
            length=length,
            width=width,
            height=height,
            material=material,
            security_deposit=security_deposit,
            quality_standard=quality_standard,
        )

        # Save the instance to the database
        new_product.save()

    # If the request method is not POST, render the form
    return render(request, 'addrent.html')

def deliveryagentadmin(request):
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

    return render(request, 'deliveryagentadmin.html')

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
    if request.method == 'POST':
        # Extract data from the request.POST dictionary
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        insurance_policy_number = request.POST.get('insurance_policy_number')
        insurance_expiry_date = request.POST.get('insurance_expiry_date')
        insurance_company = request.POST.get('insurance_company')
        bank_name = request.POST.get('bank_name')
        banking_name = request.POST.get('banking_name')
        account_number = request.POST.get('account_number')
        routing_number = request.POST.get('routing_number')
        max_delivery_distance = request.POST.get('max_delivery_distance')
        emergency_contact = request.POST.get('emergency_contact')

        # Create DeliveryAgentProfile instance and save to the database
        profile = DeliveryAgentProfile.objects.create(
            user=request.user,  # Assuming you have a User model linked to the DeliveryAgentProfile
            first_name=first_name,
            last_name=last_name,
            insurance_policy_number=insurance_policy_number,
            insurance_expiry_date=insurance_expiry_date,
            insurance_company=insurance_company,
            bank_name=bank_name,
            banking_name=banking_name,
            account_number=account_number,
            routing_number=routing_number,
            max_delivery_distance=max_delivery_distance,
            emergency_contact=emergency_contact
        )
        return redirect('deliveryagentdashboard')  # Redirect to a success page or any other desired page

    return render(request, 'deliveryagentprofile.html')
def spage(request):
    return render(request, "spage.html")
def deliveryagentdashboard(request):
    return render(request, "deliveryagentdashboard.html")
def listofservices(request):
    profiles = DeliveryAgentProfile.objects.all()
    appointments = Appointment.objects.all()
    return render(request, 'listofservices.html', {'appointments': appointments,'profiles':profiles})


def requestpage(request,appointment_id):
    print("hai")

    app = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        # Check if the form is submitted
        if 'approve' in request.POST:
            # If the 'Approve' button is clicked, set the 'approved' field to True
            app.approved = True
            app.cost = 500
            app.estimatedcost = request.POST.get('text')
            app.approved_timestamp = timezone.now()   
            app.save()
            user_email = app.client.email
            
            # Sending email to the user
            email_subject = 'Appointment Scheduled'
            email_body = f'Greeting form Farzi Furniture Store.Your appointment has been approved.\n\n'
            email_body += f'Thank you for choosing our service.Please complete the advance payment of ₹ 500 to confirm the request.\n\n'
            email_body += f'Appointment Details has been mentioned below:\n'
            email_body += f'Date: {app.date}\n'
            email_body += f'Time: {app.get_time_slot_display()}\n'
            email_body += f'Estimated Cost after going through the description: {app.estimatedcost}\n'
            email_body += f'Complete the payment here: \n'

            
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
            app.rejectionreason = "We regret to inform you that your offer has been rejected. Unfortunately, the required maintenance work cannot be accommodated within the current schedule due to high workload and priority tasks. We appreciate your interest and hope to collaborate with you in the future when circumstances permit. Thank you for your understanding kindly schedule another appointment."
            app.approved_timestamp = timezone.now()   # Save the input value to the 'cost' field
            app.save()


            user_email = app.client.email
            
            # Sending email to the user
            email_subject = 'Appointment Not Scheduled'
            email_body = f'Your appointment has not been approved.\n\n'
            email_body += f'We regret to inform you that your offer has been rejected. Unfortunately, the required maintenance work cannot be accommodated within the current schedule due to high workload and priority tasks. We appreciate your interest and hope to collaborate with you in the future when circumstances permit. Thank you for your understanding, kindly schedule another appointment.\n\n'
            
            send_mail(
                email_subject,
                email_body,
                'farzifurniturestore@gmail.com',  # Replace with your email address or the sender's email
                [user_email],  # Use the extracted user email as the recipient
                fail_silently=False,
            )

            return redirect('listofservices')

    return render(request, "requestpage.html",{'app': app})

