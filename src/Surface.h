/**
 * @file Surface.h
 * @details The Surface class and subclasses.
 * @date January 9, 2012
 * @author William Boyd, MIT, Course 22 (wboyd@mit.edu)
 */


#ifndef SURFACE_H_
#define SURFACE_H_

#ifdef __cplusplus
#ifdef SWIG
#include "Python.h"
#endif
#include "constants.h"
#include "LocalCoords.h"
#include "boundary_type.h"
#include <limits>
#include <map>
#include <vector>
#include <algorithm>
#endif


/* Forward declarations to resolve circular dependencies */
class LocalCoords;
class Cell;


int surf_id();
void reset_surf_id();


/**
 * @enum surfaceType
 * @brief The types of surfaces supported by OpenMOC.
 */
enum surfaceType {
  /** A general plane perpendicular to the 2D xy plane */
  PLANE,

  /** A circle with axis parallel to the z-axis */
  CIRCLE,

  /** A plane perpendicular to the x-axis */
  XPLANE,

  /** A plane perpendicular to the y-axis */
  YPLANE,

  /** A plane perpendicular to the z-axis */
  ZPLANE,

  /** A generalized quadratic surface */
  QUADRATIC,

  /** A hexagon with axis parallel to the z-axis */
  HEXAGON
};



/**
 * @class Surface Surface.h "src/Surface.h"
 * @brief Represents a general Surface in the 2D xy-plane
 * @details The Surface class and its subclasses are used to define the
 *          geometry for an OpenMOC simulation using a constructive solid
 *          geometry (CSG) formalism. Surfaces are used during ray tracing
 *          of charateristic tracks across the geometry.
 */
class Surface {

protected:

  /** A static counter for the number of Surfaces in a simulation */
  static int _n;

  /** A monotonically increasing unique ID for each Surface created */
  int _uid;

  /** A user-defined id for each Surface created */
  int _id;

  /** A user-defined name for the Surface */
  char* _name;

  /** The type of Surface (ie, XPLANE, CIRCLE, etc) */
  surfaceType _surface_type;

  /** The type of boundary condition to be used for this Surface
   *  (ie, VACUUM or REFLECTIVE) */
  boundaryType _boundary_type;

  /* Vector of neighboring Cells */
  std::map<int, std::vector<Cell*>* > _neighbors;

public:
  Surface(const int id=0, const char* name="");
  virtual ~Surface();

  int getUid() const;
  int getId() const;
  char* getName() const;
  surfaceType getSurfaceType();
  boundaryType getBoundaryType();

  /**
   * @brief Returns the minimum x value for one of this Surface's halfspaces.
   * @param halfspace the halfspace of the Surface to consider
   * @return the minimum x value
   */
  virtual double getMinX(int halfspace) = 0;

  /**
   * @brief Returns the maximum x value for one of this Surface's halfspaces.
   * @param halfspace the halfspace of the Surface to consider
   * @return the maximum x value
   */
  virtual double getMaxX(int halfspace) = 0;

  /**
   * @brief Returns the minimum y value for one of this Surface's halfspaces.
   * @param halfspace the halfspace of the Surface to consider
   * @return the minimum y value
   */
  virtual double getMinY(int halfspace) = 0;

  /**
   * @brief Returns the maximum y value for one of this Surface's halfspaces.
   * @param halfspace the halfspace of the Surface to consider
   * @return the maximum y value
   */
  virtual double getMaxY(int halfspace) = 0;

  /**
   * @brief Returns the minimum z value for one of this Surface's halfspaces.
   * @param halfspace the halfspace of the Surface to consider
   * @return the minimum z value
   */
  virtual double getMinZ(int halfspace) = 0;

  /**
   * @brief Returns the maximum z value for one of this Surface's halfspaces.
   * @param halfspace the halfspace of the Surface to consider
   * @return the maximum z value
   */
  virtual double getMaxZ(int halfspace) = 0;

  void setName(const char* name);
  void setBoundaryType(const boundaryType boundary_type);
  void addNeighborCell(int halfspace, Cell* cell);

  /**
   * @brief Evaluate a Point using the Surface's potential equation.
   * @details This method returns the values \f$ f(x,y) \f$ for the potential
   *          function \f$f\f$ representing this Surface.
   * @param point a pointer to the Soint of interest
   * @return the value of Point in the Plane's potential equation.
   */
  virtual double evaluate(const Point* point) const = 0;

  /**
   * @brief Finds the intersection Point with this Surface from a given
   *        Point and trajectory defined by an angle.
   * @param point pointer to the Point of interest
   * @param angle the angle defining the trajectory in radians
   * @param points pointer to a Point to store the intersection Point
   * @return the number of intersection Points (0 or 1)
   */
  virtual int intersection(Point* point, double angle, Point* points) = 0;

