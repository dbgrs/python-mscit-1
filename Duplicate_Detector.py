
number = int(input("Enter size  of list : "))
duplicate = []


for i in range(number):
    val=int(input())
    duplicate.append(val)

print("Consecutive Number1")
for i in range(number-1):
    if duplicate[i] == duplicate[i+1]:
        print(duplicate[i])



