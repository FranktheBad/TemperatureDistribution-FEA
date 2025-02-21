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

# Prefix numpy commands with np
import numpy as np

# Import gmsh parser, and prefix it with gmp
import gmshParser as gmp

# Import rect4Thermal functions
from rect4ThermalDirect import computeKe, computeFve, computeFNe

# Import export functions
from export import exportSolutionToGmsh, exportSolutionScalarToGmsh

# For sparse matrices
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
from sparseUtils import preallocateSparse


def solveFE(meshName, conductivities, BCNs, BCD_lns, BCD_nds, sourceTerm, exportName, useSparse = False, verboseOutput = True):
    mesh = gmp.Mesh()
    mesh.read_msh(meshName)

    # ------------------------------ Showcase for the mesh

    # DefineTargetElements types :
    oneDEltType = gmp.edgeElementTypeId
    twoDEltType = gmp.quadLinElementTypeId
    
    if verboseOutput:
        # ------ Loop on 1D elements and plot their nodes ids and location
        if oneDEltType in mesh.nElmts:
            for iel in range(mesh.nElmts[oneDEltType]):
                
                # Ask for the connectivity of element iel
                connecElt, physElt = mesh.getElementConnectivityAndPhysNumber(oneDEltType, iel)
                
                # Print physical number and connectivity table
                print('Element', iel, 'Physical id', physElt, 'Connectivity', connecElt)
                
                # Print the nodes coordinates
                for ivert in range(np.size(connecElt)):
                    xyzVert = mesh.getVertexCoordinates(connecElt[ivert])
                    print('Vertex', connecElt[ivert], 'XYZ', xyzVert)
                    
        # ------ We do the same for the 2D elements.
        # Notice that the code is (almost) exactly the same : we could create a function for that.
        for iel in range(mesh.nElmts[twoDEltType]):
                        
            # Ask for the connectivity of element iel
            connecElt, physElt = mesh.getElementConnectivityAndPhysNumber(twoDEltType, iel)
            
            # Print physical number and connectivity table
            print('Element', iel, 'Physical id', physElt, 'Connectivity', connecElt)
            
            # Print the nodes coordinates
            for ivert in range(np.size(connecElt)):
                xyzVert = mesh.getVertexCoordinates(connecElt[ivert])
                print('Vertex', connecElt[ivert], 'XYZ', xyzVert)

    #
    # ------------------------------ Get the ids of the prescribed nodes
    prescribedNodes = []

    # ... and their values
    prescribedValues = []

    # We add BCD_nds and the nodes of BCD_lns
    # First we begin with the nodes with a physical number
    if gmp.standaloneNodeTypeId in mesh.Elmts:
        for iNode in range(np.size(mesh.Elmts[gmp.standaloneNodeTypeId][0])):

            physNode = mesh.Elmts[gmp.standaloneNodeTypeId][0][iNode]
            idNode = mesh.Elmts[gmp.standaloneNodeTypeId][1][iNode]

            # Check if physNode is in BCD_nds
            if physNode in BCD_nds:
                prescribedValues = prescribedValues + [BCD_nds[physNode]]
                prescribedNodes = prescribedNodes + [idNode[0]]

    # We add the nodes of BCD_lns
    # Loop on the line elements, then add to prescribedNodes those whose physical id is in BCD_lns
    if oneDEltType in mesh.nElmts:
        for iel in range(mesh.nElmts[oneDEltType]):

            # Ask for the connectivity of element iel
            connecElt, physElt = mesh.getElementConnectivityAndPhysNumber(oneDEltType, iel)

            # Check if the phys id is in BCD_lns
            if physElt in BCD_lns:
                prescribedNodes.append(connecElt[0])
                prescribedNodes.append(connecElt[1])

                prescribedValues.append(BCD_lns[physElt])
                prescribedValues.append(BCD_lns[physElt])

    # Remove duplicates
    prescribedNodes, uniqueIdxs = np.unique(prescribedNodes, return_index=True)
    prescribedValues = np.array(prescribedValues)[uniqueIdxs]

    #
    # ------------------------------ Fill dofManager
    dofManager = np.zeros(mesh.getNumVertices(), dtype=int)

    # Do the numbering
    # Mark the prescribed values as -1 (only if there are prescribed values !)
    if len(prescribedValues):
        dofManager[prescribedNodes] = -1

    numDofs = 0
    for i in range(dofManager.shape[0]):
        if not dofManager[i]:
            dofManager[i] = numDofs
            numDofs += 1

    
    # Define the matrix and force vectors
    F = np.zeros(numDofs)
    
    # Initialization is done in a different manner depending if a sparse latrix is used or not.
    if not useSparse:
        K = np.zeros((numDofs, numDofs))
    else:
        dataAssembly = preallocateSparse(mesh, twoDEltType, dofManager)
        isp = 0
    
    print('-------------- Initialized --------------')
    #
    # ------------------------------ Assembly process
    print('-------------- Begin Assembly --------------')
    # Loop on the 2D elements
    for iel in range(mesh.nElmts[twoDEltType]):

        # Ask for the connectivity of element iel
        connecElt, physElt = mesh.getElementConnectivityAndPhysNumber(twoDEltType, iel)
        
        #Get vertex coordinates
        xyzVerts = np.zeros((np.size(connecElt), 3))
        
        for ivert in range(np.size(connecElt)):
            xyzVerts[ivert,:] = mesh.getVertexCoordinates(connecElt[ivert])

        # Get the actual conductivity of the element 
        conductivity = conductivities[physElt]

        # Compute the elementary stiffness matrix
        # This a possible solution (not the only one)
        Ke = computeKe(xyzVerts, conductivity)
        

        # Compute the volume force vector
        # This a possible solution (not the only one)
        Fve = computeFve(xyzVerts, sourceTerm, physElt)

        # Assemble
        for i in range(np.size(connecElt)):
            I = dofManager[connecElt[i]]

            if I > -1:
                for j in range(np.size(connecElt)):
                    J = dofManager[connecElt[j]]

                    if J > -1:
                        
                        # Assembly is not done the same way for sparse and dense matrices
                        # to ensure good performances in the latter case
                        if not useSparse:
                            K[I, J] += Ke[i, j]
                        else:
                            dataAssembly[isp,:] = [Ke[i, j], I, J]
                            isp += 1
                    else:
                        F[I] -= Ke[i, j] * prescribedValues[np.argwhere(prescribedNodes == connecElt[j])][0][0]
                        
                # We assemble here the force vector
                F[I] += Fve[i]
    
    # Sparse case : acutally fill the matrix
    if useSparse:
        K = coo_matrix((dataAssembly[:,0], (dataAssembly[:,1], dataAssembly[:,2])), shape=(numDofs, numDofs)).tocsc()
        # Free memory
        dataAssembly = None
    
    
    # Neumann force vector :
    # Loop on boundary elements (only if they exist !)
    if oneDEltType in mesh.nElmts.keys():
        for iel in range(mesh.nElmts[oneDEltType]):
            
            # Ask for the connectivity of element iel
            connecElt, physElt = mesh.getElementConnectivityAndPhysNumber(oneDEltType, iel)
            
            #Get vertex coordinates
            xyzVerts = np.zeros((np.size(connecElt), 3))
        
            for ivert in range(np.size(connecElt)):
                xyzVerts[ivert,:] = mesh.getVertexCoordinates(connecElt[ivert])
            
            # Check if there is a boundary condition
            if physElt in BCNs:
                flux = BCNs[physElt]
                
                FeN = computeFNe(xyzVerts, flux)
                
                # Assembly
                for i in range(np.size(connecElt)):
                    I = dofManager[connecElt[i]]
                    if I > -1:
                        F[I] += FeN[i]

    print('-------------- Assembly Done --------------')
    # ------------------------------  Solving the system
    print('-------------- Solve the linear system --------------')
    if not useSparse:
        U = np.linalg.solve(K, F)
    else:
        U = spsolve(K, F)
    print('-------------- Done --------------')

    # ------------------------------  Save results...
    print('-------------- Export --------------')
    fileout = open(exportName, 'w')
    #exportSolutionToGmsh(fileout, dofManager, mesh, U, prescribedNodes, prescribedValues)
    exportSolutionScalarToGmsh(fileout, dofManager, mesh, twoDEltType, U, prescribedNodes, prescribedValues)
    fileout.close()

    return

