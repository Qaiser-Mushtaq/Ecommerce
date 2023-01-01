from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Customer, Orders
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from store.middlewares.auth import Auth_middleware
from django.utils.decorators import method_decorator
# for class based views
import datetime
from django.views import View
# Create your views here.

class index(View):
    def get(self, request):
        products = None
        cart=request.session.get('cart')
        
        if not cart:
            request.session['cart']= {}
            
        product = Product.objects.all()
        categories = Category.objects.all()
    
        return render(request, "index.html", {"product":product,
                                          "category":categories})
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        
        
        
        cart = request.session.get('cart')
        
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity -1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
            
        else: 
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        
        
        product = get_object_or_404(Product, id=product)
        return render(request, 'prodetail.html', {"product":product
                                              })

def productdetails(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'prodetail.html', {"product":product
                                              })

def category_list(request,slug):
    category = Category.objects.all()
    categories = get_object_or_404(Category,slug=slug)
    products = Product.objects.filter(category=categories)
    return render(request, 'categorylist.html', {'products':products,
                                                 "category": category})

    
def login(request):
    return render(request, "login.html")
    
def validate_login(request):
    if request.method =="POST":
        post_data = request.POST
        user_email = post_data.get('email')
        pass1 = post_data.get('password')


        try:
   # customer = Customer.get_customer_by_email(user_email)
            customer = Customer.objects.get(email = user_email)
            fname = customer.first_name
            
            if customer:
                request.session['customer'] = customer.id
                request.session['customer_email'] = customer.email
                login = True
                return HttpResponseRedirect('/index')
                '''return render(request, "index.html", {"signin" :login,
                                              "fname":fname
                                              })'''
        
            else:
                error_message = "Your Email or password is incorrect"
                return render(request, "login.html", {"error":error_message})
        except:
            error_message = "Your Email or password is incorrect"
            return render(request, "login.html", {"error":error_message})

           
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/index')


def validate(request):
    PostData = request.POST
    first_name = PostData.get("firstname")
    last_name = PostData.get("lastname")
    phone = PostData.get("phone")
    email = PostData.get("email")
    password = PostData.get("password")
    
    error_message = None
    data = Customer(
             first_name = first_name,
             last_name = last_name,
             phone = phone,
             email = email,
             password = password
             )
    if not first_name:
        error_message = " First Name Required"
    elif len(first_name) < 4:
        error_message = "First Name Should be more than 4 chracters"
    elif len(last_name) < 4:
        error_message = " Last Name should be more than 4 characters long"
    elif len(phone) < 10 :
        error_message = " Phone number should be 10 digits long"
    elif len(email) < 10 :
        error_message = " Correct Email address required"
    elif not password :
        error_message = " Password required"  
    elif data.isExists():
        error_message = "Email already exists ! Please use a unique one"
    # if we get a error the fields will be entered with previous values
    values = {
        "first_name":first_name,
              "last_name":last_name,
              "phone": phone,
              "email":email    
              }
    if not error_message:
        data.password = make_password(data.password)
               
        data.save()
        signup = True
        return render(request, "index.html", {"signup":signup})
    else:
        return render (request, "signup.html", {"error":error_message, "values": values})

def signup(request):
   return render(request, "signup.html")



class cart(View):
    def get(self, request):
        
        ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in = ids )
        
        return render(request, "cart.html", {"products":products})
        
def checkout(request):
    if request.method == "POST":
       
        print(request.method)    

        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customer = request.session.get("customer")
        cart = request.session.get('cart')
        ids = (list(cart.keys()))
        products=[]
        for i in ids:
            
            products=Product.get_product_by_id(i)  
        
        
        print(address, phone, customer , cart , products)
        for product in products:
            order = Orders(
                         customer = Customer(id = customer),
                         product = product,
                         price = product.price,
                         address = address,
                         phone = phone,
                         quantity = cart.get(str(product.id)),
                         date =datetime.date.today()
            )
            order.placeorder()
        request.session['cart'] = {}   
             
        return render(request, "cart.html")
        
    else:
            
        return render(request , "checkout.html")
    
def orders(request):
    customer = request.session.get('customer')
    
    order = Orders.objects.filter(customer=customer).order_by('-date')
    return render(request, "orders.html", {"orders":order,"name":customer})
   
    