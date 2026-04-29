import streamlit as st

st.title("🏨 Hotel Booking Predictor")
st.write("Welcome to our Graduation Project App!")

# خانات إدخال البيانات (كمثال مبدئي)
lead_time = st.number_input("How many days before arrival?", min_value=0)
st.write(f"You entered: {lead_time} days")

if st.button("Predict"):
    st.success("App is working! Waiting for the SVM model...")
