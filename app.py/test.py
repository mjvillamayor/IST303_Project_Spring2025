curl -X POST http://127.0.0.1:5000/medications \
-H "Content-Type: application/json" \
-d '{"name": "Aspirin", "description": "Pain reliever", "barcode": "123456", "manufacturer": "Bayer"}'

curl -X GET http://127.0.0.1:5000/medications
