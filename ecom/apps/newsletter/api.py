import json

from django.forms import ValidationError
from django.http import JsonResponse
from django.core.validators import validate_email

from .models import Subscriber


def api_add_subscriber(request):
    data = json.loads(request.body)
    email = data['email']

    try:
        validate_email(email)
        subscriber = Subscriber.objects.get_or_create(email=email)
    except ValidationError:
        raise ValidationError('Email format is incorrect')

    return JsonResponse({'success': True})