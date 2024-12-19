import sqlite3 
import math
from helpers import *

DB = "TRGdatabase.db"

def checkInputs(k,l,d,D):
    """This function checks the given inputs against all formulas in the check one db."""
    
    #Gets formulas and replaces variables with values
    formulas, bibkeys = getCheck1Entries()
    repFormulas = replaceVars(k,l,d,D,0,formulas)

    notReal = False
    fails = []
    failBibs = []

    #Evaluates each formulas and add it and bibkey to list if False 
    for i in range(0,len(repFormulas)):
        test = evaluateMult(repFormulas[i])
        if not test:
           notReal = True
           fails.append(formulas[i])
           failBibs.append(bibkeys[i])

    return notReal, fails, failBibs


def check_n(k,l,d,D,n):
   """This function checks the initial params plus the n param against the formulas in the check two db """

   #sanitizes params for known bad inputs
   if not sanitize_n(k,l,d,D,n):
      return True, [], [], []
 
   
   #Gets formulas and replaces variables with values
   formulas, bibkeys, builders = getCheck2Entries()
   repFormulas = replaceVars(k,l,d,D,n, formulas)
   
   notReal = True 
   passes = []
   passBibs = []
   passBuilds = []

      
   #Evaluates each formula and add it, the bibkey, and the builder to lists if True 
   for i in range(0, len(repFormulas)):
      test = evaluateMult(repFormulas[i])
      if test:
         passes.append(formulas[i])
         passBibs.append(bibkeys[i])
         passBuilds.append(builders[i])
         notReal = False
          
   return notReal, passes, passBibs, passBuilds


def get_bib_DB():
  '''This function retrieves the pieces of the bibliographies from the database '''

  #connects to the database
  connect = sqlite3.connect(DB)
  cursor = connect.cursor()

  #selects all rows from bib database
  cursor.execute('''SELECT * FROM BIBLIOGRAPHY;''')

  bibKeys = []
  authors = []
  titles = []
  years = []
  bibtexs = []

  bib_elems = []

  #appends each to the lists
  for i in cursor:
     bibKeys.append(str(i[0]))
     authors.append(str(i[1])) 
     titles.append(str(i[2])) 
     years.append(str(i[3]))
     bibtexs.append(str(i[5]))

  bib_elems.append(bibKeys)
  bib_elems.append(authors)
  bib_elems.append(titles)
  bib_elems.append(years)
  bib_elems.append(bibtexs)

  return bib_elems

