# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Contact : Gregory LEGRAIN - gregory.legrain@ec-nantes.fr
#

# This file contains some helpers for sparse matrices
# in order to avoid to clutter the code in solveFE.py


import numpy as np


# Preallocate sparse data structure
def preallocateSparse(mesh, twoDEltType, dofManager):
    
    manipDofs = 0
    
    # Loop on the 2D elements
    for iel in range(mesh.nElmts[twoDEltType]):
        
        # Ask for the connectivity of element iel
        connecElt, physElt = mesh.getElementConnectivityAndPhysNumber(twoDEltType, iel)
        
        #Look for the number of dofs that have to be manipulated
        for i in range(np.size(connecElt)):
            I = dofManager[connecElt[i]]
            if I > -1:
                for j in range(np.size(connecElt)):
                    J = dofManager[connecElt[j]]
                    if J > -1:
                        manipDofs += 1
        
    
    
    # Initialise the sparse data structure
    # manipDofs x 3
    return np.zeros((manipDofs, 3))
