"""Toolkit matriciel pour codage de tresses."""
from copy import deepcopy
import logging
from typing import Literal

FORMAT = '%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# Création de types pour les tresses, représentation d'Artin

Sig=Literal[1,-1]
Noeud=tuple[int,Literal[1,-1]]
Tresse=list[Noeud]


# sigma1-1, sigma2, sigma1, sigma2
EXEMPLE_1: Tresse = [
    (1,-1),
    (2,1),
    (1,1),
    (2,1)
]
# sigma2, sigma1, sigma1, sigma2-1, sigma1, sigma1-1
EXEMPLE_2: Tresse = [
    (2,1),
    (1,1),
    (1,1),
    (2,-1),
    (1,1),
    (1,-1)
]

def nbr_brins(t: Tresse) -> int:
    """Nombre de brins utiles de la tresse"""
    return max(list(t[i][0] for i in range(len(t)))) + 1


def matcar_zero(n:int)->list[list]:
    """Initialise une matrice carrée avec des zéros."""
    return [[0 for i in range(n)] for i in range(n)]


def print_mat(m:list[list])->None:
    """Affichage d'une liste de liste en mode matrice."""
    if m==[]:
        return
    for ligne in m:
        print(ligne)
    return


def ajout2mat(m1:list[list], m2:list[list])->list[list]:
    """Ajoute 2 matrices."""
    if len(m1)!= len(m2) or len(m1[0])!= len(m2[0]):
        raise ValueError("matrices de tailles différentes")
    n=len(m1)
    return [[ m1[i][j]+m2[i][j] for j in range(n)] for i in range(n)]


def mot2mat(t:Tresse)->None:
    """Passage d'un mot à une série de matrices.
    ne marche que si il y a 3 brins ou plus.
    """
    n=nbr_brins(t)
    m0=matcar_zero(n)   #Etat 0 matrice nulle
    l_mat=[m0]           # On ajoute le matrice 0 a la liste des matrices
    nb_etat_courant=0
    #la liste des noeuds dans l'ordre de priorité gauche -> droite
    l_etats=[
        list(i for i in range(1,n+1))
    ]
    for i in range(len(t)):
        l_etat_now=deepcopy(l_etats[nb_etat_courant])
        m1 = matcar_zero(n)
        #l'élément d'indice nb_etat_courant nous renseigne sur les modifs a faire
        t_et = t[nb_etat_courant]
        j=t_et[0]         # C'est l'indice du brin qui monte en passant en dessous du prochain
        j1=l_etat_now[j-1]-1
        j2=l_etat_now[j]-1
        m1[j1][j1]=1
        m1[j2][j2]=-1
        l_etat_now[j],l_etat_now[j-1]=l_etat_now[j-1],l_etat_now[j]
        l_etats.append(l_etat_now)
        if t_et[1] ==1:
            m1[j1][j2]=1
            m1[j2][j1]=-1
        else:
            m1[j1][j2]=-1
            m1[j2][j1]=1
        l_mat.append(m1)
        nb_etat_courant+=1
    mf=matcar_zero(n)
    for _, value in enumerate(l_mat):
        mf=ajout2mat(mf, value)

    for i, value in enumerate(l_mat):
        print("état",i)
        print_mat(value)
        print("ordre :")
        print(l_etats[i])
        print(" ")
    print("état final :")
    print_mat(mf)

#3 propriétés :
#- [ i,1] suivi de [i,-1] se simplifie en l'inaction
#- [i,1] suivi de [j,1] vaut [j,1] suivi de [i,1] si en valeur abs i-j >=2
#- [i,1] [j,1] [i,1] vaut [j,1] [i,1] [j,1] si en valeur abs i-j =1

def est_poignee(t:Tresse)->bool:
    """
    renvoie la valeur de l'assertion (t est une poignee)
    """
    prefixe=t[0]
    inverse=(t[0][0],-t[0][1])
    if prefixe in t[1:-1] or inverse in t[1:-1]:
        return False
    return t[-1]==inverse

def est_poignee_cor(t:Tresse)->bool:
    """
    valeur de l'assertion (t est une poignee correcte)
    """
    if len(t)<2:
        return False
    prefixe = t[0]
    suffixe = t[1]
    bool_inverse = prefixe[0] == suffixe[0] and prefixe[1] == - suffixe[1]
    return len(t) == 2 and bool_inverse

