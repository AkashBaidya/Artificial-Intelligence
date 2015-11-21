#==============================================================================
#description     : TSP
#author          : Yakup Cengiz
#date            : 20151121
#version         : 0.1
#notes           : The traveling salesman problem (TSP) asks for the shortest route to visit a collection of cities and return to the starting point
#python_version  : 3.5.0  
#Reference       : http://www.psychicorigami.com/category/tsp/
#==============================================================================

#
import os
import math
import random
import csv
import itertools

from PIL import Image, ImageDraw, ImageFont

def ComputeDistanceMatrix(coordinates):
    '''create a distance matrix for the city coordinates
      that uses straight line distance'''
    matrix={}
    for i,(x1,y1) in enumerate(coordinates):
        for j,(x2,y2) in enumerate(coordinates):
            dx,dy       =x1-x2, y1-y2
            dist        = math.sqrt(dx*dx + dy*dy)
            matrix[i,j] = dist
    return matrix
    
def ReadCoordinatesFromFile(filePath):
    if not os.path.exists(filePath):    
        raise Exception("File %s doesn't exist"%filePath);
    
    f = open(filePath, 'rt')
    
    coordinates=[]    
    try:
        reader = csv.reader(f);
        for row in reader:
            try:
                coordinates.append((float(row[0]),float(row[1])))
            except:
                print(row)
                #raise Exception("exception occurred during reading file");
                
    finally:
        f.close()
    
    return coordinates
    
def ComputeTourLength(distanceMatrix, cities):
    totalDistance=0
    cityCount = len(cities)
    for i in range(cityCount):
        j = (i + 1) % cityCount
        city_i = cities[i]
        city_j = cities[j]
        totalDistance += distanceMatrix[city_i, city_j]
    return totalDistance
    
def AllPermutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in itertools.product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)
            
def AllEdges(size, shuffle = random.shuffle):
    r1 = list(range(size))
    r2 = list(range(size))
    
    if shuffle:
       shuffle(r1)
       shuffle(r2)
        
    for i in r1:
        for j in r2:
            yield (i,j)
         
def DrawPath(coords,tour,img_file):
    padding = 30
    coords=[(x+padding,y+padding) for (x,y) in coords]
    maxx,maxy=0,0
    for x,y in coords:
        maxx=max(x,maxx)
        maxy=max(y,maxy)
    maxx+=padding
    maxy+=padding
    img=Image.new("RGB",(int(maxx),int(maxy)),color=(255, 255, 255))
    
    font=ImageFont.load_default()
    d=ImageDraw.Draw(img);
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        x1,y1=coords[city_i]
        x2,y2=coords[city_j]
        d.line((int(x1),int(y1),int(x2),int(y2)),fill=(10, 10, 10))
        d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(64, 64, 64))
    
    
    for x,y in coords:
        x,y=int(x),int(y)
        d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(120, 120, 120))
    del d
    img.save(img_file, "PNG")