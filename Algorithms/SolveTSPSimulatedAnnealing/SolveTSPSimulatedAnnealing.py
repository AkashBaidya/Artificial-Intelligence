#==============================================================================
#description     : Solves travelling salesman problem by using Hill Climbing.
#author          : Yakup Cengiz
#date            : 20151121
#version         : 0.1
#notes           :
#python_version  : 3.5.0  
#Reference       : http://www.psychicorigami.com/category/tsp/
#==============================================================================

import math
import sys
import os
import random


CommonPath = os.path.abspath(os.path.join('..', 'Common'))
sys.path.append(CommonPath)

import tsp

def GenerateInitialPath(tour_length):
   tour=list(range(tour_length))
   random.shuffle(tour)
   return tour

MAX_ITERATION = 50000

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

def kirkpatrick_cooling(start_temp, alpha):
    T = start_temp
    while True:
        yield T
        T = alpha * T
        
def P(prev_score,next_score,temperature):
    if next_score > prev_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-prev_score)/temperature )
        
class ObjectiveFunction:
    '''class to wrap an objective function and 
    keep track of the best solution evaluated'''
    def __init__(self,objective_function):
        self.objective_function=objective_function
        self.best=None
        self.best_score=None
    
    def __call__(self,solution):
        score=self.objective_function(solution)
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
        return score
        
def ApplySimulatedAnnealing(init_function,move_operator,objective_function,max_evaluations,start_temp,alpha):
    # wrap the objective function (so we record the best)
    objective_function=ObjectiveFunction(objective_function)
    
    current        = init_function()
    current_score  = objective_function(current)
    iterationCount = 1
    
    cooling_schedule = kirkpatrick_cooling(start_temp, alpha)
    
    for temperature in cooling_schedule:
        done = False
        # examine moves around our current position
        for next in move_operator(current):
            if iterationCount >= max_evaluations:
                done=True
                break
            
            next_score=objective_function(next)
            iterationCount+=1
            
            # probablistically accept this solution always accepting better solutions
            p = P(current_score, next_score, temperature)
            # random.random() basic function random() generates a random float uniformly in the range [0.0, 1.0).
            # p function returns data in range [0.0, 1.0]
            
            if random.random() < p:
                current      = next
                current_score= next_score
                break
        # see if completely finished
        if done: break
    
    best_score = objective_function.best_score
    best       = objective_function.best

    return (iterationCount,best_score,best)
    
def SolveTSP():
    
    print("Starting to solve travel salesman problem")
    coordinates     = tsp.ReadCoordinatesFromFile(".\cityCoordinates.csv")
    distance_matrix = tsp.ComputeDistanceMatrix(coordinates);
    
    init_function      = lambda: GenerateInitialPath(len(coordinates))
    objective_function = lambda tour: -tsp.ComputeTourLength(distance_matrix, tour)
    
    start_temp,alpha = 100, 0.995
    
    iterationCount,best_score,shortestPath = ApplySimulatedAnnealing(init_function, reversed_sections, objective_function, MAX_ITERATION,start_temp,alpha)
    
    print(iterationCount, best_score, shortestPath);
    
    tsp.DrawPath(coordinates, shortestPath, "TSP.png");
    
if __name__ == "__main__":
    SolveTSP();