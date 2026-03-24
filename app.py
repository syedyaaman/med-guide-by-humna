import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
data = {
    "Fever": [1,1,0,0,1,0],
    "Cough": [1,1,0,0,0,1],
    "Headache": [1,0,1,0,1,1],
    "Chest Pain": [0,0,1,1,0,1],
    "Fatigue": [1,1,1,0,1,1],
    "Disease": ["Flu","Cold","Migraine","Heart Issue","Viral Infection","Infection"]
}

df = pd.DataFrame(data)

X = df.drop("Disease", axis=1)
y = df["Disease"]

model = DecisionTreeClassifier()
model.fit(X, y)

st.markdown(
    """
    <h1 style='text-align: center; color: #4A90E2;'>🩺 Med Guide by Humna</h1>
    <p style='text-align: center; font-size:18px;'>AI-Based Medical Advisory System</p>
    """,
    unsafe_allow_html=True
)

age = st.number_input("Enter your age", min_value=1, max_value=100)

symptoms = st.multiselect(
    "Select your symptoms",
    ["Fever", "Cough", "Headache", "Chest Pain", "Fatigue"]
)

if st.button("Get Advice"):
    st.write("### Selected Symptoms:")
    for symptom in symptoms:
      st.write("✔️", symptom)
    input_data = [0,0,0,0,0]
    symptom_list = ["Fever","Cough","Headache","Chest Pain","Fatigue"]

    for i, symptom in enumerate(symptom_list):
        if symptom in symptoms:
            input_data[i] = 1

    prediction = model.predict([input_data])

    st.subheader(f"Possible Condition: {prediction[0]}")
    st.write("### Why this result?")
    st.write("This prediction is based on the symptoms you selected using a trained decision tree model.")

    if "Chest Pain" in symptoms:
        st.error("🚨 High Risk: Seek immediate medical attention!")

    elif len(symptoms) >= 3:
        st.warning("🟡 Moderate Risk: Visit a doctor soon.")

    elif len(symptoms) == 0:
        st.info("Please select at least one symptom.")

    else:
        st.success("🟢 Low Risk: Rest, hydrate, and monitor symptoms.")
st.warning("⚠️ This is not a medical diagnosis. Please consult a doctor for serious conditions.")