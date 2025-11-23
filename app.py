import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. Page Configuration
st.set_page_config(
    page_title="Safety Analytics France",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FORCE LIGHT MODE & UX DESIGN (Advanced CSS) ---
# Ensures the app looks White/Clean (SaaS style) regardless of user's dark mode settings
st.markdown("""
    <style>
        /* Force main background to light gray (SaaS style) */
        [data-testid="stAppViewContainer"] {
            background-color: #f0f2f6;
        }
        
        /* Force sidebar to be white */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }

        /* Style Metric Cards to look like 'widgets' */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            color: #31333F; /* Dark Text */
        }
        
        /* Force metric text colors */
        [data-testid="stMetricLabel"] {
            color: #666;
        }
        [data-testid="stMetricValue"] {
            color: #333;
        }

        /* Button Styling */
        .stButton>button {
            width: 100%;
            background-color: #2563EB; /* Corporate Blue */
            color: white;
            border: none;
            border-radius: 8px;
            height: 3em;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
        }
        
        /* Remove excessive top padding */
        .block-container {
            padding-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# --- Data ---
# Region names kept in French for API compatibility
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

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ Safety Analytics")
    st.markdown("---")
    st.write("**Analysis Configuration**")
    
    selected_region = st.selectbox("Target Region:", regions)
    
    st.markdown("###") # Spacing
    st.info("The model uses demographic and historical traffic data from the selected region to predict severity.")
    
    st.markdown("###")
    predict_btn = st.button("Analyze Risk ⚡")

# --- Color Function ---
def get_color(probability):
    if probability < 0.3:
        return [0, 200, 83, 180] # Vibrant Green
    elif probability < 0.7:
        return [255, 179, 0, 180] # Orange/Yellow
    else:
        return [220, 38, 38, 180]   # Alert Red

# --- Main App ---
st.markdown("### 🇫🇷 Road Accident Risk Dashboard")
st.markdown("Predictive monitoring of accident severity in French regions.")
st.markdown("---")

url = "https://dummymodel-114787831451.europe-west1.run.app/predict"

if predict_btn:
    col1, col2 = st.columns([1, 2]) # 1/3 for data, 2/3 for map

    with st.spinner('Processing data via API...'):
        try:
            response = requests.get(url, params={'region': selected_region}, timeout=5)
            result = response.json()
            prob = result['probability_of_fatality']
            
            coords = region_coords[selected_region]
            
            # Dataframe for map
            df_map = pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]]})

            # --- Column 1: KPIs ---
            with col1:
                st.success("Analysis Complete")
                
                # Visual Risk Label
                if prob < 0.3:
                    st.markdown(f"<h2 style='color: #00c853;'>Low Risk</h2>", unsafe_allow_html=True)
                elif prob < 0.7:
                    st.markdown(f"<h2 style='color: #ffb300;'>Medium Risk</h2>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h2 style='color: #d32f2f;'>Critical Risk</h2>", unsafe_allow_html=True)

                # Metric Card (styled by CSS)
                st.metric(label="Estimated Fatality Probability", value=f"{prob:.1%}")
                
                st.write("Region Details:")
                st.code(result['region'])

            # --- Column 2: MAP ---
            with col2:
                # Dynamic radius
                radius = int(30000 + prob * 80000)
                color = get_color(prob)

                layer = pdk.Layer(
                    "ScatterplotLayer",
                    df_map,
                    get_position='[lon, lat]',
                    get_fill_color=color,
                    get_radius=radius,
                    pickable=True,
                    stroked=True,
                    get_line_color=[255, 255, 255],
                    line_width_min_pixels=2,
                )

                # Map View Settings (Light Style)
                view_state = pdk.ViewState(
                    latitude=coords[0], 
                    longitude=coords[1], 
                    zoom=6, 
                    pitch=0
                )

                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_style=pdk.map_styles.LIGHT, # Ensures clean/light background
                    tooltip={"text": "Local Risk: " + f"{prob:.2%}"}
                )
                
                st.pydeck_chart(deck)

        except Exception as e:
            st.error(f"Connection Error: {e}")

else:
    # Empty State
    st.info("👈 Select a region from the sidebar to start.")
    
    # Default Map of France (Light)
    initial_view = pdk.ViewState(latitude=46.6, longitude=1.8, zoom=5)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=initial_view,
        map_style=pdk.map_styles.LIGHT 
    ))
    
    # Mapa inicial mostrando a França inteira
    initial_view = pdk.ViewState(latitude=46.6, longitude=1.8, zoom=4.5)
    st.pydeck_chart(pdk.Deck(initial_view_state=initial_view, map_style='pdk.map_styles.ROAD'))
