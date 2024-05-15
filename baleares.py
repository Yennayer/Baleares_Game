# -*- coding: utf-8 -*-
import random
import numpy as np

# [RAPPEL] { x => blanc    |    o => noir }

########################################################################################################################
############      Fonctions De Grille:

# Fonction qui permet de créer une grille avec n'importe quelle taille
def creer_grille(taille_n):
    # Créeation de la grille de taille n
    grille = [[' ' for i in range(taille_n)] for j in range(taille_n)]
    # Remplissage de la grille
    for l in range(taille_n):
        for c in range(taille_n):
            if l < 2:
                grille[l][c] = 'o'
            if l > taille_n - 3:
                grille[l][c] = 'x'
    return grille

# Fonction qui renvoie la grille du milieu de partie
def creer_grille_milieu():
    grille = [[' ', ' ', 'o', 'o', ' ', 'o', 'o'], [' ', ' ', 'o', 'o', 'x', ' ', ' '],
              ['o', 'x', ' ', 'x', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', 'o', ' ', ' '], [' ', 'x', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', 'x', 'x', 'o', ' ', 'x'],
              [' ', ' ', 'x', 'x', 'x', 'x', ' ']]
    return grille

# Fonction qui renvoie la grille d'avant la fin de partie
def creer_grille_fin():
    grille = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'x', ' ', ' '],
              [' ', 'x', ' ', 'x', ' ', ' ', ' '],
              [' ', 'o', ' ', ' ', ' ', ' ', ' '], ['o', ' ', ' ', ' ', 'x', ' ', ' '],
              [' ', 'o', 'o', ' ', 'o', ' ', 'x'],
              [' ', ' ', 'o', ' ', ' ', ' ', 'o']]
    return grille

# Fonction qui renvoie une grille finie
def creer_grille_finie():
    grille = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'x', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', 'o', ' ', ' ', ' ', ' ', ' '], ['o', ' ', ' ', ' ', 'x', ' ', ' '],
              [' ', 'o', 'o', ' ', 'o', ' ', 'x'],
              [' ', ' ', 'o', ' ', ' ', ' ', 'o']]
    return grille

# Fonction qui affiche une grille
def afficher_grille(grille):
    # Afficher la numérotation de colonnes
    print()
    for chiffre in range(len(grille) + 1):
        print(chiffre, end=" | ")
    print('\n', '--|', '---|' * (len(grille) - 1), '---', sep='')
    n = 0
    # Afficher la grille et la numérotation de lignes
    for item in grille:
        print(chr(65 + n), *item, sep=' | ')
        print('--|', '---|' * (len(grille) - 1), '---', sep='')
        n += 1
    print()
    affichage_nb_pion(grille)

# Fonction qui affiche le nombre de pions dans le jeu
def affichage_nb_pion(grille):
    b, n = 'x', 'o'
    pion_noir, pion_blanc = 0, 0
    # La fonction parcourt la grille et calcule le nombre de pion
    for ligne in grille:
        for case in ligne:
            if case == n:
                pion_noir += 1
            elif case == b:
                pion_blanc += 1
    print("Nombre de pion blanc = ", pion_blanc, "   Nombre de pion noir = ", pion_noir, '\n')

# Fonction qui met à jour la grille après un déplacement avec prise par retournement
def maj_retournement(depart, arrivee, grille):
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    # Mémoriser le joueur et l'adversaire
    joueur = grille[xd][yd]

    # Vecteur de déplacement
    z1, z2 = xa - xd, ya - yd
    # Cas où les deux cases sont dans une même ligne
    if z1 == 0:
        if z2 >= 2:
            grille[xd][yd] = ' '
            grille[xa][ya - 1] = joueur
            grille[xa][ya] = joueur
        else:
            grille[xd][yd] = ' '
            grille[xa][ya + 1] = joueur
            grille[xa][ya] = joueur
    # Cas où les deux cases sont dans une même colonne
    elif z2 == 0:
        if z1 >= 2:
            grille[xd][yd] = ' '
            grille[xa - 1][ya] = joueur
            grille[xa][ya] = joueur
        else:
            grille[xd][yd] = ' '
            grille[xa + 1][ya] = joueur
            grille[xa][ya] = joueur
    # Cas diagonal
    else:
        # Direction Sud Est
        if z1 >= 2 and z2 >= 2:
            grille[xd][yd] = ' '
            grille[xa - 1][ya - 1] = joueur
            grille[xa][ya] = joueur
        # Direction Sud Ouest
        elif z1 >= 2 and z2 <= -2:
            grille[xd][yd] = ' '
            grille[xa - 1][ya + 1] = joueur
            grille[xa][ya] = joueur
        # Direction Nord Est
        elif z1 <= -2 and z2 >= 2:
            grille[xd][yd] = ' '
            grille[xa + 1][ya - 1] = joueur
            grille[xa][ya] = joueur
        # Direction Nord Ouest
        elif z1 <= -2 and z2 <= -2:
            grille[xd][yd] = ' '
            grille[xa + 1][ya + 1] = joueur
            grille[xa][ya] = joueur
    return grille

