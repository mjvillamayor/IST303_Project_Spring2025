from flask import Flask, jsonify, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL Database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='Ben',
        password='testingpassword',
        database='medical_system',
        port=3306,
        auth_plugin='mysql_native_password'
    )
    return connection

# API to fetch medical history for a specific patient
@app.route('/api/medical-history/<int:patient_id>', methods=['GET'])
def get_medical_history(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT mh.history_id, mh.visit_date, mh.diagnosis, mh.treatment, mh.medications, mh.notes, p.first_name AS provider_first_name, p.last_name AS provider_last_name
        FROM PatientMedicalHistory mh
        JOIN Providers p ON mh.provider_id = p.provider_id
        WHERE mh.patient_id = %s
        ORDER BY mh.visit_date DESC;
    """
    cursor.execute(query, (patient_id,))
    medical_history = cursor.fetchall()
    cursor.close()
    conn.close()

    if medical_history:
        return jsonify(medical_history), 200
    else:
        return jsonify({'message': 'No medical history found for this patient.'}), 404

# Render the HTML page at the root URL
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)