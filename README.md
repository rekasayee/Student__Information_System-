📘 Student Information System (SIS)

A Flask-based web application for managing student details, teachers, enrollments, results, and activities in an educational institution.

📝 Project Overview

The Student Information System (SIS) is a lightweight and user-friendly web application developed using Python Flask and SQLite.
It allows administrators and teachers to efficiently manage student data through a centralized and secure platform.

This system provides features like:
✔ Student management
✔ Teacher management
✔ Enrollments
✔ Results entry
✔ Activity tracking
✔ Role-based authentication
✔ Clean and responsive UI

🚀 Features
🔐 Authentication Module

User login and logout

Admin privileges

Secure session handling

Registration support

Password hashing for safety

👨‍🎓 Student Management

Add new students

Edit/update student details

Delete student records

View complete student profile

👩‍🏫 Teacher Management

Add, edit, delete teacher details

View all teachers

📝 Enrollment Management

Enroll students into subjects

Maintain structured subject allocations

📊 Result Management

Enter marks for each student

View all results in tabular format

🏆 Activities Module

Record student extracurricular activities

Track achievements and participation

🖥 User Interface

Responsive dashboard

Well-organized templates

Simple and clean UI using HTML & CSS

🗂 Project Structure
SIS/
│── app.py
│── auth.py
│── db.py
│── create_admin.py
│── create_users_table.py
│── requirements.txt
│── README.md
│── student_info.db
│
├── static/
│   └── styles.css
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── students.html
    ├── student_add.html
    ├── student_edit.html
    ├── student_detail.html
    ├── teachers.html
    ├── teacher_form.html
    ├── enrollments.html
    ├── enrollment_form.html
    ├── results.html
    ├── result_form.html
    ├── activities.html
    └── activity_form.html

🛠 Technologies Used
Component	Technology
Backend	Python, Flask
Database	SQLite
Frontend	HTML, CSS
Session Handling	Flask Sessions
Authentication	Custom login system
Styling	Custom CSS
⚙️ Installation & Setup
1. Clone the Repository
git clone <your-repo-link>
cd SIS

2. Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

3. Install Dependencies
pip install -r requirements.txt

4. Initialize the Database

The project contains scripts to initialize tables:

python create_users_table.py
python create_admin.py  # Optional: create default admin

5. Run the Application
python app.py

6. Open in Browser
http://127.0.0.1:5000/

🔑 Default Admin Credentials (If Provided)
username: admin
password: admin123  (example — change if needed)

📌 Key Flask Files Explained
app.py

Main application file

Routes for dashboard, students, teachers, results, activities

auth.py

Handles login, logout, registration

Session management

db.py

SQLite database connection

Functions for CRUD operations

templates/

All HTML pages using Jinja2 templating

static/styles.css

Custom styles
