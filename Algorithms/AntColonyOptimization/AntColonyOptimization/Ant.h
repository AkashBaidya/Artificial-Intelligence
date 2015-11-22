#ifndef ANT_H
#define ANT_H

#include <QObject>
#include "ConfigParameters.h"

class Ant
{
public:
    Ant();
    virtual ~Ant();

    // TODO Move them into private section
    int    currentCity, nextCity, pathIndex;
    int    tabu[MAX_CITIES];
    int    path[MAX_CITIES];
    double tourLength;
};

#endif // ANT_H
