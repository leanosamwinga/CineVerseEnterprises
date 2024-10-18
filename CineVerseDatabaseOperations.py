import sqlite3
from _datetime import datetime


# Function to create a customer with all its required fields. Used upon sign-up.
def createCustomer(customerFullName, customerContactNumber, username, password):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()

    cursor.execute('SELECT COUNT(*) FROM tblCustomers WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result[0] > 0:
        print("Username already exists. Please choose a different username.")
        return

    cursor.execute('INSERT INTO tblCustomers ('
                   'customerFullName, customerContactNumber, username, password)'
                   ' VALUES (?, ?, ?, ?)',
                   (customerFullName, customerContactNumber, username, password))
    connect.commit()
    connect.close()


# Function to get the customer id based on the associated username. Returns the customer id, or none.
def getCustomerIdByUsername(username):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute("SELECT customerId FROM tblCustomers WHERE username = ?", (username,))
    result = cursor.fetchone()
    connect.close()
    if result:
        return result[0]
    else:
        return None


# Function to get the customer full name based on the associated customer id.
def getCustomerFullNameByCustomerId(customerId):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute("SELECT customerFullName FROM tblCustomers WHERE customerId = ?", (customerId,))
    result = cursor.fetchone()
    connect.close()
    if result:
        return result[0]
    else:
        return None


# Function to get the film id based on the associated film title.
def getFilmIdByFilmTitle(filmChoice):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute("SELECT filmId FROM tblFilms WHERE filmTitle = ?", (filmChoice,))
    result = cursor.fetchone()
    connect.close()
    if result:
        return result[0]
    else:
        return None


# Function to validate the user's credentials against values stored in that DB column. Returns a boolean.
def verifyUserCredentials(username, password):
    # Connect to the SQLite database
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()

    cursor.execute("SELECT COUNT(*) FROM tblCustomers WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    connect.close()

    if result[0] > 0:
        return True
    else:
        return False


# Function to create a booking with the FKs and other details.
def createBooking(customerId, filmId, screenType, ticketType, bookingDate, quantity):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO tblBookings (customerId, filmId, screenType, ticketType, bookingDate, quantity)'
                   'VALUES (?, ?, ?, ?, ?, ?)',
                   (customerId, filmId, screenType, ticketType, bookingDate, quantity))
    connect.commit()
    connect.close()


# Function to create an invoice with the customer id and the total amount. Invoice date is set to the current time.
def createInvoice(bookingId, totalAmount):
    invoiceTimeStamp = datetime.now().isoformat()
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO tblInvoices (bookingId, invoiceTimeStamp, totalAmount)'
                   'VALUES (?, ?, ?)',
                   (bookingId, invoiceTimeStamp, totalAmount))
    connect.commit()
    connect.close()


# Function to delete a booking in the DB by its ID. Used by the admin.
def deleteBookingByBookingId(bookingId):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM tblBookings WHERE bookingId = ?', (bookingId,))
    connect.commit()
    connect.close()


# Function to retrieve every booking in the DB. Used by the admin.
def retrieveAllBookings():
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM tblBookings')
    bookings = cursor.fetchall()
    connect.close()
    return bookings


# Function to get the booking id of the most recently created booking
def getMostRecentBookingId():
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute("SELECT LAST_INSERT_ROWID() AS bookingId")
    result = cursor.fetchone()
    bookingId = result[0] if result else None
    connect.close()
    return bookingId


# Function to delete a customer by an id. Can be used be the admin.
def deleteCustomerByCustomerId(customerId):
    connect = sqlite3.connect('CineVerseDatabase.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM tblCustomers WHERE customerId = ?', (customerId,))
    connect.commit()
    connect.close()
