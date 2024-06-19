from utils.init import get_db_connection

db = get_db_connection()

optiuni_servicii = ["Consultatie", "Control", "Ecogragie", "Electrocardiograma", "EKG", "A doua opinie",
                        "Interpretare analize", "Test de efort"]
def get_select_options():
    cur = db.cursor()
    #cautare doctori dupa data ar trebui
    cur.execute("SELECT nume_doctor, prenume_doctor, iddoctor FROM Doctor")
    doctori = cur.fetchall();
    optiuni_doctori = [
        {
            "label": f"{doctor[0]} {doctor[1]}",
            "id": doctor[2],
        }
        for doctor in doctori
    ]

    options = {
        "optiuni_doctori": optiuni_doctori,
        "optiuni_servicii": optiuni_servicii
    }
    return options

