import re as re
import mysqlQueries as MsqlQ
from sets import Set
from itertools import groupby

#listWords(question): Extrae las palabras contenidas en la pregunta, excluyendo las primeras dos palabras que son "Why" + un verbo auxiliar.
def listWords(question):
	wordform = re.compile("\w\w+")
	words = wordform.findall(question)
	return [word.lower() for word in words[2:]]




#DocUnion(docList1, docList2): devuelve un conjunto union de los conjuntos formados por las listas de documentos docList1 y docList2.
def DocUnion(docList1, docList2):
	docList1.extend(docList2)
	return list(Set(docList1))



#organizeWordDocs(wordDocs): esta funcion genera una lista de listas de palabras, agrupadas por el documento donde fueron encontradas.
def organizeWordDocs(wordDocs):
	return [(key, list(group)) for key, group in groupby(wordDocs, lambda x: x[1])]
		




#cleanMinimun(docList, minSize=30): elimina de la lista de documentos doclist los documentos que contengan menos del numero de minSize palabras.
def cleanMinimun(docList, minSize=30):
	c = 0
	eliminated = 0
	siz = range(len(docList))
	for x in siz:
		if MsqlQ.documentSize(docList[c]) < minSize:
			docList.pop(c)
		else:
			c+=1
	return docList


#clean_nonExist(words, stopValue=10000): esta funcion elimina de la lista de palabras words que no aparecen en el corpus de Wikipedia 2006 o que aparecen en una cantidad de documentos superior a stopValue
def clean_nonExist(words, stopValue=10000):
	r = range(len(words))
	c = 0
	for x in r:
		numb = MsqlQ.appearHowManyDoc(words[c]) 
		if numb > 0 and numb < stopValue:
			c+=1
		else:
			words.pop(c)
	return words
