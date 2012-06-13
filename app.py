"""Zoek vergelijkbare woorden"""

# Eindopdracht Project Tekstanalyse
# Groep Munt, juni 2012

"""Een script dat na invoer van een zelfstandig naamwoord de tien meest lijkende woorden uit een corpus weergeeft."""


"""Vraag de gebruiker een zelfstandig naamwoord in te geven"""

# controle?

#woord = eval(input("Geef een zelfstandig naamwoord: "))

"""Maak een vector van het gegeven woord"""

basisvector = vector(woord)

"""Maak vectoren van overige zelfstandig naamwoorden en controleer afstand"""

# lege lijst aanmaken voor lijkende woorden
lijkendewoorden = []

# alle zelfstandignaamwoorden in vector zetten en vergelijken met basisvector
for znw in corpus:
    positie = 0
    gelijkenis = 0
    vector = vector(znw)
    for i in vector:
        afstand = basisvector[positie] - vector[i]
        if afstand > gelijkenis:
            gelijkenis = afstand

        positie += 1

    lijkendewoorden.append((znw, gelijkenis))

"""Presenteer de tien dichtstbijzijnde woorden"""
lijkendewoorden = sorted(lijkendewoorden, key=lambda n: n[1])
n = 0
for i in lijkendewoorden:
    print(lijkendewoorden[i][0])
    n +=1

