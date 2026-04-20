CREATE DATABASE IF NOT EXISTS medifind;
USE medifind;

DROP TABLE IF EXISTS Doctors;

CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100),
    hospital_name VARCHAR(150),
    city VARCHAR(100),
    rating FLOAT,
    latitude FLOAT,
    longitude FLOAT
);

-- =====================
-- RAICHUR (10)
-- =====================
INSERT INTO Doctors VALUES
(1,'Dr. Lakshmi Devi','Neurologist','Govt Hospital','Raichur',4.3,16.2076,77.3463),
(2,'Dr. Ramesh Gowda','Cardiologist','City Care','Raichur',4.5,16.2080,77.3450),
(3,'Dr. Suresh Patil','Dermatologist','Skin Clinic','Raichur',4.2,16.2100,77.3400),
(4,'Dr. Anita Rao','Orthopedic','Bone Care','Raichur',4.4,16.2060,77.3420),
(5,'Dr. Kavitha','Ophthalmologist','Eye Care','Raichur',4.1,16.2090,77.3480),
(6,'Dr. Prakash','ENT Specialist','ENT Clinic','Raichur',4.2,16.2050,77.3470),
(7,'Dr. Meera','Dentist','Dental Care','Raichur',4.3,16.2040,77.3490),
(8,'Dr. Vinay','General Physician','Health Center','Raichur',4.5,16.2030,77.3440),
(9,'Dr. Arjun','Nephrologist','Kidney Care','Raichur',4.2,16.2020,77.3465),
(10,'Dr. Shilpa','Gynecologist','Women Care','Raichur',4.4,16.2010,77.3455);

-- =====================
-- MUMBAI (10)
-- =====================
INSERT INTO Doctors VALUES
(11,'Dr. Rahul Mehta','Neurologist','Fortis Hospital','Mumbai',4.7,19.1726,72.9560),
(12,'Dr. Amit Shah','Cardiologist','Kokilaben','Mumbai',4.8,19.1364,72.8267),
(13,'Dr. Neha Kapoor','Dermatologist','Skin Plus','Mumbai',4.6,19.0596,72.8295),
(14,'Dr. Arjun Singh','Orthopedic','Apollo','Mumbai',4.5,19.0330,73.0297),
(15,'Dr. Sneha Joshi','Ophthalmologist','Vision Care','Mumbai',4.4,19.2183,72.9781),
(16,'Dr. Karan','ENT Specialist','ENT Center','Mumbai',4.5,19.1100,72.8700),
(17,'Dr. Pooja','Dentist','Dental Hub','Mumbai',4.6,19.1000,72.8600),
(18,'Dr. Raj','General Physician','City Clinic','Mumbai',4.7,19.1200,72.8800),
(19,'Dr. Imran','Nephrologist','Kidney Center','Mumbai',4.5,19.1400,72.8900),
(20,'Dr. Ritu','Gynecologist','Women Hospital','Mumbai',4.6,19.1300,72.8700);

-- =====================
-- BANGALORE (10)
-- =====================
INSERT INTO Doctors VALUES
(21,'Dr. Rohit Sharma','Neurologist','Columbia Asia','Bangalore',4.3,13.1000,77.5960),
(22,'Dr. Rajesh Kumar','Cardiologist','Manipal','Bangalore',4.7,12.9698,77.7500),
(23,'Dr. Meena Reddy','Dermatologist','Skin Care','Bangalore',4.5,12.9800,77.5000),
(24,'Dr. Vivek Rao','Orthopedic','Apollo','Bangalore',4.6,12.9250,77.5938),
(25,'Dr. Kavya','Ophthalmologist','Eye Clinic','Bangalore',4.4,12.9716,77.6412),
(26,'Dr. Nikhil','ENT Specialist','ENT Clinic','Bangalore',4.5,12.9600,77.6000),
(27,'Dr. Shreya','Dentist','Dental Care','Bangalore',4.6,12.9500,77.6100),
(28,'Dr. Anil','General Physician','Health Hub','Bangalore',4.7,12.9400,77.6200),
(29,'Dr. Harish','Nephrologist','Kidney Care','Bangalore',4.5,12.9300,77.6300),
(30,'Dr. Divya','Gynecologist','Women Care','Bangalore',4.6,12.9200,77.6400);

