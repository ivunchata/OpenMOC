#include <cstdlib>
#include <iostream>
#include "Surface.h"

using namespace std;


int main(int argc, char** argv) {
  
  while(true)
  {
    double x, y;
    cout <<"x, y?" << endl;
    cin >> x >> y;
//    x = 0.; y = 10.11;
    Point p1(x, y);
    Hexagon h1(0., 0., 10., 0, "Test Hexagon");
    Circle  c1(0., 0., 10., 0, "Test Circle");  

    //  cout << h1.toString() << endl;
    //  cout << c1.toString() << endl;

    cout << "Evaluating point " << p1.toString() << endl;

    cout << "hexagon: " << h1.evaluate(&p1) << endl;
    cout << " circle: " << c1.evaluate(&p1) << endl;

    if (x==-2605)
      break;
    
  }
  
  return 0;
}

