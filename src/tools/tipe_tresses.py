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
    inv=(t[0][0],-t[0][1])
    if prefixe in t[1:-1] or inv in t[1:-1]:
        return False
    return t[-1]==inv

def est_poignee_cor(t:Tresse)->bool:
    """
    valeur de l'assertion (t est une poignee correcte)
    """
    if len(t)<2:
        return False
    prefixe = t[0]
    suffixe = t[1]
    bool_inverse = prefixe[0] == suffixe[0] and prefixe[1] == - suffixe[1]
    return len(t) == 2 and bool_inverse and est_poignee(t)

def extract2poignee(t:Tresse,g:Noeud)->Tresse:
    """
    renvoie la premiere poignee extraite de t ayant comme prefixe g
    """
    inv=(g[0],-g[1])
    if g not in t or inv not in t:
        return t
    l=[g]
    place = t.index(g)+1
    if inv not in t[place:]:
        return t
    for noeud in t[place:]:
        if noeud != g and inv not in l and inv in t[place:]:
            l.append(noeud)
            place+=1
    return l

def num_generateurs(t:Tresse,g:Noeud)->int:
    """
    renvoie le nombre de générateurs g et inverses g**-1 dans t
    """
    compteur=0
    inv=(g[0],-g[1])
    for sigma in t:
        if sigma in (g ,inv):
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
    """
    renvoie la tresse inverse de t
    """
    t2=deepcopy(t)
    t2.reverse()
    t3=[]
    n=len(t2)
    for i in range(n):
        t3.append((t2[i][0],-1*t2[i][1]))
    return t3

def addition(t1:Tresse,t2:Tresse)->Tresse:
    """
    compose deux tresses, les mets bout à bout
    """
    return t1+t2

"""
diffie hellman v1
avec seulement la concatenation
"""

def init_choix_v1() -> tuple:
    """
    Initialisation de la configuration, 
    mais on controle ici alice et bob
    """
    a=Tresse(input("clé d'Alice:"))
    b=Tresse(input("clé de Bob"))
    p=Tresse(input("clé commune"))
    return (a,b,p)

def alice_1_v1(a:Tresse,p:Tresse)->Tresse:
    """
    alice crée une partie de la clé,
    on la transmettra a bob
    """
    p_a=a+p+inverse(p)
    return p_a

def bob_1_v1(b:Tresse,p:Tresse)->Tresse:
    """
    bob crée l'autre partie de la clé,
    on la transmettra a alice
    """
    p_b=b+p+inverse(b)
    return p_b

def alice_2_v1(a:Tresse,pb:Tresse)->Tresse:
    """
    bob a transmis sa partie de la clé
    on crée la clé finale
    """
    p_f=a+pb+inverse(a)
    return p_f

def bob_2_v1(b:Tresse,pa:Tresse)->Tresse:
    """
    alice a transmis sa partie de la clé
    on crée la clé finale
    """
    p_f=b+pa+inverse(b)
    return p_f

"""

diffie hellman v2
avec conjugaison
il faut vérifier
1) Gamma linéaire par rapport a sa deuxieme variable
2)alpha(x,gamma(y,x))=beta(y,gamma(x,y))
3)Impossible de trouver x avec gamma(x,_)
"""
def init_choix_v2() -> tuple:
    """
    Initialisation de la configuration,
    on crée le monoide choisi par un des deux,
    puis la clé doit provenir de celui-ci
    On controle ici soit alice soit bob pour allèger les notations
    """
 
    l=[]
    choix=()
    while choix != "exit":
        choix=input("Entrez une tresse génératrice du monoide, \n'exit' si fini :")
        if choix != "exit":
            l.append(choix)
    print(l)
    a=Tresse(input("choisissez une clé(Tresse) composée d'éléments ci dessus:"))
    return (a,l)

def gamma(x:Tresse,y:Tresse)->Tresse:
    """
    fonction conjugaison qui renvoie x*-1 +y+ x
    """
    res=inverse(x)+y+x
    return res

def alpha(u:Tresse,v:Tresse)->Tresse:
    """
    renvoie u*-1 + v
    """
    res=inverse(u)+v
    return res

def beta(u:Tresse,v:Tresse)->Tresse:
    """
    renvoie u + v*-1
    """
    res=inverse(v) + u
    return res

def alice_1_v2(a:Tresse,l_b:list[Tresse])->list[Tresse]:
    """
    alice renvoie la liste des gamma(a,tk)
    les tk sont les generateurs du monoide de bob, 
    contenus dans l_b
    """
    l2=[]
    for noeud in l_b:
        l2.append(gamma(a,noeud))
    return l2

def bob_1_v2(b:Tresse,l_a:list[Tresse])->list[Tresse]:
    """
    bob renvoie la liste des gamma(b,sk)
    les sk sont les generateurs du monoide de alice, 
    contenus dans l_a
    """
    l2=[]
    for noeud in l_a:
        l2.append(gamma(b,noeud))
    return l2

def position_gen(t:Tresse,l_gen:list[Tresse])->int:
    """
    renvoie une liste dont chaque element indique 
    l'indice d'un élément de t dans l_gen
    """
    l_ind=[]
    i=0
    while i<len(t):
        l2=[]
        l2.append(t[i])
        i+=1
        while l2 not in l_gen:
            l2.append(t[i])
            i+=1
        l_ind.append(l_gen.index(l2))
    return l_ind

def alice_2_v2(a:Tresse,l_gamma:list[Tresse],l_a:list[Tresse])->Tresse:
    """
    alice calcule gamma(b,a) a partir
    des gamma(b,sk) transmis par bob, contenus dans l_gamma
    pour décomposer a en sk on retrouve la position des
    noeuds qui composent a dans l_a puis on prend la valeur
    de meme position dans l_gamma
    """
    res=[]
    inds=position_gen(a,l_a)
    for ind in inds:
        res+= l_gamma[ind]
    return res

def bob_2_v2(b:Tresse,l_gamma:list[Tresse],l_b:list[Tresse])->Tresse:
    """
    bob calcule gamma(a,b) a partir
    des gamma(tk,b) transmis par bob, contenus dans l_gamma
    pour décomposer a en sk on retrouve la position des
    noeuds qui composent a dans l_b puis on prend la valeur
    de meme position dans l_gamma
    """
    res=[]
    inds=position_gen(b,l_b)
    for ind in inds:
        res+= l_gamma[ind]
    return res

def alice_3_v2(a:Tresse,gam:Tresse)->Tresse:
    """
    On calcule alpha(a,gamma(b,a))
    """
    res=alpha(a,gam)
    return res

def bob_3_v2(b:Tresse,gam:Tresse)->Tresse:
    """
    On calcule beta(b,gamma(a,b))
    """
    res=beta(b,gam)
    return res