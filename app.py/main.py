from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shredgnar20",
        database="medical_system"
    )

@app.route('/')
def home():
    return "Medical Provider Medication API is running!"

# Medications CRUD Operations
@app.route('/medications', methods=['POST'])
def add_medication():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medications (name, description, barcode, manufacturer) VALUES (%s, %s, %s, %s)",
        (data['name'], data['description'], data['barcode'], data['manufacturer'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Medication added successfully"}), 201

@app.route('/medications', methods=['GET'])
def get_medications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medications")
    medications = cursor.fetchall()
    conn.close()
    return jsonify(medications)

@app.route('/medications/<int:med_id>', methods=['PUT'])
def update_medication(med_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE medications SET name = %s, description = %s, barcode = %s, manufacturer = %s WHERE medication_id = %s",
        (data['name'], data['description'], data['barcode'], data['manufacturer'], med_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Medication updated successfully"})

@app.route('/medications/<int:med_id>', methods=['DELETE'])
def delete_medication(med_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medications WHERE medication_id = %s", (med_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Medication deleted successfully"})

# Patients CRUD Operations
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_info) VALUES (%s, %s, %s, %s, %s)",
        (data['first_name'], data['last_name'], data['date_of_birth'], data['gender'], data['contact_info'])
    )
    conn.commit()

    username = f"{data['first_name'].lower()}_{data['last_name'].lower()}"
    password = "Patient123!"  # You might want to generate this dynamically or let them set it

    cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
    cursor.execute(f"GRANT patient TO '{username}'@'localhost'")
    cursor.execute(f"SET DEFAULT ROLE patient FOR '{username}'@'localhost'")

    conn.commit()
    conn.close()

    return jsonify({"message": f"Patient {username} added and MySQL user created"}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return jsonify(patients)

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    return jsonify(patient) if patient else (jsonify({"message": "Patient not found"}), 404)

@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE patients SET first_name = %s, last_name = %s, date_of_birth = %s, gender = %s, contact_info = %s WHERE patient_id = %s",
        (data['first_name'], data['last_name'], data['date_of_birth'], data.get('gender'), data.get('contact_info'), patient_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Patient updated successfully"})

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Patient deleted successfully"})

# Providers CRUD Operations
@app.route('/providers', methods=['POST'])
def add_provider():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO providers (first_name, last_name, specialty, contact_info) VALUES (%s, %s, %s, %s)",
        (data['first_name'], data['last_name'], data['specialty'], data['contact_info'])
    )
    conn.commit()

    username = f"{data['first_name'].lower()}_{data['last_name'].lower()}"
    password = "Provider123!"  # Change this for security (e.g., generate dynamically)

    cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
    cursor.execute(f"GRANT provider TO '{username}'@'localhost'")
    cursor.execute(f"SET DEFAULT ROLE provider FOR '{username}'@'localhost'")

    conn.commit()
    conn.close()

    return jsonify({"message": f"Provider {username} added and MySQL user created"}), 201

@app.route('/providers', methods=['GET'])
def get_providers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers")
    providers = cursor.fetchall()
    conn.close()
    return jsonify(providers)

@app.route('/providers/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers WHERE provider_id = %s", (provider_id,))
    provider = cursor.fetchone()
    conn.close()
    return jsonify(provider) if provider else (jsonify({"error": "Provider not found"}), 404)

@app.route('/providers/<int:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE providers SET first_name = %s, last_name = %s, specialty = %s, contact_info = %s WHERE provider_id = %s",
                   (data['first_name'], data['last_name'], data.get('specialty'), data.get('contact_info'), provider_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Provider updated successfully"})

@app.route('/providers/<int:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM providers WHERE provider_id = %s", (provider_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Provider deleted successfully"})

# Prescriptions CRUD Operations
@app.route('/prescriptions', methods=['POST'])
def add_prescription():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO prescriptions (patient_id, provider_id, medication_id, dosage, frequency, start_date, end_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (data['patient_id'], data['provider_id'], data['medication_id'], data['dosage'], data['frequency'], data['start_date'], data.get('end_date'), data['status'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Prescription added successfully"}), 201

@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prescriptions")
    prescriptions = cursor.fetchall()
    conn.close()
    return jsonify(prescriptions)

@app.route('/prescriptions/<int:prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE prescriptions SET patient_id = %s, provider_id = %s, medication_id = %s, dosage = %s, frequency = %s, start_date = %s, end_date = %s, status = %s
        WHERE prescription_id = %s""",
        (data['patient_id'], data['provider_id'], data['medication_id'], data['dosage'], data['frequency'], data['start_date'], data.get('end_date'), data['status'], prescription_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Prescription updated successfully"})

@app.route('/prescriptions/<int:prescription_id>', methods=['DELETE'])
def delete_prescription(prescription_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prescriptions WHERE prescription_id = %s", (prescription_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Prescription deleted successfully"})

# Messages CRUD Operations
@app.route('/messages', methods=['POST'])
def add_message():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
        (data['sender_id'], data['receiver_id'], data['message'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Message sent successfully"}), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return jsonify(messages)

@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE messages SET message = %s WHERE message_id = %s",
        (data['message'], message_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Message updated successfully"})

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE message_id = %s", (message_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Message deleted successfully"})

# Alerts CRUD Operations
@app.route('/alerts', methods=['POST'])
def add_alert():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO alerts (patient_id, provider_id, message, status)
        VALUES (%s, %s, %s, %s)
        """,
        (data['patient_id'], data['provider_id'], data['message'], data['status'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Alert added successfully"}), 201

@app.route('/alerts', methods=['GET'])
def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alerts")
    alerts = cursor.fetchall()
    conn.close()
    return jsonify(alerts)

@app.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE alerts
        SET patient_id = %s, provider_id = %s, message = %s, status = %s
        WHERE alert_id = %s
        """,
        (data['patient_id'], data['provider_id'], data['message'], data['status'], alert_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Alert updated successfully"})

@app.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts WHERE alert_id = %s", (alert_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Alert deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)