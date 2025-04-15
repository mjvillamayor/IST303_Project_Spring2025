from flask import Flask, jsonify, render_template, request, redirect, url_for
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

# Homepage: Choose Patient or Provider
@app.route('/')
def home():
    return render_template('home.html')

# --- Role Selection Route ---
@app.route('/role/<role>')
def role(role):
    # Check if the user is a provider or a patient
    if role == 'patient':
        return redirect(url_for('patient_dashboard'))
    elif role == 'provider':
        return redirect(url_for('provider_dashboard'))
    else:
        return 'Invalid role', 404

# --- Provider Dashboard ---
@app.route('/provider_dashboard')
def provider_dashboard():
    # Here you would add an access check based on user roles if needed
    return render_template('provider.html')

# --- Patient Dashboard ---
@app.route('/patient_dashboard')
def patient_dashboard():
    # Here you would add an access check based on user roles if needed
    return render_template('patient.html')

# Patient: View Medical History
@app.route('/patient/<int:patient_id>')
def view_medical_history(patient_id):
    return render_template('patient.html', patient_id=patient_id)

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

# Provider: Edit or Create Medical History
@app.route('/provider')
def provider():
    return render_template('provider.html')

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

@app.route('/api/create-history', methods=['POST'])
def create_patient_history():
    data = request.get_json()
    patient_id = data.get('patient_id')
    provider_id = data.get('provider_id')
    visit_date = data.get('visit_date')
    diagnosis = data.get('diagnosis')
    treatment = data.get('treatment')
    medications = data.get('medications')
    notes = data.get('notes')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO PatientMedicalHistory (patient_id, provider_id, visit_date, diagnosis, treatment, medications, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (patient_id, provider_id, visit_date, diagnosis, treatment, medications, notes))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Medical history created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)