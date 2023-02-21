from fastapi import FastAPI
import uvicorn
import pandas as pd

from collections import defaultdict
from math import sqrt
import time
#import json
# Shortest path to all coordinates from any node
# Coordinates must be provided as a list containing lists of
# x/y pairs. ie [[23.2321, 58.3123], [x.xxx, y.yyy]]


def distance_between_coords(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return distance


# Adds "names" to coordinates to use as keys for edge detection
def name_coords(coords):
    coord_count = 0
    for coord in coords:
        coord_count += 1
        coord.append(coord_count)
    return coords


# Creates a weighted and undirected graph
# Returns named coordinates and their connected edges as a dictonary
def graph(coords):
    coords = name_coords(coords)
    graph = defaultdict(list)
    edges = {}
    for current in coords:
        for comparer in coords:
            if comparer == current:
                continue
            else:
                weight = distance_between_coords(current[0], current[1],comparer[0], comparer[1])
                
                
                graph[current[2]].append(comparer[2])
                edges[current[2], comparer[2]] = weight
    return coords, edges


# Returns a path to all nodes with least weight as a list of names
# from a specific node
def shortest_path(node_list, edges, start):
    neighbor = 0
    unvisited = []
    visited = []
    total_weight = 0
    current_node = start
    for node in node_list:
        if node[2] == start:
            visited.append(start)
        else:
            unvisited.append(node[2])
    while unvisited:
        for index, neighbor in enumerate(unvisited):
            if index == 0:
                current_weight = edges[start, neighbor]
                current_node = neighbor
            elif edges[start, neighbor] < current_weight:
                current_weight = edges[start, neighbor]
                current_node = neighbor
        total_weight += current_weight
        unvisited.remove(current_node)
        visited.append(current_node)
    return visited, total_weight


def driver(x):
    coords = x
    coords, edges = graph(coords)
    shortest_path(coords, edges,3)
    
    shortest_path_taken = []
    shortest_path_weight = 0

    for index, node in enumerate(coords):
        path, weight = shortest_path(coords, edges,1)
       # print('--------------------------------------')
        #print("Path", index + 1, "=", path)
        #print("Weight =", weight)
        if index == 0:
            shortest_path_weight = weight
            shortest_path_taken = path
        elif weight < shortest_path_weight:
            shortest_path_weight = weight
            shortest_path_taken = path
    
    #print("The shortest path to all nodes is:", shortest_path_taken)
    return shortest_path_taken
    #return index
   # print("The weight of the path is:", shortest_path_weight)

app = FastAPI()

@app.get("/")
async def root():


    df=pd.read_json(r'C:\Users\Anil\Downloads\employeeList.txt')
    df=df[:31]
    df=df.reset_index(drop=True)
    df1=pd.read_excel(r'C:\Users\Anil\Downloads\Book10.xlsx')
    df1=df1.reset_index(drop=True)
    geo_list = df1["GeoCode"].to_list()
    lc = []
    for el in geo_list:
        ls=[]
        ls.append(float(el.split(',')[0]))
        ls.append(float(el.split(',')[1]))
        lc.append(ls)

    df['Latitude']=df['Latitude'].astype(str)
    df['Longitude']=df['Longitude'].astype(str)
    df['geocode']=df['Latitude']+','+df['Longitude']

    eng_list=df['geocode'].to_list()
    le = []
    for i in eng_list:
        ls1=[]
        ls1.append(float(i.split(',')[0]))
        ls1.append(float(i.split(',')[1]))
        le.append(ls1)

    ds={}
    ups=[]
    up=[]
    for i in range(len(le)):
        #dx=[]
        lc.insert(0,le[i])
        #print(lc)
        lt=driver(lc)
        #time.sleep(10)

        x=lt[1:11]
        ups.append(x)
        d={}
        u=[]
        for a in x:
            ds.update({df['EmployeeCode'][i]:df['geocode'][i],df1['SubCaseID'][a-2]:df1['GeoCode'][a-2]})
            u.append(a-2)

        for ix in u:    
            df1=df1.drop(index=[ix])
        df1=df1.reset_index(drop=True)

        #ds.update(df['EmployeeCode']:df['Geocode'],df1['SubCaseID'][a-2]:df1['GeoCode'])

        #ts=[]
        #for k in d.values():
         #   ts.append(k)

        #up.remove(up[0])

        for p in ds:
            if p in geo_list:
                geo_list.remove(p)
        #print(len(geo_list))

        if len(df1)==0:
            break

        lc = []
        geo_list=df1['GeoCode'].to_list()
        for el in geo_list:
            ls=[]
            ls.append(float(el.split(',')[0]))
            ls.append(float(el.split(',')[1]))
            lc.append(ls)

        le = []
        for i in eng_list:
            ls1=[]
            ls1.append(float(i.split(',')[0]))
            ls1.append(float(i.split(',')[1]))
            le.append(ls1)
    return ds





