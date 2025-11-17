import streamlit as st
import requests

st.title('Road Accident Fatality Prediction in France')

regions = [
    'Île-de-France', 'Nouvelle-Aquitaine', 'Auvergne-Rhône-Alpes',
    'Occitanie', 'Provence-Alpes-Côte d’Azur', 'Hauts-de-France',
    'Normandie', 'Pays de la Loire', 'Bourgogne-Franche-Comté',
    'Grand Est', 'Centre-Val de Loire', 'Bretagne'
]

selected_region = st.selectbox("Select a region:", regions)

url = "https://dummymodel-114787831451.europe-west1.run.app/predict"


if st.button("Predict"):
    try:
        response = requests.get(url, params={'region': selected_region}, timeout=5)
        result = response.json()

        st.subheader("Prediction Results")
        st.write(f"**Region:** {result['region']}")
        st.write(f"**Severity:** {result['severity_label']}")
        st.write(f"**Probability of fatality:** {result['probability_of_fatality']:.2%}")

        if result['fatality_prediction'] == 1:
            st.error("⚠️ High probability of a fatal accident.")
        else:
            st.success("✔️ The model predicts a non-fatal accident.")

    except Exception as e:
        st.error(f"Error to connect with API or parse response: {e}")
