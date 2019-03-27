# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:33:58 2019

@author: Guddu
"""
from Net import Net
import Block

def reader(benchmark):
    if(benchmark=="ami33"):
        bk_list,bk_count=Block.SoftBlock.readblocks(benchmark+".blocks")
        net_list,net_count=Net.readnets(benchmark+".nets")
        Net.linkBlocks(net_list,bk_list)
        Block.Block.linkBlocks(bk_list,net_list)
        Block.Block.readPower(benchmark+".power",bk_list)
    else:
        bk_list,bk_count=Block.HardBlock.readblocks(benchmark+".blocks")
        net_list,net_count=Net.readnets(benchmark+".nets")
        Net.linkBlocks(net_list,bk_list)
        Block.Block.linkBlocks(bk_list,net_list)
        Block.Block.readPower(benchmark+".power",bk_list)
    return bk_list,net_list