from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from answerer.forms import QuestionForm
from inside.main_process import main
from django import forms
from django.http import HttpResponseRedirect
from django.template import RequestContext
from answerer.models import *


# Create your views here.
def index(request):
	test_set = ['Why is the sky blue','Why do japanese kill whales','Why is Andrew Johnson important','Why did Abigail drink blood','Why are proteins important to sports people','Why would you get sick from running','Why do seatbelts save lives','Why was king Christian X so influential','Why are your aubergines wilting','Why do earphones break so quickly','Why is tendonitis painful and potentially dangerous']
	asked = False # Definir si se realizo la pregunta
	quest = ""
	results = []
	questions = []
	results_table = []
	if request.method =="POST": 
		WhyForm = QuestionForm(request.POST)
		if WhyForm.is_valid():
			print WhyForm.cleaned_data
			asked = True
			all_results = Results.objects.all()
			quest = WhyForm.cleaned_data['Question']
			quest = quest.lower()
			is_test = WhyForm.cleaned_data['Is_test']
			if not(is_test):
				test_set = [quest]
			for quest in test_set:
				for elem in all_results:
					if elem.question == quest:
						questions.append(quest)
						break
					
				else:			
					results = main(quest,False)
					for w_matrix in results:
						r = Results(question=quest,retrieval_time=w_matrix.retrieve_time, preprocessing_time=w_matrix.preprocessing_time, training_time=w_matrix.training_time, recall_time=w_matrix.recall_time)
						r.save()
						for x in range(0,3):
							try:
								d = Document(content_txt=w_matrix.documents_content[w_matrix.most_similar_document_indexes[x][0]],link=w_matrix.document_links[w_matrix.most_similar_document_indexes[x][0]],to_result=r)
								d.save()
							except Exception, e:
								break
						
					questions.append(quest)
			
	else:
		WhyForm = QuestionForm()
	for q in questions:
		res = Results.objects.get(question=q)
		ans = Document.objects.filter(to_result=res.id)
		print ans
		results_table.append([res,ans])
	ctx = {'form':WhyForm, 'asked':asked, 'results':results_table}
	return render_to_response('index.html',ctx, context_instance=RequestContext(request))

'''
class Document(models.Model):
	content_txt = models.TextField()
	link = models.CharField(max_length=512)
	to_result = models.ForeignKey('Results')


	

class Results(models.Model):
	question = models.TextField()
	retrieval_time = models.IntegerField(default=0)
	training_time = models.IntegerField(default=0)
	recall_time = models.IntegerField(default=0)'''