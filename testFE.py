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

#Import finite element solver function
from solveFE import solveFE

#Mesh file
meshName = 'squareBimat20x20.msh'

# Setup the problem we want to solve
# Neumann boundary conditions : as a dictionary (~ map) (physicalId: qN value)
BCNs = {101:5}

# Dirichlet boundary conditions for lines : as a dictionary (~ map) (physicalId: uD value)
BCD_lns = {103:0}


# Dirichlet boundary conditions for nodes : as a dictionary (~ map) (physicalId: uD value)
BCD_nds = {}

# Conductivity (isotropic for example) : as a dictionary (~ map) (physicalId: Kfourier)
conductivities = {1000:10, 2000:1}

# Source term (constant for example) : as a lambda function, depending on
# the phydical coordinates and (if necessary) the physical id of the element.
# xyz is assumed to be a numpy array
sourceTerm = lambda xyz, physdom: 0.

exportName = 'bonusquestion.pos'


# Call the resolution routine
# Additional parameters :
# useSparse = True if you experience memory issues
# verboseOutput = False if you want minimal verbosity
useSparse = False
verboseOutput = True
solveFE(meshName, conductivities, BCNs, BCD_lns, BCD_nds, sourceTerm, exportName, useSparse, verboseOutput)


