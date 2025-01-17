import json
import DoctorFunctions as df
import PatientFunctions as pf
from colorama import Fore, Style

# List of valid days to ensure consistency in appointment scheduling
days_of_the_week = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]

#menu to handle appointment making
def appointment_menu(user, user_lvl):
    """
    Handles the appointment scheduling workflow for both doctors and patients.

    :param user: Dictionary representing the current user (doctor or patient).
    :param user_lvl: String indicating the user level ('d' for doctor, 'p' for patient).
    :return: None
    """

    match user_lvl:
        case "d":
            """
            Doctor's Appointment Menu:
            Allows the doctor to schedule an appointment for a specific patient.
            """
            # Prompt for patient details
            while True:
                patient_fname = input("Patient first name? \n").title().strip()
                patient_lname = input("Patient last name?\n").title().strip()
                patient_id = int(input("Enter the patient ID: "))
                patient = pf.get_patient(patient_fname, patient_lname, patient_id)
                #Ensures valid details for appointment
                if patient !=  -1:
                    break

            while True:
                try:
                    # Prompt the doctor for the desired appointment day
                    day = input("For what day?\n").title().strip()

                    # Validate the day
                    if day not in days_of_the_week:
                        raise ValueError("Not a valid day")
                    else:
                        # Check the doctor's availability on the selected day
                        if df.check_availability(user, day):
                            schedule_appointment(patient, user, day)
                            break
                        else:
                            print(f"{user['Name']} is not available on {day}.\n")
                except ValueError as e:
                    print(e)

        case "p":
            """
            Patient's Appointment Menu:
            Allows the patient to schedule an appointment with a doctor.
            """
            while True:
                try:
                    # Ask the patient if they have a specific doctor in mind
                    dykd = input("\nDo you have a doctor in mind? (y/n)\n").lower()
                    if dykd not in ["y", "n"]:
                        raise ValueError("Please select 'y' or 'n'.")
                    break  # Exit the loop if input is valid
                except ValueError as e:
                    print(Fore.RED + str(e) + Style.RESET_ALL)

            if dykd == "y":
                while True:
                    # Patient specifies a doctor
                    doctor_fname = (input("What is your doctor's first name?\n").title())
                    doctor_lname = (input("What is your doctor's last name?\n").title())
                    doctor_name = f"{doctor_fname} {doctor_lname}"
                    if len(doctor_name) > 2:
                        if df.search_doctor(doctor_name) > 0:
                            df.view_doctor_by_name(doctor_name)
                            break
                    else:
                        print("Invalid input. Please only enter an alphabetical string of more than three characters.")
                        continue


            elif dykd == "n":
                # Patient views all available doctors
                df.view_doctor_all()
                doctor_name = input("\nWhat is the doctor's name?\n").title()


            while True:
                print("Please choose who you would like to schedule an appointment with.\n")
                try:
                    # Prompt for doctor's ID to identify the chosen doctor
                    doctor_id = int(input("Doctor's ID:\n"))
                    doctor2 = df.get_doctor_by_id(doctor_id)
                    if doctor2 != -1:
                        if not df.check_id(doctor_name, doctor_id):
                            print(Fore.LIGHTYELLOW_EX+"Wrong ID. Please try again.\n"+Style.RESET_ALL)
                            continue
                        break
                except ValueError | UnboundLocalError:
                    print("Invalid ID")




            # Display the selected doctor's availability
            df.get_availability(doctor2)
            while True:
                try:
                    # Prompt for the desired appointment day
                    appt_date = input("\nSelect Day:\n").title().strip()
                    if appt_date not in days_of_the_week:
                        raise ValueError("Not a valid day")
                    else:
                        # Check the doctor's availability and schedule the appointment
                        if df.check_availability(doctor2, appt_date):
                            schedule_appointment(user, doctor2, appt_date)
                            break
                        else:
                            print(Fore.YELLOW + f"{doctor2['Name']} is not available on {appt_date}.\n" + Style.RESET_ALL)
                except ValueError as e:
                    print(Fore.RED + str(e) + Style.RESET_ALL)

# For Scheduling Appointments
def schedule_appointment(patient, doctor, appointment_date):
    """
    Schedules an appointment for a given patient with a specified doctor.

    :param patient: Dictionary containing patient details.
    :param doctor: Dictionary containing doctor details.
    :param appointment_date: String representing the date of the appointment.
    :return: None
    """

    # Open the AppointmentMaster.txt file in append mode to add the new appointment
    with open('Data/AppointmentMaster.txt', mode="a+") as file:
        # Create a dictionary containing the appointment details
        appointmentdict = dict(
            patientName=patient["Name"],  # Extract the patient's name
            patient_id=patient["id"],  # Extract the patient's ID
            doctorName=doctor["Name"],  # Extract the doctor's name
            doctor_contact=doctor["Contact information"],  # Extract the doctor's contact information
            doctor_id=doctor["Id"],  # Extract the doctor's ID
            appointmentDate=appointment_date  # Set the appointment date
        )

        # Write the appointment details as a JSON string into AppointmentMaster.txt
        file.write(json.dumps(appointmentdict) + "\n")

        # Print a confirmation message to indicate that the appointment has been scheduled
        print(Fore.GREEN + "Appointment Scheduled!\n" + Style.RESET_ALL)

# Searches and displays appointments
def search_appointments(user, user_level):
    """
    Searches and displays appointments for a user based on their name and role.

    :param user: Dictionary containing user details (doctor or patient).
    :param user_level: User role, either "p" for patient or "d" for doctor.
    :return: None
    """
    try:
        # Open the AppointmentMaster.txt file in read mode
        with open('Data/AppointmentMaster.txt', mode="r", newline="") as file:
            if user_level == "p":  # If the user is a patient
                count = 0  # Initialize appointment counter
                print()
                for line in file:
                    # Load each line as a JSON object
                    appointment_data = json.loads(line)
                    # Check if the patient's name matches the input name (case-insensitive)
                    if appointment_data["patientName"].strip().lower() == user["Name"].lower():
                        count += 1
                        # Print the appointment details
                        print(f"{count}. On " +
                              Fore.CYAN + f"{appointment_data['appointmentDate']} " +
                              Fore.RESET + "you have an appointment with " +
                              Fore.BLUE + f"Dr. {appointment_data['doctorName']}" + Style.RESET_ALL)
                if count == 0:  # If no appointments are found
                    print(Fore.LIGHTYELLOW_EX + "You have no scheduled appointments.\n" + Style.RESET_ALL)

            elif user_level == "d":  # If the user is a doctor
                count = 0  # Initialize appointment counter
                print()
                for line in file:
                    # Load each line as a JSON object
                    appointment_data = json.loads(line)
                    # Check if the doctor's name matches the input name (case-insensitive)
                    if appointment_data["doctorName"].strip().lower() == user["Name"].lower():
                        count += 1
                        # Print the appointment details
                        print(f"{count}. On " +
                              Fore.CYAN + f"{appointment_data['appointmentDate']} " +
                              Fore.RESET + "you have an appointment with " +
                              Fore.BLUE + f"{appointment_data['patientName']}" + Style.RESET_ALL)
                if count == 0:  # If no appointments are found
                    print(Fore.LIGHTYELLOW_EX+"No scheduled appointments.\n" +Style.RESET_ALL)

    except FileNotFoundError:
        # Handle the case where the AppointmentMaster.txt file is missing
        print("The Appointment file is missing. Please create it first.")
