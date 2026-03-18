
CREATE DATABASE MediFind;
use medifind;


CREATE TABLE Specializations (
    specialization_id INT PRIMARY KEY,
    specialization_name VARCHAR(100) NOT NULL
);

CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    city VARCHAR(50) NOT NULL,
    rating FLOAT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    specialization_id INT,
    FOREIGN KEY (specialization_id) REFERENCES Specializations(specialization_id)
);
INSERT INTO Specializations VALUES
(1, 'Cardiologist'),
(2, 'Dermatologist'),
(3, 'Neurologist'),
(4, 'Orthopedic'),
(5, 'General Physician');

INSERT INTO Doctors VALUES
(1, 'Dr. Rajesh Kumar', '9876543210', 'Bangalore', 4.5, 12.9716, 77.5946, 1),
(2, 'Dr. Meena Reddy', '9123456780', 'Hyderabad', 4.2, 17.3850, 78.4867, 2),
(3, 'Dr. Arjun Nair', '9988776655', 'Chennai', 4.8, 13.0827, 80.2707, 3),
(4, 'Dr. Priya Sharma', '9012345678', 'Delhi', 4.6, 28.7041, 77.1025, 4),
(5, 'Dr. Vikram Singh', '9090909090', 'Mumbai', 4.3, 19.0760, 72.8777, 5),
(6, 'Dr. Sneha Iyer', '9876501234', 'Bangalore', 4.7, 12.2958, 76.6394, 1),
(7, 'Dr. Rahul Verma', '9345678901', 'Pune', 4.1, 18.5204, 73.8567, 2),
(8, 'Dr. Kavya Menon', '9765432109', 'Kochi', 4.9, 9.9312, 76.2673, 3),
(9, 'Dr. Ankit Jain', '9871234560', 'Jaipur', 4.4, 26.9124, 75.7873, 4),
(10, 'Dr. Neha Kapoor', '9001122334', 'Delhi', 4.6, 28.5355, 77.3910, 5),
(11, 'Dr. Suresh Patel', '9988001122', 'Ahmedabad', 4.2, 23.0225, 72.5714, 1),
(12, 'Dr. Pooja Das', '9877776666', 'Kolkata', 4.5, 22.5726, 88.3639, 2),
(13, 'Dr. Mohan Rao', '9123987654', 'Hyderabad', 4.3, 17.3850, 78.4867, 3),
(14, 'Dr. Ritu Malhotra', '9811223344', 'Chandigarh', 4.7, 30.7333, 76.7794, 4),
(15, 'Dr. Deepak Gupta', '9898989898', 'Lucknow', 4.1, 26.8467, 80.9462, 5);
