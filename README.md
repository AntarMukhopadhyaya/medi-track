Medi-Track: Hospital Management System

Overview

Medi-Track is a web-based Hospital Management System designed to streamline patient appointment scheduling, doctor-patient interactions, and administrative management. Built using Django, Bootstrap, Tailwind CSS, and SQL, this system enhances hospital efficiency by automating appointment booking, queue management, and prescription generation.

Features

Admin

Add and delete doctors.

Confirm appointment requests for OPD.

Monitor live queue status in real-time.

Doctor

View patient queue in the doctor portal.

Reschedule delayed patients by pushing them to the end of the queue.

Generate online prescriptions and send them as PDFs via email.

Patient

Book appointments online.

View live queue status.

Receive digital prescriptions via email.

Technology Stack

Frontend: Bootstrap, Tailwind CSS

Backend: Django

Database: SQL

Installation

Prerequisites

Python (v3.8 or later)

Django

PostgreSQL/MySQL (or SQLite for development)

Setup Instructions

Clone the repository:

git clone https://github.com/AntarMukhopadhyaya/medi-track.git

Navigate to the project directory:

cd medi-track

Install dependencies:

pip install -r requirements.txt

Run database migrations:

python manage.py migrate

Start the development server:

python manage.py runserver

Access the application at http://127.0.0.1:8000/

Usage

Admins log in to manage doctors and confirm appointments.

Doctors log in to manage queues and generate prescriptions.

Patients book appointments and receive digital prescriptions.

Contribution

Contributions are welcome! Fork the repository, make necessary changes, and submit a pull request.

License

This project is licensed under the MIT License.

Contact

For inquiries, contact us at ndas20997@gmail.com.








