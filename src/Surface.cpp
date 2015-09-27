#include "Surface.h"

int Surface::_n = 0;

static int auto_id = 10000;

/**
 * @brief Returns an auto-generated unique surface ID.
 * @details This method is intended as a utility mehtod for user's writing
 *          OpenMOC input files. The method makes use of a static surface
 *          ID which is incremented each time the method is called to enable
 *          unique generation of monotonically increasing IDs. The method's
 *          first ID begins at 10000. Hence, user-defined surface IDs greater
 *          than or equal to 10000 are prohibited.
 */
int surf_id() {
  int id = auto_id;
  auto_id++;
  return id;
}


/**
 * @brief Resets the auto-generated unique Surface ID counter to 10000.
 */
void reset_surf_id() {
  auto_id = 10000;
}


/**
 * @brief Constructor assigns unique ID and user-defined ID for a Surface.
 * @details Assigns a default boundary condition for this Surface to
 *          BOUNDARY_NONE.
 * @param id an optional user-defined Surface ID
 * @param name an optional user-defined Surface name
 */
Surface::Surface(const int id, const char* name){

  /* If the user did not define an optional ID, create one */
  if (id == 0)
    _id = surf_id();

  /* Use the user-defined ID */
  else
    _id = id;

  _uid = _n;
  _n++;

  _name = NULL;
  setName(name);

  _boundary_type = BOUNDARY_NONE;
}


/**
 * @brief Destructor.
 */
Surface::~Surface() {
  if (_name != NULL)
    delete [] _name;
}


/**
 * @brief Return the Surface's unique ID.
 * @return the Surface's unique ID
 */
int Surface::getUid() const {
  return _uid;
}


/**
 * @brief Return the Surface's user-defined ID.
 * @return the Surface's user-defined ID
 */
int Surface::getId() const {
  return _id;
}


/**
 * @brief Return the user-defined name of the Surface
 * @return the Surface name
 */
char* Surface::getName() const {
  return _name;
}


/**
 * @brief Return the type of Surface (ie, XPLANE, CIRCLE, etc).
 * @return the Surface type
 */
surfaceType Surface::getSurfaceType() {
  return _surface_type;
}


/**
 * @brief Returns the type of boundary conditions for this Surface (REFLECTIVE,
 *        VACUUM or BOUNDARY_NONE)
 * @return the type of boundary condition type for this Surface
 */
boundaryType Surface::getBoundaryType(){
  return _boundary_type;
}


/**
 * @brief Sets the name of the Surface
 * @param name the Surface name string
 */
void Surface::setName(const char* name) {
  int length = strlen(name);

  if (_name != NULL)
    delete [] _name;

  /* Initialize a character array for the Surface's name */
  _name = new char[length+1];

  /* Copy the input character array Surface name to the class attribute name */
  for (int i=0; i <= length; i++)
    _name[i] = name[i];
}


/**
 * @brief Sets the boundary condition type (ie, VACUUM or REFLECTIVE) for this
 *        Surface.
 * @param boundary_type the boundary condition type for this Surface
 */
void Surface::setBoundaryType(boundaryType boundary_type) {
  _boundary_type = boundary_type;
}


/**
 * @brief Return true or false if a Point is on or off of a Surface.
 * @param point pointer to the Point of interest
 * @return on (true) or off (false) the Surface
 */
bool Surface::isPointOnSurface(Point* point) const {

  /* Uses a threshold to determine whether the point is on the Surface */
  if (std::abs(evaluate(point)) < ON_SURFACE_THRESH)
    return true;
  else
    return false;
}


/**
 * @brief Return true or false if a LocalCoord is on or off of a Surface.
 * @param coord pointer to the LocalCoord of interest
 * @return on (true) or off (false) the Surface
 */
bool Surface::isCoordOnSurface(LocalCoords* coord) {
  return isPointOnSurface(coord->getPoint());
}


/**
 * @brief Prints a string representation of all of the Surface's objects to
 *        the console.
 */
void Surface::printString() {
  log_printf(RESULT, toString().c_str());
}


