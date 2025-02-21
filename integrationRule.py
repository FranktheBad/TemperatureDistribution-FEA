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

import numpy as np
from numpy import sqrt

class quadratureRule :

    def __init__(self):
        self.nbQuadPoints = 0;
        return

    def getNbQuadraturePoints(self):
        return self.nbQuadPoints


class gaussQuadratureRule1D(quadratureRule) :

    def __init__(self):
        self.nbPdG = 3

        #Le maxi par defaut:
        self.nbQuadPoints = self.nbPdG
        # assert(nbPdG<4)
        self.gaussW = [np.array([2.]), np.array([1.,1.]), np.array([5./9.,8./9.,5./9.])]
        self.gaussPos = [np.array([0.]), np.array([-sqrt(1./3.),sqrt(1./3.)]), np.array([-sqrt(3./5.),0.,sqrt(3./5.)])]

    def getQuadraturePointsFor(self, nb):
        assert(nb < self.nbPdG + 1)
        return self.gaussPos[nb-1]

    def getQuadratureWeightsFor(self, nb):
        assert (nb < self.nbPdG + 1)
        return self.gaussW[nb-1]

    def setNbQuadPoints(self, nbp):
        self.nbQuadPoints = nbp;


    def getQuadraturePoints(self):
        return self.gaussPos[self.nbQuadPoints-1]

    def getQuadratureWeights(self):
        return self.gaussW[self.nbQuadPoints-1]

class gaussQuadratureRuleTriangle(quadratureRule) :

    def __init__(self):
        self.nbPdG = np.array([1,3,4,6,7,12,13,16])

        #Le maxi par defaut:
        self.nbQuadPoints = 3
        # assert(nbPdG<4)
        self.gaussW = {1: 0.5 * np.array([1.]),
                       3: 0.5 * np.array([.333333333333333,.333333333333333,.333333333333333]),
                       4: 0.5 * np.array([-0.5625,.520833333333333,.520833333333333,.520833333333333]),
                       6: 0.5 * np.array([0.109951743655322,0.109951743655322,0.109951743655322,0.223381589678011,0.223381589678011,0.223381589678011]),
                       7: np.array([]),
                       12: np.array([]),
                       13: np.array([]),
                       16: np.array([])}
        self.gaussPos = {1: np.array([.333333333333333,.333333333333333]),
                         3: [np.array([0.16666666666666,0.166666666666]), np.array([0.66666666666666,0.1666666666666]), np.array([0.16666666666666,0.6666666666666])],
                         4:[np.array([0.333333333333333,0.3333333333333333]), np.array([0.6,0.2]), np.array([0.2,0.6]), np.array([0.2,0.2])],
                         6: [np.array([0.816847572980459,0.091576213509771]), np.array([0.091576213509771,0.816847572980459]), np.array([0.091576213509771,0.091576213509771]),
                             np.array([0.108103018168070,0.445948490915965]), np.array([0.445948490915965,0.10810301816807]), np.array([0.445948490915965,0.445948490915965])]}

    def getQuadraturePointsFor(self, nb):
        assert(nb < self.nbQuadPoints + 1)
        return self.gaussPos[nb-1]

    def getQuadratureWeightsFor(self, nb):
        assert (nb < self.nbQuadPoints + 1)
        return self.gaussW[nb]

    def setNbQuadPoints(self, nbp):
        self.nbQuadPoints = nbp;


    def getQuadraturePoints(self):
        return self.gaussPos[self.nbQuadPoints]

    def getQuadratureWeights(self):
        return self.gaussW[self.nbQuadPoints]



class gaussQuadratureRuleQuad(quadratureRule) :

    def __init__(self):
        self.nbPdG = np.array([1,4,9])

        #4 par defaut:
        self.nbQuadPoints = 9
        # assert(nbPdG<4)
        usqt = 1./sqrt(3.)
        sqtc = sqrt(3./5.)
        self.gaussW = {1: np.array([4.]),
                       4: np.array([1., 1., 1., 1.]),
                       9: 1./81. * np.array([25., 40., 25., 40., 64., 40., 25., 40., 25.]),
                       }
        self.gaussPos = {1: np.array([0., 0.]),
                         4:[np.array([-usqt, -usqt]), np.array([usqt, -usqt]), np.array([-usqt, usqt]), np.array([usqt, usqt])],
                         9: [np.array([-sqtc, -sqtc]), np.array([0., -sqtc]), np.array([sqtc, -sqtc]),
                             np.array([-sqtc, 0.]), np.array([0.,0.]), np.array([sqtc, 0.]),
                             np.array([-sqtc, sqtc]), np.array([0., sqtc]), np.array([sqtc, sqtc])]}

    def getQuadraturePointsFor(self, nb):
        assert(nb < self.nbQuadPoints + 1)
        return self.gaussPos[nb-1]

    def getQuadratureWeightsFor(self, nb):
        assert (nb < self.nbQuadPoints + 1)
        return self.gaussW[nb]

    def setNbQuadPoints(self, nbp):
        self.nbQuadPoints = nbp;


    def getQuadraturePoints(self):
        return self.gaussPos[self.nbQuadPoints]

    def getQuadratureWeights(self):
        return self.gaussW[self.nbQuadPoints]




# return init + the integrale of the function f on the quadrangle given as input by array xy
#  xy is an array containing the  coordinates of the four points of the quadrangle, 
#  xy[i,:] is a 1d array containing the coordinate of node i.
#     3---2
#     |   |
#     0---1
#  A nine point gauss rule on a reference quadrangular is used.
def integrateOnQuadrangle(xy, f, init ):
    mapping = lambda s,t : xy[0,:]*(1.-s)*(1.-t)/4.+xy[1,:]*(1.+s)*(1.-t)/4. + xy[2,:]*(1.+s)*(1.+t)/4.+xy[3,:]*(1.-s)*(1.+t)/4. 
    gs      = lambda s,t :  -xy[0,:]*(1.-t)/4. + xy[1,:]*(1.-t)/4. + xy[2,:]*(1.+t)/4.-xy[3,:]*(1.+t)/4.
    gt      = lambda s,t :  -xy[0,:]*(1.-s)/4. - xy[1,:]*(1.+s)/4. + xy[2,:]*(1.+s)/4.+xy[3,:]*(1.-s)/4.
    J       = lambda s,t :  abs(gs(s,t)[0]*gt(s,t)[1] - gs(s,t)[1]*gt(s,t)[0])
    rule = gaussQuadratureRuleQuad()
    res = init
    for i in range(rule.getNbQuadraturePoints()):
        s,t = rule.getQuadraturePoints()[i]
        w   = rule.getQuadratureWeights()[i]
        x,y = mapping(s,t)
        j =   J(s,t)
        res = res + w*j *f(x,y)
    return res      

