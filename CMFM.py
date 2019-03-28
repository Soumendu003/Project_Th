# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:02:30 2019

@author: Guddu
"""
import Tier as T
import math
import numpy as np
import InitialPartition as IP

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
            IP.PlaceBlock(Blocks[i],Tiers[int(tierNo)])
            i+=1
    for block in Blocks:
        #print("Block "+str(block.index)+" placed at="+str(block.tier.index))
        pass
        
def TP(val):
    return val.totalPower    
    
    
def ShiftTiers(Blocks,Tiers):
    val=[]
    for i in range(len(Tiers)):
        val.append(0)

    for block in Blocks:
        val[block.tier.index]+=block.totalPower
    
    for i in range(len(Tiers)):
        Tiers[i].totalPower=val[i]
        
    Tiers.sort(key=TP,reverse=True)
    
    for i in range(0,len(Tiers)):
        Tiers[i].index=i
 
def CalculateDistributedThermalEntropy(Blocks,Tiers,Weightage):
    val=[]
    for tier in Tiers:
        val.append(tier.totalPower*Weightage[tier.index])
    #print(val)
    SumVal=sum(val)
    entropy=0
    for v in val:
        entropy+=(-1*(v/SumVal)*(math.log((v/SumVal))/math.log(len(Weightage))))
    
    return entropy

def CalculateTE(TE,Blocks,Tiers,Weightage,PowerArray,SumPower):
    
    NoOfTiers=len(Weightage)
    CurrentEntropy=CalculateDistributedThermalEntropy(Blocks,Tiers,Weightage)
    
    for i in range(0,len(Blocks)):
        for j in range(0,len(Tiers)):
            entropy=0
            if(j!=Blocks[i].tier.index):
                PowerArray[j]+=Weightage[j]*Blocks[i].totalPower
                PowerArray[Blocks[i].tier.index]-=Weightage[j]*Blocks[i].totalPower
                
                for v in PowerArray:
                    entropy+=(-1*(v/SumPower)*(math.log((v/SumPower))/math.log(NoOfTiers)))
                    
                PowerArray[j]-=Weightage[j]*Blocks[i].totalPower
                PowerArray[Blocks[i].tier.index]+=Weightage[j]*Blocks[i].totalPower
                
            else:
                entropy=CurrentEntropy
    
            TE[i][j]=entropy  
        
def CalculateGW(GW,PN,Blocks,Nets,Tiers):
    NoOfTiers=len(Tiers)
    
    Sum=np.zeros((len(Nets)),dtype='float')
    DefaultEntropy=np.zeros((len(Nets)),dtype='float')
    for j in range(0,len(Nets)):
        Sum[j]=PN[j].sum()
        for k in range(0,NoOfTiers):
            v=PN[j][k]
            S=Sum[j]
            if(v!=0):
                DefaultEntropy[j]+=(-1*(v/S)*(math.log(v/S)/math.log(NoOfTiers)))
            
    for i in range(0,len(Blocks)):
        
        for k in range(0,NoOfTiers):
            Gain=0
            count=0
            for net in Blocks[i].connectedNets:
                entropy=0
                count+=1
                if(Blocks[i].tier.index!=k):
                    PN[net.index][k]+=Blocks[i].perimeter
                    PN[net.index][Blocks[i].tier.index]-=Blocks[i].perimeter
                    
                    for l in range(0,NoOfTiers):
                        v=PN[net.index][l]
                        S=Sum[net.index]
                        if(v>0):
                            
                            entropy+=(-1*(v/S)*(math.log((v/S))/math.log(NoOfTiers))) 
                        
                    PN[net.index][k]-=Blocks[i].perimeter
                    PN[net.index][Blocks[i].tier.index]+=Blocks[i].perimeter 
                else:
                    entropy+=DefaultEntropy[net.index]
                Gain+=entropy
            GW[i][k]=Gain/count
        

def CalculatePN(PN,Blocks,Nets,Tiers):
    
    for i in range(0,len(Nets)):
        val=[]
        for k in range(0,len(Tiers)):
            val.append(0)    
        for block in Nets[i].connectedBlocks:
            val[block.tier.index]+=block.perimeter
        PN[i]=np.array(val,dtype='float')
  
def CalculateTG(TG,GW,TE,Blocks,NoOfTiers):
    
    for i in range(0,len(Blocks)):
        currentTE=TE[i][Blocks[i].tier.index]
        TG[i,:]=(TE[i,:]-currentTE)*((2+GW[i,:])/4)
             
def ThermalCMFM(Blocks,Nets,Tiers,Weightage):
    
    TE=[[float(0) for i in range(0,len(Tiers))] for j in range(0,len(Blocks))]
    TE=np.array(TE,dtype='float')
    GW=[[float(0) for i in range(0,len(Tiers))] for j in range(0,len(Blocks))]
    GW=np.array(GW,dtype='float')
    PN=[[float(0) for i in range(0,len(Tiers))] for j in range(0,len(Nets))]
    PN=np.array(PN,dtype='float')
    TG=[[float(0) for i in range(0,len(Tiers))] for j in range(0,len(Blocks))]
    TG=np.array(TG,dtype='float')
    Val=[]
    for tier in Tiers:
        Val.append(tier.totalPower*Weightage[tier.index])
    SumVal=sum(Val)
    state=1
    while(state==1):
        CalculateTE(TE,Blocks,Tiers,Weightage,Val,SumVal)
        CalculatePN(PN,Blocks,Nets,Tiers)
        CalculateGW(GW,PN,Blocks,Nets,Tiers)
        CalculateTG(TG,GW,TE,Blocks,len(Tiers))
        i,j = np.unravel_index(TG.argmax(), TG.shape)
        val=TG[i][j]
        if(val>0.01):
            IP.PlaceBlock(Blocks[i],Tiers[j])
            #print("Movement Done")
            state=1
        else:
            state=0

def getPowers(Blocks,Tiers):
    val=[]
    for i in range(len(Tiers)):
        val.append(0)

    for block in Blocks:
        val[block.tier.index]+=block.totalPower
    
    for i in range(len(Tiers)):
        Tiers[i].totalPower=val[i]
    print(val)

def getDivergence(Blocks,Tiers):
    
    div=[]
    for tier in Tiers:
        div.append(0)
    for block in Blocks:
        div[block.tier.index]+=block.area
    for tier in Tiers:
        div[tier.index]=(div[tier.index]-tier.avg_Area)/tier.avg_Area
    print(div)

def ThermallyOptimizeTiers(Blocks,Nets,Tiers,Weightage):
    ShiftTiers(Blocks,Tiers)
    getPowers(Blocks,Tiers)
    print("Initial Thermal Entropy = "+str(CalculateDistributedThermalEntropy(Blocks,Tiers,Weightage)))
    getDivergence(Blocks,Tiers)
    ThermalCMFM(Blocks,Nets,Tiers,Weightage)
    getPowers(Blocks,Tiers)
    print("Final Thermal Entropy = "+str(CalculateDistributedThermalEntropy(Blocks,Tiers,Weightage)))
    getDivergence(Blocks,Tiers)
    