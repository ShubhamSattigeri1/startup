import random
import streamlit as st
sum = 2
st.title("Hello Ladies and Gentlemen Welcome to the stage of Startup...\n You are welcomed to our most enchanting event of the year particularly the E-Summit, Fill the Form Below to get Registered for the summit.")

name = st.text_input("Enter Your Name: ")
age = st.text_input("Enter Your Age: ")
current_year = st.text_input("Enter Your Current Year: ")

valid_years = ["1", "2", "3", "4"]
if current_year not in valid_years:
    st.error("Enter a valid year (1, 2, 3, or 4) that you have been to college.")
else:
    sum+=1
contact = st.text_input("Enter Your Contact Number: ")

if len(contact) != 10 and contact:
    st.error("Enter a valid mobile number (10 digits).")
else:
    sum += 1
course = st.text_input("Enter Your Branch Name: ")
code = random.randint(999, 10000)
feespaid = st.text_input("Have You Paid Fees: ")

if feespaid.lower() == "yes":
    st.write(f"Your special Code is: {code}")
elif feespaid.lower() == "no":
    st.write("Please Pay the Fees, it contributes a lot in life....")
else:
    st.write("Please enter 'yes' or 'no'.")
if st.button("Submit"):
    if sum == 4: 
        st.success("Hi")
else:
    st.error("The Details Filled are incomple or \n try presing Enter On each line of the form.")    
    print("erro2")