import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. Configuração da Página (Deve ser o primeiro comando)
st.set_page_config(
    page_title="Safety Analytics France",
    page_icon="🛡️",
    layout="wide",  # Usa a tela inteira (visual de dashboard)
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado para visual "Clean" ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #0052cc;
        color: white;
        border-radius: 5px;
        height: 3em;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Dados Estáticos ---
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

# --- Sidebar (Menu Lateral) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2345/2345454.png", width=50) # Ícone genérico
    st.title("Safety Analytics")
    st.markdown("---")
    st.write("Configure os parâmetros da análise:")
    
    selected_region = st.selectbox("Selecione a Região:", regions)
    
    st.info("Este modelo utiliza dados históricos para prever a gravidade de acidentes em tempo real.")
    
    predict_btn = st.button("Gerar Previsão 🚀")

# --- Função Auxiliar de Cor ---
def get_color(probability):
    """Retorna cor RGB baseada na probabilidade (Verde -> Amarelo -> Vermelho)"""
    if probability < 0.3:
        return [0, 200, 83, 160] # Verde
    elif probability < 0.7:
        return [255, 179, 0, 160] # Laranja/Amarelo
    else:
        return [213, 0, 0, 160]   # Vermelho

# --- Corpo Principal ---
st.title('🇫🇷 Road Accident Risk Assessment')
st.markdown("Dashboard de monitoramento e predição de fatalidades em rodovias francesas.")

url = "https://dummymodel-114787831451.europe-west1.run.app/predict"

if predict_btn:
    # Layout de Colunas para Resultados
    col1, col2 = st.columns([1, 2]) # Coluna da esquerda estreita, mapa largo

    with st.spinner('Consultando modelo de IA...'):
        try:
            response = requests.get(url, params={'region': selected_region}, timeout=5)
            result = response.json()
            prob = result['probability_of_fatality']
            
            # Coordenadas
            coords = region_coords[selected_region]
            df_map = pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]], 'region':[selected_region]})

            # --- Coluna 1: Métricas ---
            with col1:
                st.subheader("Resultados")
                
                # Exibição condicional baseada no risco
                risk_color = "green" if prob < 0.3 else "orange" if prob < 0.7 else "red"
                st.markdown(f"### Risco: :{risk_color}[{result['severity_label']}]")
                
                st.metric(label="Probabilidade de Fatalidade", value=f"{prob:.1%}", delta="Baseado em IA")
                st.progress(prob)
                
                st.write("**Região Analisada:**")
                st.info(result['region'])

            # --- Coluna 2: Mapa Estilo "Google Maps" ---
            with col2:
                radius = int(30000 + prob * 100000)
                color = get_color(prob)

                # Camada de Círculo
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

                # Configuração do Mapa para parecer "Google Maps" (Estilo Clear/Road)
                view_state = pdk.ViewState(
                    latitude=coords[0], 
                    longitude=coords[1], 
                    zoom=6, 
                    pitch=40 # Inclinação para efeito 3D
                )

                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_style='pdk.map_styles.ROAD', # Estilo de ruas similar ao Google
                    tooltip={"text": "{region}\nRisco: " + f"{prob:.2%}"}
                )
                
                st.pydeck_chart(deck)

        except Exception as e:
            st.error(f"Falha na conexão com a API. Detalhes: {e}")

else:
    # Estado inicial (Placeholder)
    st.warning("👈 Selecione uma região no menu lateral e clique em 'Gerar Previsão' para começar.")
    
    # Mapa inicial mostrando a França inteira
    initial_view = pdk.ViewState(latitude=46.6, longitude=1.8, zoom=4.5)
    st.pydeck_chart(pdk.Deck(initial_view_state=initial_view, map_style='pdk.map_styles.ROAD'))
