#include <cstdlib>
#include <iostream>
#include "Surface.h"

using namespace std;


int main(int argc, char** argv) {

  double x, y;
  cout <<"x, y?" << endl;
  cin >> x >> y;
  Point p1(x, y);
  Hexagon h1(0., 0., 10., 0, "Test Hexagon");
  Circle  c1(0., 0., 10., 0, "Test Circle");

  cout << "Evaluating point " << p1.toString() << endl;

  cout << "hexagon: " << h1.evaluate(&p1) << endl;
  cout << " circle: " << c1.evaluate(&p1) << endl;


  return 0;
}

