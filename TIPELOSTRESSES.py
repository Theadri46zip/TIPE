from copy import deepcopy


e1=[[1,-1],[2,1],[1,1],[2,1]]
e2=[[2,1],[1,1],[1,1],[2,-1],[1,1],[1,-1]]

def nbr_brins(t):
    return max([t[i][0] for i in range(len(t))]) + 1

def list_zero(n):
    M=[]
    for i in range(n):
        M.append(0)
    return M

def matcar_zero(n):
    return [list_zero(n) for i in range(n)]
    
def lect_mat(m):
    if m==[]:
        print(" ")
    else:
        for i in range(len(m[0])):
            print(m[i])

"""
ne marche que si il y a 3 brins
"""

def ajout_diago(m1,m2):
    if len(m1)!= len(m2):
        return "matrices de tailles différentes"
    else:
        n=len(m1)
        m0=matcar_zero(n)
        for i in range(n):
            print(m1[i][i],m2[i][i])
            m0[i][i]=m1[i][i] + m2[i][i]
        return m0

def ajout_matrices(m1,m2):
    if len(m1)!= len(m2):
        return "matrices de tailles différentes"
    else:
        n=len(m1)
        m0=matcar_zero(n)
        for i in range(n):
            for j in range(n):
                m0[i][j]=m1[i][j] + m2[i][j]
        return m0
                
def mot_tomat(t):
    n=nbr_brins(t)
    m0=matcar_zero(n)   #Etat 0 matrice nulle
    mf=matcar_zero(n)   #On va calculer l'état final a partir des intermédiaires
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
        l_etatnow[j1],l_etatnow[j2]=l_etatnow[j2],l_etatnow[j1]
        l_etats.append(l_etatnow)
        if sig ==1:
            m1[j1][j2]=-1
            m1[j2][j1]=1
        else:
            m1[j1][j2]=1
            m1[j2][j1]=-1
        lmat.append(m1)
        mf = ajout_matrices(m1,mpre)
        mpre=deepcopy(m1)
        etat+=1
        

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

        
        
        
                
        
       
                
        
