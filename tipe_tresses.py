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
    prefixe=t[0]
    inverse=[t[0][0],-t[0][1]]
    if prefixe in t[1:-1] or inverse in t[1:-1]:
        return False
    return t[-1]==inverse

def pos_generateur(t,g):
    inverse=[g[0],-g[1]]
    l=[]
    for noeud in t:
        if noeud==g:
            l.append(1)
        elif noeud==inverse:
            l.append(-1)
        else:
            l.append(0)
    return l


def extract_poignee(t,g):
    #tresse_bin=pos_generateur(t,g)
    inverse=[g[0],-g[1]]
    if inverse not in t:
        return t
    else:
        l=[]
        count=0
        place=0
        for noeud in t:
            if noeud==g and g not in l:
                l.append(g)
                place=count
            else:
                count+=1
        for noeud in t[(place):]:
            if noeud != g and inverse not in l and inverse in t[place:]:
                l.append(noeud)
                place+=1
        return l
            
            


if __name__ == "__main__":
    mot2mat(EXEMPLE_1)
    print(est_poignee(EXEMPLE_2,))