# Fonction qui met à jour la grille aprés le déplacement
def maj_grille(depart, arrivee, joueur, grille):
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    # Listes de déplacement
    l_deplacement_simple = liste_arrivee_simple(depart, grille)
    l_deplacement_retournement = liste_arrivee_retournement(depart, grille)
    l_deplacement_saut = liste_arrivee_saut(depart, grille)

    # Déplacement Simple
    if arrivee in l_deplacement_simple:
        grille[xd][yd] = ' '
        grille[xa][ya] = joueur
        return grille
    # Déplacement avec prise par élimination
    if arrivee in l_deplacement_saut:
        grille[xd][yd] = ' '
        grille[xa][ya] = joueur
        return grille
    # Déplacement avec prise par retournement
    if arrivee in l_deplacement_retournement:
        return maj_retournement(depart, arrivee, grille)

########################################################################################################################
############      Fonctions de saisie:

# Fonction qui permet de choisir l'adversaire
def choix_jeu():
    print("Veuillez choisir :\n1 -> joueur vs joueur\n2 -> joueur vs IA Naïve\n3 -> joueur vs IA Avancée")
    message = input()
    while not (message == '1' or message == '2' or message == '3'):
        print("Erreur De Saisie")
        message = input()
    if message == '1':
        return 0
    elif message == '2':
        return 1
    else:
        return 2

# Fonction qui permet de choisir la grille de jeu
def choisir_grille():
    print(
        "Choissiez la grille sur laquelle vous voulez jouer !\n1 -> Grille Début\n2 -> Grille Du Milieu\n3 -> Grille Fin")
    message = input("Saisissez : 1/2/3 :  ")
    while message != '1' and message != '2' and message != '3':
        print("Erreur De Saisie !")
        message = input("Saisissez : 1/2/3 :  \n")
    if message == '1':
        return creer_grille(7)
    elif message == '2':
        return creer_grille_milieu()
    elif message == '3':
        return creer_grille_fin()

# Fonction qui permet de choisir le type de joueur
def type_joueur():
    print("Veuillez choisir votre Joueur\n1 -> 'x'\n2 -> 'o'")
    message = input()
    while not (message == '1' or message == '2'):
        print("Erreur De Saisie !")
        message = input()
    if message == '1':
        return 'x'
    elif message == '2':
        return 'o'

# Fonction qui permet d'abondonner la partie
def abandon():
    print("Voulez-vous continuer la partie ? ")
    message = input("[o/n]    ")
    while message != 'o' and message != 'n':
        print("Réponse Incorrecte !")
        message = input("[o/n]    ")
    if message == 'n':
        return True
    else:
        return False

# Fonction Qui Permet De Saisir Les Coordonnées Du Pion
def saisir_coordonnees(grille, joueur):
    erreur = True
    depart, arrivee = None, None
    while erreur == True:
        # Saisie de coordonnées de départ
        message = input("Saisissez les coordonnées de départ ! (exemple: A3 ou G2) ->  ")
        # Cas où les coordonnées ne sont pas valides
        while not (est_au_bon_format(message) and est_dans_grille(message[0], message[1], grille)
                   and case_depart(message[0], message[1], grille, joueur)):
            print("Coordonnées Incorrectes !")
            message = input("Veuillez ressaisir les coordonnées de départ !  ")
        depart = message
        # Saisie de coordonnées d'arrivée
        message = input("Saisissez les coordonnées d'arrivée ! (exemple: A3 ou G2) ->  ")
        while not (est_au_bon_format(message) and est_dans_grille(message[0], message[1], grille)):
            print("Coordonnées Incorrectes !")
            message = input("Veuillez ressaisir les coordonnées d'arrivée !  ")
        if not (message in liste_arrivee_simple(depart, grille) or message in liste_arrivee_retournement(depart,
                                                                                                         grille) or message in liste_arrivee_saut(
                depart, grille)):
            print("Deplacement incorrect")
            erreur = True
        else:
            erreur = False
            arrivee = message
    return depart, arrivee

# Fonction qui applique un enchainement lorsqu'il est possible
def enchainement(arrivee, grille):
    depart = arrivee
    liste_retournement = liste_arrivee_retournement(depart, grille)
    # Tant que la partie n'est pas finie et qu'on a la possibilité d'enchaîner
    while not est_fin_de_partie(grille) and len(liste_retournement) != 0:
        reponse = input("Voulez-vous enchaîner [o/n] ?")
        while reponse != "o" and reponse != "n":
            print("Erreur De Saisie !")
            reponse = input("Voulez-vous enchaîner [o/n] ? ")
        if reponse == 'o':
            message = input("Saisissez les coordonnées d'arrivée ! (exemple : A1) -> ")
            while not (est_au_bon_format(message) and est_dans_grille(message[0], message[1], grille)) or not (
                    message in liste_retournement):
                print(" Case Incorrecte !")
                message = input("Veuillez ressaisir les coordonnées d'arrivée ->  ")
            new_arrivee = message
            grille = maj_retournement(depart, new_arrivee, grille)
            afficher_grille(grille)
            depart = new_arrivee
            liste_retournement = liste_arrivee_retournement(depart, grille)
        else:
            return None

# Fonction qui permet de lancer la partie
def menu():
    jeu = choix_jeu()
    if jeu == 0:
        jeu_joueur()
    elif jeu == 1:
        ia_naive()
    else:
        ia_avancee()

# Fonction du jeu
def jeu():
    print("1 - Lancer la partie\n2 - Lancer la fonction générale de tests\n")
    message = input(" [1/2] : ")
    while message != '1' and message != '2':
        message = input("Erreur de saisie ! ")
    if message == '1':
        menu()
    else:
        fonction_general_tests()

########################################################################################################################
############      Fonctions De Verification:

