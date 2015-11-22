#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <qDebug>

#include "TSPSolver.h"

TSPSolver::TSPSolver(QObject *parent)
    : QObject(parent)
{
    best = MAX_TOUR;

    cities.resize(MAX_CITIES);
    ants.resize(MAX_ANTS);
}

TSPSolver::~TSPSolver()
{

}

// Initializes the TSP solver 
void TSPSolver::Initialize()
{
    // srand(time(NULL));
    int from, to, ant;
    
    // Create cities
    for(int from = 0; from < MAX_CITIES; from++)
    {
        cities[from].x = rand() % MAX_DIST;
        cities[from].y = rand() % MAX_DIST;
        
        qDebug() << cities[from].x << cities[from].y;

        for( to=0; to < MAX_CITIES; to++ )
        {
            distance[from][to]  = 0.0;
            pheromone[from][to] = INITIAL_PHEROMONE;
        }
    }
    
    //computing distance
    for(from = 0; from < MAX_CITIES; from++)
    {
        for( to =0; to < MAX_CITIES; to++)
        {
            if(to!=from && distance[from][to]==0.0)
            {
                int xd = pow( abs(cities[from].x - cities[to].x), 2);
                int yd = pow( abs(cities[from].y - cities[to].y), 2);
                
                distance[from][to] = sqrt(xd + yd);
                distance[to][from] = distance[from][to];
                
            }
        }
    }
    
    //initializing the ANTs
    to = 0;
    for( ant = 0; ant < MAX_ANTS; ant++)
    {
        if(to == MAX_CITIES)
            to=0;
        
        ants[ant].currentCity = to++;
        
        for(from = 0; from < MAX_CITIES; from++)
        {
            ants[ant].tabu[from] = 0;
            ants[ant].path[from] = -1;
        }
        
        ants[ant].pathIndex  = 1;
        ants[ant].path[0]    = ants[ant].currentCity;
        ants[ant].nextCity   = -1;
        ants[ant].tourLength = 0;
        
        //loading first city into tabu list
        ants[ant].tabu[ants[ant].currentCity] = 1;
    }
}

void TSPSolver::Solve()
{
    int currentTime = 0;
    
    while( currentTime++ < MAX_TIME )
    {
        if( MoveAnts() == 0 )
        {
            UpdatePheromoneTrails();
            
            if ( currentTime != MAX_TIME )
            {
                RestartAnts();
            }
                
            qDebug() <<"Time : " << currentTime << "Best : " << best;
        }
    }
}

// 
//checking if there are any more cities to visit for each ant
int TSPSolver::MoveAnts()
{
    int k;
    int moving = 0;
    
    for ( int k = 0; k < MAX_ANTS; k++ )
    {
        
        if( ants[k].pathIndex < MAX_CITIES )
        {
            ants[k].nextCity = SelectNextCity(k);
            ants[k].tabu[ants[k].nextCity] = 1;
            ants[k].path[ants[k].pathIndex++] = ants[k].nextCity;
            
            ants[k].tourLength += distance[ants[k].currentCity][ants[k].nextCity];
            
            //handle last case->last city to first
            
            if(ants[k].pathIndex == MAX_CITIES)
            {
                ants[k].tourLength += distance[ants[k].path[MAX_CITIES -1]][ants[k].path[0]];
            }
            
            ants[k].currentCity = ants[k].nextCity;
            moving++;
        }
    }
    
    return moving;
}

// reinitialize all ants and redistribute them
void TSPSolver::RestartAnts()
{
    int to = 0;
    
    for ( int ant = 0; ant < MAX_ANTS; ant++ )
    {
        if ( ants[ant].tourLength < best )
        {
            best      = ants[ant].tourLength;
            bestIndex = ant;
        }
        
        ants[ant].nextCity = -1;
        ants[ant].tourLength = 0.0;
        
        for( int i=0;i<MAX_CITIES;i++)
        {
            ants[ant].tabu[i] = 0;
            ants[ant].path[i] = -1;
        }
        
        if( to == MAX_CITIES )
        {
            to=0;
        }
         
        to++;

        ants[ant].currentCity   = to;
        
        ants[ant].pathIndex = 1;
        ants[ant].path[0]   = ants[ant].currentCity;
        
        ants[ant].tabu[ants[ant].currentCity] = 1;
    }
}

double TSPSolver::AntProduct(int from, int to)
{
    return(( pow( pheromone[from][to], ALPHA) * pow( (1.0/ distance[from][to]), BETA)));
}

int TSPSolver::SelectNextCity(int ant)
{
    int to;
    double denom = 0.0;
    
    int from = ants[ant].currentCity;
    
    for( to=0; to < MAX_CITIES; to++ )
    {
        if ( ants[ant].tabu[to] == 0 )
        {
            denom += AntProduct( from, to );
        }
    }
    
    Q_ASSERT(denom != 0.0);
    
    do
    {
        double p;
        to++;
        
        if(to >= MAX_CITIES)
            to=0;
        if(ants[ant].tabu[to] == 0)
        {
            p = AntProduct(from,to)/denom;
            
            double x = ((double)rand()/RAND_MAX); 
            if(x < p)
            {
                break;
            }
        }
    }while(1);
    
    return to;
}
    

//Updating trails
// Fij(t+1) = b.Fij(t) + deltaFij
// deltaFij = Q / Kn
// b  : Evaporation rate
// Q  : constant
// Kn : tour length
void TSPSolver::UpdatePheromoneTrails()
{
    //Pheromone Evaporation
    for( int from = 0; from < MAX_CITIES; from++ )
    {
        for ( int to = 0; to < MAX_CITIES ; to++ )
        {
            if ( from != to )
            {
                pheromone[from][to] *= (1.0 - RHO);
                
                if( pheromone[from][to] < 0.0 )
                {
                    pheromone[from][to] = INITIAL_PHEROMONE;
                }
            }
        }
    }
    
    //Add new pheromone to the trails
    for( int ant=0;ant<MAX_ANTS;ant++)
    {
        for( int i=0;i<MAX_CITIES;i++)
        {    
            int from, to;
            if( i < MAX_CITIES-1 )
            {
                from = ants[ant].path[i];
                to = ants[ant].path[i+1];
            }
            else
            {
                from = ants[ant].path[i];
                to = ants[ant].path[0];
            }
            
            pheromone[from][to] += (QVAL/ ants[ant].tourLength);
            pheromone[to][from] = pheromone[from][to];
            
        }
    }
    
    for (int from=0; from < MAX_CITIES;from++)
    {
        for( int to = 0; to < MAX_CITIES; to++ )
        {
            pheromone[from][to] *= RHO;
        }
    }
}