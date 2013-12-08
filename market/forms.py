__author__ = 'fesquivelc'
from django import forms

class ContactoForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'tu@email.com'}),required=True)
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo del mensaje'}),required=True)
    contenido = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido del mensaje'}),required=True)

class BusquedaProductoForm(forms.Form):
    nombreProducto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del producto'}))

class LoginForm(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'fesquivelc'}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'*******'},render_value=False),required=True)

