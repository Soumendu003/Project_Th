# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 20:41:42 2019

@author: Guddu
"""


from Block import Block 

class Net:
    
    def __init__(self,index,degree,connectedBlockIndices):
        self.index=index
        self.degree=degree
        self.connectedBlockIndices=connectedBlockIndices
        self.connectedBlocks=[]
        
        
    def readnets(file_name):
        f=open(file_name)
        lines=f.readlines()
        flag=0
        lst=[]
        count=-1
        netdegree=0
        net_list=[]
        for line in lines:
            if("NumNets" in line):
                net_no=line[10:]
                #print("Number of nets "+net_no)
                
            if("NetDegree" in line):
                if(flag):
                    obj=Net(count,netdegree,lst)
                    net_list.append(obj)
                lst=[]
                flag=1
                count+=1
                netdegree=line[12:]
            if("bk" in line):
                index=(line.split())[0][2:]
                lst.append(index)
            if("M0" in line):
                index=(line.split())[0][2:]
                lst.append(int(index))
            if("sb" in line):
                index=(line.split())[0][2:]
                lst.append(int(index))
    
        if(flag):
            obj=Net(count,netdegree,lst)
            net_list.append(obj)
        return net_list,int(net_no)
    
    def linkBlocks(Net_list,Bk_list):
        for net in Net_list:
            Blocks=[]
            for index in net.connectedBlockIndices:
                bk_obj=Block.getBlock(Bk_list,index,0,(len(Bk_list)-1))
                Blocks.append(bk_obj)
                Block.linkNet(bk_obj,net)
            net.connectedBlocks=Blocks
            
    def printConnectedBlocks(self):
        for block in self.connectedBlocks:
            print(block.index)