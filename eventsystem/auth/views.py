# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context import RequestContext

from eventsystem.auth.forms import LoginForm, RegisterForm

def login(request):
    redirect_url = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    response_dict = { 'form' : form, 'next' : redirect_url}
    return render(request, 'auth/login.html', response_dict)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data
                
                username = cleaned['email'].split("@")[0]

                user = User(username=username, email=cleaned['email'], first_name=cleaned['first_name'], last_name=cleaned['last_name'])
                user.save()
                #user = User(username=guest.email, email=guest.email, first_name=guest.first_name, last_name=guest.last_name)
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', { 'form': form, })
     
