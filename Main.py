# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 12:01:53 2019

@author: Guddu
"""

#from Block import SoftBlock as SB

import Driver


benchmarks=['ami33','ami49','n100','n200','n300'];
tiers=[2,3,4]

B,N,T=Driver.Driver(benchmarks[4],tiers[1],0.05)


#Driver.PrintTiers(B)

val=[]
density=[]
for i in range(len(T)):
    val.append(0)
    density.append(0)

for block in B:
    val[block.tier.index]+=block.power*(block.length+block.width)
    density[block.tier.index]+=block.power
    

print(val)
print(density)