# Fonction qui vérifie si le message est au bon format
def est_au_bon_format(message):
    # Taille du message doit être égale à 2, premier caractère doit être une lettre et le second doit être un chiffre
    if len(message) != 2 or not (message[0].isalpha()) or not (message[1].isdigit()):
        return False
    else:
        return True

# Fonction qui vérifie si les coordonnées sont dans la grille
def est_dans_grille(ligne, colonne, grille):
    # La ligne doit être comprise entre A et Z, la colonne doit être comprise entre 1 et la taille de la grille
    if not (65 <= ord(ligne) < 65 + (len(grille))) or \
            not (49 <= ord(colonne) < 49 + (len(grille))):
        return False
    else:
        return True

# Fonction qui vérifie si la partie est terminée
def est_fin_de_partie(grille):
    blanc, noir = 'x', 'o'
    nb_pion_noir, nb_pion_blanc = 0, 0
    # La fonction parcourt la grille et calcule le nombre de pions
    for ligne in grille:
        for case in ligne:
            if case == noir:
                nb_pion_noir += 1
            elif case == blanc:
                nb_pion_blanc += 1
    # La partie se termine si le nombre de pions est à moins de 4
    if nb_pion_blanc < 4 or nb_pion_noir < 4:
        return True
    else:
        return False

# Fonction qui vérifie si deux cases sont adjacentes
def arrivee_adjacente(depart, arrivee):
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    if (xa == xd + 1 and ya == yd + 1) or \
            (xa == xd + 1 and ya == yd - 1) or \
            (xa == xd - 1 and ya == yd + 1) or \
            (xa == xd - 1 and ya == yd - 1) or \
            (xa == xd and ya == yd + 1) or \
            (xa == xd and ya == yd - 1) or \
            (xa == xd + 1 and ya == yd) or \
            (xa == xd - 1 and ya == yd):
        return True
    else:
        return False

# Fonction qui vérifie si deux cases sont dans la même direction dans la grille
def direction(depart, arrivee):
    # Récupération des coordonnées de départ et d'arrivée
    x, y = conversion_ligne(depart[0]), int(depart[1])
    j, k = conversion_ligne(arrivee[0]), int(arrivee[1])
    # Si les deux cases sont dans la même ligne ou la même colonne
    if x == j or y == k:
        return True
    # Vérification sur les diagonales
    for indice in range(1, 8):
        if (x == j - indice and y == k - indice) or \
                (x == j + indice and y == k + indice) or \
                (x == j - indice and y == k + indice) or \
                (x == j + indice and y == k - indice):
            return True
    return False

# Fonction qui vérifie l'éxistence d'au moins d'une case vide entre deux cases
def vide_entre_case(depart, arrivee, grille):
    # Si la case de départ est la même avec la case d'arrivée, donc FAUX
    # Si les deux cases ne sont pas dans la même direction, donc FAUX
    if (depart == arrivee) or (direction(depart, arrivee)) == False:
        return False
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    # Elimination des cases adjacentes
    if (xa == xd + 1 and ya == yd + 1) or \
            (xa == xd + 1 and ya == yd - 1) or \
            (xa == xd - 1 and ya == yd + 1) or \
            (xa == xd - 1 and ya == yd - 1) or \
            (xa == xd and ya == yd + 1) or \
            (xa == xd and ya == yd - 1) or \
            (xa == xd + 1 and ya == yd) or \
            (xa == xd - 1 and ya == yd):
        return False
    # Vecteur de déplacement
    z1, z2 = xa - xd, ya - yd
    # Cas où les deux cases sont dans la même ligne
    if xd == xa:
        for n in range(min(yd, ya) + 1, max(yd, ya)):
            if grille[xa][n] != ' ':
                return False
        return True
    # Cas où les deux cases sont dans la même colonne
    elif yd == ya:
        for n in range(min(xa, xd) + 1, max(xa, xd)):
            if grille[n][yd] != ' ':
                return False
        return True
    # Cas où les deux sont dans de différentes lignes et colonnes
    else:
        # Direction Sud Est
        if z1 >= 0 and z2 >= 0:
            for n in range(xd + 1, xa):
                yd += 1
                if grille[n][yd] != ' ':
                    return False
            return True
        # Direction Sud Ouest
        if z1 >= 0 and z2 < 0:
            for n in range(xd + 1, xa):
                yd -= 1
                if grille[n][yd] != ' ':
                    return False
            return True
        # Direction Nord Est
        if z1 < 0 and z2 >= 0:
            for n in range(xd - 1, xa, -1):
                yd += 1
                if grille[n][yd] != ' ':
                    return False
            return True
        # Direction Nord Ouest
        if z1 < 0 and z2 < 0:
            for n in range(xd - 1, xa, -1):
                yd -= 1
                if grille[n][yd] != ' ':
                    return False
            return True

# Fonction qui vérifie la case de départ
def case_depart(ligne, colonne, grille, joueur):
    if grille[conversion_ligne(ligne)][int(colonne) - 1] == joueur:
        return True
    else:
        return False

# Fonction qui vérifie la validité d'un déplacement simple
def deplacement_simple(depart, arrivee, grille):
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    # Vecteur de déplacement
    z1, z2 = xa - xd, ya - yd
    if direction(depart, arrivee) and grille[xa][ya] == ' ' and (
            arrivee_adjacente(depart, arrivee) or vide_entre_case(depart, arrivee, grille)):
        return True
    else:
        return False

