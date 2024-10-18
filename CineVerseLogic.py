import CineVerseFunctionsUtil
import CineVerseDatabaseOperations
from datetime import datetime
import re

# Dictionary storing default admin credentials
adminDetails = {"adminUsername": "adminPassword"}

print("\nPlease log-in / sign-up to CiniVerse Entertainment:")

# Constants used to limit invalid login attempts
MAX_LOGIN_TRIES = 3
LOGIN_ATTEMPTS = 0

# Pre-defined boolean variables set to false / none
isUserSignedUp = False
isUserLoggedIn = False
areCredentialsForAdmin = False
username = None

while LOGIN_ATTEMPTS < MAX_LOGIN_TRIES:
    try:
        userEntryChoice = int(input("Enter your choice of entry (1: Log-in, 2: Sign-up): "))

        # Mapper to map the user input to the
        entryChoiceMapper = {1: "Log-in", 2: "Sign-up"}
        entryChoiceFromMapper = entryChoiceMapper.get(userEntryChoice)

        if entryChoiceFromMapper == list(entryChoiceMapper.values())[0]:
            print("\nWelcome to the CiniVerse log-in page!")

            # Regex validation is performed on all name entries to ensure only alphabet values are entered
            while True:
                username = input("\nPlease enter a username: ")
                if re.search(r'\d', username):
                    print("Invalid input. Username cannot contain numbers.")
                else:
                    break

            while True:
                password = input("\nPlease enter a password: ")
                if re.search(r'\d', password):
                    print("Invalid input. Password cannot contain numbers.")
                else:
                    break

            if username == list(adminDetails.keys())[0] and password == list(adminDetails.values())[0]:
                print("Admin login successful")
                areCredentialsForAdmin = True
                break
            elif CineVerseDatabaseOperations.verifyUserCredentials(username, password):
                print("Login successful")
                isUserLoggedIn = True
                break
            else:
                LOGIN_ATTEMPTS += 1
                print("Invalid username or password. Please try again.")

        elif entryChoiceFromMapper == list(entryChoiceMapper.values())[1]:
            print("\nWelcome to the CiniVerse sign-up page!")
            while True:
                firstname = input("\nPlease enter your first name: ")
                if re.search(r'\d', firstname):
                    print("Invalid input. First name cannot contain numbers.")
                else:
                    break

            while True:
                surname = input("\nPlease enter your last name: ")
                if re.search(r'\d', surname):
                    print("Invalid input. Last name cannot contain numbers.")
                else:
                    break

            customerFullName = CineVerseFunctionsUtil.capitaliseName(f"{firstname} {surname}")

            while True:
                contactNumber = str(input("\nPlease enter your contact number: "))
                if CineVerseFunctionsUtil.validateMobileNumber(contactNumber):
                    break
                else:
                    print("Invalid mobile number. Please enter an 11-digit number.")

            username = str(input("\nPlease enter a username: "))
            password = str(input("\nPlease enter a password: "))

            # Check if username already exists
            if CineVerseDatabaseOperations.getCustomerIdByUsername(username):
                print("Username already exists. Redirecting to login page...")
                break
            elif username == list(adminDetails.keys())[0] and password == list(adminDetails.values())[0]:
                print("Admin signup not allowed. Sending you to admin interface.")
                areCredentialsForAdmin = True
                break

            CineVerseDatabaseOperations.createCustomer(
                customerFullName, contactNumber, username, password)
            isUserSignedUp = True
            break
        else:
            print("Invalid input. Please enter valid numbers.")

        if LOGIN_ATTEMPTS >= MAX_LOGIN_TRIES:
            print("Maximum login attempts reached. Please try again later.")
            exit()

    except ValueError:
        print("Invalid input. Please enter a number.")

# Route to admin interface
if areCredentialsForAdmin:
    print("\nAdmin options:")
    print("1. View all previous bookings\n2. Delete a previous booking\n3. Log off")

    adminChoice = str(input("Enter your choice: "))

    if adminChoice == "1":
        allBookings = CineVerseDatabaseOperations.retrieveAllBookings()
        for booking in allBookings:
            print(booking)
    elif adminChoice == "2":
        # Admin can search the DB for the bookingId they want to delete by
        bookingIdToDelete = int(input("Enter the ID of the booking to delete: "))
        CineVerseDatabaseOperations.deleteBookingByBookingId(bookingIdToDelete)
        print("Booking deleted successfully.")
    elif adminChoice == "3":
        print("Admin logged off.")
    else:
        print("Invalid choice. Please enter a valid option.")

