from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound
from .models import *
from django.contrib import messages
from django.views.generic import View
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.files.storage import FileSystemStorage

@transaction.atomic
def request_product(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    if is_ajax:
        product_name = request.GET.get('product_name')
        user_id = int(request.GET.get('user_id'))
        customer = Customer.objects.get(id= user_id)
        obj = requested_Order(requested_medicine=product_name,customer=customer)
        obj.save()
        return JsonResponse({'success':'True'})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def get_search(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
            from collections import namedtuple
            text = request.GET.get('search')
            output = list(Products.objects.filter(brand_name__icontains=f"{text}").values())
            Product = namedtuple('Product',['id', 'brand_name', 'generic_name', 'image', 'manufacturer', 'type', 'price', 'in_stock'])
            products = []
            for p in output:
                id = int(p['id'])
                instock = Products.objects.get(id=id).in_stock
                prod = Product(int(p['id']),str(p['brand_name']),p['price'],p['image'],p['manufacturer'],p['type'],str(p['generic_name']),'false')
                products.append( (prod,instock) )
            return JsonResponse({'products':products})
    else:
        return homePage(request=request)
            

def homePage(request):
    mail = request.session.get('customer_mail')
    products = []
    for p in Products.objects.all():
        products.append((p, p.in_stock))
    if mail is not None:
        name = f'Hello , { Customer.objects.only("name").get(email=mail) }'
        url = 'logout/'
        btn_text= 'Logout'
        return render(request, 'online_pharmacy/home.html', {'products': products,'user_name': name, 'url':url, 'btn_text':btn_text})
    else:
        return render(request, 'online_pharmacy/home.html',
                      {'products': products, 'user_name': ' ', 'url': 'login/', 'btn_text': 'Login'})
 


@transaction.atomic
def signup_page(request):
    if request.method == 'POST':
        name = request.POST['name'].strip()
        phone = request.POST['phone']
        address = request.POST['address'].strip()
        email = request.POST['email'].strip()
        pwd1 = request.POST['pass1'].strip()
        pwd2 = request.POST['pass2'].strip()

        if pwd1 == pwd2:
            obj = Customer(name=name, phone_no=phone, address=address, email=email,password=pwd1)
            obj.save()
            request.session['customer_mail'] = email
            return homePage(request=request)

    return render(request, 'online_pharmacy/signup_page.html')


def login_page(request):

    if request.method == 'POST':
        mail = request.POST['email']
        pwd = request.POST['pass']

        customer = Customer.objects.filter(email=mail, password=pwd).first()

        if customer is not None :
            request.session['customer_mail'] = mail
            return render(request,'online_pharmacy/view_profile.html', context={'mail':customer.email,'customer': customer,'name':"Hello, "+customer.name })
        else:
            messages.error(request, 'Invalid Credentials !!')
            return render(request, 'online_pharmacy/login_page.html')

    return render(request, 'online_pharmacy/login_page.html')


def logout(request):
    request.session.clear()
    print('after logout   ',request.session.get('customer_mail'))
    return homePage(request=request)


def my_orders(request):
    mail = request.session.get('customer_mail')
    if mail is not None:
        name = f'Hello , {Customer.objects.only("name").get(email=mail)}'

        customer = Customer.objects.get(email=mail)
        order = Order.objects.filter(customer=customer, complete=True)
        for row in order:

            row.order = Order.objects.get(id=row.id)


        return render(request, 'online_pharmacy/view_order.html',context={'name': name , 'table': order , 'details' : OrderItems.objects.filter(order=row.order) })
    else:
        return redirect('login_page')




def store_page(request):
    allProds = []
    catprods = Products.objects.values('type', 'id')
    cats = {item['type'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(type=cat)
        n = len(prod)
        nSlides = n // 4 + ((n / 4) + ((n % 4) != 0))
        allProds.append([prod, range_with_floats(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request,'online_pharmacy/store_page.html',params)

def range_with_floats(start, stop):
    while stop > start:
        yield start
    return range_with_floats(start, stop)



def user_panel(request):
    mail = request.session.get('customer_mail')
    if mail is not None:
        name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
        return render(request, 'online_pharmacy/customer_panel.html',context={'name': name })
    else:
        return redirect('login_page')


def track_my_orders(request):
       mail = request.session.get('customer_mail')
       if mail is not None:
        name =Customer.objects.only("name").get(email=mail)
        table = Delivery_Details.objects.filter(customer=name).exclude(deliver_status =  'comp')

        DELIVER_STATUS = {'pen': 'Pending','proc': 'Processing','delv': 'Delivering','comp': 'Completed'}
        for row in table:
            row.deliver_status = DELIVER_STATUS[row.deliver_status]

        d = table
        return render(request, 'online_pharmacy/track_order.html', context={'name': name , 'd': d})
       else:
        return redirect('login_page')


def customer_pnl_view_details(request,order_id):
    mail = request.session.get('customer_mail')
    if mail is not None:
        name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
        order=Order.objects.get(id=order_id)
        delivery = Delivery_Details.objects.get(order=order)
        return render(request, 'online_pharmacy/customer_pnl_view_details.html', context={'order':order,'delivery':delivery,'items':OrderItems.objects.filter(order=order),'name': name})
    else:
        return redirect('login_page')


def customer_pnl_view_orders_details(request, order_id):
        mail = request.session.get('customer_mail')
        if mail is not None:
            name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
            order = Order.objects.get(id=order_id)
            delivery = Delivery_Details.objects.get(order=order)
            return render(request, 'online_pharmacy/customer_pnl_view_details.html',context={'order':order,'delivery':delivery,'items': OrderItems.objects.filter(order=order), 'name': name})
        else:
            return redirect('login_page')


def customer_dashboard(request):
    mail = request.session.get('customer_mail')
    if mail is not None:
        name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
        return render(request, 'online_pharmacy/dashboard.html', context={'name': name})
    else:
        return redirect('login_page')


def view_profile(request):

    if request.method == 'POST':
        img = request.POST.get('profile_pic') or None
        uname =request.POST.get('name').strip()
        phn =request.POST.get('phone')
        mail =request.POST.get('mail')
        addr =request.POST.get('address').strip()
        
        if img != None:
            print('img found') 
            Customer.objects.update_or_create(email=mail,defaults={'profile_pic':img, 'name':uname, 'phone_no':phn, 'address':addr,'email':mail } )
            customer = Customer.objects.filter(email=mail).first()
            name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
            return render(request, 'online_pharmacy/view_profile.html', context={'customer': customer ,'name':name})
        else:
            Customer.objects.update_or_create(email=mail,defaults={'name':uname, 'phone_no':phn, 'address':addr,'email':mail } )
            print('img not found')
            customer = Customer.objects.filter(email=mail).first()
            name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
            return render(request, 'online_pharmacy/view_profile.html', context={'customer': customer ,'name':name})
    else:
        print('NOT POST')     
        mail = request.session.get('customer_mail')
        if mail is not None:
            customer = Customer.objects.filter(email=mail).first()
            name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
            return render(request, 'online_pharmacy/view_profile.html', context={'customer': customer ,'name':name})
        else:
            return redirect('login_page')




def store(request):

    if Auth['logged_in']:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Products.object.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'online_pharmacy/home.html', context)


def cart(request):
    mail = request.session.get('customer_mail')
    if mail is not None:
        name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
        url = 'logout/'
        btn_text = 'Logout'
        return render(request, 'online_pharmacy/cart.html',
                      {'products': Products.objects.all(), 'user_name': name, 'url': url, 'btn_text': btn_text})
    else:
        return render(request, 'online_pharmacy/cart.html',
                      {'products': Products.objects.all(), 'user_name': ' ', 'url': 'login/', 'btn_text': 'Login'})



def view_details(request, p_id):
    print(p_id)
    p = Products.objects.get(id=p_id)
    in_stock = Products.objects.get(id=p_id).in_stock
    mail = request.session.get('customer_mail')
    if mail is not None:
        name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
        url = 'logout/'
        btn_text = 'Logout'
        return render(request, 'online_pharmacy/view_details.html',
                      {'product':p,'in_stock':in_stock, 'user_name': name, 'url': url, 'btn_text': btn_text})
    else:
        return render(request, 'online_pharmacy/view_details.html',
                      {'product':p,'in_stock':in_stock, 'user_name': ' ', 'url': 'login/', 'btn_text': 'Login'})






@csrf_exempt
def checkout(request):
    print('ORder request received')
    def get_stock(product:Products,quantity:int):
        stocks = Stock.objects.filter(products=product).order_by('purchase_date')
        required = quantity
        res = []
        for stock in stocks:

            if stock.quantity == 0:
                continue
            elif stock.quantity >= required:
                res.append((stock,required))
                return res
            else:
                required = required - stock.quantity
                res.append( (stock,stock.quantity))
        else:
            return None

    if request.method == 'POST':
        if len(request.POST.get('user_id'))>0:
            user_id = int(request.POST.get('user_id'))
            customer = Customer.objects.get(id=user_id)
            cart = request.POST.get('cart')
            cart = json.loads(cart)

            
            products ={}
            prescriptions={}
            amount = 0
            items = 0
            for key in cart.keys():
                p = Products.objects.get(id=key)
                products[p] = cart[key]
                items = items + cart[key]
                amount = amount + (p.price * cart[key])
                img = request.FILES.get('img_'+key)
                if img != None:
                    prescriptions[key]=img  
                   
            '''ADDing ORDER'''
            try:
                with transaction.atomic():
                    t_id_1 = transaction.savepoint()
                    
                    Order.objects.create(customer=customer, amount=amount, total_items=items)
                    order = Order.objects.latest('id')

                    for p in products:
                        if prescriptions.get(str(p.id)) == None:
                            OrderItems.objects.create(order=order, product=p, quantity= products[p] )
                        else:
                            print('adding ',prescriptions.get(str(p.id )))
                            OrderItems.objects.create(order=order, product=p,prescription_img=prescriptions.get(str(p.id ))   , quantity= products[p] )
                        stock = get_stock(p , products[p])
                        if stock != None:
                            for stk,qty in stock:
                                print(stk,'  ',qty)
                                stk.quantity = stk.quantity - qty
                                stk.save()

                        else:
                            return JsonResponse(
                                {'success': 'false', 'msg': 'Sorry !! we are out of stock for your ordered products'})

                    Delivery_Details.objects.create(customer=customer, order=order, deliver_addr=request.POST.get('address'),
                                                    deliver_phn=request.POST['phoneNo'], deliver_name=request.POST['name'])
                    t_id_2 = transaction.savepoint()
                    transaction.savepoint_commit(t_id_2)
                    return homePage(request=request)
            except Exception as e:
                transaction.savepoint_commit(t_id_1)
                return HttpResponse(
                    json.dumps({'success': 'false', 'msg': 'Order failed due to some unknown issue'}),
                    content_type="application/json")
        else:
            return redirect('login_page')

    else: # for just viewing checout page
        mail = request.session.get('customer_mail')
        if mail is not None:
            name = f'Hello , {Customer.objects.only("name").get(email=mail)}'
            url = 'logout/'
            btn_text = 'Logout'
            return render(request, 'online_pharmacy/checkout.html',
                          {'user_name': name, 'url': url, 'btn_text': btn_text})
        else:
            return render(request, 'online_pharmacy/checkout.html',
                          {'user_name': ' ', 'url': 'login/', 'btn_text': 'Login'})

    


@transaction.atomic
def updateItem(request):

    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)






