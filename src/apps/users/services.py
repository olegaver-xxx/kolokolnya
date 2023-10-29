import jwt, base64
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .models import User, Profile


def register_user(email, password):
    # TODO
    print('CREATE USER', email, password)
    if not password or not email:
        return False
    return True


def send_activation_email(email, password):
    encoded_jwt = jwt.encode({"user_email": email, 'password': base64.encodebytes(password.encode()).decode()}, settings.SECRET_KEY, algorithm="HS256")
    activate_url = reverse('activate')
    url = f"{'https' if settings.SECURE_CONNECTION else 'http'}://{settings.DOMAIN_NAME}{activate_url}?token={encoded_jwt}"
    send_mail(
        "[SiteName] Activate account",
        f"<a href='{url}'>Click Here To Activate</a>",
        settings.EMAIL_FROM,
        [email],
        fail_silently=False,
    )


def activate_user(token):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    password = base64.decodebytes(data['password'].encode()).decode()
    register_user(data['user_email'], password)

