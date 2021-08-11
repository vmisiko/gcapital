from django import forms
from django.forms import ModelForm



class ContactForm(forms.Form):
    
    Name = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':" Enter your first name  "}))
    
    message = forms.CharField( widget = forms.Textarea(attrs = {
    'placeholder':" Your Message "}))
    
    email = forms.CharField(widget = forms.TextInput(attrs = {
        "placeholder": "your email"
    }))

class VerifyRegForm(forms.Form):
    
    Id_number = forms.IntegerField( widget = forms.NumberInput(attrs = {
    'placeholder':" Enter Id number "}))
    
    Phone_number = forms.IntegerField( widget = forms.NumberInput(attrs = {
    'placeholder':" Enter phone number "}))
    
    
