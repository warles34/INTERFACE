# Create your views here.
from django.shortcuts import render_to_response
#from django.shortcuts import render
from wiki_model.forms import QuestionForm
from main_system import mainUse
#from django import forms
#from django.http import HttpResponseRedirect
from django.template import RequestContext


def index(request):
    asked = False # Definir si se realizo la pregunta
    question = ""
    answer = ""
    if request.method =="POST":
        WhyForm = QuestionForm(request.POST)
        if WhyForm.is_valid():
            asked = True
            question = WhyForm.cleaned_data['Question']
            answer = mainUse.return100textDocs(question)
    else:
        
        WhyForm = QuestionForm()
    ctx = {'form':WhyForm,'question':question,'asked':asked, 'answer':answer}
    return render_to_response('index.html',ctx, context_instance=RequestContext(request))

