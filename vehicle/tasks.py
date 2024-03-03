from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail

from vehicle.models import Car, Moto


@shared_task
def check_milage(pk, model):
    if model == 'Car':
        instance = Car.objects.filter(pk=pk).first()
    else:
        instance = Moto.objects.filter(pk=pk).first()

    if instance:
        prev_milage = -1
        for m in instance.milage.all():
            if prev_milage == -1:
                prev_milage = m.milage

            else:
                if prev_milage < m.milage:
                    print('Неверный пробег/пробег скручен')
                    break


def check_filter():
    filter_price = {'price__lte': 500}
    # now = datetime.datetime.now()    # настройка может понадобиться для работы с почтой
    if Car.objects.filter(**filter_price).exists():
        print('Отчет по фильтру. Чтобы отправлялось письмо, нужно убрать #')
        # send_mail(
        #     subject='Отчет по фильтру',
        #     message='У нас есть машины под ваш фильтр'
        #     from_email='admin@admin.com',
        #     recipient_list=[user.email]
        # )

