#include "antcolonyoptimization.h"
#include "TSPSolver.h"

AntColonyOptimization::AntColonyOptimization(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);

    tspSolver = new TSPSolver(this);
    tspSolver->Initialize();
    tspSolver->Solve();
}

AntColonyOptimization::~AntColonyOptimization()
{

}
