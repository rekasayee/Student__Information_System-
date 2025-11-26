# 📘 Student Information System (SIS)

A Flask-based web application for managing student details, teachers, enrollments, results, and activities in an educational institution.

---

## 📌 Project Overview

The **Student Information System (SIS)** is a lightweight and user-friendly web application developed using **Python Flask** and **SQLite**.  
It allows administrators and teachers to efficiently manage student data through a centralized and secure platform.

This system provides features like:

✔ Student management  
✔ Teacher management  
✔ Enrollments  
✔ Results entry  
✔ Activity tracking  
✔ Role-based authentication  
✔ Clean and responsive UI  

---

## 🚀 Features

### 🔐 Authentication Module
1. User login and logout  
2. Admin privileges  
3. Secure session handling  
4. Registration support  
5. Password hashing for safety  

### 👨‍🎓 Student Management
1. Add new students  
2. Edit/update student details  
3. Delete student records  
4. View complete student profile  

### 👩‍🏫 Teacher Management
1. Add, edit, delete teacher details  
2. View all teachers  

### 📝 Enrollment Management
1. Enroll students into subjects  
2. Maintain structured subject allocations  

### 📊 Result Management
1. Enter marks for each student  
2. View all results in tabular format  

### 🏆 Activities Module
1. Record student extracurricular activities  

### 🖥 User Interface
- Responsive dashboard  
- Well-organized templates  
- Simple and clean UI using HTML & CSS  

---

## 🗂 Project Structure

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
│ └── styles.css
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


---

## 🛠 Technologies Used

| Component         | Technology      |
|------------------|-----------------|
| Backend          | Python, Flask   |
| Database         | SQLite          |
| Frontend         | HTML, CSS       |
| Session Handling | Flask Sessions  |
| Authentication   | Custom login system |
| Styling          | Custom CSS      |

---

## ⚙️ Installation & Setup

### **1. Clone the Repository**
```bash
git clone <your-repo-link>
cd SIS

Install Dependencies
pip install -r requirements.txt

python create_users_table.py
python create_admin.py   # Optional: create default admin

Run the Application
python app.py

Open in Browser
http://127.0.0.1:5000/
