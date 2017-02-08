'''
Created on Jan 3, 2013

@author: warles34
'''
from django import forms



class QuestionForm(forms.Form):
    Question = forms.CharField(widget=forms.TextInput())