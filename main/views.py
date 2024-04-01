from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from accounts.models import Product,CustomUser,SellerProfile,Category,Subcategory,UserProfile
from serviceapp.models import CompareProduct, Feedback
from rest.models import Addressuser, DeliveryAgentProfile
from main.models import BookCart,Wishlist,Payment,OrderItem,Order
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
User = get_user_model
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # stdata = Category.objects.filter(status=False)
    # products12 = Product.objects.filter(status=False, admincontrol=False)
    # products3 = Category.objects.filter(status=False)
    # products1 = Subcategory.objects.filter(status=False)
    # profiles = DeliveryAgentProfile.objects.all()
    #product = Product.objects.get(id=3)
    #print(product)

    # context = {
    #     # 'products12': products12, 
    #     # 'stdata':stdata,
    #     # 'products3':products3,
    #     # 'products1':products1,
    #     # #'product':product,
    #     # 'profiles':profiles,
    # }
    return render(request,'index.html')
def cart(request):
    # Assuming you have the user object for the currently logged-in user
    user_id = request.user.id  # Replace with your user retrieval logic if needed
# Retrieve books in the user's cart
    books_in_cart = BookCart.objects.filter(user_id=user_id)
    products3 = Category.objects.filter(status=False)

# Retrieve book details for the books in the cart
    book_details = Product.objects.filter(id__in=books_in_cart.values_list('product_id', flat=True))
    print(book_details)
    print("hai")
    total_price = sum(books_in_cart.product.price * books_in_cart.quantity for books_in_cart in books_in_cart)
    
    #product_id=BookCart.request.get(product_id=product_id)
    st = BookCart.objects.filter(user_id=user_id)
    return render(request,"cart.html",{'cart_books':book_details,'st':st,'total_price':total_price,'products3':products3})
def increase_item(request, item_id):
    try:
        cart_item = BookCart.objects.get(product_id=item_id)
        product = Product.objects.get(id=cart_item.product_id)

        # Calculate the new quantity, ensuring it doesn't exceed the product's quantity
        new_quantity = min(int(cart_item.quantity) + 1, int(product.quantity))

        cart_item.quantity = str(new_quantity)
        cart_item.save()
    except BookCart.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    except Product.DoesNotExist:
        pass  # Handle the case when the associated product doesn't exist

    return redirect('cart')

def decrease_item(request, item_id):
    try:
        cart_item = BookCart.objects.get(product_id=item_id)
        
        # Decrease the quantity by 1, but ensure it doesn't go below 1
        new_quantity = max(int(cart_item.quantity) - 1, 1)
        
        cart_item.quantity = str(new_quantity)
        cart_item.save()
    except BookCart.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart

    return redirect('cart')
from django.db.models import Avg
def singleview(request, product_id):
    products3 = Category.objects.filter(status=False)
    products1 = Subcategory.objects.all()
    user_wishlist = Wishlist.objects.filter(user=request.user)
    user_wishlist_ids = [item.product.id for item in user_wishlist]
    compare_properties = CompareProduct.objects.filter(user=request.user).first()
    compare_property_list = compare_properties.products.all() if compare_properties else []
    # Fetch products in the user's cart
    user_cart = BookCart.objects.filter(user=request.user)
    user_cart_ids = [item.product.id for item in user_cart]
    # Get the product or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    star=Feedback.objects.filter(product=product)
    average_rating = star.aggregate(Avg('rating'))['rating__avg']
    ratingin=5
    order_item_exists = OrderItem.objects.filter(user=request.user, product=product).exists()
    review_item_exists = Feedback.objects.filter(userprofile=request.user, product=product).exists()

    
    # Set currency and amount (you can customize these values)
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Initialize Razorpay client
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    rating_range = range(1, 6)
    # Get the order id of the newly created order
    razorpay_order_id = razorpay_order['id']

    # Define the callback URL (you may want to customize this)
    callback_url = 'paymenthandler/'

    # Prepare context data to pass to the frontend
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
        'product': product,
        'products3':products3,
        'user_wishlist_ids': user_wishlist_ids,
        'user_cart_ids': user_cart_ids,
        'compare_properties': compare_property_list,
        'star':star,
        'order_item_exists':order_item_exists,
        'average_rating':average_rating,
        'ratingin':ratingin,
        'review_item_exists':review_item_exists,
        'rating_range':rating_range,
        'products1':products1  # Include the product in the context
    }

    # Render the 'singleview.html' template with the context
    return render(request, 'singleview.html', context=context)

