#ifndef ANTCOLONYOPTIMIZATION_H
#define ANTCOLONYOPTIMIZATION_H

#include <QtWidgets/QMainWindow>
#include "ui_antcolonyoptimization.h"

class TSPSolver;

class AntColonyOptimization : public QMainWindow
{
    Q_OBJECT

public:
    AntColonyOptimization(QWidget *parent = 0);
    ~AntColonyOptimization();

private:
    Ui::AntColonyOptimizationClass ui;
    TSPSolver*                     tspSolver;
};

#endif // ANTCOLONYOPTIMIZATION_H
