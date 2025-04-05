from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from datetime import datetime
# Create your views here.
def home(request):
    return render(request, 'home/welcome_site.html', {'today': datetime.today()})
