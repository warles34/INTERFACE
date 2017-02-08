import sys
import optparse
import re
import os
import experiments
from python_google import *
from wikipedia_url_tagCleaner import transform_from_url, return_paragraph
from lemmatizadorWordnet import lemmatizar_varios_documentos
from utility import extract_paragraph_from_snipp
from matrix_builder import WeightedMatrix
from sompy import SOM
from time import time
from datetime import datetime
from question_processing import question_preprocessing
from collections import Counter
#test_set = ['Why is the sky blue','Why do japanese kill whales','Why is Andrew Johnson important','Why did Abigail drink blood']
test_set = ['Why is the sky blue','Why do japanese kill whales','Why is Andrew Johnson important','Why did Abigail drink blood','Why are proteins important to sports people','Why would you get sick from running','Why do seatbelts save lives','Why was king Christian X so influential','Why are your aubergines wilting','Why do earphones break so quickly','Why is tendonitis painful and potentially dangerous']

q_line_random = [18635, 39876, 41977, 52101, 53187, 53196, 57840, 86647, 88168, 97917]

WIKIPEDIA_WEBPAGE = 'http://en.wikipedia.org'
file_name_form = re.compile(r'http://en.wikipedia.org/wiki/(.+)',re.DOTALL)

def main(question,training_algorithm,is_test,v_expand,page_number=10,window=100,clusters_x=10,clusters_y=10,iterations=15,directory='Resultados',term_frequency=0,offline_dir=0):
	results = []
	if is_test:
		for question in test_set:
			results.append(qa_system(question,training_algorithm,v_expand,page_number,window,clusters_x,clusters_y,iterations,directory,term_frequency,offline_dir))
	else:
		results.append(qa_system(question,training_algorithm,v_expand,page_number,window,clusters_x,clusters_y,iterations,directory,term_frequency,offline_dir))
	return results



def qa_system(question,training_algorithm,v_expand,page_number,window,clusters_x,clusters_y,iterations,directory,term_frequency,offline_dir):
	t_ = time()
	day_date = str(datetime.now())
 	FOLDER_CONTAINER = directory + "/" + day_date
	FOLDER_XML = FOLDER_CONTAINER + "/XML/"
	FOLDER_TXT = FOLDER_CONTAINER +"/TXT/"
	FOLDER_LEMMA = FOLDER_CONTAINER +"/LEMMA/"
	FOLDER_MATRIX = FOLDER_CONTAINER +"/MATRIX/"
	FOLDER_RESULTS = FOLDER_CONTAINER +"/RESULTS/"
	FOLDER_QUESTION = FOLDER_CONTAINER + "/QUESTION/"
	print "CREACION DE DIRECTORIOS"

	try:
		os.mkdir(directory)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_CONTAINER)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_XML)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_LEMMA)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_TXT)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_MATRIX)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_RESULTS)
	except Exception, e:
		print e
	try:
		os.mkdir(FOLDER_QUESTION)
	except Exception, e:
		print e
	identi = 1000
	google_url_list = get_google_url(question,1000,WIKIPEDIA_WEBPAGE)
	i_list = []
	o_list = []
	n = 0
	i = 0
	#print google_url_list
	used_links = []
	print "Buscando documentos de wikipedia"
	while n < int(page_number):
		#print n
		wiki_list = get_google_from_one_link(google_url_list[i])
		for l in range(len(wiki_list)):
			if n >= int(page_number):
				#print "se salio?"
				break
			#print l
			x =  wiki_list[l]
			new_archive_txt = FOLDER_TXT + str(identi) + ".txt"
			new_destiny = FOLDER_LEMMA + str(identi) + ".txt"
			identi+=1
			transform_from_url(x[0],new_archive_txt)
			new_d = extract_paragraph_from_snipp(new_archive_txt,x[1])
			i_list.extend(new_d)
			used_links.extend([x[0]]*len(new_d))
			os.remove(new_archive_txt)
			n+=1
			#print n
		i+=1

	onlinetime = time()-t_
	print i_list
	
	for l in i_list:
		o_list.append(FOLDER_LEMMA + l[len(FOLDER_TXT):])
	print "Lemmatizando"
	lemmatizar_varios_documentos(i_list,o_list,v_expand)
	lemmatizetime = time() - t_ - onlinetime
	question_lemma_document = question_preprocessing(question,FOLDER_QUESTION,v_expand)


	
	print "Creando matriz de pesos"
	w_matrix = WeightedMatrix()
	w_matrix.training_algorithm = training_algorithm
	w_matrix.retrieve_time = onlinetime
	w_matrix.insert_values(question_lemma_document,FOLDER_LEMMA,FOLDER_TXT)
	w_matrix.document_links = used_links
	w_matrix.question = question
	#w_matrix.normalize_TF_IDF()
	
	if term_frequency > 0:
		for x in range(term_frequency+1):
			w_matrix.remove_words_with_frequency(x)
	print w_matrix.TF_IDF_matrix
	w_matrix.preprocessing_time = time() - t_ - w_matrix.retrieve_time
	#for row in w_matrix.TF_IDF_matrix:
	#	print row
	#print
	#print
	#print
	#exit(-1)
	print "Entrenando la red neuronal"
	t0 = time()
	w_matrix.create_SOM(int(clusters_x),int(clusters_y),iterations)
	w_matrix.training_time = time() - t0
	t0 = time()
	print "Tiempo de prueba: " + str(time()-t_) + " segundos"

	lemma_question_doc = open(question_lemma_document)
	w_matrix.insert_question_vector(question_lemma_document)
	w_matrix.test()
	w_matrix.similarity_measure_jacard()
	w_matrix.recall_time = time() - t0
	w_matrix.total_time = time()-t_
	return w_matrix
	#experiments.documents_location_in_Map(w_matrix.SOM_cluster,w_matrix.TF_IDF_matrix,FOLDER_RESULTS)
	#experiments.percentage_documents_in_cluster(w_matrix.SOM_cluster,w_matrix.TF_IDF_matrix)
	#experiments.plot_words_distribution(w_matrix,FOLDER_RESULTS)
	#experiments.plot_weight_distribution(w_matrix.TF_IDF_matrix,FOLDER_RESULTS)