  bool isPointOnSurface(Point* point) const;
  bool isCoordOnSurface(LocalCoords* coord);
  double getMinDistance(Point* point, double angle);

  /**
   * @brief Converts this Surface's attributes to a character array.
   * @details The character array returned conatins the type of Surface (ie,
   *          PLANE) and the coefficients in the potential equation.
   * @return a character array of this Surface's attributes
   */
  virtual std::string toString() = 0;

  void printString();
};


/**
 * @class Plane Surface.h "src/Surface.h"
 * @brief Represents a Plane perpendicular to the xy-plane.
 */
class Plane: public Surface {

protected:

  /** The coefficient for the linear term in x */
  double _A;

  /** The coefficient for the linear term in y */
  double _B;

  /** The constant offset */
  double _C;

  /** The Plane is a friend of class Surface */
  friend class Surface;

  /** The Plane is a friend of class Circle */
  friend class Circle;

public:

  Plane(const double A, const double B, const double C,
        const int id=0, const char* name="");
  Plane(const Plane &);

  double getMinX(int halfspace);
  double getMaxX(int halfspace);
  double getMinY(int halfspace);
  double getMaxY(int halfspace);
  double getMinZ(int halfspace);
  double getMaxZ(int halfspace);
  double getA();
  double getB();
  double getC();

  double evaluate(const Point* point) const;
  int intersection(Point* point, double angle, Point* points);

  std::string toString();
};


/**
 * @class XPlane Surface.h "src/Surface.h"
 * @brief Represents a Plane perpendicular to the x-axis.
 */
class XPlane: public Plane {

private:

  /** The location of the XPlane along the x-axis */
  double _x;

public:
  XPlane(const double x, const int id=0, const char* name="");

  void setX(const double x);

  double getX();
  double getMinX(int halfspace);
  double getMaxX(int halfspace);

  std::string toString();
};


/**
 * @class YPlane Surface.h "src/Surface.h"
 * @brief Represents a Plane perpendicular to the y-axis.
 */
class YPlane: public Plane {

private:

  /** The location of the YPlane along the y-axis */
  double _y;

public:
  YPlane(const double y, const int id=0, const char* name="");

  void setY(const double y);

  double getY();
  double getMinY(int halfspace);
  double getMaxY(int halfspace);

  std::string toString();
};


/**
 * @class ZPlane Surface.h "src/Surface.h"
 * @brief Represents a Plane perpendicular to the z-axis.
 */
class ZPlane: public Plane {

private:

  /** The location of the ZPlane along the z-axis */
  double _z;

public:
  ZPlane(const double z, const int id=0, const char* name="");

  void setZ(const double z);

  double getZ();
  double getMinZ(int halfspace);
  double getMaxZ(int halfspace);

  std::string toString();
};


/**
 * @class Circle Surface.h "src/Surface.h"
 * @brief Represents a Circle in the xy-plane.
 */
class Circle: public Surface {

private:

  /** A 2D point for the Circle's center */
  Point _center;

  /** The Circle's radius */
  double _radius;

  /** The coefficient of the x-squared term */
  double _A;

  /** The coefficient of the y-squared term */
  double _B;

  /** The coefficient of the linear term in x */
  double _C;

  /** The coefficient of the linear term in y */
  double _D;

  /** The constant offset */
  double _E;

  /** The Circle is a friend of the Surface class */
  friend class Surface;

  /** The Circle is a friend of the Plane class */
  friend class Plane;

public:
  Circle(const double x, const double y, const double radius,
         const int id=0, const char* name="");

  double getX0();
  double getY0();
  double getRadius();
  double getMinX(int halfspace);
  double getMaxX(int halfspace);
  double getMinY(int halfspace);
  double getMaxY(int halfspace);
  double getMinZ(int halfspace);
  double getMaxZ(int halfspace);

  double evaluate(const Point* point) const;
  int intersection(Point* point, double angle, Point* points);

  std::string toString();
};

/**
 * @class Hexagon Surface.h "src/Surface.h"
 * @brief Represents a Hexagon in the xy-plane.
 */
class Hexagon: public Surface {

private:

  /** The number of Hexagon sides */
  const size_t _nsides = 6;

  /** A 2D point for the Hexagon's center */
  Point _center;

  /** The Hexagon's radius */
  double _radius;

  /** The Hexagon's inner radius */
  double _iradius;

  std::vector<Plane> _sides;

  /** The Hexagon is a friend of the Surface class */
  friend class Surface;

  /** The Hexagon is a friend of the Plane class */
  friend class Plane;

public:
  Hexagon(const double x, const double y, const double radius,
         const int id=0, const char* name="");
  ~Hexagon();

