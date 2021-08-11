from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from . models import  GrantApplication,Item,
from django.views import generic
from .forms import ContactForm, VerifyRegForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ShortCodeCallbacksUrl, GrantApplication,Item,Emails
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
class index(generic.ListView):
    model = Item
    template_name = "home-page.html"

    def get_context_data(self, **kwargs):
        centext = super(index, self).get_context_data(**kwargs)
        form = VerifyRegForm()

        context = {
            "form" : form
        }

        return context

class AboutUsView(generic.ListView):
    model = Item
    template_name = "about_us.html"

class ContactUsView(generic.ListView):
    model = Item
    template_name = "contact_us.html"

    def get_context_data(self, **kwargs):
        centext = super(ContactUsView, self).get_context_data(**kwargs)
        form = ContactForm()

        context = {
            "form" : form
        }

        return context

@csrf_exempt
def smsPost(request):


    
    result = request.POST
    linkid = request.POST.get('linkId')
    Text = request.POST.get('text')
    to = request.POST.get('to')
    From = request.POST.get('from')
    Id = request.POST.get('id')
    date = request.POST.get('date')

    model, code = ShortCodeCallbacksUrl.objects.get_or_create( 
        linkid = linkid,
        Text = Text,
        to = to,
        From = From,
        message_id = Id,
        date = date,   
    )

    model.save()
    
    return JsonResponse({"hey":"it worked"})  

@csrf_exempt
def confirm_assessment(request):


    # form = VerifyRegForm(request.POST or None)
    id_number = request.GET.get("Id_number")
    phone_number = request.GET.get("Phone_number")
    data = {}
    print(id_number, phone_number)
    if phone_number:

        obj = GrantApplication.objects.filter(id_number = id_number, phone_number = phone_number).exists()
         
        data["obj"] = obj

    
    return JsonResponse( data)

def formVIew(request):

    form = VerifyRegForm()

    data = {}

    data["form"] = form

    if request.method == "POST":
        form1 = VerifyRegForm(request.POST or None)
        print(request.POST)
        if form1.is_valid():
            Id_number = request.POST.get('Id_number')
            Phone_number = request.POST.get('Phone_number')

            print(Id_number)
            obj = GrantApplication.objects.filter(id_number = Id_number, phone_number =Phone_number).exists()

            context = {
                "form": form
            }
            if obj:
                print("exists")
                return render(request, "home-page.html", context)
                messages.info(request, " Exists")

            else:
                
                
                print("not exists")
                messages.info(request, "not exists")
                return render(request, "forms.html" , data)
        


    return render(request, "forms.html" , data)

def contactview(request):
    name = request.GET.get("Name")
    email_adress = request.GET.get("email")
    message = request.GET.get("message")

    print(name, email_adress, message, "this are the printed")
    data = {}
    if message:
        mails = Emails.objects.create(
            name = name,
            message = message,
            email_adress = email_adress,
        )
        mails.save()

        send_mail(  f"New enquiry from {name} ", message, email_adress, ["victormisiko.vm@gmail.com",])
        data["message"] = "Email sent successfully"


    return JsonResponse(data)

