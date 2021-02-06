from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse

from xhtml2pdf import pisa

from .models import Order

def render_to_pdf(template_src, context_dict=({})):
    """
    Parses the order to pdf for the customers
    Params:
    \n-template_src: [String] Destination path
    \n-context_dict: [Dictionary] Order's information
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()

    return None

@login_required
def admin_order_pdf(request, order_id):
    """Action for the superuser
    Params:
    \n   -order_id:[String] A unique id of the order
    Return:
    \n   -response: The generated PDF file about the order via request to the front-end
    """
    if request.user.is_superuser:
        order = get_object_or_404(Order, pk=order_id)
        pdf = render_to_pdf('order_pdf.html', {'order': order})

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            content = "attachment; filename=%s.pdf" % order_id
            response['Content-Disposition'] = content

            return response
    return HttpResponse("Not found")