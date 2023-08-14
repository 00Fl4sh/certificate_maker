# Certificate Management System

The Certificate Management System is a web application developed using Django that allows users to create, customize, verify, and download certificates. This system provides a user-friendly interface for managing certificates and their verification.

## Features

- Create certificates with title, recipient name, course, and issue date.
- Generate a unique verification code for each certificate.
- Customize certificates with font, color, and layout preferences.
- Verify certificates using a verification code or token.
- Download certificates in PDF format.

## Installation

1. Make sure you have Python 3.8+ and Django 4.2+ installed.

2. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/certificate-management-system.git
Change into the project directory:
cd certificate-management-system
Install the project dependencies:
pip install -r requirements.txt
Apply the database migrations:
python manage.py createsuperuser
Start the development server:
python manage.py runserver