# Fonction qui vérifie la validité d'un déplacement avec prise par élimination
def deplacement_saut(depart, arrivee, grille):
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    # Mémoriser le joueur et l'adversaire
    joueur = grille[xd][yd]
    ennemi = inverser_joueur(joueur)
    # Eliminations des cas invalides
    if arrivee_adjacente(depart, arrivee) or (depart == arrivee) or (grille[xa][ya] == ' ') \
            or ((direction(depart, arrivee)) == False):
        return False
    if grille[xa][ya] == ennemi and vide_entre_case(depart, arrivee, grille):
        return True
    else:
        return False

# Fonction qui vérifie la validité d'un déplacement avec prise par retournement
def deplacement_retournement(depart, arrivee, grille):
    # Récupération des coordonnées de départ et d'arrivée
    xd, yd = conversion_ligne(depart[0]), int(depart[1]) - 1
    xa, ya = conversion_ligne(arrivee[0]), int(arrivee[1]) - 1
    # Mémoriser le joueur et l'adversaire
    joueur = grille[xd][yd]
    ennemi = inverser_joueur(joueur)
    # Eliminations des cas invalides
    if arrivee_adjacente(depart, arrivee) \
            or (depart == arrivee) or (grille[xa][ya] != ' ') \
            or ((direction(depart, arrivee)) == False):
        return False
    # Vecteur de déplacement
    z1, z2 = xa - xd, ya - yd
    # Cas où les deux cases sont dans une même ligne
    if z1 == 0:
        if z2 >= 2:
            if grille[xa][ya - 1] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa, ya - 1), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa, ya - 1))):
                return True
            else:
                return False
        else:
            if grille[xa][ya + 1] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa, ya + 1), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa, ya + 1))):
                return True
            else:
                return False
    # Cas où les deux cases sont dans une même colonne
    elif z2 == 0:
        if z1 >= 2:
            if grille[xa - 1][ya] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa - 1, ya), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa - 1, ya))):
                return True
            else:
                return False
        else:
            if grille[xa + 1][ya] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa + 1, ya), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa + 1, ya))):
                return True
            else:
                return False
    # Cas diagonal
    else:
        # Direction Sud Est
        if z1 >= 2 and z2 >= 2:
            if grille[xa - 1][ya - 1] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa - 1, ya - 1), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa - 1, ya - 1))):
                return True
            else:
                return False
        # Direction Sud Ouest
        elif z1 >= 2 and z2 <= -2:
            if grille[xa - 1][ya + 1] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa - 1, ya + 1), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa - 1, ya + 1))):
                return True
            else:
                return False
        # Direction Nord Est
        elif z1 <= -2 and z2 >= 2:
            if grille[xa + 1][ya - 1] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa + 1, ya - 1), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa + 1, ya - 1))):
                return True
            else:
                return False
        # Direction Nord Ouest
        elif z1 <= -2 and z2 <= -2:
            if grille[xa + 1][ya + 1] == ennemi and \
                    (vide_entre_case(conversion_chr(xd, yd), conversion_chr(xa + 1, ya + 1), grille)
                     or arrivee_adjacente(depart, conversion_chr(xa + 1, ya + 1))):
                return True
            else:
                return False

########################################################################################################################
############      Fonctions de conversion:

# Fonction qui convertit un caractère en code ASCI
def conversion_ligne(ligne):
    return ord(ligne) - ord('A')

# Fonction qui convertit un code ASCI en caractère
def conversion_chr(x, y):
    return chr(x + 65) + str(y + 1)

# Fonction qui fait le changement de joueur
def inverser_joueur(joueur):
    if joueur == 'x':
        return 'o'
    else:
        return 'x'

########################################################################################################################
############      Fonctions de vérification pour IA Naïve:

# Fonction qui renvoie les listes des départs et d'arrivées possibles pour l'ordinateur
def case_depart_ordi(joueur, grille):
    liste = []
    taille = len(grille)
    # Parcours de la grille
    for ligne in range(taille):
        for colonne in range(taille):
            # Si la case contient le pion de l'ordinateur
            if grille[ligne][colonne] == joueur:
                depart = conversion_chr(ligne, colonne)
                liste.append(depart)
    return liste

# Liste de déplacement simple
def liste_arrivee_simple(depart, grille):
    liste = []
    taille = len(grille)
    # Parcours de la grille
    for ligne in range(taille):
        for colonne in range(taille):
            arrivee = conversion_chr(ligne, colonne)
            # Ajouter les déplacements possibles à la liste
            if deplacement_simple(depart, arrivee, grille):
                liste.append(arrivee)
    return liste

# Liste de déplacement avec prise par élimination
def liste_arrivee_saut(depart, grille):
    liste = []
    taille = len(grille)
    # Parcours de la grille
    for ligne in range(taille):
        for colonne in range(taille):
            arrivee = conversion_chr(ligne, colonne)
            # Ajouter les déplacements possibles à la liste
            if deplacement_saut(depart, arrivee, grille):
                liste.append(arrivee)
    return liste

# Liste de déplacement avec prise par retournement
def liste_arrivee_retournement(depart, grille):
    liste = []
    taille = len(grille)
    # Parcours de la grille
    for ligne in range(taille):
        for colonne in range(taille):
            arrivee = conversion_chr(ligne, colonne)
            # Ajouter les déplacements possibles à la liste
            if deplacement_retournement(depart, arrivee, grille):
                liste.append(arrivee)
    return liste

