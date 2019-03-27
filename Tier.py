# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 21:46:49 2019

@author: Guddu
"""

class Tier:
    
    def __init__(self,index,avg_Area,max_Area,min_Area):
        self.index=index
        self.avg_Area=avg_Area
        self.max_Area=max_Area
        self.min_Area=min_Area
        self.placedBlocks=set()
        
    def createTier(NoOfTier,avg_Area,max_Area,min_Area):
        tier_list=[]
        for i in range(0,NoOfTier):
            tem=Tier(i,avg_Area,max_Area,min_Area)
            tier_list.append(tem)
        return tier_list
    
    
        
        