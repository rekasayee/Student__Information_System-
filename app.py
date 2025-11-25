# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import db
import uuid
from functools import wraps
from auth import auth

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-secret-change-this"

# Initialize users table on startup
with app.app_context():
    db.init_users_table()

# ---- auth helpers that match auth.py (session['user'], session['role']) ----
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user"):
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user"):
            flash("Please log in.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated

# ----------------------
# Students
# ----------------------
@app.route("/")
@login_required
def index():
    query = request.args.get("q")
    if query:
        like_query = f"%{query}%"
        students = db.query(
            "SELECT digital_id, name, dob, age, address, phone, gender, year FROM students WHERE name LIKE ? OR digital_id LIKE ?",
            (like_query, like_query),
        )
    else:
        students = db.query("SELECT digital_id, name, dob, age, address, phone, gender, year FROM students")
    return render_template("index.html", students=students)

@app.route("/student/add", methods=["GET", "POST"])
@login_required
def student_add():
    if request.method == "POST":
        id_ = request.form.get("digital_id") or None
        name = request.form.get("name")
        dob = request.form.get("dob") or None
        age = request.form.get("age") or None
        address = request.form.get("address") or None
        phone = request.form.get("phone") or None
        gender = request.form.get("gender") or None
        year = request.form.get("year") or None
        try:
            db.execute(
                "INSERT INTO students(digital_id,name,dob,age,address,phone,gender,year) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                (id_, name, dob, int(age) if age else None, address, phone, gender, year),
            )
            flash("Student added.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("student_add.html")

@app.route("/student/<id>/edit", methods=["GET", "POST"])
@login_required
def student_edit(id):
    student = db.query("SELECT * FROM students WHERE digital_id=?", (id,), one=True)
    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("index"))
    if request.method == "POST":
        name = request.form.get("name")
        dob = request.form.get("dob") or None
        age = request.form.get("age") or None
        address = request.form.get("address") or None
        phone = request.form.get("phone") or None
        gender = request.form.get("gender") or None
        year = request.form.get("year") or None
        try:
            db.execute(
                """UPDATE students SET name=?, dob=?, age=?, address=?, phone=?, gender=?, year=? WHERE digital_id=?""",
                (name, dob, int(age) if age else None, address, phone, gender, year, id),
            )
            flash("Student updated.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("student_edit.html", s=student)

@app.route("/student/<id>/delete", methods=["POST"])
@admin_required
def student_delete(id):
    try:
        db.execute("DELETE FROM students WHERE digital_id=?", (id,))
        flash("Student deleted.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/student/<id>")
@login_required
def student_detail(id):
    student = db.query("SELECT * FROM students WHERE digital_id=?", (id,), one=True)
    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("index"))
    sem1 = db.query("SELECT Mathematics1, Physics, ComputerScience, avg_grade FROM sem1 WHERE digital_id=?", (id,))
    sem2 = db.query("SELECT Mathematics2, EnglishLiterature, History, avg_grade FROM sem2 WHERE digital_id=?", (id,))
    enroll = db.query(
        "SELECT e.enroll_id, c.course_id, c.course_name FROM enrollments e JOIN courses c ON e.course_id=c.course_id WHERE e.student_id=?",
        (id,),
    )
    acts = db.query(
        "SELECT a.activity_id, a.activity_name FROM studentactivities sa JOIN extracurricularactivities a ON sa.activity_id=a.activity_id WHERE sa.student_id=?",
        (id,),
    )
    return render_template("student_detail.html", s=student, sem1=sem1, sem2=sem2, enroll=enroll, acts=acts)

# ---------- Teachers ----------
@app.route("/teachers")
@login_required
def teachers():
    query = request.args.get("q")
    if query:
        like_query = f"%{query}%"
        rows = db.query(
            "SELECT teacher_id, name, qualification, phone, gender FROM teachers WHERE name LIKE ? OR qualification LIKE ?",
            (like_query, like_query),
        )
    else:
        rows = db.query("SELECT teacher_id, name, qualification, phone, gender FROM teachers")
    return render_template("teachers.html", teachers=rows)

@app.route("/teacher/add", methods=["GET", "POST"])
@login_required
def teacher_add():
    if request.method == "POST":
        tid = request.form.get("teacher_id")
        name = request.form.get("name")
        qual = request.form.get("qualification") or None
        phone = request.form.get("phone") or None
        gender = request.form.get("gender") or None
        try:
            db.execute("INSERT INTO teachers VALUES (?, ?, ?, ?, ?)", (tid, name, qual, phone, gender))
            flash("Teacher added.", "success")
            return redirect(url_for("teachers"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("teacher_form.html", action="Add")

@app.route("/teacher/<id>/edit", methods=["GET", "POST"])
@login_required
def teacher_edit(id):
    t = db.query("SELECT * FROM teachers WHERE teacher_id=?", (id,), one=True)
    if not t:
        flash("Teacher not found.", "warning")
        return redirect(url_for("teachers"))
    if request.method == "POST":
        name = request.form.get("name")
        qual = request.form.get("qualification") or None
        phone = request.form.get("phone") or None
        gender = request.form.get("gender") or None
        try:
            db.execute("UPDATE teachers SET name=?, qualification=?, phone=?, gender=? WHERE teacher_id=?",
                       (name, qual, phone, gender, id))
            flash("Teacher updated.", "success")
            return redirect(url_for("teachers"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("teacher_form.html", action="Edit", t=t)

@app.route("/teacher/<id>/delete", methods=["POST"])
@admin_required
def teacher_delete(id):
    try:
        db.execute("DELETE FROM teachers WHERE teacher_id=?", (id,))
        flash("Teacher removed.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("teachers"))

# ---------- Courses ----------
@app.route("/courses")
@login_required
def courses():
    query = request.args.get("q")
    if query:
        like_query = f"%{query}%"
        rows = db.query(
            "SELECT course_id, course_name, credit FROM courses WHERE course_name LIKE ? OR course_id LIKE ?",
            (like_query, like_query),
        )
    else:
        rows = db.query("SELECT course_id, course_name, credit FROM courses")
    return render_template("courses.html", courses=rows)

@app.route("/course/add", methods=["GET", "POST"])
@login_required
def course_add():
    if request.method == "POST":
        cid = request.form.get("course_id")
        name = request.form.get("course_name")
        credit = request.form.get("credit") or None
        try:
            db.execute("INSERT INTO courses VALUES (?, ?, ?)", (cid, name, int(credit) if credit else None))
            flash("Course added.", "success")
            return redirect(url_for("courses"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("course_form.html", action="Add")

@app.route("/course/<id>/delete", methods=["POST"])
@admin_required
def course_delete(id):
    try:
        db.execute("DELETE FROM courses WHERE course_id=?", (id,))
        flash("Course removed.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("courses"))

# ---------- Enrollments ----------
@app.route("/enrollments")
@login_required
def enrollments():
    rows = db.query("""
        SELECT e.enroll_id, e.student_id, s.name as student_name,
               e.course_id, c.course_name
        FROM enrollments e
        LEFT JOIN students s ON e.student_id = s.digital_id
        LEFT JOIN courses c ON e.course_id = c.course_id
    """)
    return render_template("enrollments.html", enrollments=rows)

@app.route("/enrollment/add", methods=["GET", "POST"])
@login_required
def enrollment_add():
    students = db.query("SELECT digital_id, name FROM students")
    courses = db.query("SELECT course_id, course_name FROM courses")

    if request.method == "POST":
        eid = request.form.get("enroll_id")
        sid = request.form.get("student_id")
        cid = request.form.get("course_id")
        try:
            db.execute("INSERT INTO enrollments VALUES (?, ?, ?)", (eid, sid, cid))
            flash("Enrollment added.", "success")
            return redirect(url_for("enrollments"))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("enrollment_form.html", action="Add", e=None, students=students, courses=courses)

@app.route("/enrollment/<id>/edit", methods=["GET", "POST"])
@login_required
def enrollment_edit(id):
    e = db.query("SELECT * FROM enrollments WHERE enroll_id=?", (id,), one=True)
    if not e:
        flash("Enrollment not found.", "warning")
        return redirect(url_for("enrollments"))

    students = db.query("SELECT digital_id, name FROM students")
    courses = db.query("SELECT course_id, course_name FROM courses")

    if request.method == "POST":
        sid = request.form.get("student_id")
        cid = request.form.get("course_id")
        try:
            db.execute("UPDATE enrollments SET student_id=?, course_id=? WHERE enroll_id=?", (sid, cid, id))
            flash("Enrollment updated.", "success")
            return redirect(url_for("enrollments"))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("enrollment_form.html", action="Edit", e=e, students=students, courses=courses)

@app.route("/enrollment/<id>/delete", methods=["POST"])
@admin_required
def enrollment_delete(id):
    try:
        db.execute("DELETE FROM enrollments WHERE enroll_id=?", (id,))
        flash("Enrollment deleted.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("enrollments"))

# ---------- Activities ----------
@app.route("/activities")
@login_required
def activities():
    activities_rows = db.query("SELECT activity_id, activity_name, description FROM extracurricularactivities")
    students_rows = db.query("SELECT digital_id, name FROM students")
    return render_template("activities.html", activities=activities_rows, students=students_rows)

@app.route("/activity/add", methods=["GET", "POST"])
@login_required
def activity_add():
    if request.method == "POST":
        aid = request.form.get("activity_id")
        name = request.form.get("activity_name")
        desc = request.form.get("description") or None
        try:
            db.execute("INSERT INTO extracurricularactivities VALUES (?, ?, ?)", (aid, name, desc))
            flash("Activity added.", "success")
            return redirect(url_for("activities"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("activity_form.html")

@app.route("/activity/<id>/students")
@login_required
def activity_students(id):
    rows = db.query("""SELECT s.digital_id, s.name FROM studentactivities sa
                       JOIN students s ON sa.student_id = s.digital_id WHERE sa.activity_id=?""", (id,))
    activity = db.query("SELECT * FROM extracurricularactivities WHERE activity_id=?", (id,), one=True)
    return render_template("activities.html", activities=[activity] if activity else [], students=rows, show_students=True)

@app.route("/activity/enroll", methods=["POST"])
@login_required
def activity_enroll():
    activity_id = request.form.get("activity_id")
    student_id = request.form.get("student_id")
    # Check if enrollment already exists to prevent duplicates
    existing = db.query("SELECT 1 FROM studentactivities WHERE activity_id=? AND student_id=?", (activity_id, student_id), one=True)
    if existing:
        flash("Student is already enrolled in this activity.", "warning")
    else:
        try:
            db.execute("INSERT INTO studentactivities VALUES (?, ?)", (activity_id, student_id))
            flash("Student enrolled in activity.", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return redirect(url_for("activities"))

@app.route("/activity/<aid>/remove_student/<sid>", methods=["POST"])
@admin_required
def activity_remove_student(aid, sid):
    try:
        db.execute("DELETE FROM studentactivities WHERE activity_id=? AND student_id=?", (aid, sid))
        flash("Removed student from activity.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("activities"))

# ---------- Classes ----------
@app.route("/classes")
@login_required
def classes():
    rows = db.query("""SELECT c.class_id, c.class_name, c.teacher_id, t.name as teacher_name
                       FROM classes c LEFT JOIN teachers t ON c.teacher_id = t.teacher_id""")
    return render_template("classes.html", classes=rows)

@app.route("/class/add", methods=["GET", "POST"])
@login_required
def class_add():
    teachers = db.query("SELECT teacher_id, name FROM teachers")
    if request.method == "POST":
        cid = request.form.get("class_id")
        name = request.form.get("class_name")
        teacher_id = request.form.get("teacher_id") or None
        try:
            db.execute("INSERT INTO classes VALUES (?, ?, ?)", (cid, name, teacher_id))
            flash("Class added.", "success")
            return redirect(url_for("classes"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("class_form.html", teachers=teachers)

@app.route("/class/<id>/delete", methods=["POST"])
@admin_required
def class_delete(id):
    try:
        db.execute("DELETE FROM classes WHERE class_id=?", (id,))
        flash("Class removed.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("classes"))

# ---------- Results ----------
@app.route("/results")
@login_required
def results():
    sem1 = db.query("SELECT digital_id, Mathematics1, Physics, ComputerScience, avg_grade FROM sem1")
    sem2 = db.query("SELECT digital_id, Mathematics2, EnglishLiterature, History, avg_grade FROM sem2")
    return render_template("results.html", sem1=sem1, sem2=sem2)

@app.route("/result/add", methods=["GET", "POST"])
@login_required
def result_add():
    students = db.query("SELECT digital_id, name FROM students")
    if request.method == "POST":
        table = request.form.get("table")  # sem1 or sem2
        student_id = request.form.get("student_id")
        v1 = request.form.get("v1") or None
        v2 = request.form.get("v2") or None
        v3 = request.form.get("v3") or None
        avg = request.form.get("avg") or None
        try:
            if table == "sem1":
                db.execute("INSERT OR REPLACE INTO sem1 VALUES (?, ?, ?, ?, ?)", (student_id, float(v1) if v1 else None, float(v2) if v2 else None, float(v3) if v3 else None, float(avg) if avg else None))
            else:
                db.execute("INSERT OR REPLACE INTO sem2 VALUES (?, ?, ?, ?, ?)", (student_id, float(v1) if v1 else None, float(v2) if v2 else None, float(v3) if v3 else None, float(avg) if avg else None))
            flash("Result stored.", "success")
            return redirect(url_for("results"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("result_form.html", students=students)

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.register_blueprint(auth)
    app.run(debug=True)
