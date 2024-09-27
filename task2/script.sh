#!/bin/bash


# remove requests.json file if it exists
rm -f requests.json

# create some requests
curl -X POST -H "Content-Type: application/json" -d '{"id": "1", "guestName": "John Doe", "roomNumber": 101, "requestDetails": "Towels", "priority": 1}' http://localhost:5000/requests

curl -X POST -H "Content-Type: application/json" -d '{"id": "2", "guestName": "Manaswi Raj", "roomNumber": 102, "requestDetails": "Towels", "priority": 2}' http://localhost:5000/requests

curl -X POST -H "Content-Type: application/json" -d '{"id": "3", "guestName": "Alex Smith", "roomNumber": 104, "requestDetails": "Towels", "priority": 3}' http://localhost:5000/requests

curl -X POST -H "Content-Type: application/json" -d '{"id": "4", "guestName": "Vishal Sharma", "roomNumber": 106, "requestDetails": "Towels", "priority": 1}' http://localhost:5000/requests


echo "Requests created successfully"
echo "============================================================="

# get all requests
curl -X GET http://localhost:5000/requests

echo "printed all pending requests"
echo "============================================================="

# get request by id
curl -X GET http://localhost:5000/requests/2

echo "printed request with a particular id"
echo "============================================================="


# update request by id

curl -X PUT -H "Content-Type: application/json" -d '{"priority": 5, "status": "in progress"}' http://localhost:5000/requests/1
curl -X GET http://localhost:5000/requests

echo "updated request with a particular id"
echo "============================================================="
# complete a request 
curl -X POST http://localhost:5000/requests/1/complete


curl -X GET http://localhost:5000/requests
echo "completed request with a particular id"
echo "============================================================="

# Delete a request
curl -X DELETE http://localhost:5000/requests/5

echo "deleted request with a particular id"
curl -X GET http://localhost:5000/requests
echo "============================================================="