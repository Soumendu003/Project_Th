# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 23:08:16 2019

@author: Guddu
"""
import numpy as np
import time
import  random
import tensorflow as tf

lst=[]

#test


start=time.time()
array3=np.dot(array1,array2)
end=time.time()
print((end-start)*1000)
array=np.random.randint(0,2,(500,500))

kernel=np.ones((100,25),dtype=int)

array_tensor=tf.constant(array,shape=[1,array.shape[0],array.shape[1],1],dtype="float64")
kernel_tensor=tf.constant(kernel,shape=[kernel.shape[0],kernel.shape[1],1,1],dtype="float64")

conv=tf.nn.conv2d(array_tensor,kernel_tensor,[1, 1, 1, 1], "VALID")

sess = tf.Session()
with sess.as_default():
    tem=conv.eval()
    
tem=tem[0]
tem=tem.reshape(-1)

lst=np.array(np.where(tem==0))
end=time.time()
print("time taken: "+str((end-start)*1000)+"ms")


#test
#print("time taken: "+str((end-start)*1000)+"ms")

def findVoid(lst):
    array=lst[0]
   # kernel=lst[1]
   # print(array)
    #print(kernel.shape)
    '''for i in range(0,aSize[0]-kSize[0]+1):
        tem=[]
        for j in range(0,aSize[1]-kSize[1]+1):
            feature=np.multiply(array[i:i+kSize[0],j:j+kSize[1]],kernel)
            if(np.array_equal(feature,kernel)):
                tem.append([i,j])
    return tem'''

kernel=np.ones((2,2), dtype=int)

'''new_kernel=kernel.

vfunc=np.vectorize(findVoid)
lst=[array,kernel]
print(lst[0])
print(lst[1])
tem=vfunc(lst)'''

grid=np.array([np.array(array[i:i+kernel.shape[0],j:j+kernel.shape[1]]).reshape(-1).tolist()for i in range(array.shape[0]-kernel.shape[0]+1)for j in range(array.shape[1]-kernel.shape[1]+1)])

#grid=np.zeros((kernel.shape[0]*(array.shape[0]-kernel.shape[0]+1),kernel.shape[1]*(array.shape[1]-kernel.shape[1]+1)),dtype=int)

grid_kernel=np.array(np.array(kernel[:,:]).reshape(-1).tolist()*(array.shape[0]-kernel.shape[0]+1)*(array.shape[1]-kernel.shape[1]+1))

start=time.time()
feature=np.sum(np.multiply(grid,grid_kernel),axis=1)

lst=np.where(feature==0)

end=time.time()
print("time taken: "+str((end-start)*1000)+"ms")
#print(tem)