def add_cart(request, bookid2):
    userid=request.user.id
    product = get_object_or_404(Product, id=bookid2)
    cart_item, created = BookCart.objects.get_or_create(user=request.user,product_id=product.id)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('list')
def add_cart1(request, bookid2):
    try:
        # Ensure that bookid2 is a valid integer
        bookid2 = int(bookid2)

        # Create a BookCart object (assuming your model fields match)
        userid = request.user.id
        book = BookCart(
            user_id=userid,
            product_id=bookid2
        )
        book.save()
        bookid=bookid2

        # Redirect to 'singleview' with the 'bookid' parameter
        return redirect('singleview',bookid)
    except ValueError:
        # Handle the case where bookid2 is not a valid integer
        return HttpResponseNotFound("Invalid book ID")

def delete_cart(request, bookid2):
    remove=BookCart.objects.filter(product_id=bookid2)
    remove.delete()
    return redirect('cart')
def wishlist(request):
    # Assuming you have the user object for the currently logged-in user
    user_id = request.user.id  # Replace with your user retrieval logic if needed
# Retrieve books in the user's cart
    books_in_cart = Wishlist.objects.filter(user_id=user_id)
    products3=Category.objects.filter(status=False)
# Retrieve book details for the books in the cart
    book_details = Product.objects.filter(id__in=books_in_cart.values_list('product_id', flat=True))
    return render(request,"wishlist.html",{'cart_books':book_details,'products3':products3})

def add_wishlist(request, bookid2):
    userid=request.user.id
    book = Wishlist(
        user_id=userid,
        product_id=bookid2        
    )
    book.save()
    return redirect('list')
def delete_wishlist(request, bookid2):
    remove=Wishlist.objects.filter(product_id=bookid2)
    remove.delete()
    return redirect('list')


def delete_wishlistpage(request, bookid2):
    remove=Wishlist.objects.filter(product_id=bookid2)
    remove.delete()
    return redirect('wishlist')

def catalog(request):
    stdata = Product.objects.filter(status=False)
    return render(request, "catalog.html", {'stdata': stdata})
from django.shortcuts import render
from .models import Category, Product
##########################################
###############     product_list            to display the category bed     #####################
########################################
def product_list(request):
    products3 = Category.objects.filter(status=False)
    products = Product.objects.filter(status=False)

    context = {
        'products3': products3, 
        'products':products,
    }
    
    return render(request, "product_list.html",context )

def separate(request):

    return render(request, "separate.html")



def display_all_objects(request):
    objects = CustomUser.objects.all()  # Retrieve all objects from YourModel
    seller_profiles = SellerProfile.objects.all()  # Retrieve all SellerProfile objects

    context = {
        'objects': objects,
        'seller_profiles': seller_profiles,  # Add SellerProfile data to the context
    }

    return render(request, 'display_all_objects.html', context)
# def users(request):
#     stdata = CustomUser.objects.all()
#     return render(request, "users.html", {'stdata': stdata})
#
def inactiveseller(request, stid2):
    dele=CustomUser.objects.get(id=stid2)
    if dele.is_active == False: 
        dele.is_active=True
    else:
        dele.is_active=False
    dele.save()
    return redirect('display_all_objects')

def book_list_by_category(request, category):
    products3 = Category.objects.filter(status=False)
    products1 = Subcategory.objects.all()
    category_obj = get_object_or_404(Category, category_name=category)
    print(category_obj)
    items = Product.objects.filter(category=category_obj,status=False, admincontrol=False)
    products22 = Product.objects.filter( category=category_obj,admincontrol=True)
    products23 = Product.objects.filter( category=category_obj,status=True)
    categories = Category.objects.all()
    user_wishlist = Wishlist.objects.filter(user=request.user)
    user_wishlist_ids = [item.product.id for item in user_wishlist]
    user_cart = BookCart.objects.filter(user=request.user)
    user_cart_ids = [item.product.id for item in user_cart]
    context = {
        'categories': categories,
        'category':category,
        'products12':items,
        'user_wishlist_ids': user_wishlist_ids,
        'user_cart_ids': user_cart_ids,
        'products3': products3,
        'products1':products1,
        'products22':products22,
        'products23':products23,


    }
    return render(request, 'list.html', context)
        
