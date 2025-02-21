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

Point(5) = {0, 0, 0,ta};
Point(6) = {0.4, 0.0, 0,ta};
Point(7) = {-0.4, 0.0, 0,ta};
Point(8) = {0., 0.4, 0,ta};
Point(9) = {0., -0.4, 0,ta};

Line(9)  = {1,2};
Line(10) = {2,3};
Line(11) = {4,3};
Line(12) = {1,4};

Circle(122) = {6, 5, 8};
Circle(123) = {8, 5, 7};
Circle(124) = {7, 5, 9};
Circle(125) = {9, 5, 6};
  
Line Loop(18) = {11, -10, -9, 12};
Line Loop(19) = {122, 123, 124, 125};
Plane Surface(21) = {18, 19};



Physical Point   (1)  = {1} ;
Physical Point   (2)  = {2} ;
Physical Point   (3)  = {3} ;
Physical Point   (4)  = {4} ;

Physical Line    (101)  = {9};
Physical Line    (102)  = {10};
Physical Line    (103)  = {11};
Physical Line    (104)  = {12};

Physical Surface (1000)  = {21} ;
