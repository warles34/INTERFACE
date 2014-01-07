'''
Created on Jan 3, 2013

@author: warles34
'''
from django import forms


class QuestionForm(forms.Form):
    ALGORITHMS = (
    	('eu', 'Euclidean'),
    	('fe', 'Fuzzy Euclidean'),
    	('co', 'Cosine'),
    	('ja', 'Jaccard')
    )
    Question = forms.CharField(widget=forms.TextInput(),required=False)
    Is_test = forms.BooleanField(required=False)
    training_algorithm = forms.ChoiceField(choices=ALGORITHMS)
