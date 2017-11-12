from prettytable import PrettyTable
import os
from collections import defaultdict
import unittest

""" Student class stores courses for each student taken and corresponding grades"""


class Student:

    def __init__(self, CWID, name, major, dd=None, remain_courses=None, ele_courses=None, req_courses=None):
        self.CWID = CWID
        self.name = name
        self.major = major
        if dd is None:
            self.dd = defaultdict(str)
        # restores remain courses for each student
        if remain_courses is None:
            self.remain_courses = []
        # restores all elective courses
        if ele_courses is None:
            self.ele_courses = []
        # restores all required courses
        if req_courses is None:
            self.req_courses = []

    def add_course_grade(self, course, grade):
        self.dd[course] = grade

    def courses_taken(self):
        self.valid_course_taken = []
        # add courses those are better than 'C'
        for course in self.dd.keys():
            if self.dd[course] <= 'C':
                self.valid_course_taken.append(course)

        return set(self.valid_course_taken)

    def add_req_courses(self, course_id):
        self.req_courses.append(course_id)

    def add_remain_required_course(self, course_id):
        # check the current course is taken or not
        if course_id in self.dd.keys() and self.dd[course_id] >= 'C' or course_id not in self.dd.keys():
            self.remain_courses.append(course_id)

    def get_remain_required_course(self):
        return set(self.remain_courses)

    def add_ele_course(self, course_id):
        self.ele_courses.append(course_id)

    def get_remain_elective_courses(self):
        # check if the current student has taken at least one elective
        for elec in self.ele_courses:
            if elec in list(self.courses_taken()):
                return []
        return self.ele_courses


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

        return set(self.dd.keys())

    def number_of_students(self, course_id):
        return self.dd[course_id]


""" Repository class stores all info about students and instructors and generates two summaries after reading all files"""