  double getX0();
  double getY0();
  double getRadius();
  double getMinX(int halfspace);
  double getMaxX(int halfspace);
  double getMinY(int halfspace);
  double getMaxY(int halfspace);
  double getMinZ(int halfspace);
  double getMaxZ(int halfspace);

  double evaluate(const Point* point) const;
  double evaluate(const Point* point, const size_t line_num) const;
  int intersection(Point* point, double angle, Point* points);

  std::string toString();
};


/**
 * @brief Finds the minimum distance to a Surface.
 * @details Finds the minimum distance to a Surface from a Point with a
 *          given trajectory defined by an angle to this Surface. If the
 *          trajectory will not intersect the Surface, returns INFINITY.
 * @param point a pointer to the Point of interest
 * @param angle the angle defining the trajectory in radians
 * @return the minimum distance to the Surface
 */
inline double Surface::getMinDistance(Point* point, double angle) {

  /* Point array for intersections with this Surface */
  Point intersections[2];

  /* Find the intersection Point(s) */
  int num_inters = this->intersection(point, angle, intersections);
  double distance = INFINITY;

  /* If there is one intersection Point */
  if (num_inters == 1)
    distance = intersections[0].distanceToPoint(point);

  /* If there are two intersection Points */
  else if (num_inters == 2) {
    double dist1 = intersections[0].distanceToPoint(point);
    double dist2 = intersections[1].distanceToPoint(point);

    /* Determine which intersection Point is nearest */
    if (dist1 < dist2)
      distance = dist1;
    else
      distance = dist2;
  }

  return distance;
}


/**
 * @brief Evaluate a Point using the Plane's quadratic Surface equation.
 * @param point a pointer to the Point of interest
 * @return the value of Point in the Plane's quadratic equation
 */
inline double Plane::evaluate(const Point* point) const {
  double x = point->getX();
  double y = point->getY();

  //TODO: does not support ZPlanes
  return (_A * x + _B * y + _C);
}


/**
 * @brief Return the radius of the Circle.
 * @return the radius of the Circle
 */
inline double Circle::getRadius() {
  return this->_radius;
}


/**
 * @brief Evaluate a Point using the Circle's quadratic Surface equation.
 * @param point a pointer to the Point of interest
 * @return the value of Point in the equation
 */
inline double Circle::evaluate(const Point* point) const {
  double x = point->getX();
  double y = point->getY();
  return (_A * x * x + _B * y * y + _C * x + _D * y + _E);
}

/**
 * @brief Return the radius of the Hexagon.
 * @return the radius of the Hexagon
 */
inline double Hexagon::getRadius() {
  return this->_radius;
}


/**
 * @brief Evaluate a Point using the Hexagon's sides Plane equations.
 * @param point a pointer to the Point of interest
 * @return 0.0 if on surface, -1.0 if within the Hexagon, +1.0 otherwise
 */
inline double Hexagon::evaluate(const Point* point) const {
  size_t half_nsides = 0.5 * _nsides;
  double res1, res2;
  for(size_t i = 0; i < half_nsides; ++i)
  {
    res1 = evaluate(point, i);
    if (res1 > 0.0)
      return 1.0;   // outside for i-th side
    res2 = evaluate(point, i + half_nsides);
    if (res2 > 0.0)
      return 1.0;   // outside for opposite side
    if (res1 * res2 == 0.0)
      return 0.0;   // on surface (i-th or opposite)
    // else continue
  }
  return -1.0;  // inside
}


/**
 * @brief Helper function to evaluate a single side
 * @param x the x-coordinate of the point evaluated
 * @param y the y-coordinate of the point evaluated
 * @param line number starting from 0 for top left side
 * @return 0.0 if on the side, +1 if outside of the Hexagon and -1 if inside
 */
inline double Hexagon::evaluate(const Point* point, const size_t side_num) const {
  Point pnt (point->getX(), point->getY());
  if (_sides.at(side_num).isPointOnSurface(&pnt))
  {
    // evaluate adjacent sides
    size_t side_left, side_right;
    if (side_num == 0)
      side_left = _nsides - 1;
    else
      side_left = side_num - 1;
    if (side_num == _nsides)
      side_right = 0;
    else
      side_right = side_num + 1;
    // check whether the evaluated point is on the surface between the adjacent sides
    if ( (_sides.at(side_left).evaluate(point) < 0.0 || _sides.at(side_left).isPointOnSurface(&pnt)) // at or on the correct side of left surface
          &&
         (_sides.at(side_right).evaluate(point) < 0.0 || _sides.at(side_right).isPointOnSurface(&pnt)))// at or on the correct side of right surface
      return 0.0;
    else
      return 1.0;
  }
  else  // not on surface
  {
    if (_sides.at(side_num).evaluate(point) > 0.0)
      return 1.0;   // outside
    else
      return -1.0;  // inside
  }
}


#endif /* SURFACE_H_ */
