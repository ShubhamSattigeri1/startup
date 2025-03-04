# import streamlit as st
# st.title("Hello welcome to my new project here I have created an better alternative for the compounder at clinics of India")

# def form():
#     count = 0
#     name = st.text_input("Enter Your Name: ", key = "lavdya_name1")
#     count += 1
#     age = st.text_input("Enter Your Age: ", key = "bhadvya_age2")
#     count += 1
#     phone = st.text_input("Enter Your Phone Number: ", key = "uniqueee_phone3")
#     while len(phone) != 10 and phone:
#         st.error("Enter a valid mobile number (10 digits).")
#         st.stop()
#     count += 1
#     return count, name, age, phone
# def submit(count):
#     if st.button("Submit"):
#         if count == 3:
#             st.success("Form Submitted Successfully")
#         else:
#             st.error("Form Filled is incomplete")

# count = form()
# submit(count)  

# def display_info():
#     name, age, phone = form()
#     st.write("Here are the patients yet to arrive....")
#     st.write("Name: ", name)
#     st.write("Age: ", age)
#     st.write("Phone: ", phone)
import streamlit as st
st.title("Hello welcome to my new project here I have created an better alternative for the compounder at clinics of India")

def form():
    count = 0
    name = st.text_input("Enter Your Name: ", key="unique_name1")
    count += 1
    age = st.text_input("Enter Your Age: ", key="unique_age2")
    count += 1
    phone = st.text_input("Enter Your Phone Number: ", key="unique_phone3")
    while len(phone) != 10 and phone:
        st.error("Enter a valid mobile number (10 digits).")
        st.stop()
    count += 1
    return count, name, age, phone

def submit(count):
    if st.button("Submit"):
        if count == 3:
            st.success("Form Submitted Successfully")
        else:
            st.error("Form Filled is incomplete")

count, name, age, phone = form()
submit(count)

def display_info():
    st.write("Here are the patients yet to arrive....")
    st.write("Name: ", name)
    st.write("Age: ", age)
    st.write("Phone: ", phone)

