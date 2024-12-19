from networkx import nx_agraph, Graph
from builder import *
from random import *
from pygraphviz import *


def create_graph_image(matrix, path, n):
   """This function uses pyghaphviz to draw a image of the graph from an adj matrix."""

   #Graph Object initialized
   G = Graph(overlap=False, splines = True)

   #adds all edges from adj matrix
   for i in range(0, n): 
      for j in range(0, n): 
        if matrix[i][j] == 1: 
            G.add_edge("V"+str(i),"V"+str(j)) 
   
   A = nx_agraph.to_agraph(G)

   #Format Graph
   A.node_attr['shape'] = 'circle'
   A.node_attr['color'] = 'blue'
   A.edge_attr['color'] = 'green'

   #Draw
   A.layout() 
   A.draw(path) 


def create_graph_matrix(matrix, path):
   """This function takes in an adj matrix and creates a csv file from it."""
   
   #Open file
   file = open(path,'w')
   csv = ""

   #create string of csv
   for row in matrix:
      str_row = ""
      for n in row: 
         str_row = str_row + str(n) + ','	
      csv = csv + str_row[:len(str_row)-1] + '\n'


   #Write to file
   file.write(csv[:len(csv)-1]) 

