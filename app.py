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

# --- 2. FORCE LIGHT THEME & TEXT COLOR (FIX FOR DARK MODE USERS) ---
st.markdown("""
    <style>
        /* 1. Força o fundo geral a ser claro */
        .stApp {
            background-color: #f0f2f6 !important;
        }
        
        /* 2. Força o fundo da Sidebar a ser branco */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e0e0e0;
        }

        /* 3. A CORREÇÃO CRÍTICA: Força TODO texto a ser Preto/Cinza Escuro */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #31333F !important;
        }
        
        /* 4. Corrige especificamente os textos dentro de inputs e selects */
        .stSelectbox div, .stSelectbox label {
            color: #31333F !important;
        }
        
        /* 5. Estilo dos Cards de Métricas */
        div[data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        /* Força cor dos valores das métricas */
        [data-testid="stMetricLabel"] { color: #666 !important; }
        [data-testid="stMetricValue"] { color: #333 !important; }

        /* 6. Botão Azul (Mantém texto branco apenas aqui) */
        .stButton>button {
            background-color: #2563EB !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            height: 3em;
        }
        .stButton>button p {
            color: white !important; /* Garante que o texto do botão seja branco */
        }
        
        /* Remove padding do topo */
        .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- Data ---
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
    
    st.markdown("###") 
    # Usando st.info (que tem cor própria) ou markdown puro
    st.markdown("""
    <div style="background-color: #e1f5fe; padding: 10px; border-radius: 5px; border-left: 5px solid #0288d1;">
        <small>The model uses demographic and historical traffic data from the selected region.</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("###")
    predict_btn = st.button("Analyze Risk ⚡")

# --- Color Function ---
def get_color(probability):
    if probability < 0.3:
        return [0, 200, 83, 180] 
    elif probability < 0.7:
        return [255, 179, 0, 180] 
    else:
        return [220, 38, 38, 180] 

# --- Main App ---
st.markdown("### 🇫🇷 Road Accident Risk Dashboard")
st.markdown("Predictive monitoring of accident severity in French regions.")
st.markdown("---")

url = "https://dummymodel-114787831451.europe-west1.run.app/predict"

if predict_btn:
    col1, col2 = st.columns([1, 2]) 

    with st.spinner('Processing data via API...'):
        try:
            response = requests.get(url, params={'region': selected_region}, timeout=5)
            result = response.json()
            prob = result['probability_of_fatality']
            
            coords = region_coords[selected_region]
            df_map = pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]]})

            # --- Column 1: KPIs ---
            with col1:
                # Custom Success Message Box
                st.markdown("""
                <div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>✅ Analysis Complete</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Visual Risk Label
                if prob < 0.3:
                    st.markdown(f"<h2 style='color: #00c853 !important;'>Low Risk</h2>", unsafe_allow_html=True)
                elif prob < 0.7:
                    st.markdown(f"<h2 style='color: #ffb300 !important;'>Medium Risk</h2>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h2 style='color: #d32f2f !important;'>Critical Risk</h2>", unsafe_allow_html=True)

                st.metric(label="Estimated Fatality Probability", value=f"{prob:.1%}")
                
                st.write("Region Details:")
                # Forcing code block to look okay in light mode
                st.code(result['region'])

            # --- Column 2: MAP ---
            with col2:
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

                view_state = pdk.ViewState(
                    latitude=coords[0], 
                    longitude=coords[1], 
                    zoom=6, 
                    pitch=0
                )

                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_style=pdk.map_styles.LIGHT,
                    tooltip={"text": "Local Risk: " + f"{prob:.2%}"}
                )
                
                st.pydeck_chart(deck)

        except Exception as e:
            st.error(f"Connection Error: {e}")

else:
    # Empty State with styled box
    st.markdown("""
    <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; border: 1px solid #ffeeba;">
        👈 <strong>Start here:</strong> Select a region from the sidebar to visualize risk.
    </div>
    """, unsafe_allow_html=True)
    
    initial_view = pdk.ViewState(latitude=46.6, longitude=1.8, zoom=5)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=initial_view,
        map_style=pdk.map_styles.LIGHT 
    ))
