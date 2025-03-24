import streamlit as st
import numpy as np
import joblib

# Load trained ML model
model = joblib.load("calorieburn_predictor.pkl")

# Streamlit Page Config
st.set_page_config(page_title="Fitness Tracker", page_icon="🔥", layout="centered")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        .big-title { font-size: 50px; font-weight: bold; text-align: center; color: #FF4B4B; }
        .sub-title { font-size: 22px; text-align: center; color: #333; }
        .section-header { font-size: 26px; font-weight: bold; color: #333; margin-top: 20px; }
        .metric-box { padding: 10px; border-radius: 10px; text-align: center; font-size: 22px; font-weight: bold; }
        .bmi-box { background-color: #4CAF50; color: white; }
        .calories-box { background-color: #FF9800; color: white; }
        .info-box { background-color: black; padding: 15px; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: User Input Form --------------------------------------
st.sidebar.header("👤 Enter Your Details")

gender = st.sidebar.selectbox("Select Gender", ["Male", "Female"])
age = st.sidebar.number_input("Enter Age (years)", min_value=10, max_value=100, step=1)
height = st.sidebar.number_input("Enter Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
weight = st.sidebar.number_input("Enter Weight (kg)", min_value=10.0, max_value=200.0, step=0.1)

st.sidebar.header("🏋️ Exercise Details")
duration = st.sidebar.number_input("Exercise Duration (minutes)", min_value=1, max_value=35, step=1)
heart_rate = st.sidebar.number_input("Heart Rate (bpm)", min_value=30, max_value=140, step=1)
body_temp = st.sidebar.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, step=0.1)

# Compute BMI
bmi = weight / ((height / 100) ** 2) if height > 0 else 0

# Prepare input data for the ML model
gender_numeric = 1 if gender == "Male" else 0
input_data = np.array([[gender_numeric, age, height, weight, duration, heart_rate, body_temp]])

# Predict Calories
# predicted_calories = model.predict(input_data)[0]
with st.spinner("🔄 Calculating... Please wait..."):
    predicted_calories = model.predict(input_data)[0]


# Main Page Layout ----------------------------------------------
st.markdown("<h1 class='big-title'; color:red>🔥 Fitness Tracker: Calories & BMI Predictor</h1>", unsafe_allow_html=True)

st.markdown(
    "<p style='font-size:22px; color:white; text-align:center;'>"
    "Track your fitness progress by predicting calories burned and BMI. "
    "Simply enter your details in the sidebar and get instant insights!"
    "</p>",
    unsafe_allow_html=True,
)


# Display Predicted BMI & Calories --------------------------------
st.write('---')
st.markdown("<h2 class='section-header'>📌 Your Fitness Summary</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric(label="💪 BMI", value=f"{bmi:.2f}")

with col2:
    st.metric(label="🔥 Calories Burned", value=f"{predicted_calories:.2f} kcal")

st.write('---')
st.markdown("<h2 class='section-header'>⏳ Estimated Time to Burn Calories</h2>", unsafe_allow_html=True)

st.markdown(f"""
- 🏃‍♂️ **Running**: {predicted_calories / 10:.1f} min at 10 km/h  
- 🚴‍♀️ **Cycling**: {predicted_calories / 8:.1f} min at moderate pace  
- 🚶‍♂️ **Walking**: {predicted_calories / 5:.1f} min at 5 km/h  
""")


# BMI Interpretation (Text-Based Summary) -------------------------
st.write('---')
st.markdown("<h2 class='section-header'>📊 Your BMI Analysis</h2>", unsafe_allow_html=True)

if bmi < 18.5:
    bmi_message = "Your BMI is below normal. Consider a balanced diet to gain healthy weight!"
    color = "🔵"
elif 18.5 <= bmi < 25:
    bmi_message = "Your BMI is in the normal range. Keep up the good work!"
    color = "🟢"
elif 25 <= bmi < 30:
    bmi_message = "Your BMI is slightly above normal. Consider regular exercise and a balanced diet."
    color = "🟡"
else:
    bmi_message = "Your BMI is in the obese range. It's important to adopt a healthier lifestyle!"
    color = "🔴"

st.markdown(f"<p style='font-size: 20px;'>{color} {bmi_message}</p>", unsafe_allow_html=True)


# Estimate Daily Caloric Needs (TDEE) -------------------------------
st.write('---')
st.markdown("<h2 class='section-header'>🍽️ Daily Caloric Needs Estimator</h2>", unsafe_allow_html=True)

activity_level = st.selectbox("Select Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

activity_factors = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725
}
bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)  # Mifflin-St Jeor Equation
tdee = bmr * activity_factors[activity_level]

st.success(f"🔢 Your estimated daily caloric need is **{tdee:.0f} kcal/day** to maintain your weight.")


# General Fitness Information ---------------------------------------
st.write('---')
st.markdown("<h2 class='section-header'>ℹ️ General Health & Fitness Information</h2>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-box">
        <b>📌 BMI Categories:</b>
        <ul>
            <li><b>Underweight:</b> BMI &lt; 18.5</li>
            <li><b>Normal Weight:</b> BMI 18.5 - 24.9</li>
            <li><b>Overweight:</b> BMI 25 - 29.9</li>
            <li><b>Obese:</b> BMI ≥ 30</li>
        </ul>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="info-box">
        <b>🔥 Exercise Tips:</b>
        <ul>
            <li>Stay hydrated 💧</li>
            <li>Maintain a balanced diet 🥗</li>
            <li>Get enough rest 😴</li>
            <li>Track progress & stay consistent ✅</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)


# Call-to-Action Button -----------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:30px;">
        <button style="background-color:#FF4B4B; color:white; border:none; padding:15px; font-size:22px; border-radius:10px; cursor:pointer;">
            🔥 Get Personalized Fitness Advice
        </button>
    </div>
    """,
    unsafe_allow_html=True,
)
