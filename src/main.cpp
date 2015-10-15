#include <cstdlib>
#include <iostream>
#include "Surface.h"

using namespace std;


int main(int argc, char** argv) {

  double x, y, phi;
//  cout <<"x, y?" << endl;
//  cin >> x >> y;
  x = -20;
  y = -20;
  phi = 5 * M_PI / 180.;
  Point p1(x, y), *pts;
  pts = new Point[2];
  Hexagon h1(0., 0., 10., 0, "Test Hexagon");
  Circle  c1(0., 0., 10., 0, "Test Circle");

//  cout << "Evaluating point " << p1.toString() << endl;
//
//  cout << "hexagon: " << h1.evaluate(&p1) << endl;
//  cout << " circle: " << c1.evaluate(&p1) << endl;
  
  cout << "Intersections line trough point " << p1.toString() << " and direction " << phi << endl;

  cout << "hexagon: " << h1.intersection(&p1, phi, pts) << endl;
  cout << " circle: " << c1.intersection(&p1, phi, pts) << endl;

  delete [] pts;
  return 0;
}

