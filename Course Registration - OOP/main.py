
from datetime import datetime

class Course:
    def __init__(self, code, day, start, end):
        self.code = code
        self.day = day
        self.start = start
        self.end = end

class Student:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)


students = []

try:
    n = int(input("Enter number of students: "))

    for i in range(n):
        print("\nEnter student details")

        sid = input("Enter student ID: ")
        name = input("Enter student name: ")

        s = Student(sid, name)

        total = int(input("Enter number of courses: "))

        for j in range(total):
            print("\nEnter course details")

            code = input("Enter course code: ")
            day = input("Enter day: ")
            start = input("Enter start time (HH:MM): ")
            end = input("Enter end time (HH:MM): ")

            t1 = datetime.strptime(start, "%H:%M")
            t2 = datetime.strptime(end, "%H:%M")

            if t1 >= t2:
                raise ValueError("End time must be after start time")

            c = Course(code, day, start, end)
            s.add_course(c)

        students.append(s)

    for s in students:
        print("\nStudent ID:", s.sid)
        print("Student Name:", s.name)
        print("Total courses:", len(s.courses))

        conflict = False

        for i in range(len(s.courses)):
            for j in range(i + 1, len(s.courses)):
                c1 = s.courses[i]
                c2 = s.courses[j]

                start1 = datetime.strptime(c1.start, "%H:%M")
                end1 = datetime.strptime(c1.end, "%H:%M")
                start2 = datetime.strptime(c2.start, "%H:%M")
                end2 = datetime.strptime(c2.end, "%H:%M")

                if c1.day.lower() == c2.day.lower():
                    if start1 < end2 and start2 < end1:
                        print("Conflict:", c1.code, "and", c2.code)
                        conflict = True

        if conflict == False:
            print("No conflicts found.")
            print("Student timetable:")

            for c in s.courses:
                print(c.code, c.day, c.start, "-", c.end)

except ValueError as e:
    print("Invalid input:", e)