-- =====================
-- HYDERABAD (10)
-- =====================
INSERT INTO Doctors VALUES
(31,'Dr. Anjali','Neurologist','Care Hospital','Hyderabad',4.6,17.4120,78.4480),
(32,'Dr. Srinivas','Cardiologist','Yashoda','Hyderabad',4.7,17.4239,78.4738),
(33,'Dr. Kiran','Dermatologist','Skin Clinic','Hyderabad',4.4,17.4483,78.3915),
(34,'Dr. Ravi','Orthopedic','Sunshine','Hyderabad',4.5,17.4401,78.3489),
(35,'Dr. Swathi','Ophthalmologist','Eye Care','Hyderabad',4.3,17.4948,78.3996),
(36,'Dr. Teja','ENT Specialist','ENT Center','Hyderabad',4.5,17.4500,78.4000),
(37,'Dr. Pavan','Dentist','Dental Care','Hyderabad',4.6,17.4600,78.4100),
(38,'Dr. Rakesh','General Physician','City Clinic','Hyderabad',4.7,17.4700,78.4200),
(39,'Dr. Manoj','Nephrologist','Kidney Care','Hyderabad',4.5,17.4800,78.4300),
(40,'Dr. Lavanya','Gynecologist','Women Care','Hyderabad',4.6,17.4900,78.4400);

-- =====================
-- DELHI (10)
-- =====================
INSERT INTO Doctors VALUES
(41,'Dr. Nikhil','Neurologist','Apollo','Delhi',4.7,28.6139,77.2090),
(42,'Dr. Arvind','Cardiologist','AIIMS','Delhi',4.9,28.5672,77.2100),
(43,'Dr. Pooja','Dermatologist','Skin Care','Delhi',4.5,28.6100,77.2300),
(44,'Dr. Rohan','Orthopedic','Max','Delhi',4.6,28.6200,77.2000),
(45,'Dr. Shreya','Ophthalmologist','Eye Center','Delhi',4.4,28.6300,77.2100),
(46,'Dr. Aman','ENT Specialist','ENT Clinic','Delhi',4.5,28.6400,77.2200),
(47,'Dr. Kavita','Dentist','Dental Care','Delhi',4.6,28.6500,77.2300),
(48,'Dr. Raj','General Physician','Health Hub','Delhi',4.7,28.6600,77.2400),
(49,'Dr. Imran','Nephrologist','Kidney Care','Delhi',4.5,28.6700,77.2500),
(50,'Dr. Neha','Gynecologist','Women Care','Delhi',4.6,28.6800,77.2600);

-- =====================
-- KOLKATA (10)
-- =====================
INSERT INTO Doctors VALUES
(51,'Dr. Rakesh Bose','Neurologist','Fortis','Kolkata',4.4,22.5726,88.3639),
(52,'Dr. Subhajit','Cardiologist','Apollo','Kolkata',4.5,22.5800,88.3600),
(53,'Dr. Ananya','Dermatologist','Skin Care','Kolkata',4.3,22.5700,88.3500),
(54,'Dr. Sayan','Orthopedic','City Hospital','Kolkata',4.4,22.5600,88.3700),
(55,'Dr. Ritu','Ophthalmologist','Eye Clinic','Kolkata',4.2,22.5500,88.3400),
(56,'Dr. Arka','ENT Specialist','ENT Care','Kolkata',4.3,22.5400,88.3300),
(57,'Dr. Priya','Dentist','Dental Hub','Kolkata',4.4,22.5300,88.3200),
(58,'Dr. Rahul','General Physician','Health Center','Kolkata',4.5,22.5200,88.3100),
(59,'Dr. Amit','Nephrologist','Kidney Center','Kolkata',4.3,22.5100,88.3000),
(60,'Dr. Sneha','Gynecologist','Women Hospital','Kolkata',4.4,22.5000,88.2900);




