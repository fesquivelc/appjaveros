__author__ = 'fesquivelc'
from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'fesquivelc'}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'*******'},render_value=False),required=True)