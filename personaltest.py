from rect4ThermalDirect import computeKe, computeFve

import numpy as np

square_array=[[0,0],[0,1],[1,1],[1,0]]
square_array=np.array(square_array)
con_K=1 #conductivity

sourceTerm= lambda x,y: 1
physElt=1000
KE_matrix=computeKe(square_array,con_K)
Fve_array= computeFve(square_array, sourceTerm, physElt)
print(Fve_array)