from django.db import models
from django.contrib.auth.models import User #models
from django.utils import timezone
from datetime import datetime
PRODUCT_TYPE = (('inj','Injection'),
                ('tab','tablet'),
                ('syrp','syrup'),
                ('cap','capsule'),
                ('drp','drops'),
                ('inhl','inhalers'))

DELIVER_STATUS = (('pen','Pending'),
                  ('proc','Processing'),
                  ('delv','Delivering'),
                  ('comp','Completed') )


class Customer(models.Model):
        user_id = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
        name = models.CharField(max_length=20)
        email = models.EmailField(unique=True)
        password = models.CharField(max_length=20)
        address = models.TextField()
        phone_no = models.CharField(max_length=11)
        profile_pic = models.ImageField(default="default_profile.png",null=True,blank=True)
        join_date = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name

        class Meta:
            verbose_name = "Customer"
            verbose_name_plural = "Customers"


class Products(models.Model):
        #p_id = models.AutoField(primary_key = True)
        brand_name = models.CharField(max_length=50, null=True, blank=True)
        generic_name = models.CharField(max_length=50)
        image = models.ImageField(null=True, blank=True)
        manufacturer = models.CharField(max_length=50)
        type = models.CharField(choices=PRODUCT_TYPE,max_length=4)
        price = models.FloatField()
        prescription_required = models.BooleanField(default=False)

        def __str__(self):
            return self.brand_name

        @property
        def in_stock(self):
            from django.db.models import Sum

            d= Stock.objects.filter(products = self).aggregate(Sum('quantity')).get('quantity__sum')
            if d == None:
                return False
            else:
               return int(d) > 0

        @property
        def imageURL(self):
            try:
                url = self.image.url
            except:
                url = ''
            return url

        class Meta:
            verbose_name = "Product"
            verbose_name_plural = "Products"

class Stock(models.Model):
        products = models.ForeignKey(Products, on_delete = models.CASCADE )
        quantity = models.PositiveSmallIntegerField()
        purchase_date = models.DateTimeField()
        exp_date = models.DateTimeField()

        class Meta:
            verbose_name = "Stock"
            verbose_name_plural = "Stocks"

        def __str__(self):
            return f"{self.purchase_date}"


class Order(models.Model):
        id = models.AutoField(primary_key=True, verbose_name='Order ID')
        customer = models.ForeignKey(Customer, on_delete = models.SET_NULL , null=True, blank=False )
        order_date = models.DateTimeField(default=timezone.now,verbose_name="Order Date")
        complete = models.BooleanField(default = False,verbose_name="Status", null=False,blank=False)
        amount = models.FloatField()
        total_items = models.PositiveSmallIntegerField(verbose_name="Total Items")

        def __str__(self):
            return f"{self.id}"

        class Meta:
            verbose_name = "Order"
            verbose_name_plural = "Orders"

class OrderItems(models.Model):
        #o_id
        order = models.ForeignKey(Order, on_delete = models.CASCADE, null=True, blank=True, verbose_name="Order ID")
        product = models.ForeignKey(Products,  on_delete = models.CASCADE, null=True, blank=True, verbose_name="Product")
        prescription_img = models.ImageField(null=True, blank=True)
        quantity = models.PositiveSmallIntegerField(default = 1 ,verbose_name="Quantity", null=True, blank=True)

        def __str__(self):
            return f"{self.product} {self.quantity}"

        @property
        def get_total(self):
            total = self.product.price * self.quantity
            return total


class Delivery_Details(models.Model):
        customer = models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL, blank=True,verbose_name="Customer Name")
        order = models.ForeignKey(Order, on_delete = models.CASCADE, null=True, blank=True,verbose_name="Delivery ID")
        deliver_addr = models.CharField(max_length=100 ,verbose_name="Delivery Address")
        deliver_phn = models.CharField(max_length=20,verbose_name="Delivery Phone #")
        deliver_name = models.CharField(max_length=20,verbose_name="Receiver Name")
        deliver_status = models.CharField(default='pen', choices=DELIVER_STATUS, max_length=4 ,verbose_name="Status")
        deliver_date = models.DateTimeField(null = True,verbose_name="Delivery Date")



        def __str__(self):
            return self.deliver_addr
        class Meta:
            verbose_name = "Delivery"
            verbose_name_plural = "Deliveries"
#python -m pip install Pillow



class Notifications(models.Model):
    message = models.CharField(max_length=100, blank=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

class requested_Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=False)
    requested_medicine = models.CharField(max_length=100, blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Customer {self.customer.name} has requested \" {self.requested_medicine} \" '

    class Meta:
        verbose_name = "Requested Order"
        verbose_name_plural = "Requested Orders"
