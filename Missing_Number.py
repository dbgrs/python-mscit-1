total = int(input("Enter total number of student :"))

rollno = []
nof = []

for i in range(total):
    val=int(input())
    rollno.append(val)
    

maxval = max(rollno)


for i in range(1, maxval + 1):
    found = False
    
    for j in range(total):
        if i == rollno[j]:
            found = True
            break
        
    if not found:
        nof.append(i)
  
        
for l in nof:
    print("Missing roll number :", l)
