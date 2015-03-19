from django import forms

__author__ = 'Piotr'

class ChatForm(forms.Form):
    name = forms.CharField(label=u'Your name', max_length=100)
    text = forms.CharField(label=u'Your message', widget=forms.widgets.Textarea())

class LoginForm(forms.Form):
    name = forms.CharField(label=u'Your name', max_length=100)