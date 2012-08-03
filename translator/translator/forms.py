from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(label="Username:",max_length=20)
    
