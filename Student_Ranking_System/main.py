from student import Get_Student_Details
from ranking import Get_Ranking_Student, print_student_details
from report import write_report, read_report


Student_Details = Get_Student_Details()

Student_Details = Get_Ranking_Student(Student_Details)

#print_student_details(Student_Details)

report_file = write_report(Student_Details)

read_report(report_file)
