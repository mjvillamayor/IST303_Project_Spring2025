(venv) benmorehead@Bens-MacBook-Air-7 app.py % curl -X POST http://127.0.0.1:5000/medications \
-H "Content-Type: application/json" \
-d '{"name": "Aspirin", "description": "Pain reliever", "barcode": "123456", "manufacturer": "Bayer"}'
{
  "message": "Medication added successfully"
}
(venv) benmorehead@Bens-MacBook-Air-7 app.py % curl -X GET http://127.0.0.1:5000/medications
[
  {
    "barcode": "123456",
    "created_at": "Wed, 26 Feb 2025 14:52:10 GMT",
    "description": "Pain reliever",
    "manufacturer": "Bayer",
    "medication_id": 1,
    "name": "Aspirin"
  }
]