########################################################################################################################
############      Fonctions de vérification pour IA Avancée:

# Fonction qui renvoie le nombre de risque d'élimination d'un pion
def compteur_risque(case, grille):
    liste = liste_arrivee_saut(case, grille)
    return len(liste)

# Fonction qui renvoie la liste d'un enchainement possible à partir d'une case de départ
def liste_enchainement(depart, grille):
    grille_test = np.copy(grille)
    case = depart
    liste = liste_arrivee_retournement(case, grille)
    chaine = []
    while len(liste) != 0:
        arrivee = liste[0]  #####################  A VOIR
        grille_test = maj_retournement(case, arrivee, grille_test)
        case = arrivee
        chaine.append(case)
        liste = liste_arrivee_retournement(arrivee, grille_test)
    return chaine

# Fonction qui renvoie une matrice de tous les enchainements possibles à partir d'une case départ
def matrice_enchainement(depart, grille):
    liste = liste_arrivee_retournement(depart, grille)
    grille_test = np.copy(grille)  # Copier la grille pour éviter les problèmes de pointeurs
    dep, save = depart, liste
    matrice = [[] for i in range(len(liste))]  # Creation de la matrice
    for index in range(len(liste)):  # Parcourir et remplir la matrice
        grille_test = maj_retournement(dep, liste[index], grille_test)
        matrice[index] = liste_enchainement(liste[index], grille_test)
        matrice[index].insert(0, save[index])
        dep = depart
        grille_test = np.copy(grille)
    return matrice

# Fonction qui renvoie le plus long enchainement possible
def long_chemin(depart, grille):
    matrice = matrice_enchainement(depart, grille)  # Récuperer tous les enchainements possibles
    if len(matrice) == 0:
        return matrice
    elif len(matrice) == 1:
        return matrice[0]
    else:
        taille_max, indice = 0, 0
        for index in range(len(matrice)):
            taille = len(matrice[index])
            if taille_max < taille:
                taille_max = taille
                indice = index
        return matrice[indice]

# Fonction qui renvoie les coordonnées d'un déplacement par retournement ou d'un enchainement si possible
def retournement_ia_avancee(joueur, grille):
    liste_depart = case_depart_ordi(joueur, grille)
    result = []
    dep = None # Initialisation
    # Parcours de la liste de départ
    for depart in liste_depart:
        liste = long_chemin(depart, grille)
        if len(liste) > len(result):
            result = liste
            dep = depart
    return dep, result

# Fonction qui renvoie les coordonnées de déplacement par saut si possible
def dep_saut_avancee(joueur, grille):
    liste_depart = case_depart_ordi(joueur, grille)
    dep, case = None, None # Initialisation
    # Parcours de la liste de départ
    for depart in liste_depart:
        liste_arrivee = liste_arrivee_saut(depart, grille)
        if len(liste_arrivee) != 0:
            min = compteur_risque(liste_arrivee[0], grille)
            for arrivee in liste_arrivee:
                nb_risque = compteur_risque(arrivee, grille)
                if nb_risque == 0:
                    return depart, arrivee
                elif nb_risque <= min:
                    min = nb_risque
                    case = arrivee
                    dep = depart
    return dep, case

# Fonction qui renvoie les coordonnées d'un déplacement simple si possible
def dep_simple_avancee(joueur, grille):
    liste_dep = case_depart_ordi(joueur, grille)
    dep, case = None, None # Initialisation
    # Parcours de la liste de départ
    for depart in liste_dep:
        liste_arrivee = liste_arrivee_simple(depart, grille)
        if len(liste_arrivee) != 0:
            min = compteur_risque(liste_arrivee[0], grille)
            for arrivee in liste_arrivee:
                nb_risque = compteur_risque(arrivee, grille)
                if nb_risque == 0:
                    return depart, arrivee
                elif nb_risque <= min:
                    min = nb_risque
                    case = arrivee
                    dep = depart
    return dep, case

# Fonction qui permet de choisir le meilleur déplacement selon les priorités
def choix_deplacement_ordi(joueur, grille):
    dep1, chemin = retournement_ia_avancee(joueur, grille)
    dep2, arrivee1 = dep_saut_avancee(joueur, grille)
    # Si possible de faire un déplacement par retournement
    if len(chemin) != 0:
        return 0
    # Si possible de faire un déplacement par élimination
    elif arrivee1 != None:
        return 1
    # Sinon déplacement simple
    else:
        return 2

########################################################################################################################
############      Fonctions de jeu:

# Fonction de partie : joueur contre joueur
def jeu_joueur():
    grille = choisir_grille()
    afficher_grille(grille)
    joueur = type_joueur()
    quitter = False
    while not est_fin_de_partie(grille) and not quitter:
        depart, arrivee = saisir_coordonnees(grille, joueur)
        if deplacement_retournement(depart, arrivee, grille):
            grille = maj_grille(depart, arrivee, joueur, grille)
            afficher_grille(grille)
            enchainement(arrivee, grille)
        else:
            grille = maj_grille(depart, arrivee, joueur, grille)
            afficher_grille(grille)
        joueur = inverser_joueur(joueur)

        if est_fin_de_partie(grille):
            print("\nBRAVO ! Le joueur ", inverser_joueur(joueur), " a gagné !\nLe joueur ", joueur, " a perdu !\n")
        else:
            quitter = abandon()
            if not quitter:
                print("\nJoueur ", joueur, " Jouez !\n")
            else:
                print("\nLe joueur ", inverser_joueur(joueur), " a abondonné la partie !\nLe joueur", joueur,
                      " Remporte la partie !\n")

