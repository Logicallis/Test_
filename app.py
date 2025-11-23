import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. Configuração da Página
st.set_page_config(
    page_title="SafeRoute France",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed" # Esconde a sidebar
)

# --- 2. CSS AVANÇADO: TRANSFORMAÇÃO EM WEB APP ---
st.markdown("""
    <style>
        /* RESET GERAL & LIGHT MODE FORÇADO */
        .stApp {
            background-color: #f8f9fc !important; /* Fundo Cinza Azulado Clean */
        }
        
        /* ESCONDER ELEMENTOS DE DASHBOARD */
        [data-testid="stSidebar"] { display: none; } /* Tchau Sidebar */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* NAVBAR SIMULADA */
        .navbar {
            padding: 1rem 0;
            border-bottom: 1px solid #eaeaea;
            background: white;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* HERO SECTION (Área de Input) */
        .hero-container {
            text-align: center;
            padding: 2rem 0;
        }
        
        /* ESTILO DOS INPUTS (Centralizados e Maiores) */
        .stSelectbox > div > div {
            background-color: white !important;
            border: 1px solid #ddd !important;
            border-radius: 12px !important;
            height: 50px;
            display: flex;
            align-items: center;
        }
        
        /* BOTÃO DE AÇÃO (CTA) */
        .stButton > button {
            background: linear-gradient(90deg, #2563EB 0%, #1E40AF 100%) !important;
            color: white !important;
            border: none;
            border-radius: 30px; /* Botão Redondo Moderno */
            padding: 0.5rem 2rem;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
            transition: all 0.2s ease;
            width: 100%;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        }

        /* CARD DE RESULTADO */
        .result-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin-top: 2rem;
            border: 1px solid #eaeaea;
        }
        
        /* TEXTOS */
        h1 { color: #111827 !important; font-weight: 800 !important; font-size: 2.5rem !important; text-align: center; }
        h3 { color: #374151 !important; text-align: center; font-weight: 400 !important; }
        p, label { color: #4B5563 !important; }
        
        /* FORÇAR TEXTO ESCURO NOS METRICS (Fix do Dark Mode) */
        [data-testid="stMetricLabel"] { color: #6B7280 !important; }
        [data-testid="stMetricValue"] { color: #111827 !important; }
        
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

# --- NAVBAR (HTML PURO PARA VISUAL) ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: white; border-bottom: 1px solid #eee; margin: -4rem -4rem 2rem -4rem;">
    <div style="font-weight: bold; font-size: 20px; color: #2563EB; display: flex; align-items: center;">
        <span style="font-size: 24px; margin-right: 8px;">🛡️</span> SafeRoute France
    </div>
    <div style="color: #666; font-size: 14px;">AI Risk Assessment Platform</div>
</div>
""", unsafe_allow_html=True)


# --- HERO SECTION (CENTRALIZADA) ---
st.markdown("<h1>Check Road Safety instantly</h1>", unsafe_allow_html=True)
st.markdown("<h3>Select a region below to generate a real-time AI risk assessment.</h3>", unsafe_allow_html=True)

st.write("") # Espaçamento
st.write("")

# Layout Centralizado: [Espaço Vazio] [Conteúdo] [Espaço Vazio]
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    selected_region = st.selectbox("Choose a Region", regions, label_visibility="collapsed")
    
    st.write("") # Espaçamento pequeno
    
    # Botão ocupa a largura da coluna central
    predict_btn = st.button("Analyze Risk ⚡")


# --- RESULT SECTION (MODERNA) ---
if predict_btn:
    url = "https://dummymodel-114787831451.europe-west1.run.app/predict"
    
    with st.spinner('Thinking...'):
        try:
            # Simulação de delay para parecer que a IA está "pensando" (opcional)
            # time.sleep(1) 
            
            response = requests.get(url, params={'region': selected_region}, timeout=5)
            result = response.json()
            prob = result['probability_of_fatality']
            coords = region_coords[selected_region]

            # Container Branco com Sombra (O Card)
            with st.container():
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                
                # Cabeçalho do Resultado
                col_res_1, col_res_2 = st.columns([1, 2])
                
                with col_res_1:
                    st.markdown("#### Analysis Report")
                    
                    # Definição de Cores e Texto
                    if prob < 0.3:
                        status_color = "#10B981" # Verde moderno
                        status_text = "Low Risk Environment"
                        bg_badge = "#D1FAE5"
                    elif prob < 0.7:
                        status_color = "#F59E0B" # Laranja moderno
                        status_text = "Elevated Caution"
                        bg_badge = "#FEF3C7"
                    else:
                        status_color = "#EF4444" # Vermelho moderno
                        status_text = "High Danger Zone"
                        bg_badge = "#FEE2E2"

                    # Badge de Status (HTML/CSS inline para controle total)
                    st.markdown(f"""
                        <div style="background-color: {bg_badge}; color: {status_color}; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: bold; margin-bottom: 20px;">
                            {status_text}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Fatality Probability", f"{prob:.1%}")
                    
                    st.caption(f"Region: {result['region']}")
                    st.caption("Data source: Traffic API v2.1")

                with col_res_2:
                    # Mapa Clean
                    df_map = pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]]})
                    
                    # Cor do círculo baseada no risco
                    if prob < 0.3: pdk_color = [16, 185, 129, 160]
                    elif prob < 0.7: pdk_color = [245, 158, 11, 160]
                    else: pdk_color = [239, 68, 68, 160]

                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        df_map,
                        get_position='[lon, lat]',
                        get_fill_color=pdk_color,
                        get_radius=int(30000 + prob * 80000),
                        pickable=True,
                        stroked=True,
                        get_line_color=[255, 255, 255],
                        line_width_min_pixels=2,
                    )

                    view_state = pdk.ViewState(
                        latitude=coords[0], longitude=coords[1], zoom=5.5, pitch=0
                    )

                    deck = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state,
                        map_style=pdk.map_styles.LIGHT,
                        tooltip={"text": f"Risk: {prob:.1%}"}
                    )
                    st.pydeck_chart(deck)
                
                st.markdown("</div>", unsafe_allow_html=True) # Fecha o card

        except Exception as e:
            st.error("Could not connect to the AI model. Please try again later.")

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #aaa; font-size: 12px;">
    &copy; 2024 Safety Analytics Inc. • <a href="#" style="color: #aaa;">Privacy</a> • <a href="#" style="color: #aaa;">Terms</a>
</div>
""", unsafe_allow_html=True)