def book_list_by_subcategory(request, category):
    print("Entered")
    category_obj = get_object_or_404(Subcategory,name=category)
    print(category_obj)
    products3 = Category.objects.filter(status=False)
    products1 = Subcategory.objects.all()
    
    print(category_obj)
    items = Product.objects.filter(subcategory=category_obj,status=False, admincontrol=False)
    products22 = Product.objects.filter( subcategory=category_obj,admincontrol=True)
    products23 = Product.objects.filter( subcategory=category_obj,status=True)
    categories = Category.objects.all()
    user_wishlist = Wishlist.objects.filter(user=request.user)
    user_wishlist_ids = [item.product.id for item in user_wishlist]
    user_cart = BookCart.objects.filter(user=request.user)
    user_cart_ids = [item.product.id for item in user_cart]
    context = {
        'categories': categories,
        'category':category,
        'products12':items,
        'user_wishlist_ids': user_wishlist_ids,
        'user_cart_ids': user_cart_ids,
        'products3': products3,
        'products1':products1,
        'products22':products22,
        'products23':products23,


    }
    return render(request, 'list.html', context)


    

from django.contrib.auth.decorators import login_required
def list(request):
    products3 = Category.objects.filter(status=False)
    products12 = Product.objects.filter(status=False, admincontrol=False)
    products22 = Product.objects.filter(admincontrol=True)
    products23 = Product.objects.filter(status=True)
    products1 = Subcategory.objects.all()
    
    user_wishlist = Wishlist.objects.filter(user=request.user)
    user_wishlist_ids = [item.product.id for item in user_wishlist]

    # Fetch products in the user's cart
    user_cart = BookCart.objects.filter(user=request.user)
    user_cart_ids = [item.product.id for item in user_cart]

    # Pagination
    items_per_page = 9  # Adjust this to the number of items per page you want

    paginator = Paginator(products12, items_per_page)
    page_number = request.GET.get('page')  # Get the current page number from the request
    page = paginator.get_page(page_number)

    context = {
        'products12': page,  # Use the paginated results
        'user_wishlist_ids': user_wishlist_ids,
        'user_cart_ids': user_cart_ids,
        'products3': products3,
        'products1': products1,
        'products22': products22,
        'products23': products23
    }
    return render(request, 'list.html', context)

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
from django.utils import timezone
def paymentsuccess(request):
    # Your logic for handling a successful payment goes here
    # You can use the 'order_item_id' to retrieve specific order information
    return render(request, 'paymentsuccess.html')

def paymentfail(request):
    return render(request, "paymentfail.html")
def user_orders(request):
    if request.user.is_authenticated:   

        # Query the Payment model to get payments for the authenticated user
        user_payments = Payment.objects.filter(user=request.user)
        user_payments3 = Payment.objects.filter(user=request.user, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)

        user_payments1 = OrderItem.objects.filter(user=request.user)


        context = {
            'user_payments': user_payments,
            'user_payments1': user_payments1,
            'orders_count': user_payments3.count(),


        }
        return render(request, 'user_orders.html', context)
    else:
    # Get the user's orders
        user = request.user  # Assuming the user is logged in
        orders = Payment.objects.filter(user=user)
        order2 = OrderItem.objects.all()

        products3 = Category.objects.filter(status=False)
        products12 = Product.objects.all()
        products1 = Subcategory.objects.all()
    context = {
        'user_email': user.email,
        'orders': orders,
        'orders_count': orders.count(),
        'products3': products3,
        'products1':products1,
        'products12': products12,
        'order2':order2,
        'order2_count': order2.count(),
    }
    return render(request, 'user_orders.html', context)
def deletepending(request):
    # Get the user's orders
    user = request.user  # Assuming the user is logged in
    
    order2 = OrderItem.objects.filter(user=user,status=False)
    order2.delete()
    print(order2)
    
    
    return redirect('user_orders')
