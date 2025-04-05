from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = 'home/welcome_site.html'

class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized_users.html'
    login_url = '/admin'