INSERT INTO Doctors VALUES
(61,'Dr. Vijay Kumar','Cardiologist','Apollo Hospital','Chennai',4.8,13.08,80.27),
(62,'Dr. Rekha Iyer','Dermatologist','MIOT Hospital','Chennai',4.6,13.08,80.27),
(63,'Dr. Arun Prakash','Neurologist','Fortis Hospital','Chennai',4.7,13.09,80.28),
(64,'Dr. Suresh Menon','Orthopedic','Global Hospital','Chennai',4.5,13.10,80.29),
(65,'Dr. Kavya Raman','Ophthalmologist','Eye Care','Chennai',4.4,13.11,80.30),
(66,'Dr. Nitin Nair','ENT Specialist','Apollo Clinic','Chennai',4.3,13.12,80.31),
(67,'Dr. Rajesh Iyer','Dentist','Dental Care','Chennai',4.5,13.13,80.32),
(68,'Dr. Anand Kumar','General Physician','City Hospital','Chennai',4.6,13.14,80.33),
(69,'Dr. Deepa Krishnan','Nephrologist','Kidney Center','Chennai',4.7,13.15,80.34),
(70,'Dr. Lakshmi Nair','Gynecologist','Women Care','Chennai',4.6,13.16,80.35);


-- =========================
-- PUNE (71–80)
-- =========================
INSERT INTO Doctors VALUES
(71,'Dr. Nikhil Joshi','Cardiologist','Ruby Hall Clinic','Pune',4.7,18.52,73.85),
(72,'Dr. Sneha Patwardhan','Dermatologist','Sahyadri Hospital','Pune',4.5,18.53,73.86),
(73,'Dr. Rohit Kulkarni','Neurologist','Jehangir Hospital','Pune',4.6,18.54,73.87),
(74,'Dr. Ajay Deshmukh','Orthopedic','Aditya Hospital','Pune',4.4,18.55,73.88),
(75,'Dr. Neha Joshi','Ophthalmologist','Eye Clinic','Pune',4.5,18.56,73.89),
(76,'Dr. Rahul Patil','ENT Specialist','Clinic','Pune',4.3,18.57,73.90),
(77,'Dr. Kiran More','Dentist','Smile Dental','Pune',4.6,18.58,73.91),
(78,'Dr. Sandeep Pawar','General Physician','City Hospital','Pune',4.7,18.59,73.92),
(79,'Dr. Amol Shinde','Nephrologist','Kidney Care','Pune',4.5,18.60,73.93),
(80,'Dr. Pooja Kulkarni','Gynecologist','Women Care','Pune',4.6,18.61,73.94);


-- =========================
-- AHMEDABAD (81–90)
-- =========================
INSERT INTO Doctors VALUES
(81,'Dr. Ketan Patel','Cardiologist','Zydus Hospital','Ahmedabad',4.6,23.02,72.57),
(82,'Dr. Rina Shah','Dermatologist','Sterling Hospital','Ahmedabad',4.5,23.03,72.58),
(83,'Dr. Harsh Mehta','Neurologist','Apollo Hospital','Ahmedabad',4.6,23.04,72.59),
(84,'Dr. Vijay Patel','Orthopedic','City Hospital','Ahmedabad',4.4,23.05,72.60),
(85,'Dr. Pooja Shah','Ophthalmologist','Eye Care','Ahmedabad',4.5,23.06,72.61),
(86,'Dr. Rajesh Trivedi','ENT Specialist','Clinic','Ahmedabad',4.3,23.07,72.62),
(87,'Dr. Amit Shah','Dentist','Dental Care','Ahmedabad',4.6,23.08,72.63),
(88,'Dr. Manish Patel','General Physician','Hospital','Ahmedabad',4.7,23.09,72.64),
(89,'Dr. Deepak Shah','Nephrologist','Kidney Care','Ahmedabad',4.5,23.10,72.65),
(90,'Dr. Rekha Patel','Gynecologist','Women Care','Ahmedabad',4.6,23.11,72.66);