# Fonction de partie : joueur contre IA Naïve
def ia_naive():
    grille = choisir_grille()
    afficher_grille(grille)
    joueur = type_joueur()
    ordi = inverser_joueur(joueur)
    quitter = False
    while not est_fin_de_partie(grille) and not quitter:
        if joueur == ordi:
            deplacement = random.randint(0, 2)
            liste_depart = case_depart_ordi(joueur, grille)
            index = random.randint(0, len(liste_depart) - 1)
            depart = liste_depart[index]
            # Déplacement Simple
            if deplacement == 0:
                liste = liste_arrivee_simple(depart, grille)
                while liste == []:
                    index = random.randint(0, len(liste_depart) - 1)
                    depart = liste_depart[index]
                    liste = liste_arrivee_simple(depart, grille)
                index = random.randint(0, len(liste) - 1)
                arrivee = liste[index]
                grille = maj_grille(depart, arrivee, joueur, grille)
                print("L'ordinateur a éffectué un déplacement simple !\nDe la case ", depart, " à ", arrivee, '\n')
            # Deplacement avec prise par elimination
            elif deplacement == 1:
                liste = liste_arrivee_saut(depart, grille)
                while liste == []:
                    index = random.randint(0, len(liste_depart) - 1)
                    depart = liste_depart[index]
                    liste = liste_arrivee_saut(depart, grille)
                index = random.randint(0, len(liste) - 1)
                arrivee = liste[index]
                grille = maj_grille(depart, arrivee, joueur, grille)
                print("L'ordinateur a éffectué un déplacement avec prise par élimination !\nDe la case ", depart, " à ",
                      arrivee, '\n')
            # Deplacement avec prise par retournement
            else:
                liste = liste_arrivee_retournement(depart, grille)
                while liste == []:
                    index = random.randint(0, len(liste_depart) - 1)
                    depart = liste_depart[index]
                    liste = liste_arrivee_retournement(depart, grille)
                index = random.randint(0, len(liste) - 1)
                arrivee = liste[index]
                grille = maj_grille(depart, arrivee, joueur, grille)
                print("L'ordinateur a éffectué un déplacement avec prise par retournement !\nDe la case ", depart,
                      " à ", arrivee, '\n')

            afficher_grille(grille)
            joueur = inverser_joueur(joueur)
            if est_fin_de_partie(grille):
                print("BRAVO ! Le joueur ", inverser_joueur(joueur), " a gagné !\nLe joueur ", joueur, " a perdu !\n")
            else:
                print("\nJoueur ", joueur, " Jouez !\n")
        else:
            depart, arrivee = saisir_coordonnees(grille, joueur)
            if deplacement_retournement(depart, arrivee, grille):
                grille = maj_grille(depart, arrivee, joueur, grille)
                afficher_grille(grille)
                enchainement(arrivee, grille)
            else:
                grille = maj_grille(depart, arrivee, joueur, grille)
                afficher_grille(grille)
            joueur = inverser_joueur(joueur)
            if est_fin_de_partie(grille):
                print("\nBRAVO ! Le joueur ", inverser_joueur(joueur), " a gagné !\nLe joueur ", joueur, " a perdu !\n")
            else:
                quitter = abandon()
                if not quitter:
                    print("\nJoueur ", joueur, " Jouez !\n")
                else:
                    print("\nLe joueur ", inverser_joueur(joueur), " a abondonné la partie !\nLe joueur", joueur,
                          " Remporte la partie !\n")

# Fonction de partie : joueur contre IA Avancee
def ia_avancee():
    grille = choisir_grille()
    afficher_grille(grille)
    joueur = type_joueur()
    ordi = inverser_joueur(joueur)
    quitter = False
    while not est_fin_de_partie(grille) and not quitter:
        if joueur == ordi:
            d = choix_deplacement_ordi(joueur, grille)
            # Déplacement Simple
            if d == 2:
                depart, arrivee = dep_simple_avancee(joueur, grille)
                grille = maj_grille(depart, arrivee, joueur, grille)
                print("L'ordinateur a éffectué un déplacement simple !")
                print("De la case ", depart, " à ", arrivee, '\n')
            # Deplacement avec prise par elimination
            elif d == 1:
                depart, arrivee = dep_saut_avancee(joueur, grille)
                grille = maj_grille(depart, arrivee, joueur, grille)
                print("L'ordinateur a éffectué un déplacement avec prise par élimination !")
                print("De la case ", depart, " à ", arrivee, '\n')
            # Deplacement avec prise par retournement
            else:
                depart, chemin = retournement_ia_avancee(joueur, grille)
                if len(chemin) == 1:
                    arrivee = chemin[0]
                    grille = maj_retournement(depart, arrivee, grille)
                    print("L'ordinateur a effectué un déplacement par retournement !\nDe la case ", depart, " à ",
                          arrivee, '\n')
                else:
                    print("L'ordinateur a effectué un enchainement de plusieurs déplacements !\n")
                    for arrivee in chemin:
                        grille = maj_retournement(depart, arrivee, grille)
                        print("De la case ", depart, " à ", arrivee, '\n')
                        depart = arrivee

            afficher_grille(grille)
            joueur = inverser_joueur(joueur)
            if est_fin_de_partie(grille):
                print("BRAVO ! Le joueur ", inverser_joueur(joueur), " a gagné !\nLe joueur ", joueur, " a perdu !\n")
            else:
                print("\nJoueur ", joueur, " Jouez !\n")
        else:
            depart, arrivee = saisir_coordonnees(grille, joueur)
            if deplacement_retournement(depart, arrivee, grille):
                grille = maj_grille(depart, arrivee, joueur, grille)
                afficher_grille(grille)
                enchainement(arrivee, grille)
            else:
                grille = maj_grille(depart, arrivee, joueur, grille)
                afficher_grille(grille)
            joueur = inverser_joueur(joueur)
            if est_fin_de_partie(grille):
                print("\nBRAVO ! Le joueur ", inverser_joueur(joueur), " a gagné !\nLe joueur ", joueur, " a perdu !\n")
            else:
                quitter = abandon()
                if not quitter:
                    print("\nJoueur ", joueur, " Jouez !\n")
                else:
                    print("\nLe joueur ", inverser_joueur(joueur), " a abondonné la partie !\nLe joueur", joueur,
                          " Remporte la partie !\n")

