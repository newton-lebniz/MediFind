
CREATE DATABASE MediFind;
use medifind;


CREATE TABLE Specializations (
    specialization_id INT PRIMARY KEY,
    specialization_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    city VARCHAR(50) NOT NULL,
    rating FLOAT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    specialization_id INT,
    FOREIGN KEY (specialization_id) REFERENCES Specializations(specialization_id)
);
CREATE TABLE Hospitals (
    hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_name VARCHAR(100),
    city VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    UNIQUE(hospital_name, latitude, longitude)
);
CREATE TABLE Doctor_Hospital (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT,
    hospital_id INT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id),
    UNIQUE(doctor_id, hospital_id)
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    city VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);
CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    UNIQUE(user_id, doctor_id, appointment_date)
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    doctor_id INT,
    rating FLOAT,
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    UNIQUE(user_id, doctor_id)
);
