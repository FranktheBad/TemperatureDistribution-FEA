import numpy as np
import matplotlib.pyplot as plt
def solnexact(x,y):
    exact_soln=0
    for i in range(1,100,2):
        for j in range(1,100,2):
            soln=(64/(np.pi**4*(i**2+j**2)*i*j))*np.sin((i*np.pi*(x+1))/2)*np.sin((j*np.pi*(y+1))/2)
            exact_soln+=soln
    return exact_soln

x_values=np.linspace(-1, 1, 100)
y_values=np.linspace(-1,1,100)
X,Y=np.meshgrid(x_values, y_values)
U_exact=solnexact(x=X,y=Y)
plt.contourf(X,Y,U_exact, cmap='coolwarm')
plt.colorbar(label='u(x,y)')
plt.show()