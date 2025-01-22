"""Toolkit matriciel pour codage de tresses."""
from copy import deepcopy

# sigma1-1, sigma2, sigma1, sigma2
EXEMPLE_1: list[list] = [
    [1,-1],
    [2,1],
    [1,1],
    [2,1]
]
# sigma2, sigma1, sigma1, sigma2-1, sigma1, sigma1-1
EXEMPLE_2: list[list] = [
    [2,1],
    [1,1],
    [1,1],
    [2,-1],
    [1,1],
    [1,-1]
]

def nbr_brins(t: list[list]) -> int:
    """Nombre de brins utiles de la tresse"""
    return max(list(t[i][0] for i in range(len(t)))) + 1


def matcar_zero(n):
    """Initialise une matrice carrée avec des zéros."""
    return [[0 for i in range(n)] for i in range(n)]


def print_mat(m):
    """Affichage d'une liste de liste en mode matrice."""
    if m==[]:
        print(" ")
    else:
        for _, line in enumerate(m):
            print(line)


def ajout2mat(m1, m2):
    """Ajoute 2 matrices."""
    if len(m1)!= len(m2):
        return "matrices de tailles différentes"
    n=len(m1)
    return [[ m1[i][j]+m2[i][j] for j in range(n)] for i in range(n)]


def mot2mat(t):
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

def est_poignee(t):
    """
    renvoie la valeur de l'assertion (t est une poignee)
    """
    prefixe=t[0]
    inverse=[t[0][0],-t[0][1]]
    if prefixe in t[1:-1] or inverse in t[1:-1]:
        return False
    return t[-1]==inverse

def est_poignee_cor(t):
    prefixe = t[0]
    suffixe = t[1]
    bool_inverse = prefixe[0] == suffixe[0] and prefixe[1] == - suffixe[1]
    return len(t) == 2 and bool_inverse
            
def extract2poignee(t,g):
    """
    renvoie la premiere poignee extraite de t ayant comme prefixe g
    """
    inverse=[g[0],-g[1]]
    if g not in t or inverse not in t:
        return t
    else:
        l=[g]
        place = t.index(g)+1
        if inverse not in t[(place):]:
            return t
        else:
            for noeud in t[(place):]:
                if noeud != g and inverse not in l and inverse in t[place:]:
                    l.append(noeud)
                    place+=1
            return l

def reduction_poignee(t):
    """
    renvoie la tresse sans ses extremités si c'est une poignée
    """
    if est_poignee(t):
        return t[1:-1]
    return t

def position_extraite(liste, ext):
    """
    renvoie la position (du début) d'une liste extraite dans la liste d'origine
    """

    for i in range(len(liste) - len(ext) + 1):
        if liste[i:i+len(ext)] == ext:
            return i
    raise TypeError("ext n'est pas dans la liste")


def simplification(t):
    l=deepcopy(t)
    prefixe=t[0]
    poignee = extract2poignee(t,prefixe)
    if  poignee != t:     #On peut donc extraire une poignee
        poignee_index_deb= position_extraite(t,poignee)
        longueur_poignee=len(poignee)
        poignee_index_fin= poignee_index_deb + longueur_poignee -1
        l=l[:(poignee_index_deb+1)] +l[poignee_index_deb: poignee_index_fin] +l[(poignee_index_fin+1):]
    return l

    

if __name__ == "__main__":
    #mot2mat(EXEMPLE_1)
    print(simplification(EXEMPLE_1))