-- =========================
-- JAIPUR (91–100)
-- =========================
INSERT INTO Doctors VALUES
(91,'Dr. Raj Singh','Cardiologist','SMS Hospital','Jaipur',4.7,26.91,75.78),
(92,'Dr. Neha Gupta','Dermatologist','Fortis Hospital','Jaipur',4.5,26.92,75.79),
(93,'Dr. Amit Sharma','Neurologist','Narayana Hospital','Jaipur',4.6,26.93,75.80),
(94,'Dr. Vikram Singh','Orthopedic','City Hospital','Jaipur',4.4,26.94,75.81),
(95,'Dr. Ritu Sharma','Ophthalmologist','Eye Clinic','Jaipur',4.5,26.95,75.82),
(96,'Dr. Manoj Verma','ENT Specialist','Clinic','Jaipur',4.3,26.96,75.83),
(97,'Dr. Pankaj Gupta','Dentist','Dental Care','Jaipur',4.6,26.97,75.84),
(98,'Dr. Sandeep Jain','General Physician','Hospital','Jaipur',4.7,26.98,75.85),
(99,'Dr. Deepak Agarwal','Nephrologist','Kidney Care','Jaipur',4.5,26.99,75.86),
(100,'Dr. Anjali Singh','Gynecologist','Women Care','Jaipur',4.6,27.00,75.87);


-- =========================
-- LUCKNOW (101–110)
-- =========================
INSERT INTO Doctors VALUES
(101,'Dr. Ravi Mishra','Cardiologist','SGPGI','Lucknow',4.8,26.85,80.94),
(102,'Dr. Neha Tiwari','Dermatologist','Apollo Hospital','Lucknow',4.6,26.86,80.95),
(103,'Dr. Saurabh Singh','Neurologist','KGMU','Lucknow',4.7,26.87,80.96),
(104,'Dr. Amit Verma','Orthopedic','City Hospital','Lucknow',4.5,26.88,80.97),
(105,'Dr. Ritu Mishra','Ophthalmologist','Eye Clinic','Lucknow',4.4,26.89,80.98),
(106,'Dr. Rajesh Yadav','ENT Specialist','Clinic','Lucknow',4.3,26.90,80.99),
(107,'Dr. Deepak Singh','Dentist','Dental Care','Lucknow',4.5,26.91,81.00),
(108,'Dr. Anil Kumar','General Physician','Hospital','Lucknow',4.6,26.92,81.01),
(109,'Dr. Vivek Gupta','Nephrologist','Kidney Care','Lucknow',4.5,26.93,81.02),
(110,'Dr. Pooja Singh','Gynecologist','Women Care','Lucknow',4.6,26.94,81.03);


-- =========================
-- CHANDIGARH (111–120)
-- =========================
INSERT INTO Doctors VALUES
(111,'Dr. Harpreet Singh','Cardiologist','PGI','Chandigarh',4.8,30.73,76.77),
(112,'Dr. Simran Kaur','Dermatologist','Fortis Hospital','Chandigarh',4.6,30.74,76.78),
(113,'Dr. Amanpreet Singh','Neurologist','Max Hospital','Chandigarh',4.7,30.75,76.79),
(114,'Dr. Gurpreet Singh','Orthopedic','City Hospital','Chandigarh',4.5,30.76,76.80),
(115,'Dr. Jasleen Kaur','Ophthalmologist','Eye Care','Chandigarh',4.4,30.77,76.81),
(116,'Dr. Manpreet Singh','ENT Specialist','Clinic','Chandigarh',4.3,30.78,76.82),
(117,'Dr. Rajinder Singh','Dentist','Dental Care','Chandigarh',4.6,30.79,76.83),
(118,'Dr. Sukhbir Singh','General Physician','Hospital','Chandigarh',4.7,30.80,76.84),
(119,'Dr. Baljit Singh','Nephrologist','Kidney Care','Chandigarh',4.5,30.81,76.85),
(120,'Dr. Navjot Kaur','Gynecologist','Women Care','Chandigarh',4.6,30.82,76.86);
USE medifind;

