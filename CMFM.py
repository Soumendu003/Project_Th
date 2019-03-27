# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:02:30 2019

@author: Guddu
"""

def ReadCMFM(file,Blocks,Tiers,NoOfTiers,relaxation):
    f=open(file)
    print(file)
    lines=f.readlines()
    state=0
    i=0
    for line in lines:
        if(state==2):
            break
        token=line.split()
        if ("No of Tiers=" in line):
            tiers=int(token[2][len("Tiers="):])
            relax=float(token[4][len("Percentage="):])
            if(tiers==int(NoOfTiers) and state==0 and relaxation==relax):
                state=1
            if((tiers!=int(NoOfTiers) or relaxation!=relax) and state==1) :
                state=2
        if("Block " in line and state==1):
            tierNo=token[3][3:]
            Blocks[i].tier=Tiers[int(tierNo)]
            i+=1
    for block in Blocks:
        #print("Block "+str(block.index)+" placed at="+str(block.tier.index))
        pass
        
    