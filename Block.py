# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 20:18:32 2019

@author: Guddu
"""
import math

class Block:
    
    def __init__(self):
        self.connectedBlocks=dict()
        self.tier=None
        
    def linkNet(bk_obj,net):
        bk_obj.connectedNets.append(net)
        
    def linkBlocks(Blocks,Nets):
        for block in Blocks:
            for net in block.connectedNets:
                for neighbour in net.connectedBlocks:
                    if(neighbour!=block):
                        if(str(neighbour) in block.connectedBlocks.keys()):
                            block.connectedBlocks[str(neighbour)]+=1
                        else:
                            block.connectedBlocks[str(neighbour)]=1
            
        
    def readPower(filename,Bk_list):
        f=open(filename)
        lines=f.readlines()
        index=0
        for line in lines:
            token=line.replace('\n',' ')
            token=token.split()
            if(len(token)>0):
                val=float(token[0][:])
                Bk_list[index].power=val
                index+=1
        
    def getBlock(Bk_list,index,start,last):
        mid=(start+last)//2
        if(Bk_list[mid].index==index):
            return Bk_list[mid]
        elif(Bk_list[mid].index>index and (mid-1)>=start):
            return Block.getBlock(Bk_list,index,start,mid-1)
        elif(Bk_list[mid].index<index and (mid+1)<=last):
            return Block.getBlock(Bk_list,index,mid+1,last)
        else:
            return None

    def isFloat(n):
        try:
            float(n)
            return True
        except:
            return False

class SoftBlock(Block):
    
    def __init__(self,index,area,x_deform,y_deform):
        self.index=index
        self.area=area
        self.x_deform=x_deform
        self.y_deform=y_deform
        self.length=self.width=math.sqrt(area)
        self.connectedNets=[]
        self.power=0
        super().__init__()
        
    def readblocks(file_name):
        f=open(file_name)
        lines=f.readlines()
        bk_list=[]
        for line in lines:
            if("NumSoftRectangularBlocks" in line):
                bk_num=line[28:]
                #print("Number of blocks:"+bk_num)
            if("bk" in line):
                token=line.split()
                index=token[0][2:]
                area=float(token[2])
                x_deform=token[3]
                y_deform=token[4]
                obj=SoftBlock(index,area,x_deform,y_deform)
                bk_list.append(obj)
        return bk_list,int(bk_num)
     
    
        
class HardBlock(Block):
    
    def __init__(self,index,area,length,width):
        self.index=index
        self.area=area
        self.length=length
        self.width=width
        self.connectedNets=[]
        self.power=0
        super().__init__()
    
    def readblocks(file_name):
        f=open(file_name)
        lines=f.readlines()
        bk_list=[]
        for line in lines:
            if("NumHardRectilinearBlocks :" in line):
                bk_num=line[len("NumHardRectilinearBlocks : "):]
                #print("Number of  Hard Blocks="+bk_num)
            if("M0" in line):
                token=line.split()
                index=int(token[0][2:])
                length=float(token[7][1:(len(token[7])-1)])
                #print(length)
                width=float(token[8][:(len(token[8])-1)])
                #print(width)
                area=length*width
                obj=HardBlock(index,area,length,width)
                bk_list.append(obj)
            if("sb" in line):
                token=line.split()
                index=int(token[0][2:])
                length=float(token[7][1:(len(token[7])-1)])
                #print(length)
                width=float(token[8][:(len(token[8])-1)])
                #print(width)
                area=length*width
                obj=HardBlock(index,area,length,width)
                bk_list.append(obj)
        return bk_list,int(bk_num)
    
    
            