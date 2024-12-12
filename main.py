import os
import csv

#IMPORT
def import_from_file(filename="students.csv"):
    students = []
    try:
        with open(filename, 'r', newline='') as file: #'r' read file, newline='' to manage newline characters correctly in CSV files
            for line in file:
                cut_parts = line.strip().split(',') #delete whitespaces and create a seperator as ,
                #in the file: first name, last name
                if len(cut_parts) == 2:  #no attendance provided
                    students.append({
                        'first_name': cut_parts[0].strip(),
                        'last_name': cut_parts[1].strip(),
                        'present': False  #default to False
                    })
                elif len(cut_parts) == 3:  #attendance provided
                    students.append({
                        'first_name': cut_parts[0].strip(),
                        'last_name': cut_parts[1].strip(),
                        'present': cut_parts[2].strip().lower() == 'yes'  #convert to boolean, 'yes' == True
                    })
                else: print('Something went wrong when importing the file.')
        return students
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.") #added if filenotfound exception

#EXPORT

def export_attendance(students, filename="students.csv"):
     with open(filename, 'w', newline='') as file: #'w' write file
        for student in students:
            present = 'yes' if student['present'] else 'no'
            file.write(f"{student['first_name']},{student['last_name']},{present}\n")

            
#ADDING NEW STUDENTS AND UPDATING DATABASE

# function that adds new student to the list and saves it to the file
def add_student(first_name, last_name, filename="students.csv"):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["first_name", "last_name", "present"])
        
        # "present" is false by default
        writer.writerow([first_name, last_name, False])
    print(f"Student {first_name} {last_name} was added to {filename}.")


# function that edits student list
def edit_student(old_first_name, old_last_name, new_first_name, new_last_name, filename="students.csv"):
    students = []
    updated = False

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["first_name"] == old_first_name and row["last_name"] == old_last_name:
                row["first_name"] = new_first_name
                row["last_name"] = new_last_name
                updated = True
            students.append(row)
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["first_name", "last_name", "present"])
        writer.writeheader()
        writer.writerows(students)
    
    if updated:
        print(f"Student: {old_first_name} {old_last_name} has been updated to {new_first_name} {new_last_name}.")
    else:
        print("The student hasn't been found")

            
#TESTING
#if __name__ == "__main__": #
    #students = import_from_file('C:\\Users\\PC\\Downloads\\attendance.csv')
    #add_student("John", "Doe")
    #edit_student("John", "Doe", "Jane", "Doe")
    #export_attendance(students, 'C:\\Users\\PC\\Downloads\\attendance.csv')

# CHECKING ATTENDANCE

def mark_attenfance(students):
    print("Checking attendance: ")
    for student in students:  

        # display current attendance status
        if student['present'] is None: #if there's no previous attendance recorded
            print(f"{student['first_name']} {student['last_name']} has not had their attendance recorded yet.")
        else:
            status = "present" if student['present'] else "absent"
            print(f"{student['first_name']} {student['last_name']} is currently {status}")
        
        # ask user for attendance status
        new_status = input(f"Is {student['first_name']} {student['last_name']} present today? (yes/no): ").strip().lower()

        # update attendance based on user input
        if new_status == "yes":
            student['present'] = True # Mark as present
        elif new_status == "no":
            student['present'] = False # Mark as absent
        else: 
            print("Invalid input, please enter 'yes' or 'no'.")

#MANAGING STUDENT'S DATA:
def student_data():
 student_firstName = input('Enter students first name: ')
 student_lastName = input('Enter students last name: ')
 return f"{student_firstName} {student_lastName}"

def presence_function():
    presence = input("Was the student present? (yes/no): ")
    if (presence.lower() == 'yes'):
        return 'PRESENT'
    elif (presence.lower() == 'no'):
        return 'ABSENT'
    else:
      print("Invalid output. Please try again. ")
      return presence_function()

# CREATING 'ATTENDANCE_DICTIONARY' AND CREATING 'STUDENTS' LIST - a list where every element is a dictionary
def manage_attendance():
  attendance_dictionary = {}
  student_id = 1
  while True:
   student = student_data()
   attendance_status = presence_function()
   attendance_dictionary[student_id] = [student, attendance_status]
   student_id += 1

   add_student = input("Want to add another student? (yes/no):")
   print()
   if add_student.lower() != 'yes':
     break

  #EXPORT to .csv file (integration with export_attendance())
  students = [
    {
        "first_name": s.split(' ')[0],
        "last_name": s.split(' ')[1],
        "present": a == "PRESENT"
    }
    for s_id, (s, a) in attendance_dictionary.items()
  ]

  export_attendance(students)

  #printing students' list:
  print("ATTENDANCE LIST:")
  for s_id, (student, status) in attendance_dictionary.items():
    print(f"STUDENT ID: {s_id}, NAME: {student}, ATTENDANCE STATUS: {status}")
  print()
  return attendance_dictionary

# EDITING STUDENT'S ATTENDANCE STATUS
def edit_attendance(attendance_dictionary, student_id):
  if student_id in attendance_dictionary:
    new_attendance_status = presence_function()
    attendance_dictionary[student_id][1] = new_attendance_status
  else:
    print("Student not found")
  return attendance_dictionary
  
#MENU
if __name__ == "__main__":
  attendance = {}
  students = []
  while True:
   print("MENU:")
   print("1. Manage attendance")
   print("2. Edit attendance")
   print("3. Import students")
   print("4. Export attendance")
   print("5. Exit")
   choice = input("Choose your option: ")


   if choice == "1":
      attendance = manage_attendance()
   elif choice == "2":
      student_id = int(input("Enter student ID: "))
      edit_attendance(attendance, student_id)
      print("Updated attendance: ", attendance)
   elif choice == "3":
      students = import_from_file()
      print("Imported students: ", students)
   elif choice == "4":
      export_attendance(students)
   elif choice == "5":
      print("Exiting the program.")
      break
   else:
      print("Invalid choice. Please try again.")