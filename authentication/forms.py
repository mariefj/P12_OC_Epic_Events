from django import forms
from django.contrib.auth import authenticate

# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(strip=False, widget=forms.PasswordInput)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user = None

#     def clean(self):
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         if email and password:
#             self.user = authenticate(email=email, password=password)
#             if self.user is None:
#                 raise forms.ValidationError("Invalid credentials")
#         return self.cleaned_data