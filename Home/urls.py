
from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "Home"

urlpatterns = [
    path('', views.index.as_view(), name="home",),
    path('home/', views.index.as_view(), name="home",),
    path('about_us/', views.AboutUsView.as_view(), name="about_us",),
    path('contact_us/', views.ContactUsView.as_view(), name="contact_us",),
    path('ajax_contact/', views.contactview, name="ajax_contact",),
    path('sms_callbackurl/', views.smsPost, name="sms_post"),
    path('confirm_assessment/', views.confirm_assessment, name="confirm_assessment"),
    path('forms/', views.formVIew, name="forms"),
]



