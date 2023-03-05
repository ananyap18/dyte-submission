import sqlite3

# Create a new SQLite database
conn = sqlite3.connect('ffcsdata.db')

# Create a Slots table
conn.execute('''
CREATE TABLE IF NOT EXISTS Slots (
    id INTEGER PRIMARY KEY,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    day_of_week INTEGER NOT NULL
);
''')

# Function to create a new slot
def create_slot(start_time, end_time, day_of_week):
    conn.execute('''
    INSERT INTO Slots (start_time, end_time, day_of_week)
    VALUES (?, ?, ?)
    ''', (start_time, end_time, day_of_week))
    conn.commit()

# Function to get all slots
def get_all_slots():
    cursor = conn.execute('SELECT * FROM Slots')
    slots = []
    for row in cursor:
        slot = {
            'id': row[0],
            'start_time': row[1],
            'end_time': row[2],
            'day_of_week': row[3]
        }
        slots.append(slot)
    return slots

# Function to update a slot
def update_slot(id, start_time, end_time,
