from django.db import models

# Create your models here.

class Item(models.Model):
    
    pass

class ShortCodeCallbacksUrl(models.Model):    
    linkid = models.CharField(max_length=200, null=True , blank = True)
    Text = models.CharField(max_length=200, null=True , blank = True)
    to = models.IntegerField(default= 0)
    From = models.IntegerField(default= 0)
    message_id = models.CharField(max_length=200, null=True , blank = True)
    date = models.DateTimeField(blank = True,null = True)

    
class GrantApplication(models.Model):
    name = models.CharField(max_length= 50,blank = True, null = True)
    id_number = models.CharField(max_length=15,blank = True, null = True)
    phone_number = models.IntegerField(blank = True, null = True)
    amount_request = models.FloatField(default = 0.0)
    amount_dispensed = models.FloatField(default= 0.0)
    date = models.DateTimeField(blank = True,null = True)
    paid = models.BooleanField(default=False)
    
    

class Emails(models.Model):
    name = models.CharField(max_length= 30)
    message = models.TextField(max_length= 500)
    email_adress = models.EmailField(max_length=50)
    reply = models.TextField(max_length=500, blank= True, null = True)