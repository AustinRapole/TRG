import sys
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from end_points import *
from __init__ import create_app

from flask import request

import pytest
import requests


@pytest.fixture
def app():
  app = create_app()
  app.config.update({"TESTING" : True,
  })
  yield app


@pytest.fixture
def client(app):
  return app.test_client()


@pytest.fixture
def sample_graph_input():
  return {"vert_con" : 1, "edge_con" : 2, "min_deg" : 3, "max_deg" : 4}

@pytest.fixture
def sample_graph_input_n():
  return {"vert_con" : 1, "edge_con" : 2, "min_deg" : 3, "max_deg" : 4, "n" : 5}

@pytest.fixture
def input_url():
  return "http://127.0.0.1:5000/inputGraph"

@pytest.fixture
def bib_url():
  return "http://127.0.0.1:5000/getBib"

@pytest.fixture
def draw_url():
  return "http://127.0.0.1:5000/drawGraph"


def test_graph_data_success(sample_graph_input, input_url):
  # Not necessarily input that produces a graph just that the
  # input was accepted with no issues
  response = requests.post(input_url, json = sample_graph_input)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == True


def test_graph_data_no_vert(sample_graph_input, input_url):
  no_vert = sample_graph_input
  del no_vert["vert_con"]

  response = requests.post(input_url, json = no_vert)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False


def test_graph_data_no_edge(sample_graph_input, input_url):
  no_edge = sample_graph_input
  del no_edge["edge_con"]

  response = requests.post(input_url, json = no_edge)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False


def test_graph_data_no_min(sample_graph_input, input_url):
  no_min = sample_graph_input
  del no_min["min_deg"]

  response = requests.post(input_url, json = no_min)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False


def test_graph_data_no_max(sample_graph_input, input_url):
  no_max = sample_graph_input
  del no_max["max_deg"]

  response = requests.post(input_url, json = no_max)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False


def test_graph_data_not_int(sample_graph_input, input_url):
  not_int = sample_graph_input
  not_int["vert_con"] = "AA"

  response = requests.post(input_url, json = not_int)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False


def test_graph_data_empty_str(sample_graph_input, input_url):
  empty = sample_graph_input
  empty["min_deg"] = ""

  response = requests.post(input_url, json = empty)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False


def test_graph_data_checkInps_exception(sample_graph_input, input_url, mocker, client):
  #mock = mocker.patch("end_points.request.get_json", return_value = sample_graph_input)
  mock1 = mocker.patch("end_points.checkInputs", side_effect=Exception("Mock Error"))

  response = client.post("/inputGraph", json = sample_graph_input)

  json = response.json

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json


def test_graph_data_refuse(sample_graph_input, mocker, client):
  response = client.get("/inputGraph")

  assert response.status_code == 405 # Method not allowed


def test_get_bib(bib_url):
  response = requests.get(bib_url)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == True
  assert json["bibs"] != [] # not the empty list


def test_get_bib_exception(mocker, client):
  mock1 = mocker.patch("end_points.get_bib_DB", side_effect = Exception("Mock Error"))

  response = client.get("/getBib")
  json = response.json

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json


def test_get_bib_refuse(sample_graph_input, client):
  response = client.post("getBib", json = sample_graph_input)

  assert response.status_code == 405 # Method not allowed

def test_draw_graph_ok(draw_url, sample_graph_input_n):
  response = requests.post(draw_url, json = sample_graph_input_n)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == True


def test_draw_graph_missing(draw_url, sample_graph_input_n):
  missing = sample_graph_input_n
  del missing["vert_con"]

  response = requests.post(draw_url, json = missing)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json

  missing = sample_graph_input_n
  del missing["n"]

  response = requests.post(draw_url, json = missing)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json
  

def test_draw_graph_empty(draw_url, sample_graph_input_n):
  empty = sample_graph_input_n
  empty["vert_con"] = ""

  response = requests.post(draw_url, json = empty)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json

  empty = sample_graph_input_n
  empty["n"] = ""

  response = requests.post(draw_url, json = empty)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json


def test_draw_graph_nonint(draw_url, sample_graph_input_n):
  non = sample_graph_input_n
  non["vert_con"] = ":'("

  response = requests.post(draw_url, json = non)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json

  non = sample_graph_input_n
  non["n"] = ":'("

  response = requests.post(draw_url, json = non)
  json = response.json()

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json


def test_draw_graph_notreal_false(draw_url, sample_graph_input_n, mocker, client):
  mock1 = mocker.patch("end_points.check_n")
  mock1.return_value = False, ["Test Pass"], ["Test bib"], ["Test build"]

  response = client.post("/drawGraph", json = sample_graph_input_n)
  json = response.json
  print(json)

  assert response.status_code == 200
  assert json["success"] == True
  assert json["notReal"] == False
  assert json["matrices"] != []
  assert json["passes"] != []
  assert json["images"] != []
  assert json["bibkeys"] != []


def test_draw_graph_notreal_true(draw_url, sample_graph_input_n, mocker, client):
  mock1 = mocker.patch("end_points.check_n")
  mock1.return_value = True, [], [], []

  response = client.post("/drawGraph", json = sample_graph_input_n)
  json = response.json

  print(json)
  assert response.status_code == 200
  assert json["success"] == True
  assert json["notReal"] == True


def test_draw_graph_check_n_exception(sample_graph_input_n, mocker, client):
  mock1 = mocker.patch("end_points.check_n", side_effect = Exception("Mock Error"))

  response = client.post("/drawGraph", json = sample_graph_input_n)
  json = response.json

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json
  assert "inputs" in json["error"]


def test_draw_graph_constr_graph_exception(sample_graph_input_n, mocker, client):
  mock1 = mocker.patch("end_points.construct_graphs", side_effect = Exception("Mock Error"))

  response = client.post("/drawGraph", json = sample_graph_input_n)
  json = response.json

  assert response.status_code == 200
  assert json["success"] == False
  assert "error" in json
  assert "graph" in json["error"]


def test_draw_graph_refuse(client):
  response = client.get("/drawGraph")

  assert response.status_code == 405 # Method not allowed













