# Este documento es el que se encarga de realizar los accesos a la base de datos
import MySQLdb
db=MySQLdb.connect(db= "wikipedia", passwd= "19335350Garfield", user="ochoaC")
cur = db.cursor()


#averageDoc(): Retorna el valor promedio del tamanio de los articulos de la base de datos.
def averageDoc():
	cur.execute('''SELECT AVG(FILESIZE) FROM LOCATION''')
	res = cur.fetchone()
	if res == None:
		return 0
	return res[0]

#totalAmountWORD(): Retorna el numero de raices de palabras distintas contenidas en la base de datos
def totalAmountWORD():
	cur.execute('''SELECT COUNT(*) FROM WORD''')
	res = cur.fetchone()
	if res == None:
		return 0
	return res[0]
	
	
#totalAmountDOC(): Retorna el numero de documentos que existen en la base de datos

def totalAmountDOC():
	cur.execute('''SELECT COUNT(*) FROM LOCATION''')
	res = cur.fetchone()
	if res == None:
		return 0
	return res[0]
	
	
#appearHowManyThisWord(word): retorna el numero de veces que aparece la palabra "word" en la base de datos

def appearHowManyThisWord(word):
	cur.execute('''SELECT AMOUNT FROM WORD WHERE CODE = %s''',(word))
	res = cur.fetchone()
	if res == None:
		return 0
	return res[0]
	

# appearHowManyDoc(word): retorna el numero de articulos en el que aparece la palabra "word"
def appearHowManyDoc(word):
	cur.execute('''SELECT NUMBEROFARTICLES FROM WORD WHERE CODE = %s''',(word))
	res = cur.fetchone()
	if res == None:
		return 0
	return res[0]
	

#searchRow(word,doc): retorna la inf
	
def searchRow(word,doc):
	cur.execute('''SELECT * FROM WORDPATH WHERE (WORD,PATH_ID) = (%s,%s)''',(word,doc))
	res = cur.fetchall()
	if res == ():
		return 0
	return res[0]
	
#searchDocuments(word): retorna los registros correspondientes a los documentos que contienen la palabra "word" contenida dentro del documento

def searchDocuments(word):
	cur.execute('''SELECT * FROM WORDPATH WHERE WORD = %s''',(word))
	return cur.fetchall()


#documentSize(path): retorna el tamanio en numero de palabras que contiene el documento

def documentSize(path):
	cur.execute('''SELECT FILESIZE FROM LOCATION WHERE PATHNAME = %s''',(path))
	res = cur.fetchone()
	if res == None:
		return -1
	return res[0]


#common(wordList): regresa las direcciones de los documentos que contengan todos los elementos de la lista wordList.
def common(wordList):
	select1 = 'SELECT DISTINCT PATH_ID FROM WORDPATH WHERE WORD = "'
	select2 = '" AND PATH_ID IN ('
	consult = ''
	for word in wordList:
		consult += select1 + word + select2
	consult = consult[:(len(consult)-len(select2)+1)]
	for word in wordList:
		consult = consult + ')'	
	consult = consult[:(len(consult)-1)]
	cur.execute(consult)
	return cur.fetchall()


average = averageDoc()