def search_product(request):
    query = request.GET.get('query')
    print("Query:", query)

   
    if query:
        products = Product.objects.filter(
            # Q(category__icontains=query) | Q(subcategory__icontains=query) |
              Q(brand_name__icontains=query) | Q(product_name__icontains=query) | Q(price__icontains=query) | Q(category__category_name__icontains=query)  | Q(subcategory__name__icontains=query)
        )
    else:
       
        products = []
    product_data = []
    
    for product in products:
        
        product_dict = {
            'id': product.pk,
            'product_images1': product.product_images1.url,
            'product_name':  product.product_name,
            'brand_name':  product.brand_name,
            'subcategory':  product.subcategory.name,
            'category':  product.category.category_name,
            'price':  product.price,
            
        }
        product_data.append(product_dict)
        print(product_data)
    return JsonResponse({'product': product_data})

def payment(request, order_id):
    order1 = Order.objects.get(pk=order_id)
    user = request.user
    profile = UserProfile.objects.get(user=user)
    
    # For Razorpay integration
    currency = 'INR'
    amount = order1.total_amount 
    amount_in_paise = int(amount * 100)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'  # Capture payment manually after verifying it
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args=[order_id])

    # Create a Payment record
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        amount=order1.total_amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
    payment.order.add(order1)

    # Prepare the context data
    context = {
        'user': request.user,
        'order1': order1,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'amount': order1.total_amount,
        'callback_url': callback_url,
        'profile': profile,
    }

    return render(request, 'Payment.html', context)

def order1(request, product_id):
    if request.method == 'POST':
        print(request.POST)
        # Get the form data from the POST request
        user = request.user
        product = Product.objects.get(id=product_id)  # Assuming you have a Product model
        profile = UserProfile.objects.get(user=user)  # Assuming you have a UserProfile model
        state = request.POST.get('state')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')
        aphone_no = request.POST.get('aphone_no')
        phone_no = request.POST.get('phone_no')
        addressline2 = request.POST.get('addressline2')
        addressline1 = request.POST.get('addressline1')
        district = request.POST.get('district')
        country = request.POST.get('country')
        total_amount = request.POST.get('total_amount')
        quantity = request.POST.get('quantity')
        # You can similarly get other form fields

        # Create and save the Order object
        order = Order.objects.create(
            user=user,
            profile=profile,
            state=state,
            total_amount=total_amount,
            quantity=quantity,
            country=country,
            district=district,
            addressline1=addressline1,
            addressline2=addressline2,
            phone_no=phone_no,
            aphone_no=aphone_no,
            pin_code=pin_code,
            city=city
            # Set other fields here
        )

        # Add the product to the order's many-to-many relationship
        order.product = product
        order.save()
        return redirect('payment', order_id=order.id)
        # Redirect to a success page or perform any other action
         # Replace 'success_page' with the actual URL name

    # Handle GET request (display the form)
    product = Product.objects.get(id=product_id)  # Assuming you have a Product model
    context = {
        'product': product,
        'user': request.user,
        'profile': UserProfile.objects.get(user=request.user),  # Assuming you have a UserProfile model
    }
    return render(request, 'order1.html', context)


@csrf_exempt
def paymenthandler(request, order_id):
    # Only accept POST requests.
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)  # Convert Decimal to paise

        # Capture the payment.
        razorpay_client.payment.capture(payment_id, amount)
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

        # Update the order with payment ID and change status to "Successful."
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        

        # Update the Order status to True.
        order = Order.objects.get(id=order_id)
        order.status = True
        order.save()
        # Assuming an order can have multiple products, loop through them
        for product in order.product.all():
            product.quantity =str(int(product.quantity)-(order.quantity))
            product.save()

    
        # Render the success page on successful capture of payment.
        return render(request, 'paymentsuccess.html')

    else:
        # If other than POST request is made.
        return render(request, 'paymentfail.html')

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)

    # Create a list of subcategory names
    subcategory_names = [subcategory.name for subcategory in subcategories]

    return JsonResponse(subcategory_names, safe=False)
