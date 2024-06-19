from flask import Blueprint, redirect, render_template, request, url_for

from utils.init import get_db_connection

doctor_bp = Blueprint("doctori", __name__, template_folder = "templates")
db = get_db_connection()

@doctor_bp.route("/", methods = ["POST", "GET"])
def doctori():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT * FROM Doctor ORDER BY iddoctor")
        doctori = cur.fetchall()
        return render_template(
            "doctori.html",
            doctori = doctori,
        )
    else:
        nume = request.form["nume_doctor"]
        prenume = request.form["prenume_doctor"]
        specializare = request.form["specializare"]
        cur = db.cursor()
        cur.execute(
            "INSERT INTO Doctor (nume_doctor, prenume_doctor, specializare) VALUES (?, ?, ?)",
            (nume, prenume, specializare),
        )
        db.commit()
        return redirect(url_for("doctori.doctori"))


@doctor_bp.route("/delete/<iddoctor>", methods = ["POST", "GET"])
def delete_doctor(iddoctor):
    if request.method == "POST":
        cur = db.cursor()
        cur.execute("DELETE FROM Doctor WHERE iddoctor = ?", (iddoctor))
        db.commit()
        return redirect(url_for("doctori.doctori"))
    else:
        return render_template("delete.html", id = iddoctor, url = "doctori")


@doctor_bp.route("/update/<iddoctor>", methods = ["POST", "GET"])
def update_doctor(iddoctor):
    if request.method == "POST":
        nume = request.form["nume_doctor"]
        prenume = request.form["prenume_doctor"]
        specializare = request.form["specializare"]
        cur = db.cursor()
        cur.execute(
            "UPDATE Doctor SET nume_doctor = ?, prenume_doctor = ?, specializare = ? WHERE iddoctor = ?",
            (nume, prenume, specializare, iddoctor),
        )
        db.commit()
        return redirect(url_for("doctori.doctori"))
    else:
        cur = db.cursor()
        cur.execute("SELECT * FROM Doctor WHERE iddoctor = ?", (iddoctor))
        doctor = cur.fetchone()
        return render_template("update_doctor.html", doctor = doctor, url = "doctori")
