from celery import shared_task

from celery import shared_task
from .models import GrantApplication
from Gcapital.mpesa.b2c import b2c_payments

@shared_task
def mpesa_payout_task(pk_model):

    queryset = GrantApplication.objects.filter(pk__in = pk_model)
    print("Celery worker now working")

    qs = queryset.filter(paid=False)
    for q in qs:
        
        amount = q.amount_dispensed
        phone = q.phone_number

        try:
            b2c_payments(amount,phone)
            q.paid= True
            q.save()
        except:
            pass
           