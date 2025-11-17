# app.py
import streamlit as st
import pandas as pd
import joblib
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Astro-Classifier RF",
    page_icon="🚀",
    layout="wide"
)

MODEL_PATH = 'results/models/rf_pha_classifier.joblib'
CNEOS_API_URL = "https://ssd-api.jpl.nasa.gov/cad.api"


# --- Helper Functions ---

@st.cache_data
def load_model(path):
    """Loads the pre-trained RF model."""
    try:
        model = joblib.load(path)
        return model
    except FileNotFoundError:
        st.error(f"Error: Model file '{path}' not found.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

@st.cache_data
def fetch_close_approaches():
    """Fetches upcoming close-approach data from NASA's CNEOS API."""
    try:
        params = {
            'date-min': 'now',
            'date-max': '+60',
            'dist-max': '0.05',
            'sort': 'date'
        }
        response = requests.get(CNEOS_API_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if data['count'] == '0':
            return pd.DataFrame(columns=['Object', 'Close-Approach Date', 'Distance (km)', 'Lunar Dist.', 'Size (m)', 'datetime'])

        df = pd.DataFrame(data['data'], columns=data['fields'])

        df_cleaned = df[['des', 'cd', 'dist', 'h']]
        df_cleaned.columns = ['Object', 'Close-Approach Date', 'Distance (AU)', 'H']

        df_cleaned['H'] = pd.to_numeric(df_cleaned['H'])
        df_cleaned['Distance (AU)'] = pd.to_numeric(df_cleaned['Distance (AU)'])

        df_cleaned['Size (m)'] = 10**( (27.8 - df_cleaned['H']) / 5 )

        AU_TO_KM = 149597870.7
        AU_TO_LD = 389.0
        df_cleaned['Distance (km)'] = (df_cleaned['Distance (AU)'] * AU_TO_KM).round(0)
        df_cleaned['Lunar Dist.'] = (df_cleaned['Distance (AU)'] * AU_TO_LD).round(1)

        df_cleaned['datetime'] = pd.to_datetime(df_cleaned['Close-Approach Date'])
        df_cleaned['Close-Approach Date'] = df_cleaned['datetime'].dt.strftime('%Y-%m-%d %H:%M')

        df_final = df_cleaned[['Object', 'Close-Approach Date', 'Distance (km)', 'Lunar Dist.', 'Size (m)', 'datetime']].sort_values(by='datetime')
        return df_final

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to NASA CNEOS API: {e}")
        return None
    except Exception as e:
        st.error(f"Error processing CNEOS data: {e}")
        return None

st.title("🚀 Astro-Classifier RF & Threat Monitor")
st.markdown("An app combining a Machine Learning model for **risk classification** and a live data monitor from **NASA**.")

# load model
model = load_model(MODEL_PATH)

tab1, tab2 = st.tabs(["🛰️ Threat Monitor (Live NASA API)", "🔬 Risk Simulator (Our AI Model)"])

with tab1:
    st.header("Upcoming Close Approaches (Next 60 Days)")
    st.markdown("This data is from NASA's [CNEOS 'Close Approach' API](https://ssd-api.jpl.nasa.gov/doc/cad.html). It lists known objects passing within 0.05 AU (approx. 7.5 million km) of Earth.")

    if st.button('Refresh NASA Data'):
        st.cache_data.clear()

    ca_data = fetch_close_approaches()

    if ca_data is not None and not ca_data.empty:

        st.dataframe(ca_data.drop(columns=['datetime']), use_container_width=True, hide_index=True)

        st.subheader("Approach Visualization")

        st.line_chart(ca_data, x='datetime', y='Lunar Dist.', color="#FF0000")

        st.caption("Distance in Lunar Distances (LD). 1 LD = distance from Earth to the Moon.")

    elif ca_data is not None and ca_data.empty:
        st.success("Good news! No close approaches (within 0.05 AU) are currently listed by NASA for the next 60 days.")
    else:
        st.error("Could not load close-approach data.")

#risk simulator
with tab2:
    st.header("Risk Classification Simulator")
    st.markdown("Use our trained Random Forest model to see how it classifies an object based on its parameters. This implements our `rf_pha_classifier.joblib`.")
    st.info("Play with the **'H' (Size)** and **'moid' (Proximity)** sliders to see their impact. Our model identified these as the two most important factors.")

    st.sidebar.header("Simulator Parameters")
    with st.sidebar.form(key='prediction_form'):
        st.write("Enter the 6 model features:")

        H = st.slider('Absolute Magnitude (H)', min_value=10.0, max_value=30.0, value=22.0, step=0.1, help="Smaller 'H' means a larger object. The official PHA threshold is H <= 22.0.")
        moid = st.slider('Earth MOID (moid)', min_value=0.0, max_value=0.2, value=0.05, step=0.001, format="%.3f", help="Minimum orbit intersection distance. The official PHA threshold is moid <= 0.05 AU.")

        st.markdown("---")

        q = st.number_input('Perihelion Distance (q)', min_value=0.1, max_value=5.0, value=1.0, step=0.01)
        e = st.number_input('Eccentricity (e)', min_value=0.0, max_value=2.0, value=0.5, step=0.01)
        i = st.number_input('Inclination (i) in degrees', min_value=0.0, max_value=180.0, value=10.0, step=0.1)
        a = st.number_input('Semi-Major Axis (a)', min_value=0.1, max_value=10.0, value=2.0, step=0.01)

        submit_button = st.form_submit_button(label='Run Prediction')

    if submit_button:
        # Create DataFrame in the same order the model was trained on
        input_data = pd.DataFrame(
            [[H, e, a, q, i, moid]],
            columns=['H', 'e', 'a', 'q', 'i', 'moid']
        )

        prediction = model.predict(input_data)
        prediction_proba = model.predict_proba(input_data)

        st.subheader('AI Model Prediction Result')

        if prediction[0] == 1:
            st.error('Result: HAZARDOUS (PHA = 1)', icon="⚠️")
            st.write(f"Model Confidence (Probability of Danger): **{prediction_proba[0][1] * 100:.2f}%**")
        else:
            st.success('Result: SAFE (PHA = 0)', icon="✅")
            st.write(f"Model Confidence (Probability of Danger): **{prediction_proba[0][1] * 100:.2f}%**")

        st.write("---")
        st.write("Input features used for this prediction:")
        st.dataframe(input_data, hide_index=True, use_container_width=True)