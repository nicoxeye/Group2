# Import necessary modules
import unittest
from unittest.mock import mock_open, patch

from main import (
    add_student,
    export_attendance,
    import_from_file,
    mark_attendance,
    presence_function,
    student_data,
)


class TestImport(unittest.TestCase):

    def test_import_with_valid_data(self):
        # Given
        mock_data = "John, Doe, yes\nJane, Smith, no"

        # When
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = import_from_file(mock_data)

        # Expected
        expected = [
            {'first_name': 'John', 'last_name': 'Doe', 'present': True},
            {'first_name': 'Jane', 'last_name': 'Smith', 'present': False}
        ]

        # Then
        self.assertEqual(result, expected)

    def test_import_without_present(self):  # automatic 'present' -> set to False if not given in the file
        # Given
        mock_data = "John, Doe\nJane, Smith"

        # When
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = import_from_file(mock_data)

        # Expected
        expected = [
            {'first_name': 'John', 'last_name': 'Doe', 'present': False},
            {'first_name': 'Jane', 'last_name': 'Smith', 'present': False}
        ]

        # Then
        self.assertEqual(result, expected)

    def test_import_with_empty_file(self):
        # Given
        mock_data = ""

        # When
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = import_from_file(mock_data)

        # Then
        self.assertEqual(result, [])

    def test_import_with_invalid_format(self):
        # Given
        mock_data = "John, Doe, yes, 19\nJane, Smith, no"

        # When
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = import_from_file("students.csv")

        # Expected
        expected = [
            {'first_name': 'Jane', 'last_name': 'Smith', 'present': False}
        ]

        # Then
        self.assertEqual(result, expected)

    def test_import_with_missing_file(self):
        # Given - no mock since the file doesn't exist

        # When
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = import_from_file("students.csv")

        # Then
        self.assertEqual(result, [])


class TestExport(unittest.TestCase):
    """
    students = [{'first_name': 'John', 'last_name': 'Doe', 'present': True},
    {'first_name': 'Jane', 'last_name': 'Smith', 'present': False}]

    file will contain:
    John,Doe,yes
    Jane,Smith,no
    """
    def test_export_attendance(self):
        # Given - a list of students
        mock_students_data = [{'first_name': 'John', 'last_name': 'Doe', 'present': True},
                              {'first_name': 'Jane', 'last_name': 'Smith', 'present': False}]

        # Expected
        expected = "John,Doe,yes\nJane,Smith,no\n"

        with patch("builtins.open", mock_open()) as mocked_open:
            # When
            export_attendance(mock_students_data, "students.csv")

            file_handle = mocked_open()

            actual_content = "".join(call.args[0] for call in file_handle.write.call_args_list)

            # Then
            self.assertEqual(actual_content, expected)


class TestAddStudent(unittest.TestCase):
    def test_add_student_to_existing_file(self):
        # Given - mock data
        first_name = "John"
        last_name = "Doe"
        filename = "students.csv"
        mock_data = "first_name,last_name,present\n"

        # When
        with patch("builtins.open", mock_open(read_data=mock_data)) as mocked_file:
            add_student(first_name, last_name, filename)

            # Then
            mocked_file.assert_called_once_with(filename, 'a', newline='')
            file_handle = mocked_file()
            file_handle.write.assert_called_with("John,Doe,False\r\n")  # carriage return /r for Windows


class TestMarkAttendance(unittest.TestCase):
    def test_mark_attendance_present(self):
        # Given -> a list of students with no attendance recorded
        students = [
            {"first_name": "John", "last_name": "Doe", "present": None},
            {"first_name": "Jane", "last_name": "Smith", "present": None}
        ]

        # When -> mock input to simulate user input of "yes"
        with patch("builtins.input", side_effect=["yes", "yes"]):
            mark_attendance(students)

        # Then
        self.assertTrue(students[0]["present"])  # should be marked as present for both
        self.assertTrue(students[1]["present"])

    def test_attendance_mark_absent(self):
        # Given
        students = [
            {"first_name": "John", "last_name": "Doe", "present": None},
            {"first_name": "Jane", "last_name": "Smith", "present": None}
        ]

        # When -> mock input to simulate user input of "no"
        with patch("builtins.input", side_effect=["no", "no"]):
            mark_attendance(students)

        # Then
        self.assertFalse(students[0]["present"])  # should be marked as absent for both
        self.assertFalse(students[1]["present"])


class TestStudentData(unittest.TestCase):
    def test_student_data(self):
        # Given
        first_name = "John"
        last_name = "Doe"

        # When
        with patch('builtins.input', side_effect=[first_name, last_name]):
            result = student_data()

        # Then
        self.assertEqual(result, "John Doe")


class TestPresenceFunction(unittest.TestCase):
    def test_presence_yes(self):
        with patch('builtins.input', return_value='yes'):
            result = presence_function()
            self.assertEqual(result, 'PRESENT')

    def test_presence_no(self):
        with patch('builtins.input', return_value='no'):
            result = presence_function()
            self.assertEqual(result, 'ABSENT')

    def test_presence_invalid(self):
        with patch('builtins.input', side_effect=['maybe', 'yes']):
            result = presence_function()
            self.assertEqual(result, 'PRESENT')

    def test_presence_invalid_followed_by_no(self):
        with patch('builtins.input', side_effect=['maybe', 'no']):
            result = presence_function()
            self.assertEqual(result, 'ABSENT')


if __name__ == "__main__":
    unittest.main()
