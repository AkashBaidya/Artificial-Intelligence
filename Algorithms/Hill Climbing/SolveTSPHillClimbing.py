#==============================================================================
#description     : Solves travelling salesman problem by using Hill Climbing.
#author          : Yakup Cengiz
#date            : 20151121
#version         : 0.1
#notes           :
#python_version  : 3.5.0  
#==============================================================================

import sys
import os
import random
import numpy as np

CommonPath = os.path.abspath(os.path.join('..', 'Common'))
sys.path.append(CommonPath)

import tsp

import logging

def GenerateInitialPath(tour_length):
   tour=list(range(tour_length))
   random.shuffle(tour)
   return tour

MAX_ITERATION = 50000

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)

def reversed_sections(tour):
    '''generator to return all possible variations where the section between two cities are swapped'''
    for i,j in tsp.AllEdges(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour: # no point returning the same tour
                yield copy
        
def ComputeHillClimb(init_function,move_operator,objective_function,MAX_ITERATION):
    '''
    hillclimb until either MAX_ITERATION is reached or we are at a local optima
    '''
    best=init_function()
    best_score=objective_function(best)
    
    iterationCount = 0
    
    logging.info('hillclimb started: score=%f',best_score)
    
    while iterationCount < MAX_ITERATION:
        moved = False
        for next in move_operator(best):
            if iterationCount >= MAX_ITERATION:
                break
            
            # see if this move is better than the current
            next_score      = objective_function(next)
            iterationCount += 1
            if next_score > best_score:
                best       = next
                best_score = next_score
                moved      = True
                break # depth first search
            
        if not moved:
            break # must be at a local maximum
    
    logging.info('hillclimb finished: iterationCount=%d, best_score=%f',iterationCount,best_score)
    return (iterationCount,best_score,best)

def ComputeHillClimbAndRestart(init_function,move_operator,objective_function,MAX_ITERATION):
    shortestPath       = None
    shortestPathLength = 0
    
    iterationCount = 0
    while iterationCount < MAX_ITERATION:
        remaining_evaluations = MAX_ITERATION - iterationCount
        
        print('(re)starting hillclimb %d/%d remaining'%(remaining_evaluations,MAX_ITERATION))
        evaluated, pathLength, foundShortestPath = hillclimb(init_function,move_operator,objective_function,remaining_evaluations)
        
        iterationCount += evaluated
        if pathLength > shortestPathLength or best is None:
            shortestPathLength = pathLength
            shortestPathLength = foundShortestPath
        
    return (iterationCount,shortestPathLength, shortestPath)

def SolveTSP():
    print("Starting to solve travel salesman problem")
    coordinates  = tsp.ReadCoordinatesFromFile(".\cityCoordinates.csv")
    distance_matrix = tsp.ComputeDistanceMatrix(coordinates);
    
    init_function      = lambda: GenerateInitialPath(len(coordinates))
    objective_function = lambda tour: -tsp.ComputeTourLength(distance_matrix, tour)
    
    #iterationCount,best_score,shortestPath = hillclimb(init_function, reversed_sections, objective_function, MAX_ITERATION)
    iterationCount,best_score,shortestPath = hillclimb_and_restart(init_function, reversed_sections, objective_function, MAX_ITERATION)
    
    print(iterationCount, best_score, shortestPath);
    
    tsp.DrawPath(coordinates, shortestPath, "TSP.png");

if __name__ == "__main__":
    SolveTSP();