########################################################################################################################
############      Fonctions De Tests Unitaires:
def test_inverser_joueur():
    assert inverser_joueur('x') == 'o', "Erreur Joueur"
    assert inverser_joueur('o') == 'x', "Erreur Joueur"

def test_conversion_ligne():
    assert conversion_ligne('A') == 0, "Erreur de ligne"
    assert conversion_ligne('G') == 6, "Erreur de ligne"

def test_conversion_chr():
    assert conversion_chr(0, 4) == 'A5', "Erreur de coordonnées"
    assert conversion_chr(3, 1) == 'D2', "Erreur de coordonnées"

def test_est_au_bon_format():
    assert est_au_bon_format('A2'), "Bon Format"
    assert est_au_bon_format('Z9'), "Bon Format"
    assert not est_au_bon_format('22'), "Erreur du premier caractère"
    assert not est_au_bon_format('AZ'), "Erreur du second caractère"

def test_est_dans_grille():
    grille = creer_grille(7)  # Grille De 7x7
    assert est_dans_grille('A', '3', grille), "Coordonnées Correctes"
    assert est_dans_grille('G', '7', grille), "Coordonnées Correctes"
    assert not est_dans_grille('H', '1', grille), "Erreur de ligne"
    assert not est_dans_grille('B', '9', grille), "Erreur de colonne"

def test_est_fin_de_partie():
    grille_debut = creer_grille(7)
    grille_milieu = creer_grille_milieu()
    grille_fin = creer_grille_finie()
    assert not est_fin_de_partie(grille_debut), "Erreur de grille debut"
    assert not est_fin_de_partie(grille_milieu), "Erreur de grille milieu"
    assert est_fin_de_partie(grille_fin), "Erreur Grille de fin de partie"

def test_case_depart():
    grille = creer_grille(7)
    assert case_depart('B', '7', grille, 'o'), "Déplacement correct "
    assert case_depart('F', '3', grille, 'x'), " Déplacement correct "
    assert not case_depart('D', '1', grille, 'o'), "Erreur case vide"
    assert not case_depart('B', '1', grille, 'x'), "Erreur de joueur 'x' "

def test_deplacement_simple():
    grille = creer_grille(7)
    assert deplacement_simple('B1', 'E1', grille), " Déplacement simple vertical"
    assert deplacement_simple('F4', 'E4', grille), " Déplacement simple diagonal"
    assert not deplacement_simple('B4', 'B4', grille), " Erreur même case"
    assert not deplacement_simple('A6', 'C6', grille), " Déplacement case bloquée"
    assert not deplacement_simple('F4', 'F7', grille), " Erreur de case d'arrivée"

def test_deplacement_saut():
    grille = creer_grille(7)
    assert deplacement_saut('B3', 'F3', grille), " Déplacement vertical"
    assert deplacement_saut('F1', 'B5', grille), " Déplacement diagonal"
    assert not deplacement_saut('F7', 'F7', grille), " Erreur même case"
    assert not deplacement_saut('B4', 'B6', grille), " Case adjacente"
    assert not deplacement_saut('A7', 'G7', grille), " Déplacement impossible"

def test_deplacement_retournement():
    grille = creer_grille_milieu()
    assert deplacement_retournement('F4', 'F6', grille), " Déplacement horizontal"
    assert deplacement_retournement('G5', 'E5', grille), " Déplacement vertical"
    assert deplacement_retournement('G4', 'E6', grille), "Déplacement diagonal"
    assert not deplacement_retournement('G3', 'G5', grille), " Erreur d'adversaire"
    assert not deplacement_retournement('B4', 'E4', grille), " Erreur de case d'arrivée"

def test_direction():
    assert direction('A1', 'G7'), "Erreur Diagonale"
    assert direction('C3', 'D3'), "Erreur de la ligne verticale"
    assert direction('E1', 'E7'), "Erreur de la ligne horizontale"
    assert not direction('A1', 'B7'), "Erreur de direction"
    assert not direction('G3', 'E2'), "Erreur de direction"

def test_vide_entre_case():
    grille = creer_grille(7)
    assert vide_entre_case('B1', 'F1', grille), "Cases séparées"
    assert not vide_entre_case('B3', 'B5', grille), "Erreur de case"
    assert not vide_entre_case('F1', 'F2', grille), " Erreur cases adjacentes"

