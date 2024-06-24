from time import sleep

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from rest_framework.response import Response

from .models import ProductInfo
from .serializers import CustomUserSerializer, ProductInfoSerializer


@shared_task
def send_registration_email_async(first_name, last_name, email):
    send_mail(
        'Добро пожаловать в сервис закупок розничной сети!',
        f'Спасибо за регистрацию {first_name} {last_name}!\nРады вас приветствовать на нашей платформе!',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )


@shared_task
def send_email_status_new(first_name, last_name, email, order_number, supplier):
    send_mail(
        f'Изменение статуса заказа #{order_number}',
        f'{first_name} {last_name}, cтатус вашего заказа #{order_number} изменен на "Новый".',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    ),
    send_mail(
        f'Получен новый заказ #{order_number}',
        f'С деталями заказа #{order_number} ознакомьтесь в разделе "Заказы".',
        settings.DEFAULT_FROM_EMAIL,
        supplier
    )


@shared_task
def send_email_status_canceled(first_name, last_name, email, order_number, supplier):
    send_mail(
        f'Изменение статуса заказа #{order_number}',
        f'{first_name} {last_name}, cтатус вашего заказа #{order_number} изменен на "Удален".',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    ),
    send_mail(
        f'Изменение статуса заказа #{order_number}',
        f'Cтатус заказа #{order_number} изменен на "Удален".',
        settings.DEFAULT_FROM_EMAIL,
        supplier
    )


@shared_task
def create_user_async(data):
    serializer = CustomUserSerializer(data=data[0])
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@shared_task
def upload_thumbnail_async(data, product_id):
    instance = ProductInfo.objects.get(product_id=product_id)
    serializer = ProductInfoSerializer(data=data[0], instance=instance)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)