def extract2poignee(t:Tresse,g:Noeud)->Tresse:
    """
    renvoie la premiere poignee extraite de t ayant comme prefixe g
    """
    inverse=(g[0],-g[1])
    if g not in t or inverse not in t:
        return t
    l=[g]
    place = t.index(g)+1
    if inverse not in t[place:]:
        return t
    for noeud in t[place:]:
        if noeud != g and inverse not in l and inverse in t[place:]:
            l.append(noeud)
            place+=1
    return l

def num_generateurs(t:Tresse,g:Noeud)->int:
    """
    renvoie le nombre de générateurs g et inverses g**-1 dans t
    """
    compteur=0
    inverse=(g[0],-g[1])
    for sigma in t:
        if sigma in (g ,inverse):
            compteur+=1
    return compteur

def reduction_poignee(t:Tresse)->Tresse:
    """
    Si c'est une poignee alors on la réduit
    on commence par enlever ses extremités puis on remplace si besoin le reste des generateurs par
    leur forme réduite
    """
    if est_poignee(t):
        prefix = t[0]
        sig_prefix = prefix[1]
        ind_prefix = prefix[0] # m dans le livre
        l = t[1:-1]
        t2 = []
        for (ind, sig) in l:
            if ind != ind_prefix+1:
                t2.append((ind, sig))
            elif ind == ind_prefix+1:
                t2.append((ind, -sig_prefix))
                t2.append((ind_prefix, sig))
                t2.append((ind, sig_prefix))
            else:
                t2.append((ind, sig))
        return t2
    return t

def position_extraite(liste:Tresse, ext:Tresse)->int:
    """
    renvoie la position (du début) d'une liste extraite dans la liste d'origine
    """

    for i in range(len(liste) - len(ext) + 1):
        if liste[i:i+len(ext)] == ext:
            return i
    return 0

def reduction_simple(t:Tresse)->Tresse:
    """
    on simplifie les voisins [i,sig] [i,-sig]
    """
    if len(t)<=2:
        if est_poignee_cor(t):
            return []
        return t
    t2=[]
    longueur=len(t)
    i=0
    while i<=longueur -2:
        if t[i][0] != t[i+1][0] or t[i][1] != -t[i+1][1]:
            t2.append(t[i])
        else:
            i+=1
        i+=1
    if t[longueur-2][0] != t[longueur-1][0] or t[longueur-2][1] != -t[longueur-1][1]:
        t2.append(t[longueur-1])
    return t2

def boucle_redsimp(t:Tresse)->Tresse:
    """
    on effectue la réduction simple tant qu'on le peut
    """
    t2=deepcopy(t)
    while reduction_simple(t2)!=t2:
        t2=reduction_simple(t2)
    return t2

def double_simplification(t:Tresse)->Tresse:
    """
    on effectue boucle simple puis on va chercher une poignee a réduire
    """
    t2 = boucle_redsimp(t)
    if t2==[]:
        return []
    if est_poignee(t2):
        t2 = reduction_poignee(t2)
    else:
        indice = 0
        while (poignee:=extract2poignee(t2, t2[indice])) == t2:
            indice += 1
        debut = position_extraite(t2, poignee)
        fin = debut + len(poignee)
        t2 = t2[:debut] + reduction_poignee(poignee) + t2[fin:]
    t2 = boucle_redsimp(t2)
    return t2

def simplifiable(t:Tresse)-> bool:
    """
    valeur de l'assertion (t est simplifiable ou du moins modifiable)
    """
    if len(t)<=1:
        return False
    n= nbr_brins(t)
    for i in range(n):
        positif=(i,1)
        negatif=(i,-1)
        if positif in t and negatif in t:
            return True
    return False

def boucle_2simp(t:Tresse)->Tresse:
    """
    on effectue la réduction double tant qu'on le peut
    """
    t2=deepcopy(t)
    while simplifiable(t2):
        t2=double_simplification(t2)
    return t2

def inverse(t:Tresse) -> Tresse:
    t2=deepcopy(t)
    t2.reverse()
    t3=[]
    n=len(t2)
    for i in range(n):
        t3.append((t2[i][0],-1*t2[i][1]))
    return t3

def addition(t1:Tresse,t2:Tresse)->Tresse:
    return t1+t2