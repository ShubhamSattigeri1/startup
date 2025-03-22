import streamlit as st
from back import form, submit

def display_info():
    if 'form_submitted' in st.session_state and st.session_state['form_submitted']:
        st.write("Here are the patients yet to arrive....")
        st.write("Name: ", st.session_state['name'])
        st.write("Age: ", st.session_state['age'])
        st.write("Phone: ", st.session_state['phone'])
    else:
        st.write("No information available. Please fill out the form first.")

# Main logic
if 'form_submitted' not in st.session_state:
    count, name, age, phone = form()
    submit(count)
else:
    display_info()