#ifndef CONFIGPARAMETERS_H
#define CONFIGPARAMETERS_H

#define MAX_CITIES 30
#define MAX_DIST 100
#define MAX_TOUR (MAX_CITIES * MAX_DIST)
#define MAX_ANTS 30

//Ant algorithm problem parameters
#define ALPHA               1.0
#define BETA                5.0                    // This parameter raises the weight of distance over pheromone
#define RHO                 0.5                    // Evapouration rate
#define QVAL                100
#define MAX_TOURS           20
#define MAX_TIME            (MAX_TOURS * MAX_CITIES)
#define INITIAL_PHEROMONE   (1.0/MAX_CITIES)


#endif // CONFIGPARAMETERS_H
