import sys
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)
  
# this was cringe
from helpers import *
from end_points import *
import pytest

@pytest.fixture
def getCheck1_form():
  return ['k<=l<=d<=D', 'R&l<d?l%2==1&d%2==1:True', 'k==1?2*(l)<=D:True']

@pytest.fixture
def getCheck1_bib():
  return ['Whitney-1', 'TEMP-1', 'TEMP-2']

@pytest.fixture
def getCheck2_form():
  return ['n>D+1', '!C?n>=2*(d+1)-k:True', 'l<=d?n>=max(2*(d+1),D-l+1+(d+1), D+k-l+(d+1)):True']

@pytest.fixture
def getCheck2_bib():
  return ['Temp-1', 'Temp-3', 'Temp-4']

@pytest.fixture
def getCheck2_builders():
  return ['None', 'build_random', 'build_random']

@pytest.fixture
def getSanit_form():
  return ['n>0']

@pytest.fixture
def replaceVar_forms():
  return ["k<=l<=d<=D<=n&C!R", "!&", "", "?", "KLNcr"]

@pytest.fixture
def replaceVar_check():
  return ['1<=2<=3<=4<=5 and True not  False ', ' not  and ', '', '?', 'KLNcr']


def test_handle_file(tmp_path):
   path = "testDir/nope.txt"

   file = tmp_path / path
   file.parent.mkdir()

   result = handle_file(file)
   assert result == 'None'

   file.write_text("hello world")
   assert os.path.exists(file) == True

   result = handle_file(file)
   assert result == "aGVsbG8gd29ybGQ="
   assert os.path.exists(file) == False

def test_construct_graphs(tmp_path, mocker):
      
   img_path = "testDir/image.png"
   csv_path = "testDir/matrix.csv"

   image = tmp_path / img_path
   image.parent.mkdir()
   csv = tmp_path / csv_path
   
   mock1 = mocker.patch("helpers.gen_path")
   mock1.return_value = image

   adj, img = construct_graphs([None,'build', None, 'build_random'],5)
   check = ['None','None','None']

   assert adj[:3] == check
   assert adj[3] != 'None'

   assert img[:3] == check
   assert img[3] != 'None'

   
def test_getCheck1Entries(getCheck1_form, getCheck1_bib):
  formula, bib = getCheck1Entries()

  assert formula == getCheck1_form
  assert bib == getCheck1_bib


def test_getCheck2Entries(getCheck2_form, getCheck2_bib, getCheck2_builders):
  formula, bib, builders = getCheck2Entries()

  assert formula == getCheck2_form
  assert bib == getCheck2_bib
  assert builders == getCheck2_builders


def test_getSanitizers(getSanit_form):
  form = getSanitizers()

  assert form == getSanit_form


def test_sanitize_n(mocker):
  ok = sanitize_n(1,2,3,4,5)  
  assert ok == True # should only check that "n > 0"

  ok = sanitize_n(1,1,1,1,1)
  assert ok == True

  ok = sanitize_n(1,2,3,4,-1)
  assert ok == False

  ok = sanitize_n(1,2,3,4,0)
  assert ok == False

  mock = mocker.patch("helpers.getSanitizers")
  mock.return_value = ["k==l==d==D==n"]
  
  ok = sanitize_n(1,1,1,1,1)
  assert ok == True

  ok = sanitize_n(1,2,3,4,5)
  assert ok == False


def test_replaceVar(replaceVar_forms, replaceVar_check):
  form = replaceVars(1,2,3,4,5, replaceVar_forms)

  assert form == replaceVar_check


def test_evalMult(mocker):
  forms = ["2==2?4+4:True","2==4?4+4:False","False?50+2:1>0",
  "True?20+9:1>0","False?99:1>0,222",
  "1<2<3<4","4<2<3<4<5"]


  assert evaluateMult(forms[0]) == 8
  assert evaluateMult(forms[1]) == False
  assert evaluateMult(forms[2]) == True
  assert evaluateMult(forms[3]) == 29
  assert evaluateMult(forms[4]) == (True,222)
  assert evaluateMult(forms[5]) == True
  assert evaluateMult(forms[6]) == False







