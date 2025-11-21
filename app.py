import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.title('Road Accident Fatality Prediction in France')

regions = [
    'Île-de-France', 'Nouvelle-Aquitaine', 'Auvergne-Rhône-Alpes',
    'Occitanie', 'Provence-Alpes-Côte d’Azur', 'Hauts-de-France',
    'Normandie', 'Pays de la Loire', 'Bourgogne-Franche-Comté',
    'Grand Est', 'Centre-Val de Loire', 'Bretagne'
]

region_coords = {
    'Île-de-France': (48.8566, 2.3522),
    'Nouvelle-Aquitaine': (44.8378, -0.5792),
    'Auvergne-Rhône-Alpes': (45.7640, 4.8357),
    'Occitanie': (43.6045, 1.4442),
    'Provence-Alpes-Côte d’Azur': (43.2965, 5.3698),
    'Hauts-de-France': (50.6292, 3.0573),
    'Normandie': (49.4431, 1.0993),
    'Pays de la Loire': (47.2184, -1.5536),
    'Bourgogne-Franche-Comté': (47.3220, 5.0415),
    'Grand Est': (48.5734, 7.7521),
    'Centre-Val de Loire': (47.9025, 1.9090),
    'Bretagne': (48.1173, -1.6778)
}

selected_region = st.selectbox("Select a region:", regions)

url = "https://dummymodel-114787831451.europe-west1.run.app/predict"

if st.button("Predict"):
    try:
        response = requests.get(url, params={'region': selected_region}, timeout=5)
        result = response.json()

        st.subheader("Prediction Results")
        st.write(f"**Region:** {result['region']}")
        st.write(f"**Severity:** {result['severity_label']}")

        prob = result['probability_of_fatality']

        # progress bar + metric
        st.progress(prob)
        st.metric(label="Probability of fatality", value=f"{prob:.2%}")

        # mao after predict
        coords = region_coords[selected_region]
        df = pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]], 'region':[selected_region]})

        radius = int(30000 + prob * 120000)  # círculo proporcional à probabilidade
        layer = pdk.Layer(
            "ScatterplotLayer",
            df,
            get_position='[lon, lat]',
            get_color=[0, 128, 255, 160],  # cor fixa
            get_radius=radius,
        )

        view_state = pdk.ViewState(latitude=46.6, longitude=1.8, zoom=5)
        deck = pdk.Deck(layers=[layer], initial_view_state=view_state,
                        tooltip={"text": "{region}\nProbability: " + f"{prob:.2%}"})
        st.pydeck_chart(deck)

    except Exception as e:
        st.error(f"Error to connect with API or parse response: {e}")
