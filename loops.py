# # While Loop
#This is the syntax of while loop
i = 3
while i != 0:
    print(i,".")
i = i-1

#For loop   
for i in range(5):
    print(i+1,".Hello World...")

#short and simple loops
print("Meow\n" * 3, end="")

#Ask user to iterate meow
i = 0
n = int(input("Enter a valid Number : "))
while i<n:
    print(i+1,".Meow")
    i += 1

#same for for loop
n = int(input("Enter a Valid Number : "))    
for n in range(n):
    print(n+1,".Meow.")


def form():
    name = input("Enter Your Name : ")
    age = int(input("Enter Your age : "))
    branch = input("Enter Your Branch : ")
    nat = input("Enter Your Nationality : ")
    print(f"These are your Details \n1. Name : {name}\n2. Age : {age}\n3.branch : {branch}\n4.Nationality : {nat}")

print("These are few lines of som unwitten code.")
n = int(input("Enter a Valid Number : "))    
for n in range(n):
    print(n+1,".Meow.")
print("I have called a function here : ")    
form()

#Dictionary

students = {
    "Shubham" : "IT",
    "Gaurav": "AR",
    "Pratik" : "CS"
}
for student in students:
    print(students,students[student],sep = " ")

students = {
    "Shubham" : "IT",
    "Gaurav": "AR",
    "Pratik" : "CS"
}
for student in students:
    print(f"{student} : {students[student]}")


#is this shit updated or not....
