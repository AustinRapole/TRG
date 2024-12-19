from flask import Blueprint, jsonify, request
from access_db import * 
from draw_graph import *
from helpers import *

end_points = Blueprint('end_points', __name__)


@end_points.route('/inputGraph', methods=['POST'])
def check_inputs():
    '''This endpoint takes in the intial graph inputs and gets them against the phase 1 database.
       It will return with indicate if the graph is not real and a list of violated formulas.'''

    print("Connected to /inputGraph")

    #lists of input fields
    fields = ['vert_con', 'edge_con', 'min_deg', 'max_deg']    

    data = request.get_json()

    #verifies that all fields are present in request
    for f in fields:
       if f not in data:
          return jsonify({'success': False, 'error': "Error - Missing input field"}), 200

    #catches any invalid types
    try:
        vert_con = int(data['vert_con'])
        edge_con = int(data['edge_con'])
        min_deg = int(data['min_deg'])
        max_deg = int(data['max_deg'])

    except ValueError:
        return jsonify({'success': False, 'error': "Error - Invalid input type"}), 200

    #catches any errors that could occur when checking the db
    try: 
        notReal, fails, bibkeys = checkInputs(vert_con, edge_con, min_deg, max_deg)
    except:
        return jsonify({'success': False, 'error': "Error - Unknown error occurred when checking inputs"}), 200 

    #creates response
    response = {'notReal' : notReal, 'failed_checks' : [fails, bibkeys], 'success' : True} #gets response

    return jsonify(response), 200


@end_points.route('/getBib', methods=['GET'])
def get_bib():
    '''This endpoint retrieves all entries in the bibliography db, sending them in the form of a list of lists''' 

    print("Connected to /get_req")

    #catches any issues that might occur when retrieving bibs from database
    try:
       refs = get_bib_DB()
    except:
        return jsonify({'success': False, 'error': "Error - Unknown error occurred when retrieving bibliographies"}), 200 

    #creates json response	
    response = {'success' : True, 'bibs' : refs} #gets response
    return jsonify(response), 200


@end_points.route('/drawGraph', methods=['POST'])
def draw_graph():
    '''This endpoint takes in the number of vertices, checks to see if it is real, and then attempts to draw it'''  

    print("Connected to /get_req")
    
    #list of all required fields
    fields = ['vert_con', 'edge_con', 'min_deg', 'max_deg', 'n']    

    data = request.get_json()

    #verifies that all fields are in the request
    for f in fields:
       if f not in data:
          return jsonify({'success': False, 'error': "Error - Missing input field"}), 200

    #checks that all inputs are integers
    try:
        vert_con = int(data['vert_con'])
        edge_con = int(data['edge_con'])
        min_deg = int(data['min_deg'])
        max_deg = int(data['max_deg'])
        n = int(data['n'])

    except ValueError:
        return jsonify({'success': False, 'error': "Error - Invalid input type"}), 200

    #catches all potential errors that might occur when checking formulas in db	
    try: 
       notReal, passes, bibkeys, builders  = check_n(vert_con, edge_con, min_deg, max_deg, n)
    except:
        return jsonify({'success': False, 'error': "Error - Unknown error occurred when checking inputs"}), 200 

    #draws all graph if it is real
    if not notReal:
       #catches all potential errors caused by drawing graph
       try:	
          matrices, images  = construct_graphs(builders,n)
          response = {'notReal' : notReal, 'passes' : passes, 'bibkeys' : bibkeys, 'matrices' : matrices, 'images' : images, 'success' : True} #gets response
       except:
          return jsonify({'success': False, 'error': "Error - Unknown error occurred when drawing graph"}), 200 

    else:   
       response = {'notReal' : notReal, 'success' : True} #gets response

    #creates response 	  
    return jsonify(response), 200


