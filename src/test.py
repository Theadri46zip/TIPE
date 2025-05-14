from tools.tipe_tresses import nbr_brins,boucle_2simp
from tools.tipe_tresses import EXEMPLE_2,EXEMPLE_1
from tools.tipe_graphique import tresses_n_brins

n1=nbr_brins(EXEMPLE_2)
tresses_n_brins(EXEMPLE_2,n1)
m=boucle_2simp(EXEMPLE_2)
n2=nbr_brins(EXEMPLE_2)
tresses_n_brins(m,n2)