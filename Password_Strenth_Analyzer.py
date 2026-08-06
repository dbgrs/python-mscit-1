password = input("Enter a password: ")
uppercase = False
lowercase = False
digit = False
special = False
repeated = False
special_characters = "!@#$%^&*()-_=+[]{}|\\/:;'<>,.?"

for i in range(len(password)):
    char = password[i]
    if char.isupper():
        uppercase = True
    if char.islower():
        lowercase = True
    if char.isdigit():
        digit = True
    if char in special_characters:
        special = True

for i in range(len(password) - 1):
    if(password[i] == password[i + 1]):
        repeated = True
        break

print("Password Strength Analysis:")
print("Uppercase Letters: {uppercase}")
print("Lowercase Letters: {lowercase}")
print("Digits: {digit}")
print("Special Characters: {special}")
print("Repeated Characters: {repeated}")

if uppercase and lowercase and digit and special and not repeated:
    print("Your password is strong.")
else:
    print("Your password does not meet the strength requirements.")
