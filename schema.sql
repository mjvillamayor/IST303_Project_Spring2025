USE medical_system;

CREATE TABLE users (
    user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('patient', 'provider') NOT NULL,
    patient_id BIGINT UNSIGNED DEFAULT NULL,
    provider_id BIGINT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

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
GRANT SELECT ON medical_system.PatientMedicalHistory TO patient;

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

CREATE USER 'Ben'@'localhost' IDENTIFIED BY 'testingpassword';
GRANT ALL PRIVILEGES ON medical_system.* TO 'Ben'@'localhost';

-- Testing
USE medical_system;
SHOW TABLES;
SELECT * FROM PatientMedicalHistory
SELECT * FROM PATIENTS;
SELECT * FROM MEDICATIONS;
SELECT * FROM providers;

INSERT INTO PatientMedicalHistory 
(patient_id, visit_date, diagnosis, treatment, medications, provider_id, notes)
VALUES
(3, '2024-10-05', 'Asthma', 'Inhaler prescribed', 'Albuterol', 101, 'Patient reports increased wheezing during exercise.'),
(3, '2025-01-15', 'Routine Checkup', 'General wellness review', NULL, 102, 'All vitals normal. Recommended annual flu shot.'),
(4, '2024-12-10', 'Type 1 Diabetes', 'Diet plan updated; insulin dosage adjusted', 'Insulin Glargine', 103, 'Patient responding well to new plan.'),
(5, '2025-02-20', 'High Blood Pressure', 'Medication dosage increased', 'Lisinopril', 101, 'Advised lifestyle changes including reduced salt intake.'),
(4, '2025-03-10', 'Allergic Reaction', 'Administered antihistamines', 'Diphenhydramine', 104, 'Patient experienced mild rash after seafood.'),
(6, '2025-04-01', 'Back Pain', 'Physical therapy recommended', NULL, 105, 'No signs of disc damage. Muscle strain suspected.');

INSERT INTO providers (provider_id, first_name, last_name, specialty, contact_info)
VALUES
(101, 'Emily', 'Wong', 'Pulmonology', 'emily.wong@clinic.com'),
(102, 'Jake', 'Chen', 'General Practice', 'jake.chen@health.org'),
(103, 'Sasha', 'Lee', 'Endocrinology', 'sasha.lee@hospital.net'),
(104, 'Raj', 'Kapoor', 'Allergy & Immunology', 'raj.kapoor@clinic.com'),
(105, 'Megan', 'Smith', 'Physical Therapy', 'megan.smith@ptcenter.com');

INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_info)
VALUES
('Alex', 'Johnson', '1990-05-14', 'Male', 'alex.johnson@example.com'),
('Maria', 'Lopez', '1985-08-22', 'Female', 'maria.lopez@example.com'),
('David', 'Nguyen', '1979-02-09', 'Male', 'david.nguyen@example.com'),
('Sophia', 'Patel', '2000-11-30', 'Female', 'sophia.patel@example.com');

INSERT INTO users (username, password, role, provider_id)
VALUES ('drsmith', 'testpassword', 'provider', 105);

INSERT INTO users (username, password, role, patient_id)
VALUES ('janedoe', 'testpassword', 'patient', 6);