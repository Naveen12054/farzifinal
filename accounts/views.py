from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.contrib  import messages,auth
from rest.models import DeliveryAgentProfile

from main.models import Order, Payment
from .models import Category, CustomUser, Product, SellerProfile,UserProfile,Subcategory
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model
#from .forms import UserForm, ServiceForm 

User = get_user_model()



def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        print(email)  # Print the email for debugging
        print(password)  # Print the password for debugging
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            print("Authenticated user:", user)  # Print the user for debugging
            if user is not None and user.is_active:
                        
                        if user.is_active==False:
                                print("Inside user.is_active check")
                                auth_login(request, user)
                                print(user.is_active)
                                error_message = "Inactive login credentials."
                                return render(request, 'login.html', {'error_message': error_message})
                        else:

                            if user.role==1:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('index')
                            elif user.role==2:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('seller')
                            elif user.role==5:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('listofservices')
                            elif user.role==3:
                                try:
                                    delivery_agent_profile = DeliveryAgentProfile.objects.get(user=user)
                                    auth_login(request, user)
                                    print(user.role)
                                    return redirect('deliveryagentdashboard')
                                except DeliveryAgentProfile.DoesNotExist:
                                    auth_login(request, user)
                                    print(user.role)
                                    return redirect('deliveryagentprofile')
                            else:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('admindashboard')
        #         auth_login(request, user)
        #         print("User authenticated:", user.email, user.role)
        #         return redirect('http://127.0.0.1:8000/')
            
            # if user.is_active:
            #                     error_message = "Inactive login credentials."
            #                     return render(request, 'login.html', {'error_message': error_message})
            else:
                error_message = "Invalid Login Attempt"
                return render(request, 'login.html', {'error_message': error_message})
        # else:
        #     error_message = "Please fill out all fields."
        #     return render(request, 'login.html', {'error_message': error_message})

    return render(request,'login.html')

    
def register(request):
    if request.method == 'POST':
        name1 = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('pass', None)
        role = User.CUSTOMER
        print(email)

        if name1 and email and role and password:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'login.html', {'error_message': error_message})
            
            else:
                user = User(name=name1, email=email, role=role,first_name=name1)
                user.set_password(password)  # Set the password securely
                user.save()
                user_profile=UserProfile(user=user)
                user_profile.save()
                return redirect('login')  
            
    return render(request, 'register.html')
def profile(request):
    user=request.user
    user_profile1 = request.user
    userid = user_profile1.id
    products3=Category.objects.filter(status=False)
    
    print(user_profile1)
    check=UserProfile.objects.filter(user_id=userid).exists()
    if check:
        user_profile = UserProfile.objects.get(user_id=userid)
    else:
        user_profile=None


    if request.method == 'POST':
        # Update user fields
        if check==True:

            
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.phone_no = request.POST.get('phone_no')
            user.save()

             # Update user profile fields
            user_profile.country = request.POST.get('country')
            print(user_profile.country)
            user_profile.state = request.POST.get('state')
            user_profile.city = request.POST.get('city')
            user_profile.district = request.POST.get('district')
            user_profile.aphone_no = request.POST.get('aphone_no')
            user_profile.phone_no = request.POST.get('phone_no')
            user_profile.addressline1 = request.POST.get('addressline1')
            user_profile.addressline2 = request.POST.get('addressline2')
            user_profile.pin_code = request.POST.get('pin_code')
            user_profile.save()
        else:
            user=UserProfile(
                
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                phone_no = request.POST.get('phone_no'),

             # Update user profile fields
                country = request.POST.get('country'),
                state = request.POST.get('state'),
                city = request.POST.get('city'),
                district = request.POST.get('district'),
                aphone_no = request.POST.get('aphone_no'),
                addressline1 = request.POST.get('addressline1'),
                addressline2 = request.POST.get('addressline2'),
                pin_code = request.POST.get('pin_code'),
                user_id=userid
            )
            user.save()

        return redirect('profile')
    context = {
        'user': user_profile1,
        'user_profile': user_profile,
        'products3':products3
    }
    return render(request, 'profile.html', context)


#seller profile
def sellerprofile(request):
    user = request.user
    user_profile = SellerProfile.objects.get(user=user)
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        # Update user profile fields
        user_profile.country = request.POST.get('country')
        user_profile.state = request.POST.get('state')
        user_profile.city = request.POST.get('city')
        user_profile.district = request.POST.get('district')
        user_profile.aphone_no = request.POST.get('aphone_no')
        user_profile.map = request.POST.get('map')
        user_profile.gstno = request.POST.get('gstno')
        user_profile.panno = request.POST.get('panno')
        user_profile.ownername = request.POST.get('ownername')
        user_profile.phone_no = request.POST.get('phone_no')
        user_profile.addressline1 = request.POST.get('addressline1')
        user_profile.addressline2 = request.POST.get('addressline2')
        user_profile.pin_code = request.POST.get('pin_code')
        
        user_profile.save()

        return redirect('sellerprofile') 
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'sellerprofile.html', context)

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
                user = User(name=name1, email=email, role=role,first_name=name1)
                user.set_password(password)  # Set the password securely
                user.save()
                user_profile = SellerProfile(user=user)
                user_profile.save()
                return redirect('login')  
            
    return render(request, 'seller.html')
def userLogout(request):
    logout(request)
    return redirect('/')
