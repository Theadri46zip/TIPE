from copy import deepcopy


e1=[[1,-1],[2,1],[1,1],[2,1]]
e2=[[2,1],[1,1],[1,1],[2,-1],[1,1],[1,-1]]

def nbr_brins(t):
    return max([t[i][0] for i in range(len(t))]) + 1

def matcar_zero(n):
    return [[0 for i in range(n)] for i in range(n)]
    
def lect_mat(m):
    if m==[]:
        print(" ")
    else:
        for i in range(len(m[0])):
            print(m[i])

"""
ne marche que si il y a 3 brins
"""   

def ajout2mat(m1,m2):
    if len(m1)!= len(m2):
        return "matrices de tailles différentes"
    else:
        n=len(m1)
        return [[ m1[i][j]+m2[i][j] for j in range(n)] for i in range(n)]
                
def mot_tomat(t):
    n=nbr_brins(t)
    m0=matcar_zero(n)   #Etat 0 matrice nulle
    lmat=[m0]           # On ajoute l'état 0 a la liste des états
    etat=0
    mpre=matcar_zero(n)
    l_etat=[i for i in range(1,n+1)] #la liste des noeuds dans l'ordre de priorité gauche -> droite
    l_etats=[]
    l_etats.append(l_etat)
    for i in range(len(t)):
        l_etatnow=deepcopy(l_etats[etat])
        m1 = matcar_zero(n)
        t_et = t[etat]    #l'élément d'indice état nous renseigne sur les modifs a faire      
        j=t_et[0]         # C'est l'indice du brin qui monte en passant par dessous du prochain
        sig=t_et[1]
        j1=l_etatnow[j-1]-1
        j2=l_etatnow[j]-1
        m1[j1][j1]=1   
        m1[j2][j2]=-1        
        l_etatnow[j],l_etatnow[j-1]=l_etatnow[j-1],l_etatnow[j]
        l_etats.append(l_etatnow)
        if sig ==1:
            m1[j1][j2]=-1
            m1[j2][j1]=1
        else:
            m1[j1][j2]=1
            m1[j2][j1]=-1
        lmat.append(m1)
        etat+=1
    mf=matcar_zero(n)
    for i in range(len(lmat)):
        mf=ajout2mat(mf,lmat[i])
        
    
    for i in range(len(lmat)):
        print("état",i)
        lect_mat(lmat[i])
        print("ordre :")
        print(l_etats[i])
        print(" ")
    print("état final :")
    lect_mat(mf)

"""
3 propriétés :
- [ i,1] suivi de [i,-1] se simplifie en l'inaction
- [i,1] suivi de [j,1] vaut [j,1] suivi de [i,1] si en valeur abs i-j >=2
- [i,1] [j,1] [i,1] vaut [j,1] [i,1] [j,1] si en valeur abs i-j =1
"""

def suppr_av(t,n): # n le nombre d'éléments a enlever de la tete du mot
    t1=deepcopy(t)
    t2=[]
    for i in range(n,len(t)):
        t2.append(t1[i])
    return t2

def proche_inverse(t,etat): # etat=[i,sig] compose le mot t
    i=etat[0]
    sig=etat[1]
    c=[i,-sig] # On cherche, si il existe, sa distance à [i,sig]
    ind1=t.index(etat)
    ind2=0
    if c not in t:
        return 0
    else:
        for j in range(len(t)):
            if t[j]==c :
                ind2=j
        return ind2-ind1

"""
dans la suite le but sera donc de faire en sorte que proche inverse = 1 ou -1 pour pouvoir supprimer deux états inutiles si possible
"""


def simplify(t):   #t le mot, n la complexité de la simplification ?
    mot1=deepcopy(t)
    mot2=[]
    #CONDITION D'ARRET
    if t==[]:
        return []
    else:
    
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

        
        
        
                
        
       
                
        
