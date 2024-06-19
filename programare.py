from flask import Blueprint, redirect, render_template, request, url_for
from datetime import date, timedelta, time, datetime
from utils.init import get_db_connection
from utils.options import get_select_options

programare_bp = Blueprint("programare", __name__, template_folder="templates")
db = get_db_connection()

@programare_bp.route('/', methods=['GET', 'POST'])
def programare():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("""SELECT 
        a.idprogramare,
        p.nume_pacient,
        p.prenume_pacient,
        a.serviciu,
        a.data,
        a.ora_start,
        a.ora_stop,
        a.valabil,
        d.nume_doctor,
        d.prenume_doctor 
        FROM 
        Programare AS a 
        JOIN
        Pacient AS p ON a.idpacient = p.idpacient 
        JOIN
        Doctor AS d ON a.iddoctor = d.iddoctor 
        ORDER BY a.idprogramare DESC;
        """)
        programare = cur.fetchall()
        # options = get_select_options()

        return render_template(
            "programare.html",
            programare=programare
        )



@programare_bp.route('/creare_programare', methods=['GET', 'POST'])
def creare_programare():
    if request.method == "POST":

        nume_pacient = request.form["nume_pacient"]
        prenume_pacient = request.form["prenume_pacient"]
        varsta = request.form["varsta"]
        serviciu = request.form["serviciu"]

        format_date = '%d/%m/%Y'
        data = datetime.strptime(request.form["data"], format_date)

        options = get_select_options(data)

        cur = db.cursor()
        cur.execute(
            "INSERT INTO Pacient (nume_pacient, prenume_pacient, varsta) VALUES (?, ?, ?)",
            (nume_pacient, prenume_pacient, varsta),
        )
        db.commit()
        # return redirect(url_for("programare.programare"))
        return render_template('creare_programare.html', options=options)


@programare_bp.route("/delete/<idprogramare>", methods=["POST", "GET"])
def delete_programare(idprogramare):
    if request.method == "POST":
        cur = db.cursor()
        cur.execute("DELETE FROM Programare WHERE idprogramare = ?", (idprogramare))
        db.commit()
        return redirect(url_for("programare.programare"))
    else:
        return render_template("delete.html", id=idprogramare, url="programare")


@programare_bp.route("/update/<idprogramare>", methods=["POST", "GET"])
def update_programare(idprogramare):
    if request.method == "POST":
        idpacient = request.form["idpacient"]
        iddoctor = request.form["iddoctor"]
        serviciu = request.form["serviciu"]
        format_date = '%d/%m/%Y'
        data = datetime.strptime(request.form["data"], format_date)

        valabil = int(request.form["valabil"])

        format_time = '%H:%M'
        ora_start = datetime.strptime(request.form['ora_start'], format_time).time()
        ora_stop = datetime.strptime(request.form['ora_stop'], format_time).time()
        cur = db.cursor()
        cur.execute(
            "UPDATE Programare SET idpacient = ?, iddoctor = ?, serviciu = ?, data = ?, valabil = ?, ora_start = ?, ora_stop = ? WHERE idprogramare = ?",
            (idpacient,
             iddoctor,
             serviciu,
             data,
             valabil,
             ora_start,
             ora_stop,
             idprogramare
             ),
        )
        db.commit()
        return redirect(url_for("programare.programare"))
    else:
        cur = db.cursor()
        cur.execute("SELECT * FROM Programare WHERE idprogramare = ?", (idprogramare))
        programare = cur.fetchone()
        return render_template("update_programare.html", programare=programare, url="programare")
