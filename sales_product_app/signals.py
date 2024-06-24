from time import sleep
from django.db.models import F
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from djoser.signals import user_registered
from django.conf import settings
from .models import Contact, Order, CustomUser
from .tasks import send_email_status_new, send_registration_email_async, send_email_status_canceled


def get_supplier_email(user_id):
    supplier = Order.objects.filter(user_id=user_id). \
        select_related('product_info__product__category__shops__shop'). \
        values(email=F('product_info__product__category__shops__user__email')).distinct()
    return supplier


def get_order_number(user_id, status):
    order_number = Order.objects.filter(user_id=user_id, status=status). \
        annotate().values('order_number').distinct()
    return order_number


@receiver(user_registered)
def send_registration_email(sender, user, **kwargs):
    send_registration_email_async.delay(user.first_name, user.last_name, user.email)


@receiver(post_save, sender=Contact)
def order_status_new(sender, instance, created, **kwargs):
    order_number = get_order_number(instance.user.id, 'new')
    if created:
        send_email_status_new.delay(instance.user.first_name, instance.user.last_name,
                                    instance.user.email, order_number[0]['order_number'],
                                    [email['email'] for email in get_supplier_email(instance.user.id)])


@receiver(post_delete, sender=Contact)
def order_status_delete(sender, instance, **kwargs):
    order_number = get_order_number(instance.user.id, 'canceled')
    send_email_status_canceled.delay(instance.user.first_name, instance.user.last_name,
                                     instance.user.email, order_number[0]['order_number'],
                                     [email['email'] for email in get_supplier_email(instance.user.id)])