-- =====================
-- INDORE (10)
-- =====================
INSERT INTO Doctors VALUES
(121,'Dr. Ajay Verma','Neurologist','Apollo','Indore',4.6,22.7196,75.8577),
(122,'Dr. Kunal','Cardiologist','CHL Hospital','Indore',4.7,22.7100,75.8500),
(123,'Dr. Sneha','Dermatologist','Skin Care','Indore',4.5,22.7000,75.8400),
(124,'Dr. Rohit','Orthopedic','Bombay Hospital','Indore',4.6,22.6900,75.8300),
(125,'Dr. Kavita','Ophthalmologist','Eye Clinic','Indore',4.4,22.6800,75.8200),
(126,'Dr. Rahul','ENT Specialist','ENT Care','Indore',4.5,22.6700,75.8100),
(127,'Dr. Pooja','Dentist','Dental Hub','Indore',4.6,22.6600,75.8000),
(128,'Dr. Amit','General Physician','City Clinic','Indore',4.7,22.6500,75.7900),
(129,'Dr. Imran','Nephrologist','Kidney Care','Indore',4.5,22.6400,75.7800),
(130,'Dr. Neha','Gynecologist','Women Care','Indore',4.6,22.6300,75.7700);

-- =====================
-- BHOPAL (10)
-- =====================
INSERT INTO Doctors VALUES
(131,'Dr. Rajesh','Neurologist','AIIMS','Bhopal',4.5,23.2599,77.4126),
(132,'Dr. Sharma','Cardiologist','Bansal Hospital','Bhopal',4.7,23.2500,77.4000),
(133,'Dr. Anjali','Dermatologist','Skin Care','Bhopal',4.4,23.2400,77.3900),
(134,'Dr. Vikram','Orthopedic','Chirayu','Bhopal',4.6,23.2300,77.3800),
(135,'Dr. Meera','Ophthalmologist','Eye Care','Bhopal',4.3,23.2200,77.3700),
(136,'Dr. Amit','ENT Specialist','ENT Care','Bhopal',4.5,23.2100,77.3600),
(137,'Dr. Kavita','Dentist','Dental Care','Bhopal',4.6,23.2000,77.3500),
(138,'Dr. Rohan','General Physician','City Clinic','Bhopal',4.7,23.1900,77.3400),
(139,'Dr. Suresh','Nephrologist','Kidney Care','Bhopal',4.5,23.1800,77.3300),
(140,'Dr. Neha','Gynecologist','Women Care','Bhopal',4.6,23.1700,77.3200);

-- =====================
-- NAGPUR (10)
-- =====================
INSERT INTO Doctors VALUES
(141,'Dr. Prakash','Neurologist','Care Hospital','Nagpur',4.6,21.1458,79.0882),
(142,'Dr. Kiran','Cardiologist','Wockhardt','Nagpur',4.7,21.1400,79.0800),
(143,'Dr. Sneha','Dermatologist','Skin Care','Nagpur',4.5,21.1300,79.0700),
(144,'Dr. Rohit','Orthopedic','Kingsway','Nagpur',4.6,21.1200,79.0600),
(145,'Dr. Kavita','Ophthalmologist','Eye Care','Nagpur',4.4,21.1100,79.0500),
(146,'Dr. Rahul','ENT Specialist','ENT Care','Nagpur',4.5,21.1000,79.0400),
(147,'Dr. Pooja','Dentist','Dental Care','Nagpur',4.6,21.0900,79.0300),
(148,'Dr. Amit','General Physician','City Clinic','Nagpur',4.7,21.0800,79.0200),
(149,'Dr. Imran','Nephrologist','Kidney Care','Nagpur',4.5,21.0700,79.0100),
(150,'Dr. Neha','Gynecologist','Women Care','Nagpur',4.6,21.0600,79.0000);

