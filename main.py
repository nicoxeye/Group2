import csv
import os


def import_from_file(filename="students.csv"):
# TODO: Testing if it adds to issue.
    """
    Import students from a CSV file.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        list: List of student dictionaries.
    """
    students = []
    try:
        with open(filename, "r", newline="") as file:
            for line in file:
                cut_parts = line.strip().split(",")
                if len(cut_parts) == 2:
                    students.append(
                        {"first_name": cut_parts[0].strip(), "last_name": cut_parts[1].strip(), "present": False}
                    )
                elif len(cut_parts) == 3:
                    students.append(
                        {
                            "first_name": cut_parts[0].strip(),
                            "last_name": cut_parts[1].strip(),
                            "present": cut_parts[2].strip().lower() == "yes",
                        }
                    )
                else:
                    print("Skipping malformed line in the file.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    return students


def export_attendance(students, filename="students.csv"):
    """
    Export student attendance to a CSV file.

    Args:
        students (list): List of student dictionaries.
        filename (str): Path to the output CSV file.
    """
    with open(filename, 'w', newline='') as file:
        for student in students:
            present = 'yes' if student['present'] else 'no'
            file.write(f"{student['first_name']},{student['last_name']},{present}\n")


def add_student(first_name, last_name, filename="students.csv"):
    """
    Add a new student to the database.

    Args:
        first_name (str): Student's first name.
        last_name (str): Student's last name.
        filename (str): Path to the CSV file.
    """
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["first_name", "last_name", "present"])
        writer.writerow([first_name, last_name, False])

    print(f"Student {first_name} {last_name} was added to {filename}.")


def edit_student(
      old_first_name, old_last_name, new_first_name, new_last_name, filename="students.csv"):
    """
    Edit a student's information.

    Args:
        old_first_name (str): Old first name.
        old_last_name (str): Old last name.
        new_first_name (str): New first name.
        new_last_name (str): New last name.
        filename (str): Path to the CSV file.
    """
    students = []
    updated = False
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                    row["first_name"] == old_first_name
                    and row["last_name"] == old_last_name
                ):
                    row["first_name"] = new_first_name
                    row["last_name"] = new_last_name
                    updated = True
                students.append(row)
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["first_name", "last_name", "present"]
            )
            writer.writeheader()
            writer.writerows(students)
        if updated:
            print(
                f"Student: {old_first_name} {old_last_name} has been updated to {new_first_name} {new_last_name}."
            )

        else:
            print("The student hasn't been found.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")


def mark_attendance(students):
    """
    Check and update student attendance.

    Args:
        students (list): List of student dictionaries.
    """
    print("Checking attendance:")
    for student in students:
        status = "present" if student["present"] else "absent"
        print(f"{student['first_name']} {student['last_name']} is currently {status}.")
        new_status = input(
            f"Is {student['first_name']} {student['last_name']} present today? (yes/no): "
        ).strip().lower()
        if new_status == "yes":
            student["present"] = True

        elif new_status == "no":
            student["present"] = False

        else:
            print("Invalid input, please enter 'yes' or 'no'.")


def student_data():
    """
    Collect student data from user input.
    Returns:
        dict: A dictionary containing the student's first and last names.
    """
    while True:

        student_first_name = input("Enter student's first name: ").strip()
        student_last_name = input("Enter student's last name: ").strip()
        if student_first_name and student_last_name:
            return f"{student_first_name} {student_last_name}"
        print("Both first and last names are required. Please try again.")


def presence_function():
    """
    Ask the user if the student was present.

    Returns:
        bool: True if present, False if absent.
    """
    presence = input("Was the student present? (yes/no): ")
    if presence.lower() == 'yes':
        return 'PRESENT'  # Ensure this returns a string
    elif presence.lower() == 'no':
        return 'ABSENT'  # Ensure this returns a string
    else:
        print("Invalid output. Please try again. ")
        return presence_function()


def manage_attendance():
    """
    Manage attendance for multiple students.

    Returns:
        dict: A dictionary with student IDs as keys and their details as values.
    """
    attendance_dictionary = {}
    student_id = 1

    while True:
        student = student_data()
        attendance_status = presence_function()
        attendance_dictionary[student_id] = {
            "first_name": student["first_name"],
            "last_name": student["last_name"],
            "present": attendance_status
        }
        student_id += 1

        add_student = input("Want to add another student? (yes/no): ").strip().lower()
        if add_student != "yes":
            break

    save = input("Do you want to save the attendance list to a file? (yes/no): ").strip().lower()
    if save == "yes":
        students = list(attendance_dictionary.values())
        export_attendance(students)

    print("\nATTENDANCE LIST:")
    for s_id, details in attendance_dictionary.items():
        status = "Present" if details["present"] else "Absent"
        print(f"ID: {s_id}, Name: {details['first_name']} {details['last_name']}, Status: {status}")

    return attendance_dictionary


def edit_attendance(attendance_dictionary, student_id):
# TODO: Add tests to this function.
    """
    Edit the attendance status of a specific student.

    Args:
        attendance_dictionary (dict):
        The dictionary containing attendance data.
        student_id (int): The ID of the student to edit.

    Returns:
        dict: Updated attendance dictionary.
    """

    if student_id in attendance_dictionary:
        print(f"Editing attendance for: "
              f"{attendance_dictionary[student_id]['first_name']} "
              f"{attendance_dictionary[student_id]['last_name']}")
        new_attendance_status = presence_function()
        attendance_dictionary[student_id]["present"] = new_attendance_status
        print("Attendance updated successfully.")
    else:
        print("Student not found.")
    return attendance_dictionary


if __name__ == "__main__":
    students = import_from_file()
    while True:
        print("\nMENU:")
        print("1. Check attendance")
        print("2. Add student")
        print("3. Edit student")
        print("4. Export attendance")
        print("5. Exit")
        choice = input("Choose your option: ").strip()

        if choice == "1":
            mark_attendance(students)
        elif choice == "2":
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            add_student(first_name, last_name)
        elif choice == "3":
            old_fn = input("Enter old first name: ").strip()
            old_ln = input("Enter old last name: ").strip()
            new_fn = input("Enter new first name: ").strip()
            new_ln = input("Enter new last name: ").strip()
            edit_student(old_fn, old_ln, new_fn, new_ln)
        elif choice == "4":
            export_attendance(students)
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
