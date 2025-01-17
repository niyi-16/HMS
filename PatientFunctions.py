# Importing datetime module to validate patient DOB input and calculate current age
from datetime import datetime
import ast
from colorama import Fore, Style
todaysDate = datetime.now()

def linecount(file):
    """
    Counts the number of lines in a given file.

    :param file: The file object whose lines are to be counted.
    :return: The total number of lines in the file as an integer.
    """
    # Open the file in read mode using the name attribute of the file object
    with open(file.name, mode="r") as f:
        lines = f.readlines()  # Read all lines into a list
        no_of_lines = len(lines)  # Count the number of lines in the list

    return no_of_lines  # Return the total line count


def create_patient(patient_fname=None, patient_lname=None):
    """
    This function creates a new patient file - complete
    :param patient_fname:
    :param patient_lname:
    :return:
    """
    if None in [patient_fname, patient_lname]:
        patient_fname = input("Please enter first name:\n").title().strip()  # collects name to search for patient
        patient_lname = input("Please enter last name:\n").title().strip()

    with open ('Data/patient_master.txt', 'a') as file:
        print(f"Welcome, {patient_fname} {patient_lname}. Please register by filling in the following information:\n")
        while True:
            #Receiving user input
            patient_name = f"{patient_fname} {patient_lname}".title() #Formatting name input for consistency with .title()
            patient_address = input("Address:\n")
            patient_contact = input("Email Address:\n")
            #Creating another while loop to ensure user doesn't have to re-enter all input if date is invalid
            while True:
                try: #Validating DOB input
                    patient_dob = input("Date of birth (YYYY-MM-DD):\n")
                    #Using strptime() to convert date input string to datetime object
                    patient_dob = datetime.strptime(patient_dob, '%Y-%m-%d')
                    #Calculating age based on datetime.now() by checking if user has had birthday or not this year
                    patient_age = todaysDate.year - patient_dob.year - ((todaysDate.month, todaysDate.day) < (patient_dob.month, patient_dob.day))
                    #Checking if DOB is valid
                    if patient_age < 0 or patient_age > 110:
                        print("Please enter a valid birth date.")
                        continue
                    break
                except ValueError: #Catching ValueError if date invalid
                    print(f"'{patient_dob}' is an invalid date. Please use 'YYYY-MM-DD' format.")
            #Calling get_patient() to assign a unique autoincrement id to user's file
            patient_id=linecount(file)
            #Storing user input as dictionary and formatting input for consistency/readability
            try:
                patient_info={
                    'Name': patient_name,
                    'Age': patient_age,
                    'Address': patient_address.title(),
                    'Contact': patient_contact,
                    'Date of Birth': patient_dob.strftime('%Y-%m-%d'), #Converting DOB back to string
                    'id': patient_id + 1
                    }
            #Catching UnboundLocalError in the case of invalid user input causing variable to not be assigned a value
            except UnboundLocalError:
                continue

            view_patient(patient_info)
            #Asking user to confirm if record is accurate
            confirmation=input("Is this information correct? Y/N:\n").lower()
            #Appending data to patient_master.txt if confirmed
            if confirmation in {'y', 'yes'}:
                    file.write(str(patient_info) + '\n') #Converting dictionary to string and adding linebreak to end of string for readability
                    print("\nPatient successfully registered.\n")
                    break
            #Allowing user to re-enter data if information is incorrect
            elif confirmation in {'n', 'no'}:
                continue
            #Handling input errors
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

#Function to check if patient is in patient_master.txt
# noinspection SpellCheckingInspection
def patient_search(patient_fname, patient_lname):
    """
    This function searches for patients whose name matches
    :param patient_fname:
    :param patient_lname:
    :return:
    """
    patient_name= f"{patient_fname} {patient_lname}"
    counter = 0
    try:
        with open ('Data/patient_master.txt', 'r+') as file:
            #Reading all lines in patient_master.txt
            lines=file.readlines()

        #Looping through lines (each line in file is dictionary contents that have been converted to a string)
        for line in lines:
            patient_record=ast.literal_eval(line.strip()) #literal_eval safely converts string back into dictionary
            #Checking if input name matches name key by using .get()
            if patient_record.get('Name')==patient_name:
                counter+=1

        if counter == 1:
            return True

        elif counter > 1:
            return counter

        elif counter < 1:
            return False
    except FileNotFoundError:
        print("Patient file not found.")

#Function to display patient record

# UPDATE moved from create patient
def view_patient(patient_details):
    """
    This function prints out the patient details
    :param patient_details:
    :return:
    """
    if patient_details is None:
        None

    else:
        try:
            print("Patient record:\n")
            # Define total width for the line (adjust as needed)
            total_width = 50

            for key, value in patient_details.items():
                # Calculate the number of dots to align the output
                dots_count = total_width - len(key) - len(str(value))
                dots = '.' * dots_count

                # Print the formatted line
                print(f"{key}{dots} {value}")
            print()
        except (AttributeError, UnboundLocalError):
            print()


def get_patient(patient_fname, patient_lname, patient_id=None):
    """
    This function gets patient details
    :param patient_fname:
    :param patient_lname:
    :param patient_id:
    :return:
    """

    try:
        with open('Data/patient_master.txt', 'r') as file:
            for line in file:
                data = ast.literal_eval(line)
                if patient_id is not None:
                    if (data['id'] == patient_id) and (data['Name'] == f"{patient_fname} {patient_lname}"):
                            patient = data
                elif patient_id is None:
                    if data['Name'] == f"{patient_fname} {patient_lname}":
                        patient = data
        return patient
    except UnboundLocalError:
        print(Fore.YELLOW + "\nPatient does not exist.\n" + Style.RESET_ALL)
        return - 1
    except FileNotFoundError:
        print("File Not Found")

def view_patient_all():
    try:
        with open('Data/patient_master.txt', 'r') as file:
            for line in file:
                data = ast.literal_eval(line)
                # Define total width for the line (adjust as needed)
                total_width = 50
                for key, value in data.items():
                    # Calculate the number of dots to align the output
                    dots_count = total_width - len(key) - len(str(value))
                    dots = '.' * dots_count

                    # Print the formatted line
                    print(f"{key}{dots} {value}")
                print()
    except (AttributeError, UnboundLocalError):
     print()