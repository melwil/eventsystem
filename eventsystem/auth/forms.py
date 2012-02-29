from django import forms

from django.contrib import auth
from django.contrib.auth.models import User

from eventsystem.userprofile.models import FIELD_OF_STUDY_CHOICES 

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Password")
    remember = forms.BooleanField(label="Remember me", required=False)
    user = None

    def clean(self):
        if self._errors:
            return
    
        user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError("Your account is inactive, contact xxx@xxx.xxx")
        else:
            raise forms.ValidationError("Your account does not exist or the user/password combination is incorrect.")
        return self.cleaned_data

    def login(self, request):
        try:
            User.objects.get(username=request.POST['username'])
        except:
            return False
        if self.is_valid():
            auth.login(request, self.user)
            if self.cleaned_data['remember']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="fornavn", max_length=50)
    last_name = forms.CharField(label="etternavn", max_length=50)
    email = forms.EmailField(label="epost", max_length=50)
    study = forms.ChoiceField(label="studie", choices=FIELD_OF_STUDY_CHOICES)

    def clean(self):
        super(RegisterForm, self).clean()

        cleaned_data = self.cleaned_data

        email_suffix = cleaned_data['email'].split("@")[1]

        if email_suffix != "stud.ntnu.no":
            raise forms.ValidationError("Your email needs to be @stud.ntnu.no")
        return cleaned_data

