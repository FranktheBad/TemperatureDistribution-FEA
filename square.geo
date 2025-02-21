//Mesh.ElementOrder = 2;
//Mesh.SecondOrderIncomplete = 1;

dens = 4.;
nbe = 10;

Point(1) = {-1, -1, 0, dens};
Point(2) = {-1, 1, 0, dens};
Point(3) = {1, 1, 0, dens};
Point(4) = {1, -1, 0, dens};
Line(1) = {1, 4};
Line(2) = {4, 3};
Line(3) = {3, 2};
Line(4) = {2, 1};
Line Loop(5) = {4, 1, 2, 3};


Transfinite Line {4, 1, 2, 3} = nbe+1 Using Progression 1;
Plane Surface(9) = {5};
Transfinite Surface {9} = {1, 4, 3, 2};
Recombine Surface {9};


Physical Line(101) = {1};
Physical Line(102) = {2};
Physical Line(103) = {3};
Physical Line(104) = {4};
Physical Point(1) = {1};
Physical Point(2) = {4};
Physical Point(3) = {3};
Physical Point(4) = {2};
Physical Surface(1000) = {9};

