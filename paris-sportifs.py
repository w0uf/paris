# -*- coding: utf-8 -*-
# version 1.0.0
# by Laurent Petitprez
"""Cette œuvre est mise à disposition sous licence Attribution 4.0 International.
Pour voir une copie de cette licence, visitez http://creativecommons.org/licenses/by/4.0/
ou écrivez à Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."""

bankroll_max = 100


def moyenne(liste):
    """renvoie la moyenne d'une liste
    cela correspond à la fonction moyenne du module statistics"""
    num = 0
    liste = list(liste)
    for l in liste:
        num += l
    den = len(liste)
    if den != 0:
        return num / den
    else:
        return "Erreur : liste vide"


def cout(args):
    x = 0
    for i in args:
        x += i
    return x


def gain_min(l, args):
    gains = []
    for k in range(len(l)):
        gains.append(args[k] * l[k])
    return min(gains)


def cherche_valuebet(l):
    """l est une liste de cote (*1000) - nombres entiers"""
    #    print("Recherche de Value Bet avec les côtes moyennes." )
    probas = [1000 / x for x in l]
    somprobas = 0
    for p in probas:
        somprobas += p

    benef_bm = round(somprobas, 2)
    return [round(1000 * benef_bm / x) for x in probas]


def test_surebet(l):
    """l est une liste de cote (*1000) - nombres entiers"""
    den = 1
    num = 0

    for c in l:
        den *= c
    for c in l:
        num += 1000 * den / c
    if num < den:
        print("SureBet possible !")
        nb = len(l)
        if nb > 3:
            print("Alerte : la recherche peut prendre beaucoup de temps !")
        mises_p = [x for x in range(bankroll_max + 1)]
        mises = [[x] for x in mises_p]

        for i in range(nb - 1):
            mises = [x + [y] for x in mises for y in mises_p]

            # mises contient les mises possibles
        rentabilite = 0
        solution = []
        for m in mises:
            if gain_min(l, m) > 0:
                if (gain_min(l, m) - cout(m) * 1000) / cout(m) > rentabilite:
                    rentabilite = (gain_min(l, m) - cout(m) * 1000) / cout(m)
                    solution = m
        if len(solution) == 0:
            print("Pas de solution avec les contraintes financières !")
            return True
        else:
            print("Rentabilité maximum ", round(rentabilite / 10, 2), "%")

            print("Mises :", end=" ")
            for s in solution:
                print(s, "€(", round(l[solution.index(s)] / 1000, 2), "/1)", end=" ")
            print()
            print("coût :", cout(solution), "€")
            print("Bénéfice minimum :", round(gain_min(l, solution) / 1000 - cout(solution), 2), "€")
            return True
    else:
        if num == den:
            print("Cas limitte - La somme des probas associées est 1.")

        return False


def cherche_surebet(l):
    """l est une liste de cote (*1000) - nombres entiers"""
    co = 0

    for c in l:
        co += 1000 / c
    if co > 1:
        print("Bookmakers (Plus value sur proba) :", round((co - 1) * 100, 2), "%")

    print("Corrections sur les meilleurs côtes pour Surebet :")
    for n in range(len(l)):
        a = []
        for i in l:
            if l.index(i) == n:
                c = co - 1000 / i
                if 0 < c < 1:
                    a.append(">" + str(round(1 / (1 - c), 2)))
                else:
                    a.append("+ infini")
            else:
                a.append(round(i / 1000, 3))
        for j in a:
            print(j, end=" ")
        print()


def uneliste():
    global leslistes, fini
    l = input("Liste " + str(len(leslistes) + 1) + ":").split()
    li_2 = list(round(float(x) * 1000) for x in l if float(x) > 1)
    if len(l) > len(li_2):
        print("alerte : Certaine valeurs ont été ignorées ! (", len(l) - len(li_2), ")")
    if len(leslistes) > 1 and len(li_2) == 0:
        fini = True
        #        print("Saisie terminée." )
        return
    elif len(li_2) == 0:
        print("liste vide : erreur")
    else:
        # la liste n'est pas vide
        if len(leslistes) == 0:
            leslistes.append(li_2)
        elif len(leslistes[0]) != len(li_2):
            print("Erreur :listes de longueurs différentes !")
        else:
            leslistes.append(li_2)


caption = {
    "complet":
        """Entrez les listes de côtes, séparées par des espaces.
    Chaque valeur doit être un nombre décimal supérieur à 1 avec au plus 3 chiffres significatifs.
    
    Si le nombre de chiffres est supérieure les valeurs sont arrondies.
    
    Si un nombre est inférieur à 1, il est ignoré.
    
    Vous pouvez ajouter autant de listes que vous le désirez, et finissez par ENTREE
    
    Un seul imperatif : les listes doivent être de longueurs égales.
    
    """,

    "simple":
        """Entrez les listes de côtes, séparées par des espaces. (3 chiffres significatifs)
        Les listes doivent être de longueurs égales.""",

    "minimum":
        "Listes de côtes : "
}

while 1:
    fini = False
    leslistes = []

    print(caption["minimum"])
    while not fini:
        uneliste()

    #    print("Analyse :" )
    #    print("Nombre de bookmaker :" ,len(leslistes[0]),"Nombre de paris :" ,len(leslistes))
    #    print("côtes (minimum, moyenne, meilleure):" )
    lesmax = []
    lesmoy = []
    for li in leslistes:
        lesmax.append(max(li))
        lesmoy.append(moyenne(li))
    #        print (round(min(li)/1000,2),round(moyenne(li)/1000,2),round(max(li)/1000,2))

    if not (test_surebet(lesmax)):
        print("Pas de SureBet !")
        vr = cherche_surebet(lesmax)
        vb = cherche_valuebet(lesmoy)
        print("Côtes en valuebet ", end=":")
        for v in vb:
            print(round(v / 1000, 2), end=" ")
        print()
    print("--------------------------------------------------------")
    print()
