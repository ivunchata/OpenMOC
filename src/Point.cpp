#include "Point.h"


/**
 * @brief Constructor initializes an empty Point.
 */
Point::Point() { }


/**
 * @brief Overloaded constructor to initialize a Point given coordinates
 */
Point::Point(const double x, const double y)
{
  setCoords(x, y);
}

/**
 * @brief Destructor
 */
Point::~Point() { }


/**
 * @brief Converts this Point to a character representation of its attributes.
 * @details The character array includes the x-coordinate and y-coordinates.
 * @return a character array of this Point's attributes
 */
std::string Point::toString() {
  std::stringstream string;
  string << "Point: x = " << _x << ", y = " << _y;
  return string.str();
}
