import csv
import ast
import AppointmentFunctions as af
from colorama import Style, Fore

from PatientFunctions import linecount
# ------------------------Doctors functions-------------------------------#

# Function to create a doctor profile and save it to a CSV file
def create_doctor():
    """
    Creates a doctor profile by collecting inputs for key details
    and writes the data to 'DoctorDetails.csv'.

    :return: None
    """
    # Define a dictionary with keys representing doctor details
    dctdetails = dict(
        Name="",  # Doctor's name
        Specialty="",  # Doctor's specialty
        Contact_Information="",  # Doctor's email (auto-generated)
        Availability=[],  # Doctor's availability
        Id=0  # Doctor's unique identifier (auto-generated)
    )

    # Collect user inputs for doctor details (excluding Contact_Information and Id)
    for key in dctdetails:
        if key not in ["Contact_Information", "Id"]:  # Skip keys that are auto-generated
            if key == "Availability":
                print("Enter availability days (e.g., Mon, Tue, etc.). Type 'done' when finished.")
                while True:
                    try:
                        daysAvailable = input("Enter day: ").strip().title()

                        if daysAvailable.lower() == "done":
                            break  # Exit loop when the user types 'done'

                        if daysAvailable not in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                            raise ValueError("Invalid day. Please enter a valid day (e.g., Mon, Tue).")

                        if daysAvailable in dctdetails["Availability"]:
                            raise ValueError("Day already added. Please enter a new day.")

                        dctdetails["Availability"].append(daysAvailable)

                    except ValueError as e:
                        print(f"Error: {e}")  # Display the error message and prompt again
            else:
                # Prompt the user to input the corresponding detail
                info = input(f"Enter {key}: ").strip().title()
                dctdetails[key] = info

    # Open the 'DoctorDetails.csv' file in append mode
    with open('Data/DoctorDetails.csv', mode='a', newline="") as file:
        # Create a CSV writer object using the keys of dctdetails as the column headers
        writer = csv.DictWriter(file, fieldnames=dctdetails.keys())

        # Automatically generate a unique ID for the doctor
        dctdetails['Id'] = linecount(file)

        # Automatically generate a contact email based on the doctor's name and ID
        dctdetails["Contact_Information"] = f'{dctdetails["Name"].replace(" ", "")}{dctdetails["Id"]}@email.com'

        # Write the doctor's details as a row in the CSV file
        writer.writerow(dctdetails)

    # Print a success message
    print(Fore.GREEN + "Doctor created successfully!\n" + Style.RESET_ALL)


# Function to search for a doctor in the 'DoctorDetails.csv' file based on their name
def search_doctor(doctor_name: str):
    """
    Searches for a doctor by name in the 'DoctorDetails.csv' file.

    :param doctor_name: The name of the doctor to search for.
    :return:
        - True if exactly one matching doctor is found.
        - The count of matches if multiple doctors with the same name are found.
        - False if no matching doctor is found.
        - None if the file is missing.
    """
    counter = 0  # Initialize a counter to keep track of matching names
    try:
        # Open the 'DoctorDetails.csv' file in read mode
        with open('Data/DoctorDetails.csv', mode="r", newline='') as file:
            reader = csv.DictReader(file)  # Create a CSV reader object

            # Iterate through each row in the CSV file
            for row in reader:
                # Check if the "Name" field matches the given doctor name (case-insensitive)
                if row["Name"].strip().lower() == doctor_name.lower():
                    counter += 1  # Increment the counter for each match

            # Return results based on the number of matches found
            return counter > 0

    except FileNotFoundError:
        # Handle the case where the file does not exist
        print("The doctor database file does not exist. Please create it first.")
        return None


def view_doctor_by_id(doctor_id): # id #Dasil
    """
    Displays information about a doctor  based on their ID.
    :param doctor_id:
    :return:
    """
    with open("Data/DoctorDetails.csv", mode="r", newline='') as file:
        reader = csv.DictReader(file)  # Read the CSV file
        total_width = 70
        for row in reader:
            if row["Id"] == doctor_id:
                for key, value in row.items():
                    # Calculate dots for alignment
                    dots_count = total_width - len(key) - len(str(value))
                    dots = '.' * max(dots_count, 1)  # Ensure at least one dot
                    # Print key-value pairs
                    print(f"{key}{dots} {value}")
                print()


def view_doctor_by_name(doctor_name): # name Dasil
    """
    Displays information about a doctors who share a common name.
    :param doctor_name: Name of the doctor to search for.
    :return:
    """
    # Case: Display details for a specific doctor by name
    with open("Data/DoctorDetails.csv", mode="r", newline='') as file:
        reader = csv.DictReader(file)
        total_width = 70
        for row in reader:
            # Check if the "Name" column contains the doctor's name
            if doctor_name.lower() in row["Name"].lower():  # Case-insensitive search
                for key, value in row.items():
                    # Calculate dots for alignment
                    dots_count = total_width - len(key) - len(str(value))
                    dots = '.' * max(dots_count, 1)  # Ensure at least one dot
                    # Print key-value pairs
                    print(f"{key}{dots} {value}")
                print()

