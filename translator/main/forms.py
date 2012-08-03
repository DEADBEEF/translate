from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    name = forms.CharField(label="Username",max_length=20, min_length=4)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password",widget=forms.PasswordInput())
    cpassword = forms.CharField(label="Confirm Password",widget=forms.PasswordInput())
    def clean(self):
        try:
            password1 = self.cleaned_data["password"]
            password2 = self.cleaned_data["cpassword"]
            username = self.cleaned_data["name"]
            email = self.cleaned_data["email"]
            print email
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            try:
                entry = User.objects.get(username=username)
                raise forms.ValidationError("Username already in use")
            except User.DoesNotExist:
                pass

        except KeyError:
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data
