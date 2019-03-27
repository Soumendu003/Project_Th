# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:58:21 2019

@author: Guddu
"""
from sys import maxsize
from sklearn.preprocessing import StandardScaler
import numpy as np
import ThermalWeightedConnectivity as TWC

def ConnectivityValue(block,PlacedSet):
    sum=0
    for neighbour in PlacedSet:
        if(str(neighbour) in block.connectedBlocks.keys()):
            sum+=block.connectedBlocks[str(neighbour)]
    return sum

def WeightedConnectivity(block,PlacedSet):
    weight=0
    connectivity=ConnectivityValue(block,PlacedSet)
    for neighbour in PlacedSet:
        if(str(neighbour) in block.connectedBlocks.keys()):
            conn_val=block.connectedBlocks[str(neighbour)]
            tem=(neighbour.length+neighbour.width+(conn_val/connectivity)*(block.length+block.width))**2
            tem*=conn_val
            weight+=tem
    
    return weight

def PlaceBlock(block,tier):
    if(block.tier is None):
        block.tier=tier
        tier.placedBlocks.add(block)
    else:
        prev_tier=block.tier
        block.tier=tier
        tier.placedBlocks.add(block)
        prev_tier.placedBlocks.remove(block)
        if((prev_tier.placedBlocks).isdisjoint(tier.placedBlocks)):
            pass
        else:
            raise ValueError
 

def calculateOptimumTier(blkind,connect,perimeters,powers,PlacedBlocks,Tiers,Blocks,powFactors,wireCoff,thermCoff):
    values=[]
    connectivity=connect[blkind,:].sum()
    
    for tier in Tiers:
        values.append(0)
    
    for i in PlacedBlocks:
        conn_val=connect[blkind,i]
        tem1=conn_val*wireCoff*((perimeters[i]+(conn_val/connectivity)*perimeters[blkind])**2)
        tem2=conn_val*thermCoff*((powers[i]+(conn_val/connectivity)*powers[blkind]*powFactors[Blocks[i].tier.index])**2) 
        values[Blocks[i].tier.index]+=(tem1+tem2)
     
    min_val=values[0]
    op_tier=0
    
    for i in range(1,len(Tiers)):
        if(values[i]<min_val):
            min_val=values[i]
            op_tier=i
    
    return Tiers[op_tier]
    
'''def calculateOptimumTier(block,PlacedSet,Tiers):
    values=[]
    connectivity=ConnectivityValue(block,PlacedSet)
    for tier in Tiers:
        values.append(0)
    for neighbour in PlacedSet:
        if(str(neighbour) in block.connectedBlocks.keys()):
            conn_val=block.connectedBlocks[str(neighbour)]
            tem=(neighbour.length+neighbour.width+(conn_val/connectivity)*(block.length+block.width))**2
            tem*=conn_val
            values[neighbour.tier.index]+=tem
            
    max_val=values[0]
    op_tier=0
    
    for i in range(1,len(Tiers)):
        if(values[i]<max_val):
            max_val=values[i]
            op_tier=i
    
    return Tiers[op_tier]'''
   
def NormalizePerimeterPower(Blocks):
    perimeter=[(block.length+block.width) for block in Blocks]
    power=[block.power*(block.length+block.width) for block in Blocks]
    
    scaler = StandardScaler()
    peri_array=np.array(perimeter,dtype='float')
    pow_array=np.array(power,dtype='float')
    
    peri_array=scaler.fit_transform(peri_array.reshape(-1,1))
    peri_array=peri_array.reshape(-1)
    
    pow_array=scaler.fit_transform(pow_array.reshape(-1,1))
    pow_array=pow_array.reshape(-1)
    
    for i in range(len(peri_array)):
        if peri_array[i]>2:
            peri_array[i]=2
        if peri_array[i]<-2:
            peri_array[i]=-2
    peri_array/=5
    peri_array+=0.5
    
    for i in range(len(pow_array)):
        if pow_array[i]>2:
            pow_array[i]=2
        if pow_array[i]<-2:
            pow_array[i]=-2
    pow_array/=5
    pow_array+=0.5
    
    return peri_array,pow_array
    

def TiersAndConnectivity(Blocks):
    tiers=[int(-1 if block.tier is None else block.tier) for block in Blocks]
    tiers=np.array(tiers,dtype='int')
    
    conn=[]
    for block in Blocks:
        conn1=[]
        for neighbour in Blocks:
            if(str(neighbour) in block.connectedBlocks.keys()):
                conn1.append(block.connectedBlocks[str(neighbour)])
            else:
                conn1.append(0)
        conn.append(conn1)
    conn=np.array(conn,dtype='int')
    return tiers,conn

def ThermalInitialPartition(Blocks,Nets,Tiers,tierCnt):
    
    thermCoff=0.6
    wireCoff=0.4
    
    perimeters,powers=NormalizePerimeterPower(Blocks)
    tiers,connectivity=TiersAndConnectivity(Blocks)

    PlacedBlocks=[]
    while(len(PlacedBlocks)<len(Blocks)):
        if(len(PlacedBlocks)==0):
            
            PlacedBlocks=[int(i) for i in range(len(Blocks))]
            placedSet=np.array(PlacedBlocks).reshape(-1)
            
            maxVal=-maxsize-1
            maxBlk=None
            i=0
            
            for block in Blocks:
                val=TWC.ThermalWeightedConnectivity(i,connectivity,placedSet,tiers,perimeters,powers,wireCoff,thermCoff)
                if(val>maxVal):
                    maxVal=val
                    maxBlk=block
                    blkind=i
                i+=1
                
            PlaceBlock(maxBlk,Tiers[0])
            PlacedBlocks=[]
            PlacedBlocks.append(blkind)
            
        else:
            maxVal=-maxsize-1
            maxBlk=None
            i=0
            
            for block in Blocks:
                if(i not in PlacedBlocks):
                    placedSet=np.array(PlacedBlocks).reshape(-1)
                    val=TWC.ThermalWeightedConnectivity(i,connectivity,placedSet,tiers,perimeters,powers,wireCoff,thermCoff)
                    if(val>maxVal):
                        maxVal=val
                        maxBlk=block
                        blkind=i
                i+=1
            powFactors=[[0.2,0.8],[0.08,0.28,0.64],[0.85,1,1.10,1.25]]
            tier=calculateOptimumTier(blkind,connectivity,perimeters,powers,PlacedBlocks,Tiers,Blocks,powFactors[tierCnt-2],wireCoff,thermCoff)
            PlaceBlock(maxBlk,tier)
            PlacedBlocks.append(blkind)
    
def InitialPartition(Blocks,Nets,Tiers):
    PlacedBlocks=[]
    while(len(PlacedBlocks)<len(Blocks)):
        if(len(PlacedBlocks)==0):
            maxVal=-maxsize-1
            maxBlk=None
            
            for block in Blocks:
                val=WeightedConnectivity(block,Blocks)
                if(val>maxVal):
                    maxVal=val
                    maxBlk=block
                    
            PlaceBlock(maxBlk,Tiers[0])
            PlacedBlocks.append(maxBlk)
        else:
            maxVal=-maxsize-1
            maxBlk=None
            
            for block in Blocks:
                if(block not in PlacedBlocks):
                    val=WeightedConnectivity(block,PlacedBlocks)
                    if(val>maxVal):
                        maxVal=val
                        maxBlk=block
            
            tier=calculateOptimumTier(maxBlk,PlacedBlocks,Tiers)
            PlaceBlock(maxBlk,tier)
            PlacedBlocks.append(maxBlk)