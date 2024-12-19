import pytest
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from helium import *
"""
   Followed this site initially: 
       https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
   Info about testing with selenium:
       https://pytest-with-eric.com/automation/pytest-selenium/
       
"""

@pytest.fixture
def opts(): 
  options = FirefoxOptions()
  options.add_argument("--width=1920")
  options.add_argument("--height=1080")
  return options

@pytest.fixture
def base_url():
  return "127.0.0.1:5000"

@pytest.fixture
def input_url(base_url):
  return base_url + "/input" # hopefully work :/

@pytest.fixture
def bib_url():
  return base_url + "/bib"
  

@pytest.fixture
def driver(opts):
  driver = start_firefox("127.0.0.1:5000", headless=True, options=opts)

  yield driver

  driver.quit()

def test_home(driver):
  '''
    Test access home page, relevant elements are present,
    and "Get Started!" button works
  '''
  assert driver.title == "Toadally Real Graphs"
  assert ListItem("Home").exists()
  assert ListItem("Enter Input").exists()
  assert ListItem("Bibliography").exists()
  assert Button("Get Started!").exists() == True
  
  click("Get Started!")

  assert Button("Submit").exists() # jank way of checking if we make it to input page

  driver.quit()
  

def test_input(driver):
  '''
    Go to enter input, put in values, miss one and check that missing inputs comes up,
    finish inputs, check that n pops up, enter n
    check that matrix and image button exists
  '''
  click("Enter Input")
  assert Button("Submit").exists() # basically just check we're on input

  click(S("@vertex"))
  press("1")
  click(S("@edge"))
  press("2")

  click(Button("Submit"))
  assert Text("Missing or Invalid Inputs").exists()

  click(S("@min"))
  press("3")
  click(S("@max"))
  press("ff")

  click(Button("Submit"))
  assert Text("Missing or Invalid Inputs").exists()

  click(S("@max"))
  press("4")

  click(Button("Submit"))
  assert Text("This is POTENTIALLY a Realizable Graph").exists()

  click(S("@n"))
  press("5")

  click(Button("Final Submit"))

  assert Text("This IS a Realizable Graph").exists()
  assert Button("image").exists()
  assert Button("matrix").exists()


  driver.quit()


def test_paperbib(driver):
  click("Bibliography")

  assert Text("Welcome to the Bibliography!").exists()
  
  click(Text(below="Hover over a citation and click to copy!"))
  assert Alert().text == "Citation copied to clipboard!"

  Alert().accept() # click OK on alert and then check it worked
  assert Text("Welcome to the Bibliography!").exists()

















