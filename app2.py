import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="SafeRoute France",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "CANVAS" & UX DESIGN ---
st.markdown("""
    <style>
        /* --- ANIMAÇÃO DE FUNDO (O Efeito Canvas) --- */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            /* Fundo Gradiente Animado Moderno */
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Inter', sans-serif;
        }

        /* --- REMOVER ELEMENTOS PADRÃO --- */
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); } /* Header Transparente */

        /* --- GLASSMORPHISM CONTAINER (O Efeito de Vidro) --- */
        .glass-container {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            margin-bottom: 2rem;
        }

        /* --- TYPOGRAPHY --- */
        h1 { color: #1e293b !important; font-weight: 800 !important; letter-spacing: -1px; }
        h3 { color: #475569 !important; font-weight: 500 !important; }
        
        /* --- INPUT STYLING --- */
        .stSelectbox > div > div {
            background-color: white !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px !important;
            color: #333 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* --- BOTÃO MODERNIZADO --- */
        .stButton > button {
            background: #111827 !important; /* Preto Clean estilo Vercel/Apple */
            color: white !important;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            background: #000000 !important;
        }
        
        /* --- METRIC FIX --- */
        [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 14px !important; }
        [data-testid="stMetricValue"] { color: #0f172a !important; font-size: 36px !important; font-weight: 700 !important; }

    </style>
""", unsafe_allow_html=True)

# --- DADOS ---
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

# --- LAYOUT PRINCIPAL (CONTAINER FLUTUANTE) ---

# Cria um container centralizado com efeito de vidro
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)

# Navbar Minimalista dentro do container
c_logo, c_badge = st.columns([3, 1])
with c_logo:
    st.markdown("<div style='font-size: 24px; font-weight: 800; color: #2563EB;'>🛡️ SafeRoute <span style='color: #94a3b8;'>France</span></div>", unsafe_allow_html=True)
with c_badge:
    st.markdown("<div style='text-align: right; color: #64748b; font-size: 12px; border: 1px solid #cbd5e1; padding: 4px 8px; border-radius: 20px; display: inline-block;'>v2.1 Live</div>", unsafe_allow_html=True)

st.divider()

st.markdown("<h1 style='text-align: center; margin-top: 1rem;'>Real-time Risk Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 2rem;'>AI-powered safety assessment for French regions.</p>", unsafe_allow_html=True)

# Área de Input Otimizada
col_input_1, col_input_2, col_input_3 = st.columns([1, 2, 1])
with col_input_2:
    selected_region = st.selectbox("Select Region", regions, label_visibility="collapsed")
    st.write("") # Spacer
    predict_btn = st.button("Analyze Safety Levels ✨")

st.markdown("</div>", unsafe_allow_html=True) # Fecha Container de Input

# --- RESULTADOS ---
if predict_btn:
    # Placeholder para manter layout enquanto carrega
    result_placeholder = st.empty()
    
    url = "https://dummymodel-114787831451.europe-west1.run.app/predict"
    
    with st.spinner('Running AI risk models...'):
        try:
            # time.sleep(1.5) # Descomente para ver a animação de loading
            response = requests.get(url, params={'region': selected_region}, timeout=8)
            
            if response.status_code == 200:
                result = response.json()
                prob = result['probability_of_fatality']
                coords = region_coords[selected_region]
                
                # Lógica de Cores UX
                if prob < 0.3:
                    color_hex = "#10B981" # Verde
                    risk_label = "SAFE"
                    msg = "Low risk detected."
                elif prob < 0.7:
                    color_hex = "#F59E0B" # Laranja
                    risk_label = "MODERATE"
                    msg = "Exercise caution."
                else:
                    color_hex = "#EF4444" # Vermelho
                    risk_label = "CRITICAL"
                    msg = "High danger zone."

                # --- NOVO CARD DE RESULTADO ---
                st.markdown(f"""
                <div class='glass-container' style='border-left: 8px solid {color_hex};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h4 style='margin:0; color: #64748b;'>Assessment Report</h4>
                            <h2 style='margin:0; color: {color_hex};'>{risk_label}</h2>
                            <p style='margin:0; color: #334155;'>{msg}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Layout Métricas + Mapa
                c_metrics, c_map = st.columns([1, 2])
                
                with c_metrics:
                     # Usando container nativo do Streamlit para métricas para manter responsividade
                    with st.container():
                        st.metric("Fatality Probability", f"{prob:.1%}", delta=None)
                        st.divider()
                        st.markdown(f"**Region:** {result['region']}")
                        st.markdown(f"**Lat/Lon:** {coords[0]:.2f}, {coords[1]:.2f}")
                
                with c_map:
                    # Mapa PyDeck refinado
                    df_map = pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]]})
                    
                    # Converter cor HEX para RGB Array para PyDeck
                    rgb_color = [int(color_hex[1:3], 16), int(color_hex[3:5], 16), int(color_hex[5:7], 16), 180]

                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        df_map,
                        get_position='[lon, lat]',
                        get_fill_color=rgb_color,
                        get_radius=int(30000 + prob * 50000),
                        pickable=True,
                        stroked=True,
                        get_line_color=[255, 255, 255],
                        line_width_min_pixels=3,
                        filled=True
                    )

                    view_state = pdk.ViewState(
                        latitude=coords[0], longitude=coords[1], zoom=6, pitch=30
                    )

                    deck = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state,
                        map_style=pdk.map_styles.LIGHT,
                        tooltip={"text": "Risk Level: {prob:.1%}"}
                    )
                    st.pydeck_chart(deck)

            else:
                st.error("Server Error. Please try again.")

        except Exception as e:
            st.error(f"Connection failed. Details: {e}")

# --- FOOTER DISCRETO ---
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: rgba(255,255,255,0.6); font-size: 12px;">
    SafeRoute AI © 2024
</div>
""", unsafe_allow_html=True)
