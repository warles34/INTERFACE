'''Vocabulary Expantion:
	Este programa se encarga de usar la estructura lexica que tiene la coleccion de WordNet para poder expandir las palabras contenidas en la consulta original
y asi poder tener una consulta mas amplia, sin perder la escencia del significado de la misma.'''
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import re
import sys
import itertools
from collections import Counter
from sets import Set
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
wordform = re.compile(r'\b\w\w\w+\b')
'''class wordSyn:
	init (w):
		word = w
		syn = wn.synsets(word)

'''

#checksimil(synsets1,synsets2, simFactor):Chequea la similitud entre los conjuntos de sinonimos synsets1 y synsets2, devolviendo 
#una tupla teniendo como primer valor el conjunto de sinonimos similares y como segundo valor el conjunto de los que no fueron similares  
def checksimil(synsets1,synsets2, simFactor):
	simold = -1
	sim = -1
	similset = []
	unsimilset = []
	for ss1 in synsets1:
		for ss2 in synsets2:
			if ss1.pos == ss2.pos and ss2.pos != "s" and ss2.pos != "r" and ss2.pos != "a":
				if max(sim,wn.jcn_similarity(ss1,ss2,semcor_ic)) > simFactor:
					similset.append(ss1)
				else:
					unsimilset.append(ss1)
	return (similset,unsimilset)

def expandThree(word):
	syn = wn.synsets(word)
	res = []
	if syn != []:
		for s in syn:
			res.extend(s.hypernyms())
			res.extend(s.hyponyms())
	return res
	

#generateCombination(pairs):
def generateCombination(pairs):
	synss = []
	for pair in pairs:
		synss.append(pair)
	return itertools.combinations(synss, 2)



def greaterFather(question):
	father = []
	minim = 1000000
	elems = []
	for word in question:
		s = wn.synsets(word)
		elems.extend(s)
	scomb = generateCombination(elems)
	for syn in scomb:
		possibleFathers = syn[0].lowest_common_hypernyms(syn[1])
		father.extend(possibleFathers)
	if father == []:
		return 0
	return Counter(father).most_common(1)[0][0]
		
		




#return a pair of sets (EG, Qe) where EG is {(word,{word.synsets()}} and Qe is {synsets}
def createGroups1(question):
	EG = []
	Qe = []
	superCommon = greaterFather(question)
	if superCommon:
		for word in question:
			e = wn.synsets(word)
			for syn in e:
				if syn.lowest_common_hypernyms(superCommon).count(superCommon)>0:
					EG.append((word,e))
					break
			else:
				Qe.extend(expandThree(word))
		return (EG , Qe)
	else:
		for word in question:
			Qe.extend(expandThree(word))
		return ([],Qe)


def expandByGroup(EG):
	mini = 10000000
	maxi = -1
	middle = []
	for ti in EG:
		for s in ti[1]:
			middle.append(s)
			down = s.max_depth()
			up = s.min_depth()
			if down > maxi:
				downSyn = s
				maxi = down
			if up < mini:
				upSyn = s
				mini = up
	if mini >= 10000000:
		downSyn = 0
	if maxi <= -1:
		upSyn = 0
	return (middle,downSyn,upSyn)




def completeExpansion(EG,simFactor):
	Qe = []
	simSet = Set([])
	unsimSet = Set ([])
	mini = 10000000
	maxi = -1
	middle = []
	EGTemp = EG
	for ti in EG:
		s = []
		for tj in EGTemp:
			if ti!=tj:
				(s,u) = checksimil(ti[1],tj[1], simFactor)
		if s == []:
			EG.remove(ti)
			Qe.extend(expandThree(ti[0]))
	
	(middle, lo, up) = expandByGroup(EG)
	Qe.extend(middle)
	if lo:
		Qe.extend(lo.hyponyms())
	if up:
		Qe.extend(up.hypernyms())
	return Qe
		
def expandVocab(line):
	EG = []
	Qe = []
	print "SE VA A EXPANDIR EL VOCABULARIO DESDE ESTE INSTANTE"
	(EG,Qe) = createGroups1(line)
	Qe.extend(completeExpansion(EG,0.05))
	words = []
	for e in Qe:
		for l in e.lemmas:
			words.append(l.name)
	return Set(words)
		


if __name__ == "__main__":
	q = "Why do psychologist use animals in their research"
	wordList = wordform.findall(q)[2:]
	print expandVocab(wordList)