/**
 * @brief Constructor.
 * @param A the first coefficient in \f$ A * x + B * y + C = 0 \f$
 * @param B the second coefficient in \f$ A * x + B * y + C = 0 \f$
 * @param C the third coefficient in \f$ A * x + B * y + C = 0 \f$
 * @param id the optional Surface ID
 * @param name the optional name of the Surface
 */
Plane::Plane(const double A, const double B,
             const double C, const int id, const char* name):
  Surface(id, name) {
  _surface_type = PLANE;
  _A = A;
  _B = B;
  _C = C;
}

/**
 * @brief Copy constructor.
 */ 
Plane::Plane(const Plane &p)
{
  _id = p._id;
  this->setName(p._name);
  _surface_type = PLANE;
  _A = p._A;
  _B = p._B;
  _C = p._C;
}


/**
 * @brief Returns the minimum x value of -INFINITY
 * @param halfspace the halfspace of the Surface to consider
 * @return the minimum x value of -INFINITY
 */
double Plane::getMinX(int halfspace){
  return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum x value of INFINITY.
 * @param halfspace the halfspace of the Surface to consider
 * @return the maximum x value of INFINITY
 */
double Plane::getMaxX(int halfspace){
  return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the minimum y value of -INFINITY
 * @param halfspace the halfspace of the Surface to consider
 * @return the minimum y value of -INFINITY
 */
double Plane::getMinY(int halfspace){
  return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum y value of INFINITY.
 * @param halfspace the halfspace of the Surface to consider
 * @return the maximum y value of INFINITY
 */
double Plane::getMaxY(int halfspace){
  return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the minimum z value of -INFINITY
 * @param halfspace the halfspace of the Surface to consider
 * @return the minimum z value of -INFINITY
 */
double Plane::getMinZ(int halfspace){
  return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum z value of INFINITY.
 * @param halfspace the halfspace of the Surface to consider
 * @return the maximum z value of INFINITY
 */
double Plane::getMaxZ(int halfspace){
  return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the A coefficient multiplying x in the surface equation
 * @return the value for the A coefficient
 */
double Plane::getA() {
  return _A;
}


/**
 * @brief Returns the B coefficient multiplying x in the surface equation
 * @return the value for the B coefficient
 */
double Plane::getB() {
  return _B;
}


/**
 * @brief Returns the C coefficient multiplying x in the surface equation
 * @return the value for the C coefficient
 */
double Plane::getC() {
  return _C;
}


/**
* @brief Finds the intersection Point with this Plane from a given Point and
*        trajectory defined by an angle.
* @param point pointer to the Point of interest
* @param angle the angle defining the trajectory in radians
* @param points pointer to a Point to store the intersection Point
* @return the number of intersection Points (0 or 1)
*/
inline int Plane::intersection(Point* point, double angle, Point* points) {

  double x0 = point->getX();
  double y0 = point->getY();

  int num = 0;                /* number of intersections */
  double xcurr, ycurr;        /* coordinates of current intersection point */

  /* The track is vertical */
  if ((fabs(angle - (M_PI / 2))) < 1.0e-10) {

    /* The plane is also vertical => no intersections */
    if (_B == 0)
      return 0;

    /* The plane is not vertical */
    else {
      xcurr = x0;
      ycurr = (-_A * x0 - _C) / _B;
      points->setCoords(xcurr, ycurr);

      /* Check that point is in same direction as angle */
      if (angle < M_PI && ycurr > y0)
        num++;
      else if (angle > M_PI && ycurr < y0)
        num++;
      return num;
    }
  }

  /* If the track isn't vertical */
  else {
    double m = sin(angle) / cos(angle);

    /* The plane and track are parallel, no intersections */
    if (fabs(-_A/_B - m) < 1e-11 && _B != 0)
      return 0;

    else {
      xcurr = -(_B * (y0 - m * x0) + _C) / (_A + _B * m);
      ycurr = y0 + m * (xcurr - x0);
      points->setCoords(xcurr, ycurr);

      if (angle < M_PI && ycurr > y0)
        num++;
      else if (angle > M_PI && ycurr < y0)
        num++;

      return num;
    }
  }
}


/**
 * @brief Converts this Plane's attributes to a character array.
 * @details The character array returned contains the type of Plane (ie,
 *          PLANE) and the A, B, and C coefficients in the
 *          quadratic Surface equation.
 * @return a character array of this Plane's attributes
 */
std::string Plane::toString() {

  std::stringstream string;

  string << "Surface ID = " << _id
         << ", name = " << _name
         << ", type = PLANE "
         << ", A = " << _A << ", B = " << _B << ", C = " << _C;

  return string.str();
}


/**
 * @brief Constructor for a Plane perpendicular to the x-axis.
 * @param x the location of the Plane along the x-axis
 * @param id the optional Surface id
 * @param name the optional name of the XPlane
 */
XPlane::XPlane(const double x, const int id, const char* name):
  Plane(1, 0, -x, id, name) {

  _surface_type = XPLANE;
  _x = x;
}


/**
 * @brief Set the location of this XPlane on the x-axis.
 * @param x the location of the XPlane on the x-axis
 */
void XPlane::setX(const double x) {
  _x = x;
}


/**
 * @brief Returns the location of the XPlane on the x-axis.
 * @return the location of the XPlane on the x-axis
 */
double XPlane::getX() {
  return _x;
}


/**
 * @brief Returns the minimum x value for one of this XPlane's halfspaces.
 * @param halfspace the halfspace of the XPlane to consider
 * @return the minimum x value
 */
double XPlane::getMinX(int halfspace){
  if(halfspace == +1)
    return _x;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum x value for one of this XPlane's halfspaces.
 * @param halfspace the halfspace of the XPlane to consider
 * @return the maximum x value
 */
double XPlane::getMaxX(int halfspace){
  if(halfspace == -1)
    return _x;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Converts this XPlane's attributes to a character array.
 * @details The character array returned conatins the type of Plane (ie,
 *          XPLANE) and the A, B, and C coefficients in the
 *          quadratic Surface equation and the location of the Plane on
 *          the x-axis.
 * @return a character array of this XPlane's attributes
 */
std::string XPlane::toString() {

  std::stringstream string;

  string << "Surface ID = " << _id
         << ", name = " << _name
         << ", type = XPLANE "
         << ", A = " << _A << ", B = " << _B
         << ", C = " << _C << ", x = " << _x;

  return string.str();
}


/**
 * @brief Constructor for a Plane perpendicular to the y-axis.
 * @param y the location of the Plane along the y-axis
 * @param id the optional Surface id
 * @param name the optional Surface name
 */
YPlane::YPlane(const double y, const int id, const char* name):
  Plane(0, 1, -y, id, name) {

  _surface_type = YPLANE;
  _y = y;
}


/**
 * @brief Set the location of this YPlane on the y-axis.
 * @param y the location of the YPlane on the y-axis
 */
void YPlane::setY(const double y) {
  _y = y;
}


/**
 * @brief Returns the location of the YPlane on the y-axis.
 * @return the location of the YPlane on the y-axis
 */
double YPlane::getY() {
  return _y;
}


/**
 * @brief Returns the minimum y value for one of this YPlane's halfspaces.
 * @param halfspace the halfspace of the YPlane to consider
 * @return the minimum y value
 */
double YPlane::getMinY(int halfspace){
  if(halfspace == +1)
    return _y;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum y value for one of this YPlane's halfspaces.
 * @param halfspace the halfspace of the YPlane to consider
 * @return the maximum y value
 */
double YPlane::getMaxY(int halfspace){
  if(halfspace == -1)
    return _y;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Converts this yplane's attributes to a character array
 * @details The character array returned conatins the type of Plane (ie,
 *          YPLANE) and the A, B, and C coefficients in the quadratic
 *          Surface equation and the location of the Plane on the y-axis.
 * @return a character array of this YPlane's attributes
 */
std::string YPlane::toString() {

  std::stringstream string;

  string << "Surface ID = " << _id
         << ", name = " << _name
         << ", type = YPLANE "
         << ", A = " << _A << ", B = " << _B
         << ", C = " << _C << ", y = " << _y;

  return string.str();
}


/**
 * @brief Constructor for a Plane perpendicular to the z-axis.
 * @param z the location of the Plane along the z-axis
 * @param id the optional Surface ID
 * @param name the optional Surface name
 */
ZPlane::ZPlane(const double z, const int id, const char* name):
  Plane(0, 0, -z, id, name) {

  _surface_type = ZPLANE;
  _z = z;
}


/**
 * @brief Set the location of this ZPlane on the z-axis.
 * @param z the location of the ZPlane on the z-axis
 */
void ZPlane::setZ(const double z) {
  _z = z;
}


/**
 * @brief Returns the location of the ZPlane on the z-axis.
 * @return the location of the ZPlane on the z-axis
 */
double ZPlane::getZ() {
  return _z;
}


/**
 * @brief Returns the minimum z value for one of this ZPlane's halfspaces.
 * @param halfspace the halfspace of the ZPlane to consider
 * @return the minimum z value
 */
double ZPlane::getMinZ(int halfspace){
  if(halfspace == +1)
    return _z;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum z value for one of this ZPlane's halfspaces.
 * @param halfspace the halfspace of the ZPlane to consider
 * @return the maximum z value
 */
double ZPlane::getMaxZ(int halfspace){
  if(halfspace == -1)
    return _z;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Converts this ZPlane's attributes to a character array.
 * @details The character array returned contains the type of Plane (ie,
 *          ZPLANE) and the A, B, and C coefficients in the
 *          quadratic Surface equation and the location of the Plane along
 *          the z-axis.
 * @return a character array of this ZPlane's attributes
 */
std::string ZPlane::toString() {

  std::stringstream string;

  string << "Surface ID = " << _id
         << ", name = " << _name
         << ", type = ZPLANE "
         << ", A = " << _A << ", B = " << _B
         << ", C = " << _C << ", z = " << _z;

  return string.str();
}

/**
 * @brief Constructor for an inclined Plane that is a part of a regular hexagon
 * @param x the x-coordinate of the Hexagon center
 * @param y the y-coordinate of the Hexagon center
 * @param radius the radius of the Hexagon (equal to the Hexagon side)
 * @param hex_id the number of the Hexagon side, used for easier construction
 * @param id the optional Surface ID
 * @param name the optional Surface name
 */
HexPlane::HexPlane(const double x, const double y, const double radius, 
                   const size_t hex_id, const int id, const char* name) :
  Plane(0., 0., 0., id, name) {  // A, B and C will be calculated and set below
  
  _surface_type = PLANE;
  _radius = radius;
  _center.setX(x);
  _center.setY(y);
  _side_num = hex_id;
  
  // The linear coefficients of the Plane(line) are calculated from the two
  // vertices it passes trough.
  // Determine top vertex
  Point t, _vertex[1]; // t - the top point, relative to the beginning of the CS
  t.setX(0);
  t.setY(_radius);
  
  // rotate the two points to their respective positions
  double tmp_a = _side_num * M_PI / 3;
  _vertex[0].setX(t.getX() * cos(tmp_a) - t.getY() * sin(tmp_a));
  _vertex[0].setY(t.getX() * sin(tmp_a) + t.getY() * cos(tmp_a));
  tmp_a += M_PI / 3; // point _vertex[1] is 60 degrees further from _vertex[0]
  _vertex[1].setX(t.getX() * cos(tmp_a) - t.getY() * sin(tmp_a));
  _vertex[1].setY(t.getX() * sin(tmp_a) + t.getY() * cos(tmp_a));
  
  // shift the points to the center
  _vertex[0].setX(_vertex[0].getX() + _center.getX());
  _vertex[0].setY(_vertex[0].getY() + _center.getY());
  _vertex[1].setX(_vertex[1].getX() + _center.getX());
  _vertex[1].setY(_vertex[1].getY() + _center.getY());
  
  // calculate the Plane coefficients
  _A = -(_vertex[1].getY() - _vertex[0].getY());
  _B = -(_vertex[0].getX() - _vertex[1].getX());
  _C = -(_vertex[0].getY() * _vertex[1].getX() - _vertex[0].getX() * _vertex[1].getY());
  
//  std::cout << "Ax: " << std::setprecision(3) << _vertex[0].getX() << " Ay: " << std::setprecision(3) << _vertex[0].getY() << std::endl;
//  std::cout << "Bx: " << std::setprecision(3) << _vertex[1].getX() << " By: " << std::setprecision(3) << _vertex[1].getY() << std::endl;
//  std::cout << "A:  " << std::setprecision(3) << _A                << " B:  " << std::setprecision(3) << _B << std::setprecision(3) << " C:  " << std::setprecision(3) << _C << std::endl;
//  std::cout << "------------------------------" << std::endl;
  // determine min and max points
  _min_x[0] = _min_x[1] = - std::numeric_limits<double>::infinity();
  _max_x[0] = _max_x[1] = + std::numeric_limits<double>::infinity();
  _min_y[0] = _min_y[1] = - std::numeric_limits<double>::infinity();
  _max_y[0] = _max_y[1] = + std::numeric_limits<double>::infinity();
  
//  size_t idx_a = _side_num % 2;
//  size_t idx_b = (_side_num + 1) % 2;
//  
//  if (_side_num % 3 == 0) // side_num is 0 or 3
//  {
//    _min_x[idx_a] = _vertex[idx_b].getX();
//    _max_x[idx_a] = _vertex[idx_a].getX();
//    _min_y[idx_a] = _vertex[idx_b].getY();
//    _max_y[idx_a] = _vertex[idx_a].getY();
//  }
//
//  if (_side_num % 3 == 1) // side_num is 1 or 4, i.e. the two vertical sides
//  {
//    _max_x[0] = _vertex[0].getX(); // =_vertex[1].getX()
//    _min_x[1] = _vertex[0].getX(); // =_vertex[1].getX()
//    _min_y[idx_a] = _vertex[idx_b].getY();
//    _max_y[idx_a] = _vertex[idx_a].getY();
//  }
//
//  if (_side_num % 3 == 2) // side_num is 0 or 3
//  {
//    _min_x[idx_a] = _vertex[idx_a].getX();
//    _max_x[idx_a] = _vertex[idx_b].getX();
//    _min_y[idx_a] = _vertex[idx_b].getY();
//    _max_y[idx_a] = _vertex[idx_a].getY();
//  }
}

/**
 * @brief Returns the minimum x value for one of this HexPlane's halfspaces. 
 * If the halfspace is from the side of the hexagon center, additional limits are applied.
 * @param halfspace the halfspace of the HexPlane to consider
 * @return the minimum x value
 */
double HexPlane::getMinX(int halfspace){
  return _min_x[(halfspace + 1) / 2];   // indices are 0 for hs=-1 and 0 for hs=1
}

/**
 * @brief Returns the maximum x value for one of this HexPlane's halfspaces. 
 * If the halfspace is from the side of the hexagon, additional limits are applied.
 * @param halfspace the halfspace of the HexPlane to consider
 * @return the maximum x value
 */
double HexPlane::getMaxX(int halfspace){
  return _max_x[(halfspace + 1) / 2];   // indices are 0 for hs=-1 and 0 for hs=1
}

/**
 * @brief Returns the minimum y value for one of this HexPlane's halfspaces. 
 * If the halfspace is from the side of the hexagon, additional limits are applied.
 * @param halfspace the halfspace of the HexPlane to consider
 * @return the minimum y value
 */
double HexPlane::getMinY(int halfspace){
  return _min_y[(halfspace + 1) / 2];   // indices are 0 for hs=-1 and 0 for hs=1
}

/**
 * @brief Returns the maximum y value for one of this HexPlane's halfspaces. 
 * If the halfspace is from the side of the hexagon, additional limits are applied.
 * @param halfspace the halfspace of the HexPlane to consider
 * @return the maximum y value
 */
double HexPlane::getMaxY(int halfspace){
  return _max_y[(halfspace + 1) / 2];   // indices are 0 for hs=-1 and 0 for hs=1
}

/**
 * @brief constructor.
 * @param x the x-coordinate of the Circle center
 * @param y the y-coordinate of the Circle center
 * @param radius the radius of the Circle
 * @param id the optional Surface ID
 * @param name the optional Surface name
 */
Circle::Circle(const double x, const double y,
               const double radius, const int id, const char* name):
  Surface(id, name) {

  _surface_type = CIRCLE;
  _A = 1.;
  _B = 1.;
  _C = -2.*x;
  _D = -2.*y;
  _E = x*x + y*y - radius*radius;
  _radius = radius;
  _center.setX(x);
  _center.setY(y);
}


/**
 * @brief Return the x-coordinate of the Circle's center Point.
 * @return the x-coordinate of the Circle center
 */
double Circle::getX0() {
  return _center.getX();
}


/**
 * @brief Return the y-coordinate of the Circle's center Point.
 * @return the y-coordinate of the Circle center
 */
double Circle::getY0() {
  return _center.getY();
}


/**
 * @brief Returns the minimum x value for one of this Circle's halfspaces.
 * @param halfspace the halfspace of the Circle to consider
 * @return the minimum x value
 */
double Circle::getMinX(int halfspace){
  if (halfspace == -1)
    return _center.getX() - _radius;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum x value for one of this Circle's halfspaces.
 * @param halfspace the halfspace of the Circle to consider
 * @return the maximum x value
 */
double Circle::getMaxX(int halfspace){
  if (halfspace == -1)
    return _center.getX() + _radius;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the minimum y value for one of this Circle's halfspaces.
 * @param halfspace the halfspace of the Circle to consider
 * @return the minimum y value
 */
double Circle::getMinY(int halfspace){
  if (halfspace == -1)
    return _center.getY() - _radius;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum y value for one of this Circle's halfspaces.
 * @param halfspace the halfspace of the Circle to consider
 * @return the maximum y value
 */
double Circle::getMaxY(int halfspace){
  if (halfspace == -1)
    return _center.getY() + _radius;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the minimum z value of -INFINITY.
 * @param halfspace the halfspace of the Circle to consider
 * @return the minimum z value of -INFINITY
 */
double Circle::getMinZ(int halfspace){
  return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum z value of INFINITY.
 * @param halfspace the halfspace of the Circle to consider
 * @return the maximum z value of INFINITY
 */
double Circle::getMaxZ(int halfspace){
  return std::numeric_limits<double>::infinity();
}


/**
 * @brief Finds the intersection Point with this circle from a given Point and
 *        trajectory defined by an angle (0, 1, or 2 points).
 * @param point pointer to the Point of interest
 * @param angle the angle defining the trajectory in radians
 * @param points pointer to a an array of Points to store intersection Points
 * @return the number of intersection Points (0 or 1)
 */
int Circle::intersection(Point* point, double angle, Point* points) {

  double x0 = point->getX();
  double y0 = point->getY();
  double xcurr, ycurr;
  int num = 0;                        /* Number of intersection Points */
  double a, b, c, q, discr;

  /* If the track is vertical */
  if ((fabs(angle - (M_PI / 2))) < 1.0e-10) {

    /* Solve for where the line x = x0 and the Surface F(x,y) intersect
     * Find the y where F(x0, y) = 0
     * Substitute x0 into F(x,y) and rearrange to put in
     * the form of the quadratic formula: ay^2 + by + c = 0 */
    a = _B * _B;
    b = _D;
    c = _A * x0 * x0 + _C * x0 + _E;

    discr = b*b - 4*a*c;

    /* There are no intersections */
    if (discr < 0)
      return 0;

    /* There is one intersection (ie on the Surface) */
    else if (discr == 0) {
      xcurr = x0;
      ycurr = -b / (2*a);
      points[num].setCoords(xcurr, ycurr);
      if (angle < M_PI && ycurr > y0)
        num++;
      else if (angle > M_PI && ycurr < y0)
        num++;
      return num;
    }

    /* There are two intersections */
    else {
      xcurr = x0;
      ycurr = (-b + sqrt(discr)) / (2 * a);
      points[num].setCoords(xcurr, ycurr);
      if (angle < M_PI && ycurr > y0)
        num++;
      else if (angle > M_PI && ycurr < y0)
        num++;

      xcurr = x0;
      ycurr = (-b - sqrt(discr)) / (2 * a);
      points[num].setCoords(xcurr, ycurr);
      if (angle < M_PI && ycurr > y0)
        num++;
      else if (angle > M_PI && ycurr < y0)
        num++;
      return num;
    }
  }

  /* If the track isn't vertical */
  else {
    /* Solve for where the line y-y0 = m*(x-x0) and the Surface F(x,y)
     * intersect. Find the (x,y) where F(x, y0 + m*(x-x0)) = 0
     * Substitute the point-slope formula for y into F(x,y) and
     * rearrange to put in the form of the quadratic formula:
     * ax^2 + bx + c = 0
     */
    double m = sin(angle) / cos(angle);
    q = y0 - m * x0;
    a = _A + _B * _B * m * m;
    b = 2 * _B * m * q + _C + _D * m;
    c = _B * q * q + _D * q + _E;

    discr = b*b - 4*a*c;

    /* There are no intersections */
    if (discr < 0)
      return 0;

    /* There is one intersection (ie on the Surface) */
    else if (discr == 0) {
      xcurr = -b / (2*a);
      ycurr = y0 + m * (points[0].getX() - x0);
      points[num].setCoords(xcurr, ycurr);
      if (angle < M_PI && ycurr > y0)
        num++;
      else if (angle > M_PI && ycurr < y0)
        num++;
      return num;
    }

    /* There are two intersections */
    else {
      xcurr = (-b + sqrt(discr)) / (2*a);
      ycurr = y0 + m * (xcurr - x0);
      points[num].setCoords(xcurr, ycurr);
      if (angle < M_PI && ycurr > y0) {
        num++;
      }
      else if (angle > M_PI && ycurr < y0) {
        num++;
      }

      xcurr = (-b - sqrt(discr)) / (2*a);
      ycurr = y0 + m * (xcurr - x0);
      points[num].setCoords(xcurr, ycurr);
      if (angle < M_PI && ycurr > y0) {
        num++;
      }
      else if (angle > M_PI && ycurr < y0) {
        num++;
      }

      return num;
    }
  }
}


/**
 * @brief Converts this Circle's attributes to a character array.
 * @details The character array returned conatins the type of Plane (ie,
 *          CIRCLE) and the A, B, C, D and E coefficients in the
 *          quadratic Surface equation.
 * @return a character array of this Circle's attributes
 */
std::string Circle::toString() {

  std::stringstream string;

  string << "Surface ID = " << _id
         << ", name " << _name
         << ", type = CIRCLE "
         << ", A = " << _A << ", B = " << _B
         << ", C = " << _C << ", D = " << _D << ", E = " << _E
         << ", x0 = " << _center.getX()
         << ", y0 = " << _center.getY()
         << ", radius = " << _radius;

    return string.str();
}

/**
 * @brief constructor.
 * @param x the x-coordinate of the Hexagon center
 * @param y the y-coordinate of the Hexagon center
 * @param outer radius the radius of the Hexagon
 * @param id the optional Surface ID
 * @param name the optional Surface name
 */
Hexagon::Hexagon(const double x, const double y,
               const double radius, const int id, const char* name):
  Surface(id, name) {

  _surface_type = HEXAGON;
  _radius = radius;
  _iradius = _radius * sqrt(3) * 0.5;
  _center.setX(x);
  _center.setY(y);
  
  // The linear coefficients of the Plane(line) are calculated from the two
  // vertices it passes trough.
  Point t;  // the top vertex
  t.setX(0);
  t.setY(_radius);
  double tmp_angle = M_PI * 2. / _nsides;
  
  for (size_t i=0 ; i < _nsides ; ++i)
  {
    double tmp_ang = i * tmp_angle;  // work angle: a multiple of PI/3 for a hexagon
    Point tmp_a, tmp_b;                       // work points, the plane will be passing trough them.
    // rotate the two points to their respective positions
    tmp_a.setX(t.getX() * cos(tmp_ang) - t.getY() * sin(tmp_ang));
    tmp_a.setY(t.getX() * sin(tmp_ang) + t.getY() * cos(tmp_ang));
    tmp_ang += tmp_angle;            // point tmp_b is 60 degrees further from tmp_a
    tmp_b.setX(t.getX() * cos(tmp_ang) - t.getY() * sin(tmp_ang));
    tmp_b.setY(t.getX() * sin(tmp_ang) + t.getY() * cos(tmp_ang));

    // shift the points to the center
    tmp_a.setX(tmp_a.getX() + _center.getX());
    tmp_a.setY(tmp_a.getY() + _center.getY());
    tmp_b.setX(tmp_b.getX() + _center.getX());
    tmp_b.setY(tmp_b.getY() + _center.getY());

    // calculate the Plane coefficients
    double A, B, C;
    A = tmp_b.getY() - tmp_a.getY();
    B = tmp_a.getX() - tmp_b.getX();
    C = tmp_a.getY() * tmp_b.getX() - tmp_a.getX() * tmp_b.getY();

    // append using default constructor for Plane
    _sides.emplace_back(A, B, C);
  }
}

Hexagon::~Hexagon() {
  _sides.clear();
}

/**
 * @brief Return the x-coordinate of the Hexagon's center Point.
 * @return the x-coordinate of the Hexagon center
 */
double Hexagon::getX0() {
  return _center.getX();
}


/**
 * @brief Return the y-coordinate of the Hexagon's center Point.
 * @return the y-coordinate of the Hexagon center
 */
double Hexagon::getY0() {
  return _center.getY();
}


/**
 * @brief Returns the minimum x value for one of this Hexagon's halfspaces.
 * @param halfspace the halfspace of the Hexagon to consider
 * @return the minimum x value
 */
double Hexagon::getMinX(int halfspace){
  if (halfspace == -1)
    return _center.getX() - _iradius;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum x value for one of this Hexagon's halfspaces.
 * @param halfspace the halfspace of the Hexagon to consider
 * @return the maximum x value
 */
double Hexagon::getMaxX(int halfspace){
  if (halfspace == -1)
    return _center.getX() + _iradius;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the minimum y value for one of this Hexagon's halfspaces.
 * @param halfspace the halfspace of the Hexagon to consider
 * @return the minimum y value
 */
double Hexagon::getMinY(int halfspace){
  if (halfspace == -1)
    return _center.getY() - _radius;
  else
    return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum y value for one of this Hexagon's halfspaces.
 * @param halfspace the halfspace of the Hexagon to consider
 * @return the maximum y value
 */
double Hexagon::getMaxY(int halfspace){
  if (halfspace == -1)
    return _center.getY() + _radius;
  else
    return std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the minimum z value of -INFINITY.
 * @param halfspace the halfspace of the Hexagon to consider
 * @return the minimum z value of -INFINITY
 */
double Hexagon::getMinZ(int halfspace){
  return -std::numeric_limits<double>::infinity();
}


/**
 * @brief Returns the maximum z value of INFINITY.
 * @param halfspace the halfspace of the Hexagon to consider
 * @return the maximum z value of INFINITY
 */
double Hexagon::getMaxZ(int halfspace){
  return std::numeric_limits<double>::infinity();
}

/**
 * @brief Finds the intersection Point with this hexagon from a given Point and
 *        trajectory defined by an angle (0, 1, or 2 points).
 * @param point pointer to the Point of interest
 * @param angle the angle defining the trajectory in radians
 * @param points pointer to a an array of Points to store intersection Points
 * @return the number of intersection Points (0, 1 or 2)
 */
int Hexagon::intersection(Point* point, double angle, Point* points) {
  return 1;
}


/**
 * @brief Converts this Hexagon's attributes to a character array.
 * @details The character array returned conatins the type of Plane (ie,
 *          HEXAGON) and the A, B, C, D and E coefficients in the
 *          quadratic Surface equation.
 * @return a character array of this Hexagon's attributes
 */
std::string Hexagon::toString() {
  
  std::stringstream string;

  string << "Surface ID = " << _id
         << ", name " << _name
         << ", type = HEXAGON "
         << std::endl;
  for(size_t i=0; i < _sides.size(); ++i)
  {
    string << ", side[" << i << "]: "
           << " A = " << _sides.at(i).getA()
           << " B = " << _sides.at(i).getB()
           << " C = " << _sides.at(i).getC()
           << std::endl;
  }
  string << ", x0 = " << _center.getX()
         << ", y0 = " << _center.getY()
         << ", radius = " << _radius
         << ", inner radius = " << _iradius;

  return string.str();
}