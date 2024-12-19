import sys
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)
  
# this was cringe
from access_db import *
from helpers import *
from end_points import *
import pytest

def test_checkInput_real(mocker):
  mock1 = mocker.patch("access_db.getCheck1Entries")
  mock1.return_value = ["k<=l<=d<=D"], ["Test-1"] 

  notReal, fails, failBibs = checkInputs(1, 2, 3, 4)
  assert notReal == False
  assert fails == []
  assert failBibs == []

  notReal, fails, failBibs = checkInputs(4, 9, 11, 22)
  assert notReal == False
  assert fails == []
  assert failBibs == []

  
def test_checkInput_notReal(mocker):

  mock1 = mocker.patch("access_db.getCheck1Entries")
  mock1.return_value = ["k<=l<=d<=D", "k>l", "k<=D"], ["Test-1", "Test-2", "Test-3"] 

  checkBibs1 = ["Test-1", "Test-3"]
  checkForms1 = ["k<=l<=d<=D","k<=D"]

  checkBibs2 = ["Test-2"]
  checkForms2 = ["k>l"]

  notReal, fails, failBibs = checkInputs(6, 5, 4, 3)
  assert notReal == True
  assert fails == checkForms1
  assert failBibs == checkBibs1

  notReal, fails, failBibs = checkInputs(23, 214, 215, 409)
  assert notReal == True
  assert fails == checkForms2
  assert failBibs == checkBibs2


def test_check_n_good_sanitize1(mocker):
  mock1 = mocker.patch("access_db.getCheck2Entries")
  mock1.return_value = ["k>l>d>D", "k>l", "n>0?!True:True"], ["Test-1", "Test-2", "Test-3"],['None','None','builder'] 

  notReal, passes, passBibs, passBuilds = check_n(1,2,3,4,3)
  assert notReal == True
  assert passes == []
  assert passBibs == []
  assert passBuilds == []
  
def test_check_n_good_sanitize2(mocker):
  mock1 = mocker.patch("access_db.getCheck2Entries")
  mock1.return_value = ["k>l>d>D", "k<=l", "n>0?True:True"], ["Test-1", "Test-2", "Test-3"],['None','None','builder'] 

  checkForms1 = ["k<=l","n>0?True:True"]
  checkBuilds1 = ['None', 'builder']
  checkBibs1 = ["Test-2", "Test-3"]
 
  checkForms2 = ["k>l>d>D","n>0?True:True"]
  checkBuilds2 = ['None', 'builder']
  checkBibs2 = ["Test-1", "Test-3"]

  notReal, passes, passBibs, passBuilds = check_n(1,2,3,4,5)
  assert notReal == False
  assert passes == checkForms1
  assert passBibs == checkBibs1
  assert passBuilds == checkBuilds1

  notReal, passes, passBibs, passBuilds = check_n(23, 22, 21, 20, 122)
  assert notReal == False
  assert passes == checkForms2
  assert passBibs == checkBibs2
  assert passBuilds == checkBuilds2


def test_check_n_bad_sanitize(mocker):
  mock1 = mocker.patch("access_db.sanitize_n")
  mock1.return_value = False 

  notReal, passes, passBibs, passBuilds = check_n(1, 3, 33, 99, 1)
  assert notReal == True
  assert passes == []
  assert passBibs == []
  assert passBuilds == []

def test_get_bib_DB(mocker):
  elems = get_bib_DB()

  # Check that all items are there then check they arent empty
  assert len(elems) == 5
  assert elems[0] != []
  assert elems[1] != []
  assert elems[2] != []
  assert elems[3] != []
  assert elems[4] != []


