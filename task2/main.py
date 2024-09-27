from flask import Flask, request, jsonify, abort
import json
import os
from threading import Lock

app = Flask(__name__)

# defining path of the request file
DATA_FILE = 'requests.json'

# Lock for managing file access (to ensure thread-safe writes)
file_lock = Lock()

# Utility function to load data from the JSON file
def load_requests():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Utility function to save data to the JSON file
def save_requests(requests):
    with file_lock:  # Ensure safe writes
        with open(DATA_FILE, 'w') as file:
            json.dump(requests, file, indent=4)

# Endpoint: POST /requests (Create a new service request)
@app.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    
    # Validate the required fields
    required_fields = ['id', 'guestName', 'roomNumber', 'requestDetails', 'priority']
    if not all(field in data for field in required_fields):
        abort(400, "Missing required fields")

    data['status'] = 'received'  # Default status

    # Load current requests
    requests = load_requests()
    
    for req in requests:
        # print(req)
        if(req['id']==data['id']):
            abort(400, "Request ID already exists")
    
    # Add the new request
    requests.append(data)

    # Save the updated list of requests
    save_requests(requests)

    return jsonify(data), 201

# Endpoint: GET /requests (Retrieve all requests sorted by priority)
@app.route('/requests', methods=['GET'])
def get_all_requests():
    requests = load_requests()
    
    # Sort requests by priority (ascending) and status
    sorted_requests = sorted(requests, key=lambda r: (r['priority'], r['status']))
    
    return jsonify(sorted_requests), 200

# Endpoint: GET /requests/<id> (Retrieve a specific request by ID)
@app.route('/requests/<string:request_id>', methods=['GET'])
def get_request_by_id(request_id):
    requests = load_requests()
    
    # Find the request by ID
    request_data = next((req for req in requests if req['id'] == request_id), None)
    
    if request_data is None:
        abort(404, "Request not found")
    
    return jsonify(request_data), 200

# Endpoint: PUT /requests/<id> (Update details or priority of an existing request)
@app.route('/requests/<string:request_id>', methods=['PUT'])
def update_request(request_id):
    requests = load_requests()
    data = request.get_json()
    
    # Find the request by ID
    request_data = next((req for req in requests if req['id'] == request_id), None)
    
    if request_data is None:
        abort(404, "Request not found")
    
    # Update request fields
    if 'guestName' in data:
        request_data['guestName'] = data['guestName']
    if 'roomNumber' in data:
        request_data['roomNumber'] = data['roomNumber']
    if 'requestDetails' in data:
        request_data['requestDetails'] = data['requestDetails']
    if 'priority' in data:
        request_data['priority'] = data['priority']
    if 'status' in data:
        request_data['status'] = data['status']

    # Save the updated list
    save_requests(requests)

    return jsonify(request_data), 200

# Endpoint: DELETE /requests/<id> (Delete a completed or canceled request)
@app.route('/requests/<string:request_id>', methods=['DELETE'])
def delete_request(request_id):
    requests = load_requests()
    
    # Find the request by ID
    request_data = next((req for req in requests if req['id'] == request_id), None)
    
    if request_data is None:
        abort(404, "Request not found")
    
    # Only allow deleting completed or canceled requests
    if request_data['status'] not in ['completed', 'canceled']:
        abort(400, "Only completed or canceled requests can be deleted")
    
    # Remove the request
    requests = [req for req in requests if req['id'] != request_id]
    
    # Save the updated list
    save_requests(requests)

    return '', 204

# Endpoint: POST /requests/<id>/complete (Mark a request as completed)
@app.route('/requests/<string:request_id>/complete', methods=['POST'])
def complete_request(request_id):
    requests = load_requests()
    
    # Find the request by ID
    request_data = next((req for req in requests if req['id'] == request_id), None)
    
    if request_data is None:
        abort(404, "Request not found")
    
    # Mark as completed
    request_data['status'] = 'completed'

    # Save the updated list
    save_requests(requests)

    return jsonify(request_data), 200

if __name__ == '__main__':
    app.run(debug=True)
    # disable debug = True when deploying to production
