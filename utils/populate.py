from datetime import date, timedelta, time, datetime
from utils.init import get_db_connection

db = get_db_connection()

def populate_app(iddoctor, start_date, end_date):
    """Populates appointments for a doctor between dates"""
    cur = db.cursor()
    ora_start = "9:00"
    ora_stop = "17:00"

    time_format = "%H:%M"

    start_time = datetime.strptime(ora_start, time_format).time()
    end_time = datetime.strptime(ora_stop, time_format).time()

    for day in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=day)
        for hour in range("09:00", "17:00"):
            start_time = time(hour)
            end_time = time(hour + 1)  # Assuming 1-hour appointments
            cur.execute("INSERT INTO Programare (iddoctor, data, ora_start, ora_stop, valabil) VALUES (?, ?, ?, ?, ?)",
                        (iddoctor, current_date, start_time, end_time, True))

    db.commit()
    # cur.close()
    # db.close()

doctors = [
    {'iddoctor': 1, 'start_date': '2024-06-19', 'end_date': '2024-06-21'},
    {'iddoctor': 1, 'start_date': '2024-06-24', 'end_date': '2024-06-28'},
    {'iddoctor': 1, 'start_date': '2024-07-1', 'end_date': '2024-07-5'},
    {'iddoctor': 2, 'start_date': '2024-06-24', 'end_date': '2024-06-28'},
    {'iddoctor': 2, 'start_date': '2024-07-1', 'end_date': '2024-07-5'},
    {'iddoctor': 3, 'start_date': '2024-06-24', 'end_date': '2024-06-28'},
    {'iddoctor': 4, 'start_date': '2024-07-1', 'end_date': '2024-07-5'},
]

for doctor in doctors:
    populate_app(doctor['iddoctor'], date.fromisoformat(doctor['start_date']), date.fromisoformat(doctor['end_date']))
