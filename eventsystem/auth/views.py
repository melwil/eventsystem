# -*- coding: utf-8 -*-

import uuid

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext

from eventsystem.auth.forms import LoginForm, RegisterForm
from eventsystem.auth.models import RegisterToken
from eventsystem.userprofile.models import UserProfile

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

                # Create the user
                user = User(username=username, email=cleaned['email'], first_name=cleaned['first_name'], last_name=cleaned['last_name'])
                user.set_password(cleaned['password'])
                user.is_active = False
                user.save()

                # Create the userprofile
                up = UserProfile(user=user, year=cleaned['year'], field_of_study=cleaned['study'], study_program=cleaned['field_of_study'])
                up.save()

                # Create the registration token
                token = uuid.uuid4().hex
                rt = RegisterToken(user=user, token=token)
                rt.save()
                
                email_message = u"""
                    You have registered an account in the event system at realfagdagen.no.

                    To use your account, you need to verify it. You can do that by visiting the link below.
                    The link is to a different site, which is the actual host for the eventsystem.

                    http://absint.online.ntnu.no:6554/auth/verify/%s/

                    Feel free to contact staff from realfagdagen if you do not wish to use this link to verify your account.
                """ % (token)
                
                # Send varification mail
                send_mail('Verify your account', email_message, 'event@realfagdagen.no', [user.email,])

                messages.success(request, "Your account has been created. Check you email for a link to verify your account. The link will be to absint.online.ntnu.no, but it is safe.")

                return HttpResponseRedirect('/')
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', { 'form': form, })
    
def verify(request, token):
    rt = get_object_or_404(RegisterToken, token=token)

    user = getattr(rt, 'user')

    user.is_active = True
    user.save()

    messages.success(request, "User '"+user.username+"' successfully activated. You can now log in.")

    return HttpResponseRedirect('http://org.ntnu.no/realfagdagen/?page_id=319')

