# Este es el documento que realiza el trabajo de la expansion de vocabulario y la organizacion en orden  
# de relevancia dada por frecuencias de palabras. Realiza este trabajo completo en alto nivel, apoyandose de
# los otros documentos contenidas en la misma carpeta. 
import vocabularyExpansion as VE
import sys
import mysqlQueries as MsqlQ
import rankScores as RS
import overListFunctions as LF
import time
from nltk.stem.snowball import EnglishStemmer
import overListFunctions as listFunc
stemmer = EnglishStemmer()
answerFolder = "/Users/warles34/Document/Research/CODE/Tesis/Wikipedia/2006TXT/"



#stemm(wordList): Cada una de las palabras contenidas en la lista "wordList" son cortadas a manera de llegar a 
#una forma raiz que representa el lema de esa palabra, conteniendo todas sus formas flexionadas (ya sea de numero,
# de conjugacion, de tiempo, etc)

def stemm(wordList):
	return [EnglishStemmer.stem(stemmer,word) for word in wordList]



#retrieve100Best(wordDocs, bm25=1, retrieveSize=150): esta funcion toma una lista de palabras
def retrieve100Best(wordDocs, bm25=1, retrieveSize=150):
	docRowList = listFunc.organizeWordDocs(wordDocs)
	print "start the retrieve"
	if bm25:
		tuples = [(docRow[0],RS.SumBM25(docRow[1])) for docRow in docRowList]
		
	else:
		tuples = [(docRow[0],RS.sumTFIDF(docRow[1])) for docRow in docRowList]
	print "end the ranking, start the sort"
	return sorted(tuples, key=lambda second: -second[1])[:retrieveSize]
	

#save(docList, inputFolder, outputFolder, question): doclist es una lista de tuplas que contienen el titulo de un 
#documentos de wikipedia, y la relevancia que este documentos tiene respecto a la pregunta inicial. Esta funcion lee 
#y busca los titulos de los documentos contenidos en docList, y los guarda en un archivo de texto junto con el puntaje 
#de relevancia recibido por el procesamiento realizado, a modo que sea mas facil de entender para un lector humano. 
def save(docList, inputFolder, outputFolder, question):
	g = open(outputFolder + question + ".txt", 'w')
	for doc in docList:
		f = open(inputFolder + doc[0],'r')
		text = f.readline()
		f.close()
		g.write("\n\n[[[[[[[[[[[[[[[[[[[[[[[[[[[ "+ str(doc[1]) + "|" + doc[0] + " ]]]]]]]]]]]]]]]]]]]]]]]]]]]\n")
		g.write(text)
	g.close()


#rank100bestAnswers(question, WantToSave=0): este programa representa el programa principal el cual recibe la pregunta 
#y retorna en orden de relevancia una lista de direcciones a documentos con el respectivo puntaje asignado y por el cual 
#fueron organizados.
def rank100bestAnswers(question, WantToSave=0):
	words = LF.listWords(question)
	words = stemm(words)
	words = LF.clean_nonExist(words)
	aWord = []
	words = VE.expandVocab(words)
	print words
	for word in words:
		numb = MsqlQ.appearHowManyDoc(word) 
		aWord.extend(MsqlQ.searchDocuments(word))
	print aWord
	goods = retrieve100Best(aWord)
	
	return goods

# return100textDocs(question): esta funcion se encarga de, luego de realizar la organizacion de las direcciones de los documentos
# respuesta, conseguir el contenido de estos contenidos y regresarlos en texto plano.
def return100textDocs(question):
	t = time.time()
	goods = rank100bestAnswers(question)
	t = time.time() - t
	print t 
	res = []
	for elem in goods:
		filename ='/Users/warles34/Documents/Research/CODE/Tesis/Wikipedia/2006TXT/' + str(elem[0])
		f = open(filename,'r')
		doc = f.read()
		doc = doc.split("\n")
		f.close
		res.append((doc, elem[1]))
	return res	
	

if __name__ == "__main__":
	d = rank100bestAnswers(sys.argv[1])
	print d

