from django.forms import ModelForm
from django import forms

class checkoutForm(forms.Form):
	buy = forms.CharField(label='buy', max_length=100)