#This module contains the functions needed to build the adjacency matrices for the graphs
#These functions names are stored in the check two database.

from random import choice

def build_random(vert_num):
  """This function randomly generates an adjacency matrix for an undirected graph of size n."""

  #opts store options to randomly choose from  
  opts = [0,1]
  matrix = []

  #initialize array
  for r in range(0, vert_num):
     matrix.append([])
     for c in range(0, vert_num):
        matrix[r].append(0)   

  #randomly generate adjacency matrix by adding a 1 or 0 in every spot
  for r in range(0, vert_num):
     for c in range(r, vert_num):
        if r == c:
           matrix[r][c] = 0
        else:
           matrix[r][c] = choice(opts)
           matrix[c][r] = matrix[r][c]

  return matrix

