from flask import Blueprint, redirect, render_template, request, url_for

from utils.init import get_db_connection

pacient_bp = Blueprint("pacienti", __name__, template_folder = "templates")
db = get_db_connection()

@pacient_bp.route("/", methods = ["POST", "GET"])
def pacienti():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT * FROM Pacient ORDER BY idpacient")
        pacienti = cur.fetchall()
        return render_template(
            "pacienti.html",
            pacienti = pacienti,
        )
    else:
        nume = request.form["nume_pacient"]
        prenume = request.form["prenume_pacient"]
        varsta = int(request.form["varsta"])
        cur = db.cursor()
        cur.execute(
            "INSERT INTO Pacient (nume_pacient, prenume_pacient, varsta) VALUES (?, ?, ?)",
            (nume, prenume, varsta),
        )
        db.commit()
        return redirect(url_for("pacienti.pacienti"))


@pacient_bp.route("/delete/<idpacient>", methods = ["POST", "GET"])
def delete_pacient(idpacient):
    if request.method == "POST":
        cur = db.cursor()
        cur.execute("DELETE FROM Pacient WHERE idpacient = ?", (idpacient))
        db.commit()
        return redirect(url_for("pacienti.pacienti"))
    else:
        return render_template("delete.html", id = idpacient, url = "pacienti")


@pacient_bp.route("/update/<idpacient>", methods = ["POST", "GET"])
def update_pacient(idpacient):
    if request.method == "POST":
        nume = request.form["nume_pacient"]
        prenume = request.form["prenume_pacient"]
        varsta = int(request.form["varsta"])
        cur = db.cursor()
        cur.execute(
            "UPDATE Pacient SET nume_pacient = ?, prenume_pacient = ?, varsta = ? WHERE idpacient = ?",
            (nume, prenume, varsta, idpacient),
        )
        db.commit()
        return redirect(url_for("pacienti.pacienti"))
    else:
        cur = db.cursor()
        cur.execute("SELECT * FROM Pacient WHERE idpacient = ?", (idpacient))
        pacient = cur.fetchone()
        return render_template("update_pacient.html", pacient = pacient, url = "pacienti")