-- =====================
-- COIMBATORE (10)
-- =====================
INSERT INTO Doctors VALUES
(151,'Dr. Siva','Neurologist','KMCH','Coimbatore',4.6,11.0168,76.9558),
(152,'Dr. Kumar','Cardiologist','Ganga Hospital','Coimbatore',4.7,11.0100,76.9500),
(153,'Dr. Priya','Dermatologist','Skin Care','Coimbatore',4.5,11.0000,76.9400),
(154,'Dr. Naveen','Orthopedic','PSG','Coimbatore',4.6,10.9900,76.9300),
(155,'Dr. Kavya','Ophthalmologist','Eye Clinic','Coimbatore',4.4,10.9800,76.9200),
(156,'Dr. Hari','ENT Specialist','ENT Care','Coimbatore',4.5,10.9700,76.9100),
(157,'Dr. Anu','Dentist','Dental Care','Coimbatore',4.6,10.9600,76.9000),
(158,'Dr. Ramesh','General Physician','City Clinic','Coimbatore',4.7,10.9500,76.8900),
(159,'Dr. Vinay','Nephrologist','Kidney Care','Coimbatore',4.5,10.9400,76.8800),
(160,'Dr. Meena','Gynecologist','Women Care','Coimbatore',4.6,10.9300,76.8700);

-- =====================
-- VISAKHAPATNAM (10)
-- =====================
INSERT INTO Doctors VALUES
(161,'Dr. Suresh','Neurologist','Apollo','Visakhapatnam',4.6,17.6868,83.2185),
(162,'Dr. Ramesh','Cardiologist','Care Hospital','Visakhapatnam',4.7,17.6800,83.2100),
(163,'Dr. Anjali','Dermatologist','Skin Care','Visakhapatnam',4.5,17.6700,83.2000),
(164,'Dr. Kiran','Orthopedic','Seven Hills','Visakhapatnam',4.6,17.6600,83.1900),
(165,'Dr. Swathi','Ophthalmologist','Eye Care','Visakhapatnam',4.4,17.6500,83.1800),
(166,'Dr. Teja','ENT Specialist','ENT Care','Visakhapatnam',4.5,17.6400,83.1700),
(167,'Dr. Pavan','Dentist','Dental Care','Visakhapatnam',4.6,17.6300,83.1600),
(168,'Dr. Rakesh','General Physician','City Clinic','Visakhapatnam',4.7,17.6200,83.1500),
(169,'Dr. Manoj','Nephrologist','Kidney Care','Visakhapatnam',4.5,17.6100,83.1400),
(170,'Dr. Lavanya','Gynecologist','Women Care','Visakhapatnam',4.6,17.6000,83.1300);

-- =====================
-- SURAT (10)
-- =====================
INSERT INTO Doctors VALUES
(171,'Dr. Patel','Neurologist','Apollo','Surat',4.6,21.1702,72.8311),
(172,'Dr. Shah','Cardiologist','Sterling','Surat',4.7,21.1600,72.8200),
(173,'Dr. Mehta','Dermatologist','Skin Care','Surat',4.5,21.1500,72.8100),
(174,'Dr. Desai','Orthopedic','Sunshine','Surat',4.6,21.1400,72.8000),
(175,'Dr. Bhavya','Ophthalmologist','Eye Care','Surat',4.4,21.1300,72.7900),
(176,'Dr. Rakesh','ENT Specialist','ENT Care','Surat',4.5,21.1200,72.7800),
(177,'Dr. Sejal','Dentist','Dental Care','Surat',4.6,21.1100,72.7700),
(178,'Dr. Nitin','General Physician','City Clinic','Surat',4.7,21.1000,72.7600),
(179,'Dr. Harsh','Nephrologist','Kidney Care','Surat',4.5,21.0900,72.7500),
(180,'Dr. Aarti','Gynecologist','Women Care','Surat',4.6,21.0800,72.7400);