def admindashboard(request):
    user_count = CustomUser.objects.count()
    count = CustomUser.objects.filter(role=1).count()
    count1 = Payment.objects.filter(payment_status='successful').count()
    productcount = Product.objects.filter(status=False).count()
    context = {'count': count,
               'user_count': user_count,
               'count1':count1,
               'productcount':productcount,
               }
    return render(request, 'admindashboard.html',context)



def category(request):
    stdata = Category.objects.filter(status=False)
    return render(request, "category.html", {'stdata': stdata})
def update(request, stid2):
    # Get the Category object for the given ID
    category = get_object_or_404(Category, id=stid2)

    # Get all Subcategories that belong to the selected Category
    subcategories = Subcategory.objects.filter(category=category)

    return render(request, 'addcategory.html', {'category': category, 'subcategories': subcategories})
def newcategory(request):

    error_message = ''
    new_category = Category.objects.filter(status=False)
    subcategories=Subcategory.objects.all()

    if request.method == 'POST':
        if 'cat' in  request.POST:

        # Create a new Category instance and assign values
            new_category = Category()
            new_category.category_name = request.POST.get('category_name')
            new_category.category_image = request.FILES.get('category_image')
            new_category.descriptioncat = request.POST.get('descriptioncat')
            new_category.save()
            
            return redirect("newcategory")
        else:
            categories = Category.objects.filter(status=False)
            print('Entered')
            name = request.POST['name']
            category_id = request.POST['category_id']

            print(category_id)
            description = request.POST['description']
            
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.create(
            name=name,
            description = description,
            category=category,
            )  


    context = {
            'new_category': new_category,
            'subcategories':subcategories
        
            }
    return render(request, "newcategory.html", context)
    
#######################################################
#To add Product 
def sellerindex(request):
    
    stdata = Category.objects.filter(status=False)
    category_name = request.POST.get('category')
    sub = request.POST.get('subcategory')
    stdata1 = Category.objects.filter(pk__iexact=category_name)
    stdata2 = Subcategory.objects.filter(name__iexact=sub)
    user = request.user
    userid = user.id
    if request.method == 'POST':
        print(request.POST.get('product_name'))
        print(request.POST.get('brand_name'))
        print(request.POST.get('product_description'))
        print(request.POST.get('material_description'))
        print(request.POST.get('measurements'))
        print(request.POST.get('maintenance'))
        print(request.POST.get('price'))
        print(request.POST.get('quantity'))
        print(request.POST.get('category'))
        print(request.POST.get('subcategory'))
        # Create a new Category instance and assign values
        newproduct =    Product(
        product_name = request.POST.get('product_name'),
        brand_name = request.POST.get('brand_name'),
        product_description = request.POST.get('product_description'),
        material_description = request.POST.get('material_description'),
        measurements = request.POST.get('measurements'),
        maintenance = request.POST.get('maintenance'),
        price = request.POST.get('price'),
        quantity = request.POST.get('quantity'),
        category = stdata1[0],
        subcategory = stdata2[0],

        product_images1 = request.FILES.get('product_images1'),
        product_images2 = request.FILES.get('product_images2'),
        product_images3 = request.FILES.get('product_images3'),
        product_images4 = request.FILES.get('product_images4'),
        user_id=userid
        )
        newproduct.save()   
        
        return redirect("product")
    return render(request, "sellerindex.html",{'stdata': stdata})
#######################################################
def categoryajax(request, category):
    stdata1 = Subcategory.objects.filter(category_id=category).values('name')

    # Extract the values from the queryset and add them to the data list
    data = []
    for item in stdata1:
        data.extend(item.values())

    # Print the data for debugging (optional)
    print(data)
    
    # Return the data as a JSON response
    return JsonResponse(data, safe=False)
def product(request):
    user_id = request.user.id
    stdata = Product.objects.filter(user_id=user_id, status=False)
    stdata1 = Product.objects.all()
    items_per_page = 3  # Change this to 3 to display 3 cards per page

    paginator = Paginator(stdata, items_per_page)
    page_number = request.GET.get('page')  # Get the current page number from the request
    page = paginator.get_page(page_number)
    return render(request, "product.html", {'stdata': stdata, 'stdata1': stdata1, 'page': page})
######################################################
def updateproduct(request, stid2):
    stid=Product.objects.get(id=stid2)
    stdata = Category.objects.all()
    stid1=Product.objects.filter(id=stid2)
    if request.method == 'POST':
        
        stid.product_name = request.POST.get('product_name')
        stid.brand_name = request.POST.get('brand_name')
        stid.product_description = request.POST.get('product_description')
        stid.material_description = request.POST.get('material_description')
        
        stid.measurements = request.POST.get('measurements')
        stid.maintenance = request.POST.get('maintenance')
        stid.price = request.POST.get('price')
        stid.quantity = request.POST.get('quantity')

        stid.save()
        return redirect("product")

    return render(request, 'updateproduct.html', {'stid1': stid1,'stdata':stdata})
######################################################

def deletecategory(request, stid2):
    dele=Category.objects.get(id=stid2)
    dele.status=True
    dele.save()
    return redirect('category')

def deleteproduct(request, stid2):
    dele=Product.objects.get(id=stid2)
    dele.status=True
    dele.save()
    return redirect('product')
def deleteproductadmin(request, stid2):
    dele=Product.objects.get(id=stid2)
    dele.admincontrol=True
    dele.save()
    return redirect('list')
def addproductadmin(request, stid2):
    dele=Product.objects.get(id=stid2)
    dele.admincontrol=False
    dele.save()
    return redirect('list')

def sellerpage(request):
    return render(request, "sellerpage.html")

