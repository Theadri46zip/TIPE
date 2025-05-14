"""toolkit pour représentation graphique des tresses"""
from typing import Literal
import matplotlib.pyplot as plt
import logging
import matplotlib.colors as mcolors

# Création de types pour les tresses, représentation d'Artin
Sig=Literal[1,-1]
Noeud=tuple[int,Literal[1,-1]]
Tresse=list[Noeud]

EXEMPLE_1: Tresse = [
    (1,-1),
    (2,1),
    (1,1),
    (2,1)]

def differentes_couleurs(n):
    """Génère n couleurs distinctes en utilisant l'espace HSV/TSV.
    Les teintes sont réparties uniformément, avec saturation et valeur élevées.
    Retourne une liste de triplets RGB."""
    tsv_couleurs = []
    for i in range(n):
        teinte = i / n           #teinte
        saturation = 0.9      #saturation
        valeur = 0.9           #valeur (luminosité)
        tsv_couleurs.append((teinte, saturation, valeur))
    return [mcolors.hsv_to_rgb(tsv) for tsv in tsv_couleurs]

def decomposition(T):
    """Décompose une liste de tuples (a, b) en deux listes distinctes : [a1, a2, ...], [b1, b2, ...]
    Équivaut à la fonction zip(*L)"""
    return [a for a, _ in T], [b for _, b in T]

def index(L, val):
    """Renvoie l'indice de la première occurrence de val dans la liste L.
    Équivaut à L.index(val)"""
    for i in range(len(L)):
        if L[i] == val:
            return i

def tresses_trois_brins(L):
    """Représente une tresse à 3 brins
     L : liste de tuples (i, s)
        i : 1 ou 2 => croisement entre brins i et i+1
        s : signature => -1 le brin i passe au dessus de i+1 et inversement"""
    nb_brins = 3                                                               #nombre de brins
    couleurs = ['red', 'green', 'blue']                                        #couleur des brins
    ordre_brins = [0, 1, 2]                                                  #ordre initial des brins
    ordres_par_etape = [ordre_brins.copy()]                                 #on copie la liste des ordres des brins 
    trajectoires = [[(pos, 0, False)] for pos in range(nb_brins)]              # Trajectoires : liste de tuples (x, y, est_croisement)
    y = 0                                                                      # initialise la hauteur à 0
    if L==[]:
        for pos, brin in enumerate(ordre_brins):                           #parcourt les brins avec leur position initiale 
            trajectoires[brin].append((pos, 1, False))                        #ajoute point final pour faire une ligne verticale
        y = 1
    else:
        for i, (croisement, _) in enumerate(L):                                #parcourt les croisements dans L, i est l'indice de l'étape et ignore la signature.
                                                                               
            n_ordre = ordre_brins.copy()                                       #copie ordre des brins
            n_ordre[croisement - 1], n_ordre[croisement] = n_ordre[croisement], n_ordre[croisement - 1] #echange l'ordre brins
            for pos, brin in enumerate(ordre_brins):                           #parcourt l'ordre des brins avant le croisement 
                n_pos = index(n_ordre, brin)                                   #trouve la nouvelle postition après le croisement
                # Marquer le segment suivant comme un croisement
                trajectoires[brin][-1] = (trajectoires[brin][-1][0], trajectoires[brin][-1][1], True) #met à jour la trajectoire du dernier brin pour indiquer le croisement et marquer le segment suivant comme un croisement                
                trajectoires[brin].append((n_pos, y + 1, False))               #ajout du brin après croisement 
            ordre_brins = n_ordre                                              #mise a jour de l'ordre                
            ordres_par_etape.append(ordre_brins.copy())                        #on ajoute l'ordre des brins 
            y += 1                                                             #passage au niveau suivant 
        for pos, brin in enumerate(ordre_brins):                               #parcourt l'ordre final des brins
            trajectoires[brin].append((pos, y, False))                         #ajoute les derniers points

    fig, t = plt.subplots(figsize=(5, y), facecolor='white')                  #créer la figure 

    for brin in range(nb_brins):                                               #parcourt chaque brin
        points = trajectoires[brin]                                            #récupère la liste des points
        xp, yp = decomposition([(x, y) for x, y, _ in points])                 #décompose la liste en 2 listes x et y
        for j in range(len(xp) - 1):                                           #parcourt les segments
            x0, x1 = xp[j], xp[j+1]                                            #récupère 2 points x d'un segment                                    
            y0, y1 = yp[j], yp[j+1]                                            #récupère 2 points y d'un segment
            couleur = couleurs[brin]                                           

            est_croisement = points[j][2]                                      # Troisième élément du tuple (est_croisement)
            if est_croisement:                                                 # test s'il y a croisement
                i, s = L[y0]                                                   #récupère le tuple 
                ordre = ordres_par_etape[y0]                                   #récupère son ordre
                brin_g = ordre[i - 1]                                          #indice du brin à gauche        
                brin_d = ordre[i]                                              #indice du brin à droite  
                brin_dessous = brin_g if s == 1 else brin_d                    #détermine lequel passe en dessous

                if brin == brin_dessous:                                       #vérification si le brin passe en dessous
                    frac = 0.10                                                #fraction du segment à blanchir (10%)
                    d_x = x1 - x0                                               #différence entre les 2 points x    
                    d_y = y1 - y0                                               #différence entre les 2 points y
                    x_a = x0 + d_x * (0.5 - frac)          #coordonnée avant le trou : la coordonnée initiale + (50-10%) de la longeur du segment
                    y_a = y0 + d_y * (0.5 - frac)          #même chose pour y 
                    x_b = x0 + d_x * (0.5 + frac)          #coordonnée après le trou
                    y_b = y0 + d_y * (0.5 + frac)          #même chose pour y
                    t.plot([x0, x_a], [y0, y_a], color=couleur, linewidth=2)   #trace la partie du segment avant le trou
                    t.plot([x_b, x1], [y_b, y1], color=couleur, linewidth=2,)   #trace la partie du segment après le trou
                else:
                  t.plot([x0, x1], [y0, y1], color=couleur, linewidth=2)      #on trace le segment entier si ce n'est pas un croisement 

    sigma_labels = [fr'$\sigma_{{{i}}}^{{{s}}}$' for i, s in L]                    #écriture des sigma en label
    for label in sigma_labels:
        t.plot([], [], label=label)                                               #création de label sans les axes

    t.legend(loc='center left', bbox_to_anchor=(0, 0.5), fontsize=14,              #ajout de la légende
              frameon=False, handlelength=0, handletextpad=0, labelspacing=2.3)
    t.set_xlim(-0.5, 2.5)
    t.set_ylim(y, 0)                                                       #inverse l'axe y pour avoir une tresse vers le bas
    for pos, brin in enumerate([1,2,3]):
        t.text(pos, -0.2, str(brin), ha='center', va='bottom', fontsize=12)
    t.axis('off')
    t.text(1, -0.9, "Tresse à 3 brins", ha='center', va='top', fontsize=14)   #positionnement du titre
    plt.show()

