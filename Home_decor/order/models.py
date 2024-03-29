from django.db import models
import datetime
from user_app.models import Account
from account.models import Address
from product_management.models import Product_Variant
from product_management.models import Coupon 

# Create your models here.
class ShippingAddress(models.Model):
    #The use of two addesses is necessary. Because if there is only one address and user changes anything then the
    # shipping address will be changed.   
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=50)
    town_city       = models.CharField(max_length=100)
    street_address  = models.CharField(max_length=255)
    state           = models.CharField(max_length=50)
    country_region  = models.CharField(max_length=50)
    zip_code        = models.CharField(max_length=20)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.street_address} "
    
class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.method_name




class Payment(models.Model):
    PAYMENT_STATUS_CHOICES =(
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
        ("REFUNDED", "Refunded"),
        ("CANCELLED", "Cancelled"),
        )
    payment_method      = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid             = models.BooleanField(default=False)
    payment_order_id    = models.CharField(max_length=100,null=True,blank=True)
    payment_id          = models.CharField(max_length=100,null=True,blank=True)
    payment_signature   = models.CharField(max_length=100, null=True, blank=True)
    amount_paid         = models.IntegerField(null=True, blank=True)
    payment_status      = models.CharField(choices = PAYMENT_STATUS_CHOICES,max_length=20)
    created_at          = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Check if payment status is 'SUCCESS'
        if self.payment_status == 'SUCCESS':
            # If yes, set is_paid to True
            self.is_paid = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_order_id
    



class Order(models.Model):
    ORDER_STATUS_CHOICES =(
        ("New", "New"),
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Shipped", "Shipped"),
        ("Cancelled", "Cancelled"),
        ("Returned", "Returned"),
        )
    user                = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment             = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True,blank=True,related_name='order')
    order_number        = models.CharField(max_length=100)
    shipping_address    = models.OneToOneField(ShippingAddress, on_delete=models.CASCADE,null=True)
    order_total         = models.DecimalField(max_digits=12, decimal_places=2)
    order_tax           = models.DecimalField(max_digits=12, decimal_places=2)
    additional_discount = models.IntegerField(default=0,null=True)
    shipping_charge     = models.IntegerField(default=0, null=True)
    offer               = models.IntegerField(default=0, null=True)
    order_status        = models.CharField(choices = ORDER_STATUS_CHOICES,max_length=20,default='New')
    is_ordered          = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    coupon_code         = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    wallet_discount     = models.IntegerField(default=0,null=True)
    
    # order_note = models.CharField(max_length=100,blank=True,null=True)
    # ip = models.CharField(max_length=50,blank=True)
    def generate_order_number(self):
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        print(current_date)
        last_order = Order.objects.filter(order_number__startswith=f'ORD{current_date}').last()
        print(last_order)
        if last_order :
            sequence_number = int(last_order.order_number[-6:]) + 1
            print(sequence_number)
            print('workiing')
        else:
            print('No work')
            sequence_number = 1

        return f"ORD{current_date}{sequence_number:06d}"

    def delete(self, *args, **kwargs):
        # Delete the related ShippingAddress instance if exists
        if self.shipping_address:
            self.shipping_address.delete()

        # Delete the related Payment instance if exists
        if self.payment:
            self.payment.delete()

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if self.pk:  # Check if the instance is already saved (updating)
            original_order = Order.objects.get(pk=self.pk)
            if self.order_status != original_order.order_status:
                # Update order status
                original_order_products = original_order.order_products.all()
                for order_product in original_order_products:
                    order_product.order_product_status = self.order_status
                    order_product.save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Order {self.order_number}'
        # return self.order_number


class OrderProduct(models.Model):
    ORDER_STATUS_CHOICES =(
        ("New", "New"),
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Shipped", "Shipped"),
        ("Cancelled", "Cancelled"),
        ("Returned", "Returned"),
        )
    order                       = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_products')
    user                        = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    product_variant             = models.CharField(max_length=255)
    quantity                    = models.IntegerField()
    product_price               = models.DecimalField(max_digits=12, decimal_places=2)
    images                      = models.ImageField(upload_to='media/order/images')
    ordered                     = models.BooleanField(default=False)
    order_product_status        = models.CharField(choices = ORDER_STATUS_CHOICES,max_length=20,default='New')
    created_at                  = models.DateTimeField(auto_now_add=True)
    updated_at                  = models.DateTimeField(auto_now=True)
   

    def total_price(self):
        return self.product_price * self.quantity
    
    def __str__(self):
        return self.order.order_number   
    