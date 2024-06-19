from flask import Blueprint, redirect, render_template, request, url_for
from datetime import date, timedelta, time, datetime
from utils.init import get_db_connection
from utils.options import get_select_options
from utils.timetable import timeslots

ore = [
        {
            "label":"9:00", "value":"9:00"
        },
        {
            "label": "10:00", "value": "10:00"
        },
        {
            "label": "11:00", "value": "11:00"
        },
        {
            "label": "12:00", "value": "12:00"
        },
        {
            "label": "13:00", "value": "13:00"
        },
        {
            "label": "14:00", "value": "14:00"
        },
        {
            "label": "15:00", "value": "15:00"
        },
        {
            "label": "16:00", "value": "16:00"
        },
        {
            "label": "17:00", "value": "17:00"
        }
    ]

# from utils.options import get_select_options
# import logging

programare_bp = Blueprint("programare", __name__, template_folder="templates")
db = get_db_connection()

@programare_bp.route('/', methods=['GET', 'POST'])
def programare():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT * FROM Programare ORDER BY idprogramare")

        programare = cur.fetchall()

        return render_template(
            "programare.html",
            programare=programare
        )
    else:
        return redirect(url_for("programare.programare"))

# def get_available_slots(nume_doctor, data):
#     cur = db.cursor()
#     cur.execute("""
#         SELECT ora_start, ora_stop
#         FROM Programare AS p
#         JOIN Doctor AS d ON p.iddoctor = d.iddoctor
#         WHERE d.nume_doctor = ? AND p.data = ?
#     """, (nume_doctor, data))
#     rezervari = cur.fetchall()
#
#     # Programul de lucru al doctorului
#     work_start = datetime.strptime("09:00", "%H:%M").time()
#     # work_end = datetime.strptime("17:00", "%H:%M").time()
#
#     # Convertim rezervările în intervale de timp
#     reserved_intervals = [(datetime.strptime(r[0], "%H:%M").time(), datetime.strptime(r[1], "%H:%M:%S").time()) for r in rezervari]
#
#     # Calculează intervalele disponibile
#     available_slots = []
#     current_start = work_start
#
#     for interval in reserved_intervals:
#         if current_start < interval[0]:
#             available_slots.append((current_start, interval[0]))
#         current_start = interval[1]
#
#     if current_start < work_end:
#         available_slots.append((current_start, work_end))
#
#     return available_slots

@programare_bp.route('/creare_programare', methods=['GET', 'POST'])
def creare_programare():
    if request.method == "POST":

        nume = request.form["nume"]
        prenume = request.form["prenume"]
        varsta = request.form["varsta"]
        serviciu = request.form["serviciu"]

        format_date = '%d/%m/%Y'
        data = datetime.strptime(request.form["data"], format_date).date()

        format_time = '%H:%M'
        ora = datetime.strptime(request.form["ora_start"], format_time).time()

        iddoctor = request.form["iddoctor"]

        cur = db.cursor()
        cur.execute(
            "INSERT INTO Programare (iddoctor, nume, prenume, serviciu, data, ora_start) VALUES(?, ?, ?, ?, ?, ?)",
            (iddoctor, nume, prenume, serviciu, varsta, data, ora)
        )
        db.commit()
        options = get_select_options();
        timeslots = ore
        return render_template('creare_programare.html', options = options, timeslots = timeslots)
    else:
        options = get_select_options();
        timeslots = ore
        return render_template('creare_programare.html', options=options, timeslots=timeslots)

    # else:

    # # elif request.method == "GET":
    #     # Obține datele pentru template-ul de creare programare
    #     nume_doctor = request.args.get("nume_doctor", None)
    #     data = request.args.get("data", None)
    #     available_slots = []
    #     if nume_doctor and data:
    #         data = datetime.strptime(data, '%d/%m/%Y').date()
    #         available_slots = get_available_slots(nume_doctor, data)
    #     options = get_select_options(data)
    #     return render_template('creare_programare.html', options={'optiuni_servicii': [], 'available_slots': available_slots})

        # app.register_blueprint(programare_bp, url_prefix="/programare")

# @programare_bp.route("/delete/<idprogramare>", methods=["POST", "GET"])
# def delete_programare(idprogramare):
#     if request.method == "POST":
#         cur = db.cursor()
#         cur.execute("DELETE FROM Programare WHERE idprogramare = ?", (idprogramare))
#         db.commit()
#         return redirect(url_for("programare.programare"))
#     else:
#         return render_template("delete.html", id=idprogramare, url="programare")
#
#
# @programare_bp.route("/update/<idprogramare>", methods=["POST", "GET"])
# def update_programare(idprogramare):
#     if request.method == "POST":
#         iddoctor = request.form["iddoctor"]
#         serviciu = request.form["serviciu"]
#         format_date = '%d/%m/%Y'
#         data = datetime.strptime(request.form["data"], format_date)
#
#         valabil = int(request.form["valabil"])
#
#         format_time = '%H:%M'
#         ora_start = datetime.strptime(request.form['ora_start'], format_time).time()
#         ora_stop = datetime.strptime(request.form['ora_stop'], format_time).time()
#         cur = db.cursor()
#         cur.execute(
#             "UPDATE Programare SET idpacient = ?, iddoctor = ?, serviciu = ?, data = ?, valabil = ?, ora_start = ?, ora_stop = ? WHERE idprogramare = ?",
#             (idpacient,
#              iddoctor,
#              serviciu,
#              data,
#              valabil,
#              ora_start,
#              ora_stop,
#              idprogramare
#              ),
#         )
#         db.commit()
#         return redirect(url_for("programare.programare"))
#     else:
#         cur = db.cursor()
#         cur.execute("SELECT * FROM Programare WHERE idprogramare = ?", (idprogramare))
#         programare = cur.fetchone()
#         return render_template("update_programare.html", programare=programare, url="programare")