def view_doctor_all(): #all doctors #Dasil
    """
    Displays information about all doctors.
    :return:
    """
    with open("Data/DoctorDetails.csv", mode="r", newline='') as file:
        reader = csv.DictReader(file)  # Read the CSV file
        total_width = 70
        for row in reader:
            for key, value in row.items():
                # Calculate the number of dots to align the output
                dots_count = total_width - len(key) - len(str(value))
                dots = '.' * dots_count
                # Print details for each doctor in the file
                print(f"{key}{dots} {value}")
            print()


def view_doctor(doctor: dict): # Dasil Added
    """
    Displays information about doctors.
    :param doctor: dict: Dictionary with doctor details to display.
    :return: None
    """
    with open("Data/DoctorDetails.csv", mode="r", newline='') as file:
        reader = csv.DictReader(file)  # Read the CSV file
        total_width = 70

    # Case: Display details directly from a dictionary
        print(f"\n{doctor['Name']}'s Information:")
        for key, value in doctor.items():
            # Calculate the number of dots to align the output
            dots_count = total_width - len(key) - len(str(value))
            dots = '.' * dots_count
            # Print details for each doctor in the file
            print(f"{key}{dots} {value}")
        print()


def get_doctor_by_id(doctor_id: int):
    """
    Returns information about a doctor based on their ID.
    :param doctor_id:
    :return: Dictionary containing doctor details.
    """
    doctor = "" # Initailizes to empty String.
    try:
        with open("Data/DoctorDetails.csv", mode="r", newline='') as file:
            # if doctor id is greater than number of lines in the file it raises an error
            if doctor_id not in range(1, linecount(file)):
                doctor = -1
                raise UnboundLocalError

            else: # Searches for the Doctor and
                reader = csv.DictReader(file)
                for row in reader:
                    if  int(row["Id"]) == int(doctor_id): # when match found, it returns it
                        row["Availability"] = ast.literal_eval(row["Availability"])
                        doctor = row
                        return doctor
    except UnboundLocalError:
        # in the case doctor does not exist
        print(Fore.YELLOW + "Doctor does not exist." + Style.RESET_ALL)
        return doctor
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(Fore.RED + "File does not exist." + Style.RESET_ALL)

def check_id(doctor_name, doctor_id):
    """
    Verifies that the id matches the name of the doctor.
    :param doctor_name: name of the doctor
    :param doctor_id: id of the doctor
    :return:
    """
    _match = False
    with open("Data/DoctorDetails.csv", mode="r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["Id"]) == doctor_id and row["Name"] == doctor_name:
                _match = True
    return _match

def get_doctor(doctor_id, doctor_name):  # Dasil Added
    """
    Retrieves doctor details from the 'DoctorDetails.csv' file based on the provided ID, and name,

    :param doctor_id: The unique ID of the doctor to search for.
    :param doctor_name: The name of the doctor to search for.
    :return: A dictionary containing the doctor's details if found.
    """

    doctor = ""
    try:
        # Open the 'DoctorDetails.csv' file in read mode
        with open('Data/DoctorDetails.csv', mode="r", newline="") as file:
            if doctor_id not in range(1, linecount(file)):
                doctor = -1
                raise UnboundLocalError

            else:
                reader = csv.DictReader(file)  # Create a CSV reader object
                # Iterate through each row in the file
                for row in reader:
                    # Check if both the name and ID match
                    if (row["Name"].strip().lower() == doctor_name.lower()) and int(row["Id"]) == doctor_id:
                        row["Availability"] = ast.literal_eval(row["Availability"])
                        doctor = row
                        return doctor

    except UnboundLocalError:
        print(Fore.YELLOW + "Doctor does not exist." + Style.RESET_ALL)
        return doctor
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(Fore.RED + "File does not exist." + Style.RESET_ALL)

def check_availability(doctor, day): # Dasil
    """
        Checks and displays doctor availability based on provided ID, name, or both.

        :param doctor: The name of the doctor to search for.
        :param day: The unique ID of the doctor to search for.
        :return: boolean if the doctor is available or not.
        """
    return day.title() in doctor["Availability"]


def get_availability(doctor):
    '''
    prints out the days the doctor is available.
    :param doctor: dictionary containing doctor details.
    :return: None
    '''
    print(f"\nDr.{doctor['Name']}' is available on the following days:")
    print(*doctor["Availability"], sep=", ")

#Modularized from main function
def doctor_submenu(doctor):
    """
    Sub menu for doctor view
    :param doctor:
    :return:  None
    """
    while True:
        try:
            dmc = int(input("\nPlease select an option\n" +
                            "1. Manage Appointments\n" +
                            "2. Exit\n"))

            match dmc:

                case 1:
                    # search appointment file for doctors name and return all matching records
                    af.search_appointments(doctor, "d")

                    while True:
                        appt_choice = int(input("\nWould you like to?\n" +
                                                "1. Schedule a new appointment\n" +
                                                "2. Go Back\n"))
                        try:
                            match appt_choice:
                                case 1:  # Handles appointment making and should write to appointment file
                                    af.appointment_menu(doctor, "d")
                                case 2:  # Goes back to Doctor info section
                                    break
                                case _:
                                    raise ValueError
                        except ValueError:
                            print(Fore.RED + "Invalid input please select from 1 - 2." + Style.RESET_ALL)


                case 2:
                    break  # Should exit program
                case _:
                    raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid input please use a number" + Style.RESET_ALL)