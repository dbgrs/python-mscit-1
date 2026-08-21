
def Get_Student_Details():
        print("Student Rank Processing Engine. \n")
      
        number_of_students = int(input("Enter The Number of Students: "))

        Student_Details = []

        number_of_subjects = 5

        for i in range(number_of_students):
        
            print("\n Enter Student Details")
            print("----------------------------------------")

            Roll_number = input("Enter Roll Number: ")
            Name = input("Enter Name: ")

            Marks = []

            Subjects = ["Data Structure", "Linux System Administration", "Python", "Networking", "Java"]

            for j in range(number_of_subjects):
                Mark = int(input(f"Enter Marks For {Subjects[j]}: "))
                if(Mark >= 0 and Mark <= 100):
                    Marks.append(Mark)
                else:
                    print("Entered Number of Marks is not valid.")


            Student = { "RollNo" : Roll_number, "Name" : Name, "Marks" : Marks, "Total" : 0, "Percentage" : 0, "Rank" : 0, "Grade" : ''}

            Student_Details.append(Student)      

        return Student_Details

