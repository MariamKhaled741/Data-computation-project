import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Hotel Predictor", page_icon="🏨", layout="wide")

# السايد بار (القائمة الجانبية)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/a/a2/Alexandria_University_logo.png", width=100)
st.sidebar.title("Team Members")
st.sidebar.write("1. Mariam Khaled (Leader)")
st.sidebar.write("2. ... (Add other names)")

# محتوى الصفحة الرئيسي
st.title("🏨 Hotel Booking Cancellation Predictor")
st.markdown("---")
st.write("This app uses **SVM (Support Vector Machine)** to predict if a hotel booking will be canceled or not.")

# تنظيم المدخلات في أعمدة
col1, col2 = st.columns(2)

with col1:
    st.subheader("Booking Details")
    hotel = st.selectbox("Hotel Type", ["City Hotel", "Resort Hotel"])
    lead_time = st.number_input("Days before arrival (Lead Time)", min_value=0, value=10)
    adr = st.number_input("Price (ADR)", min_value=0.0, value=100.0)

with col2:
    st.subheader("Guest Requirements")
    deposit = st.selectbox("Deposit Type", ["No Deposit", "Non Refund", "Refundable"])
    special_requests = st.slider("Special Requests", 0, 5, 0)
    parking = st.radio("Car Parking Needed?", ["No", "Yes"])

st.markdown("---")
if st.button("Predict Now"):
    st.warning("Waiting for the final SVM model from the team...")

st.info("Faculty of Computers and Data Science - Alexandria University")