from collections import Counter
import json
from django.db.models import Count
from django.db.models import Sum
def salesadmin(request):
    # Query the Order model and include related models (Product and User)
    successful_payments = Payment.objects.filter(payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)
    orders = OrderItem.objects.filter(order__in=successful_payments)
    categories = set(order.product.category.category_name for order in orders)
    # Count occurrences of each category
    category_counts = {category: sum(1 for order in orders if order.product.category.category_name == category) for category in categories}
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    category_counts_json = json.dumps(category_counts)    
    order = OrderItem.objects.all()
    orders1 = OrderItem.objects.filter(order__in=successful_payments)
    orders = OrderItem.objects.filter(order__in=successful_payments)
    total_price_sum = orders.aggregate(total_price_sum=Sum('total_price'))['total_price_sum']
    total_arts_uploaded=orders1.count()
    totalorderscount=orders.count()
    ordercount=order.count()
    successful_orders = Payment.objects.filter(payment_status=Payment.PaymentStatusChoices.SUCCESSFUL).values('user__name').annotate(order_count=Count('id'))

    # Print the results
    for order in successful_orders:
        print(f"User: {order['user__name']}, Successful Orders Count: {order['order_count']}")
    
    successful_order = Payment.objects.filter(payment_status=Payment.PaymentStatusChoices.SUCCESSFUL).values('user__name').annotate(order_count=Count('id')).order_by('-order_count')

    context = {
        'orders': orders,
        'orders1':orders1,
        'total_arts_uploaded':total_arts_uploaded,
        'totalorderscount':totalorderscount,
        'ordercount':ordercount,
        'category_counts':category_counts,
        'category_counts_json':category_counts_json,
        'total_price_sum':total_price_sum,
        'successful_order':successful_order,
        
    }
    return render(request, 'salesadmin.html', context)
def seminar(request):
    user_id = request.user.id
    order = Product.objects.request.GET.get('userid')
    print(order)

    orders = Order.objects.filter(status=True, user_id=user_id)
    print(orders)
    context = {
        'orders': orders
    }
    return render(request, 'seminar.html', context)

def ordercart(request, product_id):
    if request.method == 'POST':
        print(request.POST)
        # Get the form data from the POST request
        user = request.user
        product = Product.objects.get(id=product_id)  # Assuming you have a Product model
        profile = UserProfile.objects.get(user=user)  # Assuming you have a UserProfile model
        state = request.POST.get('state')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')
        aphone_no = request.POST.get('aphone_no')
        phone_no = request.POST.get('phone_no')
        addressline2 = request.POST.get('addressline2')
        addressline1 = request.POST.get('addressline1')
        district = request.POST.get('district')
        country = request.POST.get('country')
        total_amount = request.POST.get('total_amount')
        quantity = request.POST.get('quantity')
        # You can similarly get other form fields

        # Create and save the Order object
        order = Order(
            user=user,
            product=product,
            profile=profile,
            state=state,
            total_amount=total_amount,
            quantity=quantity,
            country=country,
            district=district,
            addressline1=addressline1,
            addressline2=addressline2,
            phone_no=phone_no,
            aphone_no=aphone_no,
            pin_code=pin_code,
            city=city
            # Set other fields here
        )
        order.save()
        
        return redirect('payment', order_id=order.id)
        # Redirect to a success page or perform any other action
         # Replace 'success_page' with the actual URL name

    # Handle GET request (display the form)
    product = Product.objects.get(id=product_id)  # Assuming you have a Product model
    context = {
        'product': product,
        'user': request.user,
        'profile': UserProfile.objects.get(user=request.user),  # Assuming you have a UserProfile model
    }
    return render(request, 'order1.html', context)

def create_order(request):
    user = request.user
    cart_items = BookCart.objects.filter(user=user, status=True)
    profile = UserProfile.objects.get(user=user) 
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    order = None  # Define 'order' before the if block

    if request.method == 'POST':
        if cart_items.exists():
            # Create an order for each cart item
            for cart_item in cart_items:
                print(type(total_price))
                order = Payment.objects.create(
                    user=request.user,
                    profile=request.user.userprofile,  # Assuming you have a UserProfile linked to CustomUser
                    total_amount=total_price,  
                )
                print(order)
                # Mark the cart item as processed
                order.cart_items.add(cart_item)                
                order.country=profile.country
                order.district=request.POST.get('district')
                order.addressline1=request.POST.get('addressline1')
                order.addressline2=request.POST.get('addressline2')
                order.phone_no=request.POST.get('phone_no')
                order.aphone_no=request.POST.get('aphone_no')
                order.state=request.POST.get('state')
                order.city=request.POST.get('city')
                order.pin_code=request.POST.get('pin_code')
                
                order.save()
            # Optionally, you can redirect the user to a success page or any other page after creating the orders.
            return redirect('payment', order_id=order.id)

    context = {
        'cart_items':cart_items,
        'user': request.user,
        'profile': profile,
    }  
    # Handle GET request or any other case (e.g., when the cart is empty)
    # Render a template or return a response as needed.
    return render(request, 'create_order.html', context)


