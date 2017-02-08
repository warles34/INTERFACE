import mysqlQueries as MsqlQ
import math
#######TF_IDF\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


#TF(wordAmount,docSize): Calcula el Term Frequency dividiendo la frecuencia "wordAmount" de una determinada palabra entre el tamanio del documento docSize
def TF(wordAmount,docSize):
	return float(wordAmount) / math.log(1 +float(docSize))

#IDF(howManyDoc):funcion que retorna el logaritmo de la frecuencia de cuantos documentos contienen el termino estudiado. La suma de 0.5 es una relajacion de la ecuacion que elimina los casos de division entre cero.
def IDF(howManyDoc):
	return math.log((float(MsqlQ.totalAmountDOC())- howManyDoc + 0.5)/ (0.5 + howManyDoc))
	

#TF_IDF(row): funcion que regresa el calculo tf_idf de una palabra especifica respecto a un documento especifico
def TF_IDF(row):
	documenFrequency = MsqlQ.appearHowManyDoc(row[0])
	docS = MsqlQ.documentSize(row[1])
	termFrequency = row[2]
	return TF(termFrequency,docS)*IDF(documenFrequency)
	

#sumTFIDF(rowList): regresa la suma de los valores regresados por TF_IDF evaluado en cada uno de los elementos del rowList, que contiene la relacion de todas las palabras que aparecen en el query respecto a un documentos especifico
def sumTFIDF(rowList):
	c = 0
	for row in rowList:
		c+= TF_IDF(row)
	return c

	
	
#######Okapi BM25\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
	

#BM25_Score(term_frequency, document_size, howManyDoc, k1=1.2, b=0.75): regresa la evaluacion de la funcion Okapi BM25 
def BM25_Score(term_frequency, document_size, howManyDoc, k1=1.2, b=0.75):
	return (IDF(howManyDoc))*(float(term_frequency)*(k1 + 1)/(term_frequency + k1*(1 - b + b*(float(document_size)/float(MsqlQ.average)))))
	

#SumBM25(rowList): regresa la suma de los valores regresados por BM25_Score evaluado en una serie de valores derivados de cada uno de los elementos de rowList, los cuales son la cantidad de palabras que contiene el documento, la frecuencia con la que aparece una de las palabras del query y en cuantos documentos esa palabra aparece.
def SumBM25(rowList):
	res = 0
	for row in rowList:
		docSize = MsqlQ.documentSize(row[1])
		termFrequency = row[2]
		documenFrequency = MsqlQ.appearHowManyDoc(row[0])
		res += BM25_Score(termFrequency,docSize,documenFrequency)
	return res


