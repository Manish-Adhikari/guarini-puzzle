# Simple representation of Gaurini's puzzle

import numpy as np

a=np.array([[1,0,1],[0,0,0],[2,0,2]])
print('The representational array is:\n ',a)

#implementing the process in the diagram
a[2][1]=a[0][0]
a[1][0]=a[0][2]
a[0][1]=a[2][2]
a[1][2]=a[2][0]

a[0][2]=a[2][1]
a[2][2]=a[1][0]
a[2][0]=a[0][1]
a[0][0]=a[1][2]

a[1][0]=a[0][2]
a[0][1]=a[2][2]
a[1][2]=a[2][0]
a[2][1]=a[0][0]

a[2][2]=a[1][0]
a[2][0]=a[0][1]
a[0][0]=a[1][2]
a[0][2]=a[2][1]

#Dummy array
s=np.array([[1,0,1],[0,0,0],[1,0,1]])
a=a*s
print('Solved array:\n',a)
