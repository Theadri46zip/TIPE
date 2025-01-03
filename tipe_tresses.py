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
            m1[j1][j2]=-1
            m1[j2][j1]=1
        else:
            m1[j1][j2]=1
            m1[j2][j1]=-1
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


def suppr_av(t,n): # n le nombre d'éléments a enlever de la tete du mot
    """Supprime n éléments du mot."""
    t1=deepcopy(t)
    t2=[]
    for i in range(n,len(t)):
        t2.append(t1[i])
    return t2

def proche_inverse(t,sigma) -> int:
    """Identifie le plus proche inverse du générateur sigma.
    Renvoie la distance entre sigma et cet inverse
    sigma=[i,sig] est un élément du mot t
    """
    i=sigma[0]
    sig=sigma[1]
    c=[i,-sig] # si l'inverse existe, on cherche sa distance à [i,sig]
    ind1=t.index(sigma)
    ind2=0
    if c not in t:
        return 0
    for j, value in enumerate(t):
        if value==c :
            ind2=j
    return ind2-ind1


#On créée d'abord une fonction qui détermine si le mot est simplifiable ou non
#Ce sera la condition d'arret

"""
def simplifiable(t):
    #On ne va pas plus loin si tous les caractères n'ont pas d'inverse
    simpli=False
    for i in t:
        if proche_inverse(t,i)>0:
            simpli=True
    if not simpli:
        return False
    else:
        for i in t:
            pos=t.index(i)
            if abs(proche_inverse(t,i))==1:
                return True
            
            if abs(proche_inverse(t,i))


"""


"""
dans la suite le but sera de faire en sorte que proche inverse = 1 ou -1 
pour pouvoir supprimer deux états inutiles si possible
"""


def simplify(t):   #t le mot, n la complexité de la simplification ?
    """Réduction de tresse."""
    mot1=deepcopy(t)
    mot2=[]
    #CONDITION D'ARRET
    if t==[]:
        return []
    for j in range(len(t)):
        t1=mot1[j][0]
        s1=mot1[j][1]
        t2=mot1[j+1][0]
        s2=mot1[j+1][1]
        t3=mot1[j+2][0]
        s3=mot1[j+2][1]
        if t1 == t2 and s1 == -s2 :
            mot2=suppr_av(mot1,2)
            return simplify(mot2)

        if t1 == t3 and s1 == -s3:
            if abs((t1-t2))>=2:
                mot1[j],mot1[j+1] = mot1[j+1],mot1[j]
#COMPLETER LE PROGRAMME QUAND J'AI UNE PISTE

if __name__ == "__main__":
    mot2mat(EXEMPLE_1)
    print(proche_inverse(EXEMPLE_2, [1,-1]))
