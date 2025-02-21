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

# ----------------------------------------------------------------------
#  COMMAND-LINE VERSION...
# ----------------------------------------------------------------------

# Parsing
import argparse
import tomli
# Import finite element solver function
from solveFE import solveFE

# Parse command line arguments
parser = argparse.ArgumentParser(description='Command line interface to testFE.')
parser.add_argument('toml_name', default='validation2stage4.toml', nargs='?', help='path to the toml config file (default value=test.toml)')
args = parser.parse_args()

# Parse config file
with open(args.toml_name, mode='rb') as fp:
    config = tomli.load(fp)


#Mesh file
meshName = config['mesh']['name']

# Setup the problem we want to solve
# Neumann boundary conditions : as a dictionary (~ map) (physicalId: qN value)
BCNs = {}
for bck, bcv in config['BCs_Neumann'].items():
    BCNs[bcv['physId']] = bcv['value']
    


# Dirichlet boundary conditions for lines : as a dictionary (~ map) (physicalId: uD value)
BCD_lns = {}
for bck, bcv in config['BCs_Dirichlet_line'].items():
    BCD_lns[bcv['physId']] = bcv['value']


# Dirichlet boundary conditions for nodes : as a dictionary (~ map) (physicalId: uD value)
BCD_nds = {}
for bck, bcv in config['BCs_Dirichlet_nodes'].items():
    BCD_nds[bcv['physId']] = bcv['value']

# Conductivity (isotropic for example) : as a dictionary (~ map) (physicalId: Kfourier)
conductivities = {}
for condk, condv in config['Conductivities'].items():
    conductivities[condv['physId']] = condv['value']

# Source term (constant for example) : as a lambda function, depending on
# the phydical coordinates and (if necessary) the physical id of the element.
# xyz is assumed to be a numpy array
sourceTerm = lambda xyz, physdom: 0.

for srck, srcv in config['Source'].items():
    if srcv['sourceType'] != 'constant':
        raise NotImplementedError('Only constant source terms are handled through the CLI')
    else:
        sourceTerm = lambda xyz, physdom: srcv['value']


exportName = config['export']['exportName']


# Call the resolution routine
# Additional parameters :
# useSparse = True if you experience memory issues
# verboseOutput = False if you want minimal verbosity
useSparse = config['solver_options']['useSparse']
verboseOutput = config['solver_options']['verboseOutput']
solveFE(meshName, conductivities, BCNs, BCD_lns, BCD_nds, sourceTerm, exportName, useSparse, verboseOutput)


