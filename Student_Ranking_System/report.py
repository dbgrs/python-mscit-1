
import csv
import os
from datetime import datetime


def write_report(Student_Details):

    folder_name = "report"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"Ranking_report_{current_time}.csv"

    file_path = os.path.join(folder_name, filename)

    with open(file_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Roll Number",
            "Name",
            "Data Structure",
            "Linux System Administration",
            "Python",
            "Networking",
            "Java",
            "Total",
            "Percentage",
            "Grade",
            "Rank"
        ])

        for Student in Student_Details:

            writer.writerow([
                Student["RollNo"],
                Student["Name"],
                Student["Marks"][0],
                Student["Marks"][1],
                Student["Marks"][2],
                Student["Marks"][3],
                Student["Marks"][4],
                Student["Total"],
                Student["Percentage"],
                Student["Grade"],
                Student["Rank"]
            ])

    print(f"\nReport generated successfully!")
    print(f"Report saved at: {file_path}")

    return file_path


def read_report(file_path):

    print("\nReading Ranking Report")
    print("-" * 150)

    with open(file_path, "r", newline="") as file:

        reader = csv.reader(file)

        header = next(reader)

        print("{:<12} {:<20} {:<18} {:<30} {:<10} {:<12} {:<8} {:<8} {:<12} {:<8} {:<6}".format(*header))

        print("-" * 150)

        for row in reader:
            print("{:<12} {:<20} {:<18} {:<30} {:<10} {:<12} {:<8} {:<8} {:<12} {:<8} {:<6}".format(*row))
