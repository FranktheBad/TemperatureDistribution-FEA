nbele = 20;
nbpt = nbele+1;
ta = 2/nbele;
/* Point      1 */
Point(newp) = {-1.0,-1.0,0.0,ta};
/* Point      2 */
Point(newp) = {1.0,-1.0,0.0,ta};
/* Point      3 */
Point(newp) = {1.0,1.0,0.0,ta};
/* Point      4 */
Point(newp) = {-1.0,1.0,0.0,ta};

Point(5) = {1, 0, 0,ta};
Point(6) = {-1, 0.0, 0,ta};

Line(9) = {1, 2};
Line(10) = {2, 5};
Line(3) = {5, 6};
Line(12) = {6, 1};
Line(20) = {5, 3};
Line(11) = {3, 4};
Line(22) = {4, 6};

Line Loop(8) = {11, 22, -3, 20};
Plane Surface(22) = {8};
Line Loop(10) = {9, 10, 3, 12};
Plane Surface(21) = {10};


Transfinite Surface {21} = {1, 2, 5, 6};
Transfinite Surface {22} = {6, 5, 3, 4};


Physical Point   (1)  = {1} ;
Physical Point   (2)  = {2} ;
Physical Point   (3)  = {3} ;
Physical Point   (4)  = {4} ;

Physical Line    (101)  = {9};
Physical Line    (102)  = {10,20};
Physical Line    (103)  = {11};
Physical Line    (104)  = {12,22};

Physical Surface (1000)  = {21} ;
Physical Surface (2000)  = {22} ;

