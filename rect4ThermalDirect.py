import numpy as np
from integrationRule import integrateOnQuadrangle

# TODO
# Computation of the elementary stiffness matrix Ke
# xyzVerts (INPUT): Coordinates of the nodes of the element (4x3 numpy array)
# conductivity (INPUT): Conductivity on the current element (scalar number).
# Ke (OUTPUT): Elementary stiffness matrix (4x4 numpy array).
def compute_coeff(xyzVerts):
    C_s=[]
    x_s=xyzVerts[:,0]
    y_s=xyzVerts[:,1]
    mat_sys=np.array([[1,1,1,1],x_s,y_s,x_s*y_s]).T
    for i in range(len(mat_sys)):
        rhs=np.zeros((4,1))
        rhs[i]=1
        C_matrix= np.linalg.solve(mat_sys,rhs)
        C_s.append(C_matrix)
    C_s_matrix=np.array(C_s)
    return C_s_matrix



def computeKe(xyzVerts, conductivity):
    
    # Ke_xy is a function that should return the quantity that has to be integrated
    # in order to compute Ke: Ke = integral of Ke_xy on the element
    # NOTE: Ke_xy is a matricial quantity !
    # Set a dummy value for the moment
    def Compute_Be(x, y):
        B_e=np.zeros((2,4))
        C_1=compute_coeff(xyzVerts)[:,1]   
        C_3=compute_coeff(xyzVerts)[:,3]
        C_2=compute_coeff(xyzVerts)[:,2]
        B_e[0,:]=C_1.flatten()+(C_3.flatten()*y)
        B_e[1,:]=C_2.flatten()+(C_3.flatten()*x)
        return B_e
    K=conductivity
    K=np.eye(2)*K
    Ke_xy = lambda x,y:Compute_Be(x,y).T@ K @ Compute_Be(x,y)

    
    # Function to compute the integral of Ke_xy
    # Works even if the element is not square
    # Used as a black box here !
    Ke = np.zeros((4, 4)) # Initialize Ke
    Ke = integrateOnQuadrangle(xyzVerts[:,:2], Ke_xy, Ke) # Integrate Ke_xy on the element

    return Ke



# TODO
# Computation of the elementary volume force vector Fve (source term effects)
# xyzVerts (INPUT): Coordinates of the nodes of the element (4x3 numpy array)
# sourceTerm (INPUT): Source term evaluator.
# physElt (INPUT): physical id of the current element (integer)
# Fe (OUTPUT): Elementary force vector (4 components numpy array)
#
#
# NOTE: The evaluator is a function of two variables: (xyz, physElt).
# xyz = numpy array containing the coordinates of the evaluation point
# physElt = physical id of the current element (integer)
def computeFve(xyzVerts, sourceTerm, physElt):
    
    # Similar to the approach used for the stiffness matrix
    # Fve_xy is a function that should return the quantity that has to be integrated
    # in order to compute Fve: Fve = integral of Fve_xy on the element
    # NOTE: Fve_xy is a vectorial quantity !
    # Set a dummy value for the moment
    def compute_Ne(x,y):
        C_0=compute_coeff(xyzVerts)[:,0]
        C_1=compute_coeff(xyzVerts)[:,1]   
        C_3=compute_coeff(xyzVerts)[:,3]
        C_2=compute_coeff(xyzVerts)[:,2]
        Ne=C_0+(C_1*x)+(C_2*y)+(C_3*x*y)
        Ne=Ne.flatten()

        return Ne
    def Fve_xy(x,y):
        Ne=compute_Ne(x,y)
        return sourceTerm(np.array([x,y,0.]),physElt)*Ne
    # Fve_xy = lambda x,y: np.ones(4)
    # Function to compute the integral of Fve_xy
    # Works even if the element is not square
    # Used as a black box here !
    Fve = np.zeros(4) # Initialize Fve
    Fve = integrateOnQuadrangle(xyzVerts[:,:2], Fve_xy, Fve) # Integrate

    return Fve

# TODO
# Computation of the elementary Neumann force vector FNe
# xyzVerts (INPUT): Coordinates of the nodes of the edge (2x3 numpy array)
# flux (INPUT): Value of the prescribed flux on the current edge (scalar number)
# FNe (OUTPUT): Elementary force vector (2 components numpy array)
def computeFNe(xyzVerts, flux):
    le=np.linalg.norm(xyzVerts[1]-xyzVerts[0])
    # Set a dummy value for the moment
    FNe = np.ones(2)   

    return flux*(le/2)*FNe
