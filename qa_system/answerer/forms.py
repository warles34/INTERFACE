'''
Created on Jan 3, 2013

@author: warles34
'''
from django import forms


class QuestionForm(forms.Form):
    
    Question = forms.CharField(widget=forms.TextInput(),required=False)
    Is_test = forms.BooleanField(required=False)

class UpdateForm(forms.Form):
	CORRECT = (
		1,2,3,-1)
	rank = forms.ChoiceField(choices=CORRECT)
	