def tresses_n_brins(L, n):
    """Représente une tresse à n brins en couleur RGB aléatoire.
    L : liste de tuples (i, s)
        i : entre 1 et n-1 => croisement entre brins i et i+1
        s : signature => -1 si le brin i passe au-dessus de i+1, +1 sinon
    n : nombre de brins (entier positif)"""
    nb_brins = n
    ordre_brins = list(range(nb_brins))  # [0, 1, ..., n-1]
    ordres_par_etape = [ordre_brins.copy()]
    trajectoires = [[(pos, 0, False)] for pos in range(nb_brins)]
    couleurs=differentes_couleurs(nb_brins)
    y = 0
    if L == []:
        for pos, brin in enumerate(ordre_brins):
            trajectoires[brin].append((pos, 1, False))
        y = 1
    else:
        for i, (croisement, _) in enumerate(L):
            n_ordre = ordre_brins.copy()
            n_ordre[croisement - 1], n_ordre[croisement] = n_ordre[croisement], n_ordre[croisement - 1]
            for pos, brin in enumerate(ordre_brins):
                n_pos = index(n_ordre, brin)
                trajectoires[brin][-1] = (trajectoires[brin][-1][0], trajectoires[brin][-1][1], True)
                trajectoires[brin].append((n_pos, y + 1, False))
            ordre_brins = n_ordre
            ordres_par_etape.append(ordre_brins.copy())
            y += 1
        for pos, brin in enumerate(ordre_brins):
            trajectoires[brin].append((pos, y, False))

    fig, t = plt.subplots(figsize=(max(5, n), y), facecolor='white')

    for brin in range(nb_brins):
        points = trajectoires[brin]
        x_p, y_p = decomposition([(x, y) for x, y, _ in points])
        for j in range(len(x_p) - 1):
            x0, x1 = x_p[j], x_p[j+1]
            y0, y1 = y_p[j], y_p[j+1]
            est_croisement = points[j][2]
            if est_croisement:
                i, s = L[y0]
                ordre = ordres_par_etape[y0]
                brin_g = ordre[i - 1]
                brin_d = ordre[i]
                brin_dessous = brin_g if s == 1 else brin_d

                if brin == brin_dessous:
                    frac = 0.10
                    d_x = x1 - x0
                    d_y = y1 - y0
                    x_a = x0 + d_x * (0.5 - frac)
                    y_a = y0 + d_y * (0.5 - frac)
                    x_b = x0 + d_x * (0.5 + frac)
                    y_b = y0 + d_y * (0.5 + frac)
                    t.plot([x0, x_a], [y0, y_a], color=couleurs[brin], linewidth=2, zorder=1)
                    t.plot([x_b, x1], [y_b, y1], color=couleurs[brin], linewidth=2, zorder=1)
                else:
                    t.plot([x0, x1], [y0, y1],color=couleurs[brin], linewidth=2, zorder=2)
            else:
                t.plot([x0, x1], [y0, y1], color=couleurs[brin],linewidth=2, zorder=2)

    sigma_labels = [fr'$\sigma_{{{i}}}^{{{s}}}$' for i, s in L]
    for label in sigma_labels:
        t.plot([], [], label=label)

    t.legend(loc='center left', bbox_to_anchor=(-0.02, 0.47), fontsize=14,
              frameon=False, handlelength=0, handletextpad=0, labelspacing=2)
    t.set_xlim(-0.5, n-0.5)
    t.set_ylim(y, -0.8)

    # Ajouter les numéros 1 à n au pied de chaque brin (en haut du graphique, y=0) avec l'ordre final
    for pos, brin in enumerate(range(n)):
        t.text(pos, -0.4, str(brin + 1), ha='center', va='bottom', fontsize=12)

    t.text((n-1)/2, -1.4, f"Tresse à {n} brins", ha='center', va='top', fontsize=14)   # Placer le titre manuellement plus haut
    t.axis('off')
    plt.show()




