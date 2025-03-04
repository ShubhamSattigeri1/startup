import streamlit as st
from back import display_info, form
#st.write("Here are the patients yet to arrive....")
def display_info():
    name, age, phone = form()
    st.write("Here are the patients yet to arrive....")
    st.write("Name: ", name)
    st.write("Age: ", age)
    st.write("Phone: ", phone)

display_info()