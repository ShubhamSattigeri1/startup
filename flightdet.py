import streamlit as st
airports = ["JFK - John F. Kennedy International Airport", 
            "LAX - Los Angeles International Airport", 
            "ORD - O'Hare International Airport", 
            "ATL - Hartsfield-Jackson Atlanta International Airport", 
            "DFW - Dallas/Fort Worth International Airport"]

st.write("Hello Passenger")
# List of available airports (example list, you can expand it)
fm = st.selectbox("Enter Departure airport:", airports, key = "1")
to = st.selectbox("Enter Destination airport:", airports, key = "2")
pho = st.text_input("Enter Phone number:", key = "3")
kg = st.text_input("Enter Weight of luggage left (kg):", key = "4")

if fm == to:
    st.error("Departure and Destination airports cannot be the same")
else:
    st.write("Your flight is from", fm, "to", to, ".")
    st.write("You will receive a text message at", pho, ".")
    st.write("Please make sure your luggage is under", kg, "kg.")
    st.write("Have a safe flight!")