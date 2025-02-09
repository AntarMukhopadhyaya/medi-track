Software Requirements Specification (SRS)

Hospital Management System

1. Introduction

1.1 Purpose

The Hospital Management System (HMS) is designed to streamline patient appointment scheduling, enhance doctor-patient interactions, and improve administrative efficiency. This system provides a seamless experience for patients, doctors, and administrators by integrating advanced scheduling, live queue management, and online prescription generation.

1.2 Scope

The HMS will:

Allow patients to book appointments and view queue status.

Enable doctors to manage their appointment queues and reschedule delayed patients.

Provide admins with tools to manage doctors, confirm appointment requests, and monitor live queues.

Generate digital prescriptions that are emailed to patients.

1.3 Technology Stack

Frontend: Bootstrap, Tailwind CSS

Backend: Django

Database: SQL

2. Functional Requirements

2.1 Actors and Their Functionalities

2.1.1 Admin

Add and delete doctors from the system.

Confirm appointment requests for Outpatient Department (OPD).

Monitor live queue status in real time.

2.1.2 Doctor

View patient queue through the doctor portal.

Reschedule patients in case of delays, pushing them to the end of the queue.

Generate online prescriptions after consultation.

Ensure prescriptions are automatically emailed to patients in PDF format.

2.1.3 Patient

Book appointments for OPD consultations.

View live queue status.

Receive digital prescriptions via email.

3. System Features

3.1 Appointment Management

Patients can book appointments through an intuitive interface.

Admin approval is required for appointment confirmation.

Doctors can see their queue in real time.

3.2 Queue Management

Live queue status is visible to both patients and doctors.

Doctors can reschedule patients who are delaying and move them to the last position in the queue.

Admin can monitor queue progression and ensure smooth operations.

3.3 Prescription Management

Doctors can generate online prescriptions after consultation.

The system will generate prescriptions in PDF format.

Patients receive prescriptions via email automatically.

3.4 Admin Panel

Admin can add or remove doctors from the system.

The panel provides real-time insights into queue management.

4. Non-Functional Requirements

4.1 Performance

The system should handle simultaneous appointment requests efficiently.

Queue updates should be reflected in real time.

4.2 Security

Role-based authentication for Admin, Doctor, and Patient.

Secure storage of patient records and prescription data.

4.3 Usability

Intuitive UI for patients, doctors, and admins.

Mobile-responsive design using Bootstrap and Tailwind CSS.

4.4 Scalability

The system should support future expansion to additional hospital departments.

5. System Architecture

5.1 Overview

Frontend: Built using Bootstrap and Tailwind CSS for a clean and responsive UI.

Backend: Django handles authentication, database operations, and business logic.

Database: SQL stores patient records, appointment details, and prescriptions.

Email Integration: Prescriptions are automatically emailed to patients as PDFs.

6. Conclusion

The Hospital Management System aims to enhance operational efficiency and improve patient care by integrating real-time queue management, appointment scheduling, and digital prescriptions. Built on a robust tech stack, the system ensures smooth interactions between patients, doctors, and administrators.
