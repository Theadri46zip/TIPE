"""Codage de tresses et cryptographie"""
from copy import deepcopy
from typing import Literal

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
    """Passage d'un mot à une série de matrices """
    n=nbr_brins(t)
    m0=matcar_zero(n)   #Etat 0 matrice nulle
    l_mat=[m0]           # On ajoute la matrice 0 a la liste des matrices
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

#REDUCTION

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

#diffie hellman 

def oppose(element:int,booleen:bool)->int:
    """
    renvoie element si booleen =False, -element sinon
    """
    if booleen:
        return -1*element
    return element

def convert_slt_to_lt(element:str)->list[tuple]:
    """
    transforme une 
    liste de tuples de forme str
    en liste de liste de tuples
    """
    l2=[]
    st=[]
    negative=False
    for carac in element:
        if carac not in ["[","]","(",")",","," "]:
            if carac=="-":
                negative=True
            else:
                st.append(oppose(int(carac),negative))
                negative=False
        if carac==")":
            l2.append((st[0],st[1]))
            st=[]
    return l2

def convert_lslt_to_llt(l:list[str])->list[list[tuple]]:
    """
    transforme une liste de liste de tuples de forme str
    en liste de liste de tuples
    """
    l2=[]
    for element in l:
        sl=[]
        st=[]
        negative=False
        for carac in element:
            if carac not in ["[","]","(",")",","," "]:
                if carac=="-":
                    negative=True
                else:
                    st.append(oppose(int(carac),negative))
                    negative=False
            if carac==")":
                sl.append((st[0],st[1]))
                st=[]
        l2.append(sl)
    return l2

def init_choix() -> tuple[list[tuple],list[list[tuple]]]:
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
    l=convert_lslt_to_llt(l)
    print(l)
    a=input("choisissez une clé(Tresse) composée d'éléments ci dessus:")
    a=convert_slt_to_lt(a)
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

def alice_1(a:Tresse,l_b:list[Tresse])->list[Tresse]:
    """
    alice renvoie la liste des gamma(a,tk)
    les tk sont les generateurs du monoide de bob, 
    contenus dans l_b
    """
    l2=[]
    tresse_temp=[]
    for noeud in l_b:
        tresse_temp=gamma(a,noeud)
        l2.append(boucle_2simp(tresse_temp))
    return l2

def bob_1(b:Tresse,l_a:list[Tresse])->list[Tresse]:
    """
    bob renvoie la liste des gamma(b,sk)
    les sk sont les generateurs du monoide de alice, 
    contenus dans l_a
    """
    l2=[]
    tresse_temp=[]
    for noeud in l_a:
        tresse_temp=gamma(b,noeud)
        l2.append(boucle_2simp(tresse_temp))
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

def alice_2(a:Tresse,l_gamma:list[Tresse],l_a:list[Tresse])->Tresse:
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

def bob_2(b:Tresse,l_gamma:list[Tresse],l_b:list[Tresse])->Tresse:
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

def alice_3(a:Tresse,gam:Tresse)->Tresse:
    """
    On calcule alpha(a,gamma(b,a))
    """
    res=alpha(a,gam)
    res=boucle_2simp(res)
    return res

def bob_3(b:Tresse,gam:Tresse)->Tresse:
    """
    On calcule beta(b,gamma(a,b))
    """
    res=beta(b,gam)
    res=boucle_2simp(res)
    return res

def final_alice_and_bob()->tuple[Tresse,Tresse]:
    """
    alice et bob entrent leur clé et on execute le processus 
    qui permet de trouver la clé commune
    """
    print("AU TOUR D'ALICE")
    a,sa=init_choix()
    print("AU TOUR DE BOB")
    b,sb=init_choix()
    #sb et sa sont échangés publiquement
    #a et b restent privés
    a_1=alice_1(a,sb)
    b_1=bob_1(b,sa)
    #a_1 et b_1 sont échangés publiquement
    a_2=alice_2(a,b_1,sa)
    b_2=bob_2(b,a_1,sb)
    fa=alice_3(a,a_2)
    fb=bob_3(b,b_2)
    return fa,fb
