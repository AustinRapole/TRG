import os
from base64 import *
import sqlite3 
import math
import uuid
from builder import *
from draw_graph import *

DB = 'TRGdatabase.db'

def gen_path(path, ext):
   """This function generates a random temp file name"""
     
   return path + str(uuid.uuid4()) + ext  


def handle_file(path):
   """This function turns file into a base4 encoded string then deletes the file. """

   #makes sure the file exits
   if not os.path.exists(path):
      return 'None'

   #opens file and encodes contents
   with open(path, 'rb') as image:
      image_bytes = b64encode(image.read()) 

   #deletes file
   os.remove(path)

   return image_bytes.decode('ascii')  


def construct_graphs(builders, n):
      """This function handles process of creating base64 encoding of the csv file for the adjacency matrix and 
      the png file of the graph image, using the given builder functions"""

      #stores base64 strings for csvs and pngs
      adj_matrices = []
      images = []
      
      #loops through builders functions
      for b in builders:

          #if none add, none place holder
          if b == None or n >= 50:
             adj_matrices.append('None')
             images.append('None')
             continue

	  #try to run builder function and add None if failed
          try:
             matrix = eval(b + "(" + str(n) + ")")
          except:
             adj_matrices.append('None')
             images.append('None')
             continue

          #creates file, encodes, and deletes file then adds string to list
          img_path = gen_path("Drawings/", ".png")    
          create_graph_image(matrix, img_path, n)
          image_bytes = handle_file(img_path)	  
          images.append(image_bytes)

          #creates file, encodes, and deletes file then adds string to list
          csv_path = gen_path("Matrices/" , ".csv")    
          create_graph_matrix(matrix, csv_path)
          matrix_bytes = handle_file(csv_path)
          adj_matrices.append(matrix_bytes)

      return adj_matrices, images

def getCheck1Entries():
    """This function gets the data from each row in CHECKONE.""" 

    connect = sqlite3.connect(DB)
    cursor = connect.cursor()
    cursor.execute('''SELECT * FROM CHECKONE;''')

    formula = []
    bibkeys = []
     
    #adds bibkeys and formulas to list
    for i in cursor:
        bibkeys.append( str(i[0]) )
        formula.append( str(i[1]) )

    cursor.close()
    connect.close()

    return formula, bibkeys


def getCheck2Entries():
    """This function gets the data from each row in CHECKTWO. """  

    connect = sqlite3.connect(DB)
    cursor = connect.cursor()
    cursor.execute('''SELECT * FROM CHECKTWO;''')

    formula = []
    bibkeys = []
    builders = []


    #adds bibkeys, formulas, and builders to list
    for i in cursor:
        bibkeys.append( str(i[0]) )
        formula.append( str(i[1]) )
        builders.append( str(i[2]) )

    cursor.close()
    connect.close()

    return formula, bibkeys, builders


def completeGraph(d,n):
    return (d<(n-1))

def regularGraph(d,D):
    return (d==D)

def getSanitizers():
    """This function gets all the formulas from the sanitizer database."""

    connect = sqlite3.connect(DB)
    cursor = connect.cursor()
    cursor.execute('''SELECT * FROM SANITIZEN;''')

    formulas = []

    #adds each row of the database 
    for i in cursor:
       formulas.append( str(i[0]) )
    
    return formulas 


def replaceVars(k,l,d,D,n, formulas):
    """This funcitons replace and variables in a list of formulas with their corresponding values."""

    fixedList = []

    #loop through the list and replaces vars with the appropriate values
    for f in formulas:
        temp = list(f)
        for c in range(len(temp)):
            if temp[c] == 'k':
                temp[c] = str(k)
            if temp[c] == 'l':
                temp[c] = str(l)
            if temp[c] == 'd':
                temp[c] = str(d)
            if temp[c] == 'D':
                temp[c] = str(D)
            if temp[c] == 'n':
                temp[c] = str(n)
            if temp[c] == 'C':
                temp[c] = str(completeGraph(d,n))
            if temp[c] == 'R':
                temp[c] = (" " + str(regularGraph(d,D)) + " ")
            if temp[c] == "&":
                temp[c] = str(" and ")
            if temp[c] == "!":
                temp[c] = str(" not ")
                
        #turns list of chars back into a string       
        fixedList.append(''.join(temp))

    return fixedList


def sanitize_n(k,l,d,D,n):
    """This function sanitizes the list of params using the sanitizing formulas """
    formulas = getSanitizers()
    formulas = replaceVars(k,l,d,D,n, formulas)

    #if any formula is false retrun False
    for f in formulas:
       if not evaluateMult(f):
          return False

    return True

def evaluateMult(string):
    """This funciton evaluates our if statement syntax."""

    conditional = -1
    expression = -1
    test = False

    #Find ?
    if(string.find("?") != -1):

        #find location of the ? and the :
        for i in range(0, len(string)):
            if(string[i] == '?'):
                conditional = i
            if(string[i] == ':'):
                expression = i
        #If condition true, return eval of stuff before colon. Else, return eval of the stuff after  		
        if(eval(string[0:conditional])):
            test = eval(string[conditional+1:expression])
        else:
            test = eval(string[expression+1:len(string)])

    #No if. just a normal eval function call
    else:
        test = eval(string)

    return test

