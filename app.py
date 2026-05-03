import streamlit as st
import pandas as pd
import joblib
import numpy as np
import sys
import sklearn.compose

# Patch for sklearn compatibility
if not hasattr(sklearn.compose._column_transformer, '_RemainderColsList'):
    class _RemainderColsList: pass
    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

def fix_adr(X):
    X = X.copy()
    if 'adr' in X.columns:
        X['adr'] = pd.to_numeric(X['adr'], errors='coerce').fillna(0)
        X['adr'] = X['adr'].apply(lambda x: 0 if x < 0 else x)
    return X

import __main__
__main__.fix_adr = fix_adr
sys.modules['__main__'].fix_adr = fix_adr

st.set_page_config(page_title="Hotel Booking Predictor", layout="wide")
st.title("Hotel Reservation Cancellation Predictor")

@st.cache_resource
def load_all_assets():
    return joblib.load('hotel_model_package.pkl')

try:
    data_pkg = load_all_assets()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    lead_time = st.number_input("Lead Time (Days)", min_value=0, value=30)
    market_segment = st.selectbox("Market Segment", ['Online TA', 'Offline TA/TO', 'Groups', 'Direct', 'Corporate'])
    deposit_type = st.selectbox("Deposit Type", ['No Deposit', 'Non Refund', 'Refundable'])

with col2:
    adr = st.number_input("Average Daily Rate (ADR)", min_value=0.0, value=120.0)
    customer_type = st.selectbox("Customer Type", ['Transient', 'Contract', 'Transient-Party', 'Group'])
    total_special_requests = st.slider("Special Requests", 0, 5, 1)

with col3:
    hotel = st.selectbox("Hotel Type", ["City Hotel", "Resort Hotel"])
    distribution_channel = st.selectbox("Distribution Channel", ['TA/TO', 'Direct', 'Corporate', 'GDS'])
    has_parking = st.selectbox("Required Parking?", ["No", "Yes"])

if st.button("Predict Cancellation Status", use_container_width=True):
    input_dict = {
        'lead_time': lead_time, 'adr': adr, 'total_of_special_requests': total_special_requests,
        'has_parking': 1 if has_parking == "Yes" else 0, 'market_segment': market_segment,
        'deposit_type': deposit_type, 'customer_type': customer_type, 'hotel': hotel,
        'distribution_channel': distribution_channel, 'company_cancel_rate': 0.15,
        'meal': 'BB', 'reserved_room_type': 'A', 'assigned_room_type': 'A',
        'arrival_date_month': 'July', 'arrival_date_year': 2017, 'arrival_date_week_number': 27,
        'arrival_date_day_of_month': 1, 'stays_in_weekend_nights': 0, 'stays_in_week_nights': 2,
        'adults': 2, 'children': 0, 'babies': 0, 'is_repeated_guest': 0,
        'previous_cancellations': 0, 'previous_bookings_not_canceled': 0,
        'booking_changes': 0, 'days_in_waiting_list': 0, 'required_car_parking_spaces': 0,
        'total_nights': 2, 'total_people': 2, 'room_changed': 0,
        'agent_cancel_rate': 0.2, 'country_cancel_rate': 0.2
    }
    
    input_df = pd.DataFrame([input_dict])
    
    for col in input_df.columns:
        if col in data_pkg['num_cols']:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
        else:
            input_df[col] = input_df[col].astype(object)

    try:
        processed = data_pkg['preprocessor'].transform(input_df)
        selected = processed[:, data_pkg['selected_mask']]
        compressed = data_pkg['pca'].transform(selected)
        prediction = data_pkg['model'].predict(compressed)
        
        if prediction[0] == 1:
            st.error("Prediction: CANCELED")
        else:
            st.success("Prediction: NOT CANCELED")
            
    except Exception as e:
        st.error(f"Error during prediction: {e}")