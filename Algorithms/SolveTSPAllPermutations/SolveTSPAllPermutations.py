#==============================================================================
#description     : Solves travelling salesman problem by generating all possible states
#author          : Yakup Cengiz
#date            : 20151121
#version         : 0.1
#notes           :
#python_version  : 3.5.0  
#Reference       : http://www.psychicorigami.com/category/tsp/
#==============================================================================

import sys
import os
import numpy as np
import itertools

CommonPath = os.path.abspath(os.path.join('..', 'Common'))
sys.path.append(CommonPath)

import tsp

def AllPermutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in itertools.product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)
   
def SolveTSP():
    print("Starting to solve travel salesman problem")
    #coordinates  = {(1,1), (2,3), (3,3), (3,1)}
    coordinates  = tsp.ReadCoordinatesFromFile(".\cityCoordinates.csv")
    pointCount = len(coordinates)
    
    print ("Point Count %d" %pointCount)
    #assert 5 == len(coordinates) # city count
    
    distance_matrix = tsp.ComputeDistanceMatrix(coordinates);
    print(distance_matrix);
    
    #assert 25 == len(distance_matrix)
    cities = np.arange(pointCount)
    
    shortestPathLength  = sys.float_info.max;
    shortestPath = {}
    
    for path in tsp.AllPermutations(cities):
        
        totalTravel = tsp.ComputeTourLength(distance_matrix, path);
        if totalTravel < shortestPathLength :
            shortestPathLength  = totalTravel;
            shortestPath = path;
        print(path, totalTravel)
   
    print("Shortest Path Length : %f" % shortestPathLength);     
    print("Shortest Path :", shortestPath);
    
    tsp.DrawPath(coordinates, shortestPath, "TSP.png");
    
if __name__ == "__main__":
    SolveTSP()