# Route to main booking flow
else:
    print(f"\nWelcome to CineVerse Entertainment!\n\nPlease choose a ticket type and a screen type:")

    ticketQuantities = {}
    totalPrice = 0

    while True:
        try:
            userTicketType = int(input("Enter ticket type (1: Child, 2: Teenager, 3: Adult, 4: Student): "))
            userScreenType = int(input("Enter screen type (1: 2D, 2: 3D, 3: IMAX): "))

            ticketTypeMapper = {1: "Child", 2: "Teenager", 3: "Adult", 4: "Student"}
            screenTypeMapper = {1: "2D", 2: "3D", 3: "IMAX"}

            ticketTypeFromMapper = ticketTypeMapper.get(userTicketType)
            screenTypeFromMapper = screenTypeMapper.get(userScreenType)

            if ticketTypeFromMapper and screenTypeFromMapper:
                quantity = int(input(f"Enter quantity of {ticketTypeFromMapper.lower()} tickets: "))
                ticketQuantities[ticketTypeFromMapper] = ticketQuantities.get(ticketTypeFromMapper, 0) + quantity
                totalPrice += CineVerseFunctionsUtil.getTicketPrice(
                    ticketTypeFromMapper, screenTypeFromMapper) * quantity

                if not CineVerseFunctionsUtil.isAddAnotherTicket():
                    break
            else:
                print("Invalid input. Please enter valid numbers.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("\nPlease choose a film from the catalogue: ")

    filmChoiceMapper = {
        1: "Jurassic Cabin",
        2: "The Dark Night",
        3: "The Nightmare on First Street",
        4: "Quantum Mania",
        5: "The Shape of Time"
    }

    for key, value in filmChoiceMapper.items():
        print(f"{key}: {value}")

    filmChoice = None

    while filmChoice is None:
        try:
            userFilmChoice = int(input("\nEnter the number corresponding to your choice: "))
            if userFilmChoice in filmChoiceMapper:
                filmChoice = filmChoiceMapper[userFilmChoice]
                print("\nThe film you have chosen is:", filmChoice)
            else:
                print("Invalid film choice. Please enter a number from 1 to 5")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        # Using ISO 8601 format for the years, months and days
        userBookingDate = str(input("\nEnter booking date (YYYY-MM-DD): "))
        try:
            # Converting the input from string to datetime to validate date is not in the past
            userBookingDateConverted = datetime.strptime(userBookingDate, "%Y-%m-%d").date()
            dateToday = datetime.today().date()

            if userBookingDateConverted >= dateToday:
                bookingDate = userBookingDateConverted.strftime("%Y-%m-%d")
                break
            else:
                print("Booking date cannot be in the past. Please enter a valid date.")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    # Functionality to commit a booking to the DB if the user has logged in or signed up and chosen their booking
    if isUserSignedUp or isUserLoggedIn:
        customerId = CineVerseDatabaseOperations.getCustomerIdByUsername(username)
        fullName = CineVerseDatabaseOperations.getCustomerFullNameByCustomerId(customerId)
        filmId = CineVerseDatabaseOperations.getFilmIdByFilmTitle(filmChoice)

        # Renamed here for readability when inserting into the DB
        screenTypeForInsertion = screenTypeFromMapper
        ticketTypeForInsertion = ticketTypeFromMapper

        CineVerseDatabaseOperations.createBooking(
            customerId, filmId, screenTypeForInsertion,
            ticketTypeForInsertion, bookingDate, sum(ticketQuantities.values()))
        print(f"\nBooking created by {fullName} for {filmChoice} on {bookingDate}.")

        # Calling function which retrieves the booking id of the ultimate booking
        bookingId = CineVerseDatabaseOperations.getMostRecentBookingId()
        CineVerseDatabaseOperations.createInvoice(bookingId, totalPrice)
        print(f"Invoice created for {fullName} for a total of £{totalPrice}.")

        print("\nThank you for booking with CineVerse!")