class Repository:
    def __init__(self, stu_dict=None, ins_dict=None):
        # temporarily uses two lists separatively to store students and instructors
        if stu_dict is None:
            self.stu_dict = defaultdict(Student)
        if ins_dict is None:
            self.ins_dict = defaultdict(Instructor)

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
                self.stu_dict[stu_cwid] = Student(
                    stu_cwid, stu_name, stu_major)
                # self.stu_list.append(Student(stu_cwid, stu_name, stu_major))
                stu_info = []
            fp.close()

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
                self.ins_dict[ins_cwid] = Instructor(
                    ins_cwid, ins_name, ins_dpt)
                # self.ins_list.append(Instructor(ins_cwid, ins_name, ins_dpt))
                ins_info = []
            fp.close()

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
                self.stu_dict[stu_cwid].add_course_grade(
                    course_id, grade_letter)

                self.ins_dict[ins_cwid].add_course_students(course_id)

                grade_info = []
            fp.close()

    def read_majors(self, path):
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            print('File Not Found')
        else:
            for line in fp:
                major_info = line.strip().split('\t')
                major = major_info[0]
                reqOrEle = major_info[1]
                course_id = major_info[2]
                for stu in self.stu_dict.values():
                    if stu.major == major and reqOrEle == 'R':
                        stu.add_req_courses(course_id)
                        stu.add_remain_required_course(course_id)
                    if stu.major == major and reqOrEle == 'E':
                        stu.add_ele_course(course_id)
                major_info = []
            fp.close()

    def create_student_summary(self):
        self.pt = PrettyTable(
            field_names=['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for cwid in self.stu_dict.keys():
            # sorts each lists containing courses taken
            self.course_taken = sorted(
                list(self.stu_dict[cwid].courses_taken()))
            self.remain_required_courses = sorted(
                list(self.stu_dict[cwid].get_remain_required_course()))
            self.remain_elective_courses = sorted(
                list(self.stu_dict[cwid].get_remain_elective_courses()))
            self.pt.add_row(
                [cwid, self.stu_dict[cwid].name, self.course_taken, self.remain_required_courses, self.remain_elective_courses])
        print(self.pt)
        # returns pt for unittest
        return self.pt

    def create_major_summary(self):
        try:
            fp = open('./majors.txt', 'r')
        except FileNotFoundError:
            print('File Not Found')
        else:
            majors = []
            for line in fp:
                major_info = line.strip().split('\t')
                major = major_info[0]
                majors.append(major)
            # removing duplicate majors using set
            majors = list(set(majors))
            self.pt = PrettyTable(
                field_names=['Dept', 'Required', 'Electives'])
            for major in majors:
                for stu in self.stu_dict.values():
                    if stu.major == major:
                        self.required_courses = stu.req_courses
                        self.electives = stu.ele_courses
                        self.pt.add_row(
                            [major, sorted(self.required_courses), sorted(self.electives)])
                        break
            fp.close()
            print(self.pt)
            return self.pt

    def create_instructor_summary(self):
        self.pt = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for cwid in self.ins_dict.keys():
            for k, v in self.ins_dict[cwid].dd.items():
                self.pt.add_row([cwid, self.ins_dict[cwid].name,
                                 self.ins_dict[cwid].dpt, k, v])

        print(self.pt)
        return self.pt


# def main():
#     r1 = Repository()
#     r1.read_stu('./students.txt')
#     r1.read_ins('./instructors.txt')
#     r1.read_grade('./grades.txt')
#     r1.read_majors('./majors.txt')
#     r1.create_major_summary()
    # r1.create_student_summary()
    # r1.create_instructor_summary()


class Test_data(unittest.TestCase):
    def test_majors(self):
        r1 = Repository()
        r1.read_stu('./students.txt')
        r1.read_ins('./instructors.txt')
        r1.read_grade('./grades.txt')
        r1.read_majors('./majors.txt')
        pt_major = r1.create_major_summary()
        # value in set are unordered
        if pt_major._rows[0][0] == 'SFEN':
            self.assertEqual(pt_major._rows[0][0], 'SFEN')
            self.assertEqual(pt_major._rows[0][1], [
                'SSW 533', 'SSW 540', 'SSW 555', 'SSW 564', 'SSW 565', 'SSW 567', 'SSW 690', 'SSW 695'])
            self.assertEqual(pt_major._rows[0][2], [
                             'CS 501', 'CS 513', 'CS 545'])
        else:
            self.assertEqual(pt_major._rows[0][0], 'SYEN')
            self.assertEqual(pt_major._rows[0][1], [
                'SYS 612', 'SYS 671', 'SYS 672', 'SYS 673', 'SYS 674', 'SYS 800'])
            self.assertEqual(pt_major._rows[0][2], [
                'SSW 540', 'SSW 565', 'SSW 810'])

    def test_stu(self):
        r1 = Repository()
        r1.read_stu('./students.txt')
        r1.read_ins('./instructors.txt')
        r1.read_grade('./grades.txt')
        r1.read_majors('./majors.txt')
        pt_stu = r1.create_student_summary()
        self.assertEqual(pt_stu._rows[7][0], '11658')
        self.assertEqual(pt_stu._rows[7][1], 'Kelly, P')
        self.assertEqual(pt_stu._rows[7][2], [])
        self.assertEqual(pt_stu._rows[7][3], [
                         'SYS 612', 'SYS 671', 'SYS 672', 'SYS 673', 'SYS 674', 'SYS 800'])
        self.assertEqual(pt_stu._rows[7][4], ['SSW 540', 'SSW 565', 'SSW 810'])

        self.assertEqual(pt_stu._rows[5][0], '11399')
        self.assertEqual(pt_stu._rows[5][1], 'Cordova, I')
        self.assertEqual(pt_stu._rows[5][2], ['SSW 540'])
        self.assertEqual(pt_stu._rows[5][3], [
                         'SYS 612', 'SYS 671', 'SYS 672', 'SYS 673', 'SYS 674', 'SYS 800'])
        self.assertEqual(pt_stu._rows[5][4], [])

    def test_instructor(self):
        r2 = Repository()
        r2.read_stu('./students.txt')
        r2.read_ins('./instructors.txt')
        r2.read_grade('./grades.txt')
        r2.read_majors('./majors.txt')
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
    # main()
