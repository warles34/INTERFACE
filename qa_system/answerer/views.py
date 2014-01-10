from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from answerer.forms import *
from inside.main_process import main
from django import forms
from django.http import HttpResponseRedirect
from django.template import RequestContext
from answerer.models import *


# Create your views here.
def index(request):
	#test_set = ['Why is the sky blue','Why do japanese kill whales','Why is Andrew Johnson important']
	test_set = ['Why is the sky blue','Why do japanese kill whales','Why is Andrew Johnson important','Why did Abigail drink blood','Why are proteins important to sports people','Why would you get sick from running','Why do seatbelts save lives','Why was king Christian X so influential','Why are your aubergines wilting','Why do earphones break so quickly','Why is tendonitis painful and potentially dangerous']
	asked = False # Definir si se realizo la pregunta
	quest = ""
	results = []
	questions_id = []
	results_table = []
	request.session['update_ids'] = []
	request.session['update_values'] = []
	algorithms = dict([('eu', 'Euclidean'),('fe', 'Fuzzy Euclidean'),('co', 'Cosine'),('ja', 'Jaccard')])
	if request.method =="POST": 
		WhyForm = QuestionForm(request.POST)
		if WhyForm.is_valid():
			print WhyForm.cleaned_data
			asked = True
			all_results = Results.objects.all()
			quest = WhyForm.cleaned_data['Question']
			quest = quest.lower()
			is_test = WhyForm.cleaned_data['Is_test']
			train_algo = WhyForm.cleaned_data['training_algorithm']
			v_expand = WhyForm.cleaned_data['Expandir_vocabulario']
			if not(is_test):
				test_set = [quest]
			for quest in test_set:
				try:
					print quest
					print v_expand
					print train_algo
					r = Results.objects.get(question=quest,expanded_vocabulary=v_expand,training_algorithm=train_algo)
					questions_id.append(r.id)
				except Exception, e:
					#for elem in all_results:
					#	if elem.question == quest:
					#		same_question_results = Results.objects.filter(question=elem.question)
					#		for r in same_question_results:
					#			if r.training_algorithm == train_algo:
					#				questions_id.append(r.id)
					#				break
					#		if r.training_algorithm == train_algo:
					#			break
					#else:			
					results = main(quest,train_algo,False,v_expand)
					for w_matrix in results:
						r = Results(question=quest,training_algorithm=train_algo,retrieval_time=w_matrix.retrieve_time, preprocessing_time=w_matrix.preprocessing_time, training_time=w_matrix.training_time, recall_time=w_matrix.recall_time,supervised_answer=0,expanded_vocabulary=v_expand,iterations=w_matrix.iterations)
						r.save()
						for x in range(0,3):
							try:
								d = Document(content_txt=w_matrix.documents_content[w_matrix.most_similar_document_indexes[x][0]],link=w_matrix.document_links[w_matrix.most_similar_document_indexes[x][0]],to_result=r,automatic_ranking=x,supervised_ranking=0)
								d.save()
							except Exception, e:
								print e
								break
						
					questions_id.append(r.id)
			
	else:
		WhyForm = QuestionForm()
	for id_ in questions_id:
		res = Results.objects.get(id=id_)
		ans = Document.objects.filter(to_result=res.id)
		print ans
		results_table.append([res,ans])
	ctx = {'form':WhyForm, 'asked':asked, 'results':results_table, 'algorithms':algorithms}
	asked = False
	return render_to_response('index.html',ctx, context_instance=RequestContext(request))


def update(request):
	searched = False
	question = ""
	answers = []
	if request.method == "POST":
		if request.POST['test'] == "BUSCAR":
			searched = True
			try:
				print request.POST['question']
				print request.POST['algorithm']
				res = Results.objects.get(question=request.POST['question'],training_algorithm=request.POST['algorithm'])

				question = res.question
				ans = Document.objects.filter(to_result=res.id)
				for x in range(len(ans)):
					answers.append(ans[x])
			except Exception, e:
				request.method = ""
				searched = False
		elif request.POST['test'] == "MODIFICAR":
			print request.POST['succesful_answer']
			if int(request.POST['succesful_answer']):
				best = Document.objects.get(pk=int(request.POST['succesful_answer']))
				print best.content_txt
				best.supervised_ranking=1
				best.save()
				res = Results.objects.get(pk=best.to_result)
				answs = Document.objects.filter(to_result=res.id)
				for x in range(len(answs)):
					if answs[x]:
						res.supervised_answer = x
						res.to_success_answer = answs[x].id
						res.save()
						break

			request.method = ""

		#res.retrieval_time = 0
		#res.save()

	#for r in Results.objects.all():
	#	print r.question
	all_ = Results.objects.all()
	ctx = {'results':all_, 'answers':answers, 'question':question, 'searched':searched}
	return render_to_response('update.html',ctx, context_instance=RequestContext(request))


def show(request):
	pass
	searched = False
	question = ""
	answers = []
	r_q = []
	r_v = []
	r_a = []
	results = []
	if request.method == "POST":
		if request.POST['test'] == "LISTAR":
			ShowForm = ResultsForm(request.POST)
			if ShowForm.is_valid():
				searched = True
				print ShowForm.cleaned_data['Pregunta_realizada']
				print ShowForm.cleaned_data['Vocabulario_expandido']
				print ShowForm.cleaned_data['Algoritmo_usado']

				if ShowForm.cleaned_data['Pregunta_realizada']:
					try:
						r_q = Results.objects.filter(question=ShowForm.cleaned_data['Pregunta_realizada'])
					except:
						pass
				else:
						r_q = Results.objects.all()
				if ShowForm.cleaned_data['Vocabulario_expandido'] != "":
					try:
						r_v = Results.objects.filter(expanded_vocabulary=ShowForm.cleaned_data['Vocabulario_expandido'])
					except:
						pass
				else:
						r_v = Results.objects.all()
				if ShowForm.cleaned_data['Algoritmo_usado']:
					try:
						r_a = Results.objects.filter(training_algorithm=ShowForm.cleaned_data['Algoritmo_usado'])
					except:
						pass
				else:
						r_a = Results.objects.all()

				r = list(set(r_q).intersection(set(r_a)).intersection(set(r_v)))
				print r
				for elem in r:
					res = Results.objects.get(id=elem.id)
					ans = Document.objects.filter(to_result=res.id)
					results.append([res,ans])
				request.method = ""
	ShowForm = ResultsForm()
	ctx = {'results':results, 'searched':searched,'show':ShowForm}
	return render_to_response('show.html',ctx, context_instance=RequestContext(request))

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