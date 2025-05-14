from tools.tipe_tresses import init_choix_v2,alice_1_v2,alice_2_v2,alice_3_v2,bob_1_v2,bob_2_v2,bob_3_v2,boucle_2simp
from tools.tipe_tresses import EXEMPLE_2,EXEMPLE_1
from tools.tipe_tresses import gamma,alpha,beta,boucle_2simp,position_gen


sa=[[(1,1),(2,1)], [(3,1),(1,-1)], [(2,1)]]
a=[(2,1),(3,1),(1,-1)]
sb=[[(2,1),(1,-1)], [(3,-1)], [(1,1),(3,1)]]
b=[(2,1),(1,-1),(3,-1),(1,1),(3,1)]

a_1=alice_1_v2(a,sb)
b_1=bob_1_v2(b,sa)

a_2=alice_2_v2(a,b_1,sa)
b_2=bob_2_v2(b,a_1,sb)

fa=alice_3_v2(a,a_2)
fb=bob_3_v2(b,b_2)
print("fa:",boucle_2simp(fa))
print("fb:",boucle_2simp(fb))

