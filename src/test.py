from tools.tipe_tresses import nbr_brins,boucle_2simp,final_alice_and_bob_v2
from tools.tipe_tresses import EXEMPLE_2,EXEMPLE_1
from tools.graph_tipe import tresses_n_brins

#1ers tests
sa=[[(1,1),(2,1)],[(3,1),(1,-1)],[(2,1)]]
a=[(2,1),(3,1),(1,-1)]
sb=[[(2,1),(1,-1)],[(3,-1)],[(1,1),(3,1)]]
b=[(2,1),(1,-1),(3,-1),(1,1),(3,1)]


print(final_alice_and_bob_v2())
