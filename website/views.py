from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html" 

class ContactView(TemplateView):
    template_name = "website/contact.html" 
    
class AboutView(TemplateView):
    template_name = "website/about.html" 
    