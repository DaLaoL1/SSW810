from prettytable import PrettyTable
import os
from collections import defaultdict
import unittest

""" Student class stores courses for each student taken and corresponding grades"""


class Student:

    def __init__(self, CWID, name, major, dd=None):
        self.CWID = CWID
        self.name = name
        self.major = major
        if dd is None:
            self.dd = defaultdict(str)

    def add_course_grade(self, course, grade):
        self.dd[course] = grade

    def courses_taken(self):
        self.course_list = []
        for k, v in self.dd.items():
            self.course_list.append(k)
        # convert list to set in case of replicates
        return set(self.course_list)


""" Instructor class stores all instructors info, courses they taught and number of students in each course"""


class Instructor:

    def __init__(self, CWID, name, dpt, dd=None):
        self.CWID = CWID
        self.name = name
        self.dpt = dpt
        if dd is None:
            self.dd = defaultdict(int)

    def add_course_students(self, course):
        self.dd[course] += 1

    def courses_taught(self):
        self.courses_taught = []
        for k, v in self.dd.items():
            self.courses_taught.append(k)
        return set(self.courses_taught)

    def number_of_students(self, course_id):
        return self.dd[course_id]


""" Repository class stores all info about students and instructors and generates two summaries after reading all files"""


class Repository:
    def __init__(self, stu_list=None, ins_list=None):
        # temporarily uses two lists separatively to store students and instructors
        if stu_list is None:
            self.stu_list = []
        if ins_list is None:
            self.ins_list = []

    def read_stu(self, path):
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            print('File not found')
        else:
            for line in fp:
                stu_info = line.strip().split('\t')
                # skips the object with missing attributes
                if len(stu_info) != 3:
                    continue
                stu_cwid = stu_info[0]
                stu_name = stu_info[1]
                stu_major = stu_info[2]
                # adds a new student object to the list
                self.stu_list.append(Student(stu_cwid, stu_name, stu_major))
                stu_info = []

    def read_ins(self, path):
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            print('File not found')
        else:
            for line in fp:
                ins_info = line.strip().split('\t')
                # skips an instructor object with missing attributes
                if len(ins_info) != 3:
                    continue
                ins_cwid = ins_info[0]
                ins_name = ins_info[1]
                ins_dpt = ins_info[2]
                # adds a new instructor object into the list
                self.ins_list.append(Instructor(ins_cwid, ins_name, ins_dpt))
                ins_info = []

    def read_grade(self, path):
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            print('File Not Found')
        else:
            for line in fp:
                grade_info = line.strip().split('\t')
                # skips adding grade and course info to both objects if there is a missing attribute
                if len(grade_info) != 4:
                    continue
                stu_cwid = grade_info[0]
                course_id = grade_info[1]
                grade_letter = grade_info[2]
                ins_cwid = grade_info[3]
                for stu in self.stu_list:
                    if stu.CWID == stu_cwid:
                        stu.add_course_grade(course_id, grade_letter)
                for ins in self.ins_list:
                    if ins.CWID == ins_cwid:
                        ins.add_course_students(course_id)
                grade_info = []

    def create_student_summary(self):
        self.pt = PrettyTable(
            field_names=['CWID', 'Name', 'Completed Courses'])
        for stu in self.stu_list:
            # sorts each lists containing courses taken
            self.pt.add_row(
                [stu.CWID, stu.name, sorted(list(stu.courses_taken()))])
        print(self.pt)
        # returns pt for unittest
        return self.pt

    def create_instructor_summary(self):
        self.pt = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for ins in self.ins_list:
            for k, v in ins.dd.items():
                self.pt.add_row([ins.CWID, ins.name, ins.dpt, k, v])

        print(self.pt)
        return self.pt


# def main():
#     r1 = Repository()
#     r1.read_stu('./students.txt')
#     r1.read_ins('./instructors.txt')
#     r1.read_grade('./grades.txt')
#     # r1.create_student_summary()
#     r1.create_instructor_summary()


class Test_data(unittest.TestCase):
    def test_student(self):
        r1 = Repository()
        # uses relative path to read files
        r1.read_stu('./students.txt')
        r1.read_grade('./grades.txt')
        pt_stu = r1.create_student_summary()

        self.assertEqual(pt_stu._rows[0][0], '10103')
        self.assertEqual(pt_stu._rows[0][1], 'Baldwin, C')
        self.assertEqual(
            pt_stu._rows[0][2], ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'])

        self.assertEqual(pt_stu._rows[2][0], '10172')
        self.assertEqual(pt_stu._rows[2][1], 'Forbes, I')
        self.assertEqual(
            pt_stu._rows[2][2], ['SSW 555', 'SSW 567'])

    def test_instructor(self):
        r2 = Repository()
        r2.read_stu('./students.txt')
        r2.read_ins('./instructors.txt')
        r2.read_grade('./grades.txt')
        pt_ins = r2.create_instructor_summary()

        self.assertEqual(pt_ins._rows[0][0], '98765')
        self.assertEqual(pt_ins._rows[0][1], 'Einstein, A')
        self.assertEqual(pt_ins._rows[0][2], 'SFEN')
        self.assertEqual(pt_ins._rows[0][3], 'SSW 567')
        self.assertEqual(pt_ins._rows[0][4], 4)

        self.assertEqual(pt_ins._rows[6][0], '98763')
        self.assertEqual(pt_ins._rows[6][1], 'Newton, I')
        self.assertEqual(pt_ins._rows[6][2], 'SFEN')
        self.assertEqual(pt_ins._rows[6][3], 'SSW 555')
        self.assertEqual(pt_ins._rows[6][4], 1)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
