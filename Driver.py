# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 23:04:38 2019

@author: Guddu
"""
import Input_Output as IO
import Tier
import InitialPartition as IP
import time
import CMFM


def PrintTiers(Blocks):
    for block in Blocks:
        print("Block "+str(block.index)+" is placed at tier "+str(block.tier.index)+" Block area="+str(block.area))
    
    
def CalculateAreaConstraints(Blocks,relaxation):
    area=0
    for block in Blocks:
        area+=block.area
    Max_area=area*(1+relaxation)
    Min_area=area*(1-relaxation)
    
    return area,Max_area,Min_area

def Driver(benchmark,NoOfTiers,relaxation):
    
    Blocks,Nets=IO.reader(benchmark)
    
    avg_area,Max_area,Min_area=CalculateAreaConstraints(Blocks,relaxation)
    
    avg_area/=NoOfTiers
    
    Tiers=Tier.Tier.createTier(NoOfTiers,avg_area,Max_area,Min_area)
    
    file=benchmark+"_final.txt"
    
    Weightages=[[0.75,1],[0.6,0.8,1],[0.5,0.7,0.85,1]]
    
    start=time.time()
    CMFM.ReadCMFM(file,Blocks,Tiers,NoOfTiers,relaxation)
    CMFM.ShiftTiers(Blocks,Tiers)
    
    CMFM.ThermallyOptimizeTiers(Blocks,Nets,Tiers,Weightages[NoOfTiers-2])
    
    end=time.time()
    print("time taken for Initial Partition: "+str((end-start)*1000)+"ms")

    
    return Blocks,Nets,Tiers