from tools.tipe_tresses import mot2mat,final_alice_and_bob_v2,reduction_poignee,boucle_2simp
from tools.tipe_tresses import EXEMPLE_2,EXEMPLE_1
from tools.graph_tipe import tresses_n_brins

#1ers tests
sa=[[(1,1),(2,1)],[(3,1),(1,-1)],[(2,1)],[(4, 1), (2, -1)]]
a=[(2,1),(4,1),(2,-1),(3,1),(1,-1)]
sb=[[(2,1),(1,-1)],[(3,-1)],[(1,1),(3,1)],[(2,-1),(2,-1)]]
b=[(2,1),(1,-1),(2,-1),(2,-1),(3,-1),(1,1),(3,1)]

mot2mat([(1,1)])