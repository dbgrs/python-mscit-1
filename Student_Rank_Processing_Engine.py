print("Student Rank Processing Engine")

nuber_of_student = int(input("Enter Number  of Students :"))

Student_Details = dict()

for i in range(nuber_of_student):
    Student_Details = { 'Roll No' : int(input("Enter Roll No")), 'Name of student' : str(input("Enter Name")), 'Marks' : list(input("Enter Marks")) }

print(Student_Details.items())

for key,value  in Student_Details.items():
        print(f"Key: {key}, value: {value}")

