from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"form_full_name",
                        "placeholder":"your full name .."
                        }
                        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class":"form-control",
                "placeholder":"your email address"
                }
                ))
    content = forms.CharField(widget=
            forms.Textarea(attrs={
                "class":"form-control",
                "placeholder":"your message"}
                ))

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email

    # def clean_content(self):
    #     raise forms.ValidationError("Content is wrong")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    email= forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput , label="confirm password")

    def clean_username(self):
        user_name = self.cleaned_data.get('username')
        qs = User.objects.filter(username=user_name)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return user_name
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("passwords must match")
        return data
