"""
# PROG 1700 Final Project
# Dasil Adam, W0509891
# Olivia MacEachern, W0429875
# Jayden Graham, W0517691

This program is a clinic file management system. It allows staff (administrators and doctors)
and patients to manage clinic records such as viewing and editing patient information,
scheduling appointments, and viewing doctor details. The program provides different menus
and functionalities depending on the user role.
"""

# Importing required libraries
import msvcrt  # Used to block program termination until a key is pressed
from difflib import Match

from colorama import Fore, Style  # Used for colored console output

# Importing custom modules for managing appointments, doctors, and patients
import AppointmentFunctions as af
import DoctorFunctions as df
import PatientFunctions as pf

def main():
    """
    Main entry point of the program.
    This function handles the initial user role selection and routes the user
    to the appropriate menus based on their role (patient or staff).
    """
    print("Welcome to the clinic file management program.")

    while True:
        try:
            # Prompt user to select their role
            user_level = input("Are you a (S)taff member or a (P)atient?\n(E to exit)\n").lower()

            # Ensure valid input
            if user_level not in ('s', 'p', 'e'):
                raise ValueError("Invalid Choice")  # Raise an error for invalid input
            elif user_level == 'e':
                # Exit the program if the user selects 'E'
                print("Exiting...")
                break
            else:
                break
        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL, "\n")


    match user_level:
        # ------------------------- Patient Workflow ------------------------- #
        case "patient" | "p":
            """
            Handle operations for patients:
            - Search for existing patient records
            - Create a new patient record if none exists
            - Manage or view appointments
            """
            # Collect patient name
            patient_fname = input("Please enter your first name:\n").title().strip()
            patient_lname = input("Please enter your last name:\n").title().strip()

            # Check if the patient exists in the records
            if not pf.patient_search(patient_fname, patient_lname):
                # If patient not found, create a new patient record
                print("Patient not found. Creating a new record...")
                pf.create_patient(patient_fname, patient_lname)
                patient_details = pf.get_patient(patient_fname, patient_lname)

            else:
                # Retrieve and validate patient details if found
                while True:
                    try:
                        # Prompt for patient ID and validate input
                        patient_id = int(input("Please enter your ID Number:\n").strip())
                    except ValueError:
                        print(Fore.RED + "Invalid input, please enter a number\n" + Style.RESET_ALL)
                    else:
                        # Fetch patient details using ID
                        patient_details = pf.get_patient(patient_fname, patient_lname, patient_id)

                        # If no match, retry
                        if patient_details == -1:
                            continue
                        else:
                            break

            print(Fore.GREEN + f"\nWelcome {patient_details['Name']}\n" + Style.RESET_ALL)

            while True:
                print("1- View your information\n" +
                      "2- Create or View Appointments\n" +
                      "3- Exit the program\n")
                try:
                    # Get the patient's menu choice
                    pmc = int(input("Please select an option\n"))

                    match pmc:
                        case 1:
                            # View and display patient information
                            pf.view_patient(patient_details)
                        case 2:
                            # Manage appointments (view existing or schedule new ones)
                            af.search_appointments(patient_details, "p")
                            new_appt = input(
                                "\nWould you like to make a new appointment? (Y/N)\n").lower()
                            if new_appt == "y":
                                af.appointment_menu(patient_details, "p")
                        case 3:
                            # Exit the program
                            print("Now exiting program.")
                            msvcrt.getch()  # Wait for key press before closing
                            break
                        case _:
                            # Handle invalid menu choices
                            raise ValueError
                except ValueError:
                    print(
                        Fore.RED + "Invalid input. Please select an option from 1-3.\n" + Style.RESET_ALL)

        # ------------------------- Staff Workflow ------------------------- #
        case "staff" | "s":
            """
            Handle operations for staff members:
            - Admins: Manage doctors, patients, and view/edit records
            - Doctors: View and manage their own details and appointments
            """
            # Prompt for staff type (admin or doctor)
            staff_lvl = input("(A)dmin or (D)octor?\n").lower()

            # Admin Menu
            if staff_lvl == "a" or staff_lvl == "admin":
                while True:
                    # Display admin menu options
                    print("...............Admin Menu................\n" +
                          "1. Add Doctor\n" +
                          "2. Add Patient\n" +
                          "3. View all Patients\n" +
                          "4. Search Patient\n" +
                          "5. View Doctor\n" +
                          "6. View All Doctors\n" +
                          "7. Exit\n")
                    try:
                        # Get the admin's menu choice
                        amc = int(input("Select menu option:\n"))

                        match amc:
                            case 1:
                                # Add a new doctor record
                                df.create_doctor()
                            case 2:
                                # Add a new patient record
                                pf.create_patient()

                            case 3:
                                #Displays all patients
                                pf.view_patient_all()

                            case 4:
                                # searches for individual patients
                                while True:
                                    patient_fname = input("Patient first name? \n").title().strip()
                                    patient_lname = input("Patient last name?\n").title().strip()

                                # Fetch patient details by ID
                                    try:
                                        patient_id = int(input("Please enter Patient ID Number:\n").strip())
                                    except ValueError:
                                        print(Fore.RED + "Please enter a valid ID!\n" + Style.RESET_ALL)
                                        continue
                                    patient_details = pf.get_patient(patient_fname, patient_lname, patient_id)
                                    if patient_details != -1:
                                        break
                                while True:
                                    pf.view_patient(patient_details)

                                    # If patient details are invalid, return to admin menu
                                    if patient_details is None:
                                        break
                                    else:
                                        try:
                                            # Provide options for managing the patient's appointments
                                            patient_submenu = int(input("Patient menu\n" +
                                                                        "1. Create or manage an appointment\n" +
                                                                        "2. Exit patient view\n"))
                                            match patient_submenu:
                                                case 1:
                                                    # Search for and schedule appointments
                                                    af.search_appointments(patient_details, "p")
                                                    while True:
                                                        try:
                                                            appt_choice = int(
                                                                input("\n1. Schedule a new appointment\n" +
                                                                      "2. Go Back\n"))
                                                            match appt_choice:
                                                                case 1:
                                                                    af.appointment_menu(patient_details, "p")
                                                                case 2:
                                                                    break
                                                                case _:
                                                                    raise ValueError
                                                        except ValueError:
                                                            print(
                                                                Fore.RED + "Invalid input. Please select an option from 1-2.\n" + Style.RESET_ALL)
                                                case 2:
                                                    # Return to admin menu
                                                    break
                                                case _:
                                                    raise ValueError
                                        except ValueError:
                                            print(
                                                Fore.RED + "Invalid input. Please select an option from 1-2.\n" + Style.RESET_ALL)
                            case 5:
                                # View doctor details
                                while True:
                                    doctor_id = int(input("Enter the doctor's ID: "))
                                    doctor = df.get_doctor_by_id(doctor_id)
                                    if doctor != -1:
                                        df.view_doctor(doctor)
                                        df.doctor_submenu(doctor)
                                        break


                            case 6:
                                # Displays all doctors
                                df.view_doctor_all()

                            case 7:
                                # Exit admin menu
                                print("Exiting Admin Menu...")
                                break
                            case _:
                                raise ValueError
                    except ValueError:
                        print(Fore.RED + "Invalid input. Please select an option from 1-5.\n" + Style.RESET_ALL)

            # Doctor Menu
            elif staff_lvl == "d" or staff_lvl == "doctor":
                failed_attempts = 0

                while True:
                    try:
                        docname = input("Doctor name?\n").title().strip()
                        if df.search_doctor(docname) > 0:
                            doc_id = int(input("Enter your ID: "))
                            if df.check_id(docname, doc_id):
                                doctor = df.get_doctor(doc_id, docname)
                                if doctor != -1:
                                    print("Access granted\n")
                                    # Display doctor details and submenu
                                    df.view_doctor(doctor)
                                    df.doctor_submenu(doctor)
                                    break
                            else:
                                failed_attempts += 1 # Failed attempts + 1
                                print("Invalid Details, try again\n")
                                if failed_attempts > 2:  # Maximun number of tries
                                    print(Fore.RED + "Please contact an administrator for help" + Style.RESET_ALL)
                                    break  # Ends program


                        else:
                            # Increment failed attempts and warn the user
                            failed_attempts += 1
                            if failed_attempts > 2: # Maximun number of tries
                                print(Fore.RED + "Please contact an administrator for help" + Style.RESET_ALL)
                                break # Ends program
                    except ValueError:
                        print(Fore.YELLOW + "\nPlease enter a Valid ID" + Style.RESET_ALL)
                    except UnboundLocalError as e:
                        print(e)




if __name__ == "__main__":
    # Execute the main program
    main()
