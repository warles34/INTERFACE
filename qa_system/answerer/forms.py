'''
Created on Jan 3, 2013

@author: warles34
'''
from django import forms
from models import *


class QuestionForm(forms.Form):
    ALGORITHMS = (
    	('eu', 'Euclidean'),
    	('fe', 'Fuzzy Euclidean'),
    	('co', 'Cosine'),
    	('ja', 'Jaccard')
    )
    Question = forms.CharField(widget=forms.TextInput(),required=False)
    Is_test = forms.BooleanField(required=False)
    Expandir_vocabulario = forms.BooleanField(required=False)
    training_algorithm = forms.ChoiceField(choices=ALGORITHMS)

class ResultsForm(forms.Form):
    ALGORITHMS = (
        ('', 'Todos'),
        ('eu', 'Euclidean'),
        ('fe', 'Fuzzy Euclidean'),
        ('co', 'Cosine'),
        ('ja', 'Jaccard')
    )
    Q = [("","Todas")]
    print Q
    Q = [(r.question,r.question) for r in Results.objects.all()]
    print Q
    Q = list(set(Q))
    Q = [("","Todas")] + Q
    V = (("","Todas"),(0,"no"),(1,"si"))
    #print Q
    #Q = (("1","1"),("1","1"),("1","1"),("1","1"))
    Pregunta_realizada = forms.ChoiceField(choices=Q,required=False)
    Vocabulario_expandido = forms.ChoiceField(choices=V,required=False)
    Algoritmo_usado = forms.ChoiceField(choices=ALGORITHMS,required=False)