def homepage(request):
    user=request.user
    cart_items = BookCart.objects.filter(user=request.user, status=True)
    total_price = Decimal(sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items))
    profile = UserProfile.objects.get(user=user) 

    
    currency = 'INR'

    # Set the 'amount' variable to 'total_price'
    amount = int(total_price*100)
    # amount=20000

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
    if request.method == 'POST':
        print(request.POST.get('state'))
        

        order = Payment.objects.create(
            user=request.user,
            profile=request.user.userprofile,
            
            country=profile.country,
            district=request.POST.get('district'),
            addressline1=request.POST.get('addressline1'),
            addressline2=request.POST.get('addressline2'),
            phone_no=request.POST.get('phone_no'),
            aphone_no=request.POST.get('aphone_no'),
            state=request.POST.get('state'),
            city=request.POST.get('city'),
            total_amount=total_price,
            pin_code=request.POST.get('pin_code'),
        )

        # Add the products to the order
        for cart_items in cart_items:
            order.cart_items.add(cart_items)

        # Save the order to generate an order ID
        order.save()

    # Create a context dictionary with all the variables you want to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'profile': profile,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'homepage.html', context=context)

def checkout_complete(request):
    user = request.user
    
    #\cart = get_object_or_404(AddCart, user=user)
    cart_items = BookCart.objects.filter(user=user)
    products = BookCart.objects.filter(user=user)
    profile = UserProfile.objects.get(user=user) 
    if not cart_items:
        return render(request, 'order1.html')
    total_price = Decimal(sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items))
    # total_price = cart_item.product.selling_price * cart_item.quantity    
    currency = 'INR'

    # Set the 'amount' variable to 'total_price'
    amount = int(total_price*100)
    # amount=20000

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    order = Payment.objects.create(
        user=request.user,
        amount=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
    phone_no = request.POST.get('phone_no')
    print("phone_no")
    print(phone_no)
    if request.method == 'POST':

        print(request.POST.get('state'))

    print("phone_no")
    # Add the products to the order
    for cart_item in cart_items:
        product = cart_item.product
        price = product.price
        quantity = cart_item.quantity
        total_item_price = price * quantity

        # Create an OrderItem for this product
        order_item = OrderItem.objects.create(
            user=user,
            order=order,
            product=product,  # Set the seller of the product as the seller of the order item
            quantity=quantity,
            price=price,
            total_price=total_item_price,
            country=request.POST.get('country'),
            district=request.POST.get('district'),
            addressline1=request.POST.get('addressline1'),
            addressline2=request.POST.get('addressline2'),
            phone_no=request.POST.get('phone_no'),
            aphone_no=request.POST.get('aphone_no'),
            state=request.POST.get('state'),
            city=request.POST.get('city'),
            pin_code=request.POST.get('pin_code')


        )

    # Save the order to generate an order ID
    order.save()

    # Create a context dictionary with all the variables you want to pass to the template
    context = {
        'order_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
        'profile':profile,
        'user':user,
        'products':products,
        

    }

    return render(request, 'order1.html', context)
##############single product##########

def buyNowComplete(request, product_id):
    
    user = request.user
    profile = get_object_or_404(UserProfile, user=user) 
    



    try:
        
        product = get_object_or_404(Product, id=product_id)
        total_price = Decimal(product.price * 1)
        print(total_price)
        amount = int(total_price * 100)
        
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency='INR',
            payment_capture='0'
        ))

        razorpay_order_id = razorpay_order['id']
        callback_url = '/paymenthandler/'

        order = Payment.objects.create(
            user=request.user,
            amount=amount/100,
            razorpay_order_id=razorpay_order_id,
            payment_status=Payment.PaymentStatusChoices.PENDING,
        )
        

        # Add the product to the order
        order_item = OrderItem.objects.create(
            order=order,
            user=user,
            product=product,
            quantity=1,
            price=product.price,
            total_price=amount,
            
            
        )
        
        order.save()
        cart_items=Product.objects.get(id=product_id)
        print("echo")
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            selected_address_id = request.POST.get('selected_address')
            phone_no = request.POST.get('phone_no')
            aphone_no = request.POST.get('aphone_no')
            addressline1 = request.POST.get('addressline1')
            addressline2 = request.POST.get('addressline2')
            city = request.POST.get('city')
            district = request.POST.get('district')
            state = request.POST.get('state')
            country = request.POST.get('country')
            pin_code = request.POST.get('pin_code')
            selected_address = Addressuser.objects.get(id=selected_address_id)
            print(selected_address)
            print("addressssssss")
            
            # Create a new OrderItem instance with the form data
            order_item1 = OrderItem(
                user=request.user,  # Assuming you have a logged-in user
                name=name,
                email=email,
                phone_no=phone_no,
                aphone_no=aphone_no,
                addressline1=addressline1,
                addressline2=addressline2,
                city=city,
                district=district,
                state=state,
                country=country,
                address=selected_address,
                pin_code=pin_code
            )
            order_item1.save()
        # Create a context dictionary with variables for the template
        print("echo1")
        
        context = {
            'product': cart_items,
            'total_price': total_price,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': 'INR',
            'callback_url': callback_url,
            'profile':profile,
            

        }

        return render(request, 'order1.html', context=context)

    except (Product.DoesNotExist, ) as e:
        # Handle cases where product or seller does not exist
        return HttpResponseBadRequest("Product or Seller does not exist.")

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature.
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        if not result:
            # Signature verification failed.
            return render(request, 'paymentfail.html')

        # Signature verification succeeded.
        # Retrieve the order from the database
        try:
            order = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        except Payment.DoesNotExist:
            return HttpResponseBadRequest("Order not found")

        if order.payment_status == Payment.PaymentStatusChoices.SUCCESSFUL:
            # Payment is already marked as successful, ignore this request.
            return HttpResponse("Payment is already successful")

        if order.payment_status != Payment.PaymentStatusChoices.PENDING:
            # Order is not in a pending state, do not proceed with stock update.
            return HttpResponseBadRequest("Invalid order status")

        
        amount = int(order.amount * 100) 
        razorpay_client.payment.capture(payment_id, amount)

        
        order.payment_id = payment_id
        order.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        order.save()
        
        user=request.user
        # Retrieve the cart items associated with the cart
        cart_items = BookCart.objects.filter(user=user)
        for cart_item in cart_items:
            product = cart_item.product
            if product.price >= cart_item.quantity:
                # Decrease the product stock and update ProductSummary
                
                product.quantity =str(int(product.quantity)-(cart_item.quantity))
                product.save()
                # Remove the item from the cart
                cart_item.delete()
            else:
                
                return HttpResponseBadRequest("Insufficient stock for some items")
        
        return redirect('user_orders')

        # return redirect('order_summary', order_id=order.id)

    return HttpResponseBadRequest("Invalid request method")


from xhtml2pdf import pisa
def print_as_pdf(request, stid2):
    if request.user.is_authenticated:   

        # Query the Payment model to get payments for the authenticated user
        user_payments = Payment.objects.filter(user=request.user)
        user_payments1 = OrderItem.objects.filter(user=request.user,order_id=stid2)
        print("red")
        print(user_payments1)
        context = {
            'user_payments': user_payments,
            'user_payments1': user_payments1,

        }

    
    template_path = 'templates\printpdf.html'  # Update with the actual path to your HTML template.

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contract_{stid2}.pdf"'

    # Render the HTML template to PDF
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
        rendered_html = render(request, 'printpdf.html', context)

        # Create a PDF using pisa
        pisa_status = pisa.CreatePDF(
            rendered_html.content,
            dest=response,
            link_callback=None  # Optional: Handle external links
        )
    return response