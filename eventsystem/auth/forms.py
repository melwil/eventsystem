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
            raise forms.ValidationError("Your account does not exist or the user/password combination is incorrect. Did you remember to register?")
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
    first_name = forms.CharField(label="first name", max_length=50)
    last_name = forms.CharField(label="last name", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="password", )
    v_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="repeat password")
    email = forms.EmailField(label="email", max_length=50)
    study = forms.ChoiceField(label="student union", choices=FIELD_OF_STUDY_CHOICES)
    year = forms.IntegerField(label="year")
    field_of_study = forms.CharField(label="field of study", max_length=50)

    def clean(self):
        super(RegisterForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data
           
            # Check passwords
            if cleaned_data['password'] != cleaned_data['v_password']:
                raise forms.ValidationError("Your password do not match")

            # Check email suffix and username
            username, email_suffix = cleaned_data['email'].split("@")
            if User.objects.filter(username=username).count() > 0:
                raise forms.ValidationError("There is already a user with that email")    
            if email_suffix != "stud.ntnu.no":
                raise forms.ValidationError("Your email needs to be @stud.ntnu.no")

            # Check year
            year = cleaned_data['year']
            if year < 1:
                raise forms.ValidationError("Year can't be less than 1")
            if year > 5:
                raise forms.ValidationError("Year can't be more than 5. If it still should be, contact an admin.")
            
            return cleaned_data
