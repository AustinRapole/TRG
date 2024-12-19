import sys
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)
  
# this was cringe
import pytest
import TRGadmin
import access_db 
import helpers 

TRGadmin.db = "test_admin.db" 
access_db.DB = "test_admin.db" 
helpers.DB = "test_admin.db" 

def test_add():


  test_file1 = "adminTest/addTest.txt"
  test_file2 = "adminTest/addBib.txt"
  
  check1_form = ["FORMULA"]
  check1_bib = ["HUNTER"]

  check2_form = ["FORMULA","FORMULA1"]
  check2_bib = ["NATHAN","NATHAN1"]
  check2_func = ["FUNC","FUNC1"]

  check_sans = ["SOMETHING"]
  check_bib = [["NATHAN","Paine","Bethea-13"],["author","Thomas Paine",""],["title","Common Sense",""],["2016","1776",""]]

  TRGadmin.addFun(test_file1)
  TRGadmin.addFun(test_file2)

  formulas1, bibkeys1 = helpers.getCheck1Entries()
  formulas2, bibkeys2, funcs = helpers.getCheck2Entries()
  sans = helpers.getSanitizers()
  bibs = access_db.get_bib_DB()

  assert formulas1 == check1_form
  assert bibkeys1 == check1_bib

  assert formulas2 == check2_form
  assert bibkeys2 == check2_bib
  assert check2_func == funcs

  assert sans == check_sans
  assert bibs[:4] == check_bib
  
  
def test_update():
   
  test_file = "adminTest/update.txt"
  
  check1_form = ["NEWVAL"]
  check1_bib = ["HUNTER"]

  check2_form = ["FORMULA","FORMULA1"]
  check2_bib = ["NATHAN","NATHAN1"]
  check2_func = ["NEWFUNC","FUNC1"]

  check_sans = ["NEWFORM"]
  check_bib = [["NEWBIB","Paine","Bethea-13"],["author","Thomas Paine","NATHAN"],["title","Common Sense",""],["2016","1776",""]]

  TRGadmin.upFun(test_file)

  formulas1, bibkeys1 = helpers.getCheck1Entries()
  formulas2, bibkeys2, funcs = helpers.getCheck2Entries()
  sans = helpers.getSanitizers()
  bibs = access_db.get_bib_DB()

  assert formulas1 == check1_form
  assert bibkeys1 == check1_bib

  assert formulas2 == check2_form
  assert bibkeys2 == check2_bib
  assert check2_func == funcs

  assert sans == check_sans
  assert bibs[:4] == check_bib


def test_delete():
   

  test_file = "adminTest/delete.txt"

  TRGadmin.delFun(test_file)

  formulas1, bibkeys1 = helpers.getCheck1Entries()
  formulas2, bibkeys2, funcs = helpers.getCheck2Entries()
  sans = helpers.getSanitizers()
  bibs = access_db.get_bib_DB()

  assert formulas1 == []
  assert bibkeys1 == []

  assert formulas2 == []
  assert bibkeys2 == []
  assert funcs == []

  assert sans == []
  assert bibs[:4] == [[],[],[],[]]
  
  






