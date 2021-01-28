from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from apps.order.views import render_to_pdf
from django.contrib.auth.models import User
from apps.store.models import StoreAdmin


def decrement_product_quantity(order):
    for item in order.items.all():
        product = item.product
        product.num_available -= item.quantity
        product.save()

def send_order_confirmation(order):
    subject = 'Order confirmation'
    from_email = 'noreply@ecom.com'
    to = ['mail@ecom.com', order.email]
    text_content = 'Your order is successful!'
    html_content = render_to_string('order_confirmation.html', {'order': order})

    pdf = render_to_pdf('order_pdf.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    if pdf:
        name = 'order_%s.pdf' % order.id
        msg.attach(name, pdf, 'application/pdf')

    msg.send()

def get_owned_stores(request):
    owned_stores = []
    if not request.user.is_anonymous:
        user = User.objects.get(id=request.user.id)
        store_admins = StoreAdmin.objects.filter(user=user)
        
        for admin in store_admins:
            owned_stores.append(admin.store)
    return owned_stores