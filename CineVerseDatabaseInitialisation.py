import sqlite3

connect = sqlite3.connect('CineVerseDatabase.db')
cursor = connect.cursor()

# Creating tblInvoices to be used for storing the order the costs and dates when the customer made the booking
cursor.execute('''CREATE TABLE IF NOT EXISTS tblInvoices (
    invoiceId INTEGER PRIMARY KEY,
    bookingId INTEGER,
    invoiceTimeStamp TEXT,
    totalAmount REAL,
    FOREIGN KEY (bookingId) REFERENCES tblBookings(bookingId)
)''')


# Creating tblCustomers to store all the customer information
cursor.execute('''CREATE TABLE IF NOT EXISTS tblCustomers (
    customerId INTEGER PRIMARY KEY,
    customerFullName TEXT,
    customerContactNumber TEXT,
    username TEXT,
    password TEXT
    )
    ''')

# Creating tblFilms to store details regarding films, not strictly required but allows for scaling
cursor.execute('''CREATE TABLE IF NOT EXISTS tblFilms (
    filmId INTEGER PRIMARY KEY,
    filmTitle TEXT,
    filmDescription TEXT,
    filmDuration INTEGER,
    releaseDate TEXT
    )
    ''')

# Creating tblBookings to store details regarding the booking, in addition to links to the customer, invoice, and film
cursor.execute('''CREATE TABLE IF NOT EXISTS tblBookings (
    bookingId INTEGER PRIMARY KEY,
    customerId INTEGER,
    filmId INTEGER,
    screenType TEXT,
    ticketType TEXT,
    bookingDate TEXT,
    quantity INTEGER,
    FOREIGN KEY (customerId) REFERENCES tblCustomers(customerId),
    FOREIGN KEY (filmId) REFERENCES tblFilms(filmId)
    )
    ''')

connect.commit()

films = [
    ('Jurassic Cabin', 127, 'An adventure in a remote cabin with prehistoric creatures.', '1993-07-16'),
    ('The Dark Night', 152, 'A gripping tale of vigilante justice in a city plagued by crime.', '2008-07-24'),
    ('The Nightmare on First Street', 91, 'A horror film about a terrifying nightmare.', '1985-08-30'),
    ('Quantum Mania', 124, 'A sci-fi adventure exploring the mysteries of quantum physics.', '2023-02-17'),
    ('The Shape of Time', 78, 'A romantic drama spanning generations with a twist of time travel.', '1962-09-10')
]

cursor.executemany('INSERT INTO tblFilms (filmTitle, filmDuration, filmDescription, releaseDate)'
                   ' VALUES (?, ?, ?, ?)', films)

connect.commit()
connect.close()
