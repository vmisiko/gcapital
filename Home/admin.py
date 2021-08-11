
from django.contrib import admin
from .models import ShortCodeCallbacksUrl, GrantApplication, Emails
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from Gcapital.mpesa.b2c import b2c_payments
from .tasks  import mpesa_payout_task
# Register your models here.

class CallbacksUrlAdmin(admin.ModelAdmin):
    list_display = ["linkid",
                    "Text",
                    "to",
                    "From",
                    "message_id",
                    "date"
                 ]

admin.site.register(ShortCodeCallbacksUrl,CallbacksUrlAdmin)

class GrantApplicationAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "phone_number",
                    "amount_request",
                    "amount_dispensed",
                    "date",
                    "paid"
                 ]
    actions = ["apply_deductions","mpesa_payout"]


    def apply_deductions(self, request, queryset):
        qs = queryset.filter(paid=False)
        print("executing 3.5 percent")
        for i,q in enumerate(qs):
            if i != len(qs)-1:
                amount = q.amount_request
                
                deducted = 0.965*float(amount)
                q.amount_dispensed = deducted
                q.save()
            else:
                amount = q.amount_request
                
                deducted = 0.965*float(amount)
                q.amount_dispensed = deducted
                q.save()
                self.message_user(request, "Application of 3.5 percent has completed successfully")

    apply_deductions.short_description = "Apply 3.5 percent deductions to Amount requested"

    def mpesa_payout(self, request, queryset):
        
        pk_model = []
        for q in queryset:
            pk_model.append(q.pk)
        print(pk_model)
        # mpesa_payout_task.delay(pk_model)
        try:  
            mpesa_payout_task.delay(pk_model)
            self.message_user(request, "Please wait this may take a while. Refresh after some few minutes")
        except:
            self.message_user(request, "Failed! Retry again")

    mpesa_payout.short_description = "Apply Mpesa Payout"

        # qs = queryset.filter(paid=False)
        # for i,q in enumerate(qs):
        #     if i != len(qs)-1:
        #         amount = q.amount_dispensed
        #         phone = q.phone_number
        #         try:
        #             b2c_payments(amount,phone)
        #             q.paid= True
        #             q.save()
        #         except:
        #             self.message_user(request, "payout failed")
        #     else:
        #         amount = q.amount_dispensed
        #         phone = q.phone_number
        #         try:
        #             b2c_payments(amount,phone)
        #             q.paid= True
        #             q.save()
        #             self.message_user(request, "payout was successful")
        #         except:
        #             self.message_user(request, "payout failed")

    
    mpesa_payout.short_description = "Pay using Mpesa" 

admin.site.register(GrantApplication,GrantApplicationAdmin)

class EmailsAdmin(admin.ModelAdmin):

    list_display = [ 
                    "name",
                    "message",
                 ]


    change_form_template = "change_form.html"


    def response_change(self, request, obj):

        if "Reply email" in request.POST:
            
            try:
                print(obj.reply, "this is the reply")
                send_mail(f"Re: Enquiry for {obj.message}", obj.reply, "victormisiko.vm@gmail.com" ,[obj.email_adress,] )

                obj.save()
                self.message_user(request, "email reply was successful")
            except BadHeaderError:

                self.message_user(request, "email reply not sent try again.")

            # return HttpResponseRedirect(".")

        return super().response_change(request, obj)

admin.site.register(Emails,EmailsAdmin)

