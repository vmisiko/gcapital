import re
from django.db.models import signals
from django.dispatch import receiver
from .models import ShortCodeCallbacksUrl, GrantApplication
from Gcapital.mpesa.LipaNaMpesa import lipa_na_mpesa
from MpesaApp.models import LNMOnline, C2bTransaction
# import africastalking
import africastalking

# Initialize SDK
username = "sandbox"    # use 'sandbox' for development in the test environment
api_key = "023b2739b4c9e880b6d2f2dc0b6acc55e66415b82bc6fcb55c359873e1374606"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS



@receiver(signals.post_save, sender = ShortCodeCallbacksUrl)
def initiate_application(sender, instance, **kwargs):

    text = instance.Text
    phone = str(instance.From)
    phone_number = phone.split("+")[1]
    date = instance.date
    # print(phone_number, "without +")

    amount = "100"
    callbackurl = "https://de155fc3.ngrok.io/mobile/lnm/"
    applied, role = GrantApplication.objects.get_or_create( phone_number = phone)

    if text:
        keywordlist = text.split()
        keyword = keywordlist[0]
        text1= " ".join(keywordlist[1:])
        
        # print(keyword , "this is the keyword")

        if keyword == "GRANT":
            lipa_na_mpesa(phone_number = phone_number, amount = amount , callbackurl = callbackurl, AccountReference = phone_number )
            response = sms.send_premium( message ="Thank you for showing intrest to worKing with us.\n please deposit Ksh. 100 Assessment fee to Paybill Number : 254951, Account Name : Grant, to register on Africa Capital Grants portal ", 
                            short_code= "20635",
                            recipients= [phone,],
                            )
            # print(response)
            applied.save()

        if keyword == "NAME":
            response = sms.send( message ="starting with the word ID, please enter your ID Number, using the format below \n ID your_id_number i.e ( ID 33xxxxxx ) ", 
                            sender_id= "20635", 
                            enqueue = False,
                            recipients = [phone,],
                            )

            # print(response)
            applied.name = text1
            applied.date = date
            applied.save()
            

        elif keyword == "ID":
            response = sms.send( message ="starting with the word AMOUNT, please enter your amount applying for, using the format below \n AMOUNT amount_requesting i.e ( AMOUNT 400 ) ", 
                            sender_id= "20635",
                            enqueue = False,
                            recipients= [phone,],
                            )
            # print(response)
            applied.id_number = text1
            applied.date = date
            applied.save()

        elif keyword == "AMOUNT":
            response = sms.send( message ="Congradulations. Your assessment is complete. It takes 1,2 days to process your application and recieve your grant. If successful, you will be notified, through sms. ", 
                            sender_id= "20635",
                            enqueue = False,
                            recipients= [phone,],
                            )

            applied.amount_request = text1 
            applied.date = date
            applied.save() 
        else:
            response = sms.send( message ="You have not entered right format, please use the correct format as instructed. ", 
                            sender_id= "20635",
                            enqueue = False,
                            recipients= [phone,],
                            )



    else:
        # response = sms.send( message ="", 
        #                     recipients= ["+254721649416"],
        #                     sender_id= "20635",
        #                     enqueue = False,
        #                     )
        # print(response)
        pass

@receiver(signals.post_save, sender = LNMOnline)
def inititor(sender, instance, **kwargs):
    amount = instance.Amount
    phone_number = instance.PhoneNumber
    phone = f"+{phone_number}"
    print(phone, "this is fixed phone number")
    if amount ==1:
        response = sms.send( 
                            message ="Your Assesment fees has been recieved.Starting with the word NAME, please enter your full names, using the format below: \n NAME FIRSTNAME LASTNAME i.e ( NAME JOHN DOE) ", 
                            recipients= [phone,],
                            sender_id= "20635", 
                            enqueue = False,            
                            )
        # print(response)
    




        
        

    
    

