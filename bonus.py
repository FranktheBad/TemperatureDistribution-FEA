import numpy as np
import matplotlib.pyplot as plt

def exactsoln_bonus(x,K1,K2,qN):
    if -1<=x and x<=0:
        exact_soln=(qN/K1)*(x+1)
    else:
        exact_soln=(qN*x/K2)+(qN/K1)
    
    return exact_soln

x_value=np.linspace(-1,1,100)
y_value=np.linspace(-1,1,100)
X,Y=np.meshgrid(x_value,y_value)
U=np.zeros_like(X)
for i in range(U.shape[0]):
    U[i]=exactsoln_bonus(x=x_value[i],K1=2,K2=10,qN=5)
#U=np.transpose(U)
plt.contourf(X,Y,U, cmap='plasma')
plt.show
