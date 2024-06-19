from utils.init import get_db_connection

db = get_db_connection()

def get_available_time_slots(data):
    cur = db.cursor()
    # Assuming you have a table Programare with fields idprogramare, data, start_time, end_time
    cur.execute("""
        SELECT ora_start, ora_stop
        FROM Programare
        WHERE data = ?
        ORDER BY ora_start
    """, (data))
    appointments = cur.fetchall()

    # Define working hours (e.g., 09:00 to 17:00)
    working_hours = [("09:00", "10:00"), ("10:00", "11:00"), ("11:00", "12:00"), ("12:00", "13:00"),
                     ("13:00", "14:00"), ("14:00", "15:00"), ("15:00", "16:00"), ("16:00", "17:00")]

    # Filter out occupied time slots
    available_time_slots = []
    for start, end in working_hours:
        if not any(appointment['start_time'] <= start < appointment['end_time'] for appointment in appointments):
            available_time_slots.append((start, end))

    return available_time_slots
