USE medical_system;

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    contact_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medications (
    medication_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    barcode VARCHAR(50) UNIQUE NOT NULL,
    manufacturer VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE providers (
    provider_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialty VARCHAR(100),
    contact_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id) ON DELETE CASCADE,
    provider_id INT REFERENCES providers(provider_id) ON DELETE SET NULL,
    medication_id INT REFERENCES medications(medication_id) ON DELETE CASCADE,
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) CHECK (status IN ('active', 'expired', 'discontinued')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES providers(provider_id) ON DELETE CASCADE,
    receiver_id INT REFERENCES providers(provider_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id) ON DELETE CASCADE,
    provider_id INT REFERENCES providers(provider_id) ON DELETE SET NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('unread', 'read', 'resolved')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PatientMedicalHistory (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id BIGINT UNSIGNED NOT NULL,
    visit_date DATE NOT NULL,
    diagnosis VARCHAR(255),
    treatment TEXT,
    medications TEXT,
    provider_id BIGINT UNSIGNED,  -- Adjusted to match Providers table
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (provider_id) REFERENCES Providers(provider_id)
);

-- Create roles
CREATE ROLE admin;
CREATE ROLE provider;
CREATE ROLE patient;

-- Grant permissions to roles
GRANT ALL PRIVILEGES ON medical_system.* TO admin;

GRANT SELECT, INSERT, UPDATE, DELETE ON medical_system.patients TO provider;
GRANT SELECT, INSERT, UPDATE, DELETE ON medical_system.prescriptions TO provider;
GRANT SELECT, INSERT, UPDATE, DELETE ON medical_system.messages TO provider;

GRANT SELECT ON medical_system.patients TO patient;
GRANT SELECT ON medical_system.messages TO patient;

-- Create users and assign roles
CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'admin_password';
GRANT admin TO 'admin_user'@'localhost';

CREATE USER 'dr_smith'@'localhost' IDENTIFIED BY 'provider_password';
GRANT provider TO 'dr_smith'@'localhost';

CREATE USER 'john_doe'@'localhost' IDENTIFIED BY 'patient_password';
GRANT patient TO 'john_doe'@'localhost';

-- Ensure users activate their roles on login
SET DEFAULT ROLE admin TO 'admin_user'@'localhost';
SET DEFAULT ROLE provider TO 'dr_smith'@'localhost';
SET DEFAULT ROLE patient TO 'john_doe'@'localhost';

-- Give DB access
CREATE USER 'mark'@'192.168.12.249' IDENTIFIED BY 'MarkCGU';
GRANT ALL PRIVILEGES ON medical_system.* TO 'mark'@'192.168.12.249';
FLUSH PRIVILEGES;

CREATE USER 'millicent'@'192.168.4.37' IDENTIFIED BY 'MillicentCGU';
GRANT ALL PRIVILEGES ON medical_system.* TO 'millicent'@'192.168.4.37';
FLUSH PRIVILEGES;

CREATE USER 'jade'@'76.89.206.90' IDENTIFIED BY 'JadeCGU';
GRANT ALL PRIVILEGES ON medical_system.* TO 'jade'@'76.89.206.90';
FLUSH PRIVILEGES;

CREATE USER 'test'@'192.168.1.250' IDENTIFIED BY 'testcase';
GRANT ALL PRIVILEGES ON medical_system.* TO 'test'@'192.168.1.250';
FLUSH PRIVILEGES;