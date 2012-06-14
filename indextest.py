#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
#
# export PATH=/net/aps/64/bin:$PATH
# export PYTHONPATH=/net/aps/64/lib/python3.1

import string


#Functie nodig voor het sorteren van de scorelijst (als dictionary)
def byFreq(pair):
	return pair[1]

#Indexlijsten inladen en verwerken als lijst#
fnamesubj = "filesubj.txt"
fnameobj = "fileobj.txt"
fnameverb = "fileverb.txt"
fnameconj = "fileznw.txt"

infilesubj = open(fnamesubj,"r",encoding="utf-8")
infileobj = open(fnameobj,"r",encoding="utf-8")
infileverb = open(fnameverb,"r",encoding="utf-8")
infileconj = open(fnameconj,"r",encoding="utf-8")

dictsubj = eval(infilesubj.read())
dictobj = eval(infileobj.read())
dictverb = eval(infileverb.read())
dictconj = eval(infileconj.read())


infilesubj.close()
infileobj.close()
infileverb.close()
infileconj.close()

#resultaatlijsten declareren
znwhits = dict()
wordscores = dict()
subjhits =  list()
subjverbhits = list()
objhits =  list()
objverbhits = list()
keyword = input("Wat wilt u als zoekwoord?: ")
listscorekeyword = [keyword]
listscorehits = list()


#Relevante woorden zoeken in conjuncties
for key, value in dictconj.items():
    if key == keyword:
        for item in znwhits:
            if value[0] in item:
                znwhits[value[0]] = znwhits[value[0]] + 1
            else:
                znwhits[value[0]] = value[1]

#Resultaten van de conjuncties verwerken in de scorelijst
for key, value in znwhits.items():
    if key in wordscores:
        wordscores[key] = wordscores[key] + (value * 2.5)
    else:
        wordscores[key] = value * 2.5

#Werkwoorden zoeken die voorkomen met het zoekwoord in de lijst subjhits plaatsen. Hierbij wordt niet rekening gehouden met werkwoorden die vaker voorkomen bij een subject
for key, value in dictsubj.items():
    if key == keyword:
        for item in value:
            if item[0] not in subjhits:
                    if item[0] != "zijn":
                            if item[0] != "worden":
                                    if item[0] != "hebben":
                                            subjhits.append(item[0])

#Werkwoorden zoeken die voorkomen met het zoekwoord in de lijst objhits plaatsen. 
for key, value in dictobj.items():
    if key == keyword:
        for item in value:
            if item[0] not in objhits:
                    if item[0] != "zijn":
                            if item[0] != "worden":
                                    if item[0] != "hebben":
                                            objhits.append(item[0])

#Resultaten van de onderwerpen (werkwoorden) vergelijken met andere onderwerpen bij deze werkwoorden
for werkwoord in subjhits:
    for key, value in dictverb.items():
            if key == werkwoord:
                for item in value:
                    if item[0] not in subjverbhits:
                        if item[0] != keyword:
                            subjverbhits.append(item[0])

#Resultaten van de onderwerpen (werkwoorden) vergelijken met andere onderwerpen bij deze werkwoorden 2
for werkwoord in objhits:
    for key, value in dictverb.items():
            if key == werkwoord:
                for item in value:
                    if item[0] not in objverbhits:
                        if item[0] != keyword:
                            objverbhits.append(item[0])

#Waarden berekenen van de werkwoorden bij het zoekwoord
for werkwoord in subjhits+objhits:
        if werkwoord in dictverb.keys():
                for key, value in dictverb.items():
                        if key == werkwoord:
                                for item in value:
                                        if item[0] == keyword:
                                                listscorekeyword.append(item[1])
        else:
                listscorekeyword.append(0)

                            
#Waarden berekenen bij verschillende gevonden onderwerpen
for wordhit in subjverbhits:
        hitlist = [wordhit]
        for werkwoord in subjhits:
                hitlist.append(0)
                for key, value in dictverb.items():
                        if key == werkwoord:
                                for item in value:
                                        if item[0] == wordhit:
                                                hitlist[-1] = item[1]

        listscorehits.append(hitlist)

#Waarden berekenen bij verschillende gevonden onderwerpen
for wordhit in objverbhits:
        hitlist = [wordhit]
        for werkwoord in objhits:
                hitlist.append(0)
                for key, value in dictverb.items():
                        if key == werkwoord:
                                for item in value:
                                        if item[0] == wordhit:
                                                hitlist[-1] = item[1]

        listscorehits.append(hitlist)

#indices bepalen van zelfstandige naamwoorden (met als rol subject) t.o.v. het zoekwoord
for score in listscorehits:
    indexnummer = 1
    relevantiewaarde = 0
    for waarde in score:
        if not isinstance(waarde, str):
            if (waarde + listscorekeyword[indexnummer]) == 0:
                relevantiewaarde = relevantiewaarde + 0
            elif waarde >= listscorekeyword[indexnummer]:
                relevantiewaarde = relevantiewaarde + (2 * listscorekeyword[indexnummer] / (waarde + listscorekeyword[indexnummer]))
                indexnummer = indexnummer + 1
            else:
                relevantiewaarde = relevantiewaarde + (2 * waarde / (waarde + listscorekeyword[indexnummer]))
                indexnummer = indexnummer + 1
    score.append(relevantiewaarde)

#Relevantiewaarden van de subjecten toevoegen in de scorelijst
for score in listscorehits:
    if score[0] in wordscores:
        wordscores[score[0]] = wordscores[score[0]] + (score[-1] * 1.5)
    else:
        wordscores[score[0]] = score[-1] * 1.5

#Uitvoer als er geen wordscores is

if wordscores == {}:
        print("Er zijn geen relevantie woorden gevonden.")
else:

#scorelijst sorteren en de top 20 woorden tonen
        itemsscore = list(wordscores.items())
        itemsscore.sort()
        itemsscore.sort(key=byFreq, reverse=True)
        count = 0
        top10 = []
        for i in range(10):
                woord, relevantie = itemsscore[i]
                top10.append(woord)
        print("De woorden die het meest op",keyword,"lijken zijn: {0}.".format(", ".join(top10)))
