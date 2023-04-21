from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.admin import AdminSite
from django.shortcuts import render,redirect
from django.http import HttpResponse
# Register your models here.
from .models import *
from datetime import date, timedelta
from django.db.models import Sum
from decimal import Decimal
'''
===================
'''

class MyAdminSite(AdminSite):

    def get_urls(self):
         from django.urls import path
         urls = super().get_urls()
         u = [
             path('online_pharmacy/order_details/<int:order_id>/', self.admin_view(self.order_details)),
             path('', self.admin_view(self.index)),
         ]
         return u+urls


    def today_sale(self):
        amt = Order.objects.filter(order_date__contains=date.today()).aggregate(Sum('amount')).get('amount__sum')
        if amt == None:
            return 0
        else:
            return Decimal(amt)


    def weekly_sales(self):
        #print(date.today())
        weekly_sales = []
        for i in range(7):
            dt = date.today() - timedelta(i)
            amt = Order.objects.filter(order_date__contains=dt).aggregate(Sum('amount')).get('amount__sum')

            if amt == None:
                amt = 0
            else:
                amt = int(amt)

            dt =dt.strftime("%d/%m/%Y")
            print(dt)
            weekly_sales.append([f"{dt}",amt])
        return weekly_sales

    def index(self,request):
        weekly_sales= self.weekly_sales()

        new_order_count = Delivery_Details.objects.filter(deliver_status='pen').count()
        in_process_order_count = Delivery_Details.objects.filter(deliver_status='proc').count()
        completed_order_count =Delivery_Details.objects.filter(deliver_status='comp').count()
        delivering_order_count = Delivery_Details.objects.filter(deliver_status='delv').count()
        today_sale =self.today_sale()
        context={'new_order_count':new_order_count,'in_process_order_count':in_process_order_count,'completed_order_count':completed_order_count,
                 'delivering_order_count':delivering_order_count, 'today_sale':today_sale, 'weekly_sales':weekly_sales}
        return render(request,'admin/index.html',context)

    # add prescription
    def order_details(self, request,order_id):
         order = Order.objects.get(id=order_id)
         order_items = OrderItems.objects.filter(order=order)
         
         delivery_details = Delivery_Details.objects.get(order=order)
         return render(request,'admin/order_items.html',{'order':order,'order_items':order_items,'delivery_details':delivery_details})

admin_site = MyAdminSite()



'''
----------------------
'''


# Admin panel header customizations
admin_site.site_header = "Medicom"

admin_site.site_title = "Medicom"
admin_site.index_title = "Welcome to Medicom Admin Panel"


#admin_site.unregister(User)
#admin_site.unregister(Group)


# class for overriding recent actions log in database

class dontLogRecentActions:
    def log_addition(self, *args):
        return

    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return


# Customizing models for admin panel
#           Products
class ProductsAdmin(dontLogRecentActions, admin.ModelAdmin):
    list_display = ("brand_name","generic_name","type","price")
    list_filter = ("type","price")
    search_fields = ("brand_name","generic_name")
    #fields = ("first_name", "last_name", "courses") #fields displayed on add and edit in same order as specified here


#       Stock
class StockAdmin(dontLogRecentActions,admin.ModelAdmin):
    list_display = ("id","products", "quantity")

    def products(self, obj):
        return Products.objects.order_by().values_list('brand_name', flat=True).distinct()




#       Orders
class OrderAdmin(dontLogRecentActions,admin.ModelAdmin):
    list_display =("id","order_date","delivery_date","Items_Details","status")
    search_fields = ('id',)


    def delivery_date(self,obj):
        return  Delivery_Details.objects.only('deliver_date').get(order=obj).deliver_date

    # show status column
    def status(self,obj):
        from django.utils.html import format_html
        DELIVER_STATUS = {'pen': 'Pending','proc': 'Processing','delv': 'Delivering','comp': 'Completed'}
        status = Delivery_Details.objects.only('deliver_status').get(order=obj).deliver_status
        str=''
        if status == 'pen':
            str="<b style='color: white; background-color: red;'>{}</b>"
        elif status == 'proc':
            str = "<b style='color: black; background-color: yellow;'>{}</b>"
        elif status == 'delv':
            str = "<b style='color: black; background-color: lightgreen;'>{}</b>"
        elif status == 'comp':
            str = "<b style='color: yellow; background-color: green;'>{}</b>"

        return format_html(str, DELIVER_STATUS [status])

    # items details column
    def Items_Details(self,obj):
        from django.utils.html import format_html
        str = "<a href='/admin/online_pharmacy/order_details/{}/'>View Details</a>" #/order_details/{}
        return format_html(str,obj.id)

    # permisions
    def has_add_permission(self,request):
        return False
    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    # actions drop down options
    def processing(modeladmin, request, queryset):
        for q in queryset:
            print(q)
            obj = Delivery_Details.objects.get(order=q)
            obj.deliver_status = 'proc'
            obj.deliver_date = None
            obj.save()

    def pending(modeladmin, request, queryset):
        for q in queryset:
            print(q)
            obj = Delivery_Details.objects.get(order=q)
            obj.deliver_status = 'pen'
            obj.deliver_date = None
            obj.save()


    def deliverying(modeladmin, request, queryset):
        for q in queryset:
            print(q)
            obj = Delivery_Details.objects.get(order=q)
            obj.deliver_status = 'delv'
            obj.deliver_date = None
            obj.save()


    def completed(modeladmin, request, queryset):
        for q in queryset:
            print(q)
            obj = Delivery_Details.objects.get(order=q)
            obj.deliver_status = 'comp'
            order = Order.objects.get(id=obj.order.id)
            order.complete=True
            order.save()
            obj.deliver_date = datetime.now()
            obj.save()

    # adding actions to drop down
    processing.short_description = "Status - Processing"
    pending.short_description = "Status - Pending "
    deliverying.short_description = "Status - Delivering "
    completed.short_description = "Status - Completed "
    actions = [pending, processing, deliverying, completed]



#       Delivery Details
class Delivery_DetailsAdmin(dontLogRecentActions,admin.ModelAdmin):
    list_display = ("order","customer", "deliver_addr", "deliver_phn", "deliver_name","deliver_status","deliver_date")

    def has_add_permission(self,request):
        return False

#       Customer
class CustomerAdmin(dontLogRecentActions, admin.ModelAdmin):

    list_display = ("name", "email", "phone_no", "address","password")


    def has_add_permission(self,request):
        return False


class Order_itemsAdmin(dontLogRecentActions,admin.ModelAdmin):
    list_display =("order","product","quantity")

    def has_add_permission(self,request):
        return False


class Requested_OrdersAdmin(dontLogRecentActions,admin.ModelAdmin):
    list_display = ("customer", "requested_medicine","date")

    def has_add_permission(self,request):
        return False
    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False


class NotificationsAdmin(dontLogRecentActions,admin.ModelAdmin):
    list_display = ("message",)

    def has_add_permission(self,request):
        return False
    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False


admin_site.register(Products,ProductsAdmin)
admin_site.register(Stock,StockAdmin)
admin_site.register(Customer,CustomerAdmin)
admin_site.register(Order,OrderAdmin)
#admin_site.register(Order)
#admin_site.register(Delivery_Details)

admin_site.register(requested_Order,Requested_OrdersAdmin)
#admin_site.register(Notifications,NotificationsAdmin)
#admin_site.register(OrderItems)

