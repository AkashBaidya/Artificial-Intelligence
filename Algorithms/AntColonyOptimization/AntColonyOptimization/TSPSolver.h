#ifndef TSPSOLVER_H
#define TSPSOLVER_H

#include <QVector>
#include <QObject>
#include "ConfigParameters.h"
#include "Ant.h"
#include "City.h"

class TSPSolver : public QObject
{
    Q_OBJECT

public:
    TSPSolver(QObject *parent);
    ~TSPSolver();

    void Initialize();
    void Solve();

private:
    void   UpdatePheromoneTrails();
    int    MoveAnts();
    int    SelectNextCity( int ant );
    double AntProduct(int from, int to);
    void   RestartAnts();

    double best;
    int    bestIndex;

    //runtime Structures and global variables
    QVector<City> cities;
    QVector<Ant>  ants;

    double         distance[MAX_CITIES][MAX_CITIES];
    double         pheromone[MAX_CITIES][MAX_CITIES];

};

#endif // TSPSOLVER_H
