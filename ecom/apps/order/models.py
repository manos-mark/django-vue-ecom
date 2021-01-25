from apps.store.models import Product

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'
    ARRIVED = 'arrived'

    STATUSES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (ARRIVED, 'Arrived')
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    payment_intent = models.CharField(max_length=255)

    used_coupon = models.CharField(max_length=50, blank=True, null=True)

    shipped_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=ORDERED)

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.created_at)

    def get_total_quantity(self):
        return sum(int(item.quantity) for item in self.items.all())

    # TODO: Fix this to sent emails when the status has been changed from the admin panel setter.
    #       The problem is that it is sending emails every time the object is created 
    # def __setattr__(self, attrname, val):
    #     super(Order, self).__setattr__(attrname, val)
    #     if (attrname == 'status'):
    #         print(self.status)
    #         print(val.__str__())

    #         if (self.status.__str__() != val.__str__()):
    #             if (val == self.ORDERED):
    #                 html = render_to_string('order_confirmation.html', {'order': self})
    #                 send_mail('Order confirmation', 'Your order is successful!', 'noreply@ecom.com', \
    #                     ['manos.mark@gmail.com', self.email], fail_silently=False, html_message=html)
    #             elif (val == self.SHIPPED):
    #                 html = render_to_string('order_sent.html', {'order': self})
    #                 send_mail('Order in proccess', 'Your order has been sent!', 'noreply@ecom.com', \
    #                     ['manos.mark@gmail.com', self.email], fail_silently=False, html_message=html)
    #             elif (val == self.ARRIVED):
    #                 html = render_to_string('order_arrived.html', {'order': self})
    #                 send_mail('Order arrived', 'Your order has been arrived!', 'noreply@ecom.com', \
    #                     ['manos.mark@gmail.com', self.email], fail_silently=False, html_message=html)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id