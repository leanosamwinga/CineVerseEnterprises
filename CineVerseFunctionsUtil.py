# Two-dimensional dictionary storing ticket combination
ticketTypes = {
    "Child": {"2D": 4.00, "3D": 5.00, "IMAX": 10.00},
    "Teenager": {"2D": 6.00, "3D": 7.00, "IMAX": 12.00},
    "Adult": {"2D": 10.00, "3D": 11.00, "IMAX": 15.00},
    "Student": {"2D": 8.00, "3D": 9.00, "IMAX": 13.00},
}


# Function to calculate the price plus VAT, rounded to 2 decimal places for currency notation
def totalPriceIncludingVAT(price):
    VAT = 0.2
    return round(price * (1 + VAT), 2)


# Function to calculate ticket price based on the ticket combination. Handles KeyError exception.
def getTicketPrice(ticketType, screenType):
    try:
        price = ticketTypes[ticketType][screenType]
        return totalPriceIncludingVAT(price)
    except KeyError:
        return "Invalid ticket type or screen type."


# Function to ask user if they want to add another ticket combination to their booking. Returns a boolean.
def isAddAnotherTicket():
    while True:
        choice = str(input("Do you want to add another ticket to the booking? (yes/no): "))
        if choice.lower() == "yes" or "y":
            return True
        elif choice.lower() == "no" or "n":
            return False
        else:
            print("Invalid input. Please enter 'yes' / 'y' or 'no' / 'n'.")


# Function to validate the inputted mobile number is 11 digits long.
def validateMobileNumber(mobileNumber):
    return len(mobileNumber) == 11 and mobileNumber.isdigit()


# Function to capitalise the first letter of the firstname and surname for DB storage and readability.
def capitaliseName(fullName):
    return ' '.join(name.capitalize() for name in fullName.split())