def test_case_depart_ordi():
    grille = creer_grille(7)
    assert case_depart_ordi('o', grille) == ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'B1', 'B2', 'B3', 'B4', 'B5',
                                             'B6', 'B7'], "Liste des cases du joueur 'o' "
    assert case_depart_ordi('x', grille) == ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'G1', 'G2', 'G3', 'G4', 'G5',
                                             'G6', 'G7'], " Liste des cases du joueur 'x' "

def test_liste_arrivee_simple():
    grille = creer_grille_milieu()
    assert liste_arrivee_simple('G4', grille) == [], "Erreur Case bloquée"
    assert liste_arrivee_simple('A4', grille) == ['A5'], "Un seul déplacement possible"
    assert liste_arrivee_simple('B3', grille) == ['A2', 'B1', 'B2', 'C3', 'D3', 'E3'], "Liste de déplacements possibles"

def test_liste_arrivee_saut():
    grille = creer_grille_milieu()
    assert liste_arrivee_saut('A3', grille) == [], "Erreur case bloquée"
    assert liste_arrivee_saut('B3', grille) == ['F3'], "Un seul déplacement possible"
    assert liste_arrivee_saut('F7', grille) == ['A7', 'D5', 'F5'], " liste de déplacements possibles"

def test_liste_arrivee_retournement():
    grille = creer_grille_milieu()
    assert liste_arrivee_retournement('A3', grille) == [], "Retournement impossible"
    assert liste_arrivee_retournement('A7', grille) == ['G7'], "Un seul retournement possible"
    assert liste_arrivee_retournement('B4', grille) == ['B6', 'D4'], "Liste de retournements possibles"

def test_compteur_risque():
    grille = creer_grille(7)
    grille_milieu = creer_grille_milieu()
    assert compteur_risque('A1', grille) == 0, "Case bloquée 0 risque"
    assert compteur_risque('B2', grille) == 2, "Case éxposée à 2 adversaires"
    assert compteur_risque('D5', grille_milieu) == 3, "Case éxposée à 3 adversaires"

def test_liste_enchainement():
    grille = creer_grille_milieu()
    assert liste_enchainement('A3', grille) == [], "Aucun déplacement possible"
    assert liste_enchainement('F4', grille) == ['F6'], "Un seul retournement possible"
    assert liste_enchainement('G5', grille) == ['E5', 'C5'], "2 enchainements possibles"
    assert liste_enchainement('C1', grille) == ['C3', 'C5', 'A5'], " 3 enchainements possibles"

def test_matrice_enchainement():
    grille = creer_grille_milieu()
    assert matrice_enchainement('A3', grille) == [], "Aucun enchainement possible"
    assert matrice_enchainement('F4', grille) == [['F6']], "Un seul retournement possible"
    assert matrice_enchainement('B4', grille) == [['B6'], ['D4']], "2 déplacements par retournement possibles"

def test_long_chemin():
    grille = creer_grille_milieu()
    assert long_chemin('A3', grille) == [], "Aucun chemin possible"
    assert long_chemin('C1', grille) == ['C3', 'C5', 'A5'], "Le plus long enchainement"

def test_retournement_ia_avancee():
    grille_debut = creer_grille(7)
    grille_milieu = creer_grille_milieu()
    assert retournement_ia_avancee('o', grille_debut) == (None, []), "Retournement impossible"
    assert retournement_ia_avancee('o', grille_milieu) == (
    'C1', ['C3', 'C5', 'A5']), "Le meilleur enchainement possible pour le pion 'o' "
    assert retournement_ia_avancee('x', grille_milieu) == (
    'G5', ['E5', 'C5']), "Le meilleur enchainement possible pour le pion 'x' "

def test_dep_saut_avancee():
    grille_milieu = creer_grille_milieu()
    assert dep_saut_avancee('o', grille_milieu) == (
    'F5', 'C2'), "Coordonnées du meilleur déplacement par saut pour le pion 'o' "
    assert dep_saut_avancee('x', grille_milieu) == (
    'G6', 'A6'), "Coordonnées du meilleur déplacement par saut pour le pion 'x' "

def test_dep_simple_avancee():
    grille_milieu = creer_grille_milieu()
    assert dep_simple_avancee('x', grille_milieu) == (
    'B5', 'A5'), "Coordonnées du meilleur déplacement simple pour le pion 'x' "
    assert dep_simple_avancee('o', grille_milieu) == (
    'A3', 'A1'), "Coordonnées du meilleur déplacement simple pour le pion 'o' "

# Fonction générale de tests
def fonction_general_tests():
    print("Appel aux fonctions de Test :")
    test_inverser_joueur()
    test_conversion_ligne()
    test_conversion_chr()
    test_est_au_bon_format()
    test_est_dans_grille()
    test_est_fin_de_partie()
    test_case_depart()
    test_deplacement_simple()
    test_deplacement_saut()
    test_deplacement_retournement()
    test_direction()
    test_vide_entre_case()
    test_case_depart_ordi()
    test_liste_arrivee_simple()
    test_liste_arrivee_saut()
    test_liste_arrivee_retournement()
    test_compteur_risque()
    test_liste_enchainement()
    test_matrice_enchainement()
    test_long_chemin()
    test_retournement_ia_avancee()
    test_dep_saut_avancee()
    test_dep_simple_avancee()
    print("Ok pour tous les tests !")

########################################################################################################################
### Programme Principal

jeu()