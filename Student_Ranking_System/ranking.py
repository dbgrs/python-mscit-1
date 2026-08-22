from student import Get_Student_Details

def Get_Ranking_Student(Student_Details):
    for Student in Student_Details:
        print("----------------------------------------")
        for key, value in Student.items():

            Student["Total"] = sum(Student["Marks"])
            Student["Percentage"] = Student["Total"] / 5

            percentage = Student["Percentage"]

            if(percentage >= 90 and percentage <= 100):
                Student["Grade"] = 'A'
            elif(percentage >= 80 and percentage < 90):
                Student["Grade"] = 'B'
            elif(percentage >= 70 and percentage < 80):
                Student["Grade"] = 'C'
            elif(percentage >= 60 and percentage < 70):
                Student["Grade"] = 'D'
            elif(percentage >= 50 and percentage < 60):
                Student["Grade"] = 'E'
            else:
                Student["Grade"] = 'F'

            Student_Details.sort(key=lambda student: student["Percentage"], reverse=True)

            rank = 0
            previous_percentage = None

            for student in Student_Details:

                current_percentage = student["Percentage"]

                if current_percentage != previous_percentage:
                    rank = rank + 1

                student["Rank"] = rank

                previous_percentage = current_percentage
    
    return Student_Details

    

def print_student_details(Student_Details):

    print("Student Details")

    for Student in Student_Details:
        
        print("----------------------------------------")

        for key, value in Student.items():
            print(f"{key}: {value}")

    return Student_Details
