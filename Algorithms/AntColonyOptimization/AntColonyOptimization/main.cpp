#include "antcolonyoptimization.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    AntColonyOptimization w;
    w.show();
    return a.exec();
}
