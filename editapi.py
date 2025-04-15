from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='Ben',
        password='testingpassword',
        database='medical_system',
        port=3306,
        auth_plugin='mysql_native_password'
    )

@app.route('/')
def home():
    return render_template('editindex.html')  # Serve the HTML page with the form

@app.route('/api/edit-history/<int:patient_id>', methods=['PUT'])
def edit_patient_history(patient_id):
    data = request.get_json()
    diagnosis = data.get('diagnosis')
    treatment = data.get('treatment')
    medications = data.get('medications')
    notes = data.get('notes')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE PatientMedicalHistory
        SET diagnosis = %s, treatment = %s, medications = %s, notes = %s
        WHERE patient_id = %s;
    """
    cursor.execute(query, (diagnosis, treatment, medications, notes, patient_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Medical history updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5050)