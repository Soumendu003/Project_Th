# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 12:07:23 2019

@author: Guddu
"""

def readblocks(file_name):
    f=open(file_name)
    lines=f.readlines()
    bk_index=[]
    bk_area=[]
    for line in lines:
        if("NumSoftRectangularBlocks" in line):
            bk_num=line[28:]
            print("Number of blocks:"+bk_num)
        if("bk" in line):
            token=line.split()
            index=token[0][2:]
            area=token[2]
            bk_index.append(index)
            bk_area.append(float(area))
            print("area is "+area)
    
    return bk_index,bk_area,int(bk_num)
    
    
def readnets(file_name):
    f=open(file_name)
    lines=f.readlines()
    flag=0
    lst=[]
    count=1
    net_index=[]
    net_list=[]
    for line in lines:
        if("NumNets" in line):
            net_no=line[10:]
            print("Number of nets "+net_no)
            
        if("NetDegree" in line):
            if(flag):
                net_list.append(lst)
            lst=[]
            flag=1
            net_index.append(count)
            count+=1
            netdegree=line[12:]
            print("Net degree "+netdegree)
        if("bk" in line):
            index=(line.split())[0][2:]
            lst.append(index)
    
    if(flag):
        net_list.append(lst)
        net_index.append(count)
    return net_index,net_list,net_no