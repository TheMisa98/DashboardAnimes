import plotly.express as px
import pandas as pd
import streamlit as st
import queries_olap as qr

# Simulación de datos
data = pd.DataFrame({
    'Anime': ['Naruto', 'Dragon Ball', 'One Piece', 'Attack on Titan', 'Death Note'],
    'Genero': ['Aventura', 'Aventura', 'Aventura', 'Acción', 'Drama'],
    'Vistas': [2500, 3000, 2000, 3500, 4000],
    'Localidad': ['JPN', 'USA', 'CAN', 'BRA', 'MEX']
})

# Define la paleta de colores
palette = {
    "blanco": "#F3F3F3",
    "gris": "#A3A3A3",
    "rosa_piel": "#FFD6BA",
    "rosa_claro": "#FFAD9F",
    "rosa": "#FF8C9D"
}

# Configura la página
st.set_page_config(
    page_title="Dashboard de Anime",
    page_icon=":tv:",
    layout="wide"
)

# Sección para interacción del usuario
st.sidebar.title("Configuración")

# Filtro por género de persona
filtro_genero_persona = st.sidebar.selectbox("Filtrar por género de persona", ["Masculino", "Femenino", "No binario"])

# Por simplicidad, utilizaremos una lista predefinida aquí
todos_los_paises = ["Todos los países", 'JPN', 'USA', 'CAN', 'BRA', 'MEX']

# Ejemplo de control interactivo
filtro_genero = st.sidebar.selectbox("Filtrar por género", ["Acción", "Aventura", "Comedia", "Drama"])
filtro_localidad = st.sidebar.selectbox("Filtrar por localidad", todos_los_paises)


# Título del dashboard
st.title("Dashboard de Anime")

# Filtrar los datos
data_filtrada = data[data['Localidad'] != "Todos los países"]
data_filtrada = data_filtrada.sort_values(by='Vistas', ascending=False)

# Dividir la página en dos columnas
column1, column2 = st.columns(2)

# Crear un histograma de los animes más vistos
with column1:
    st.header("Animes más vistos")
    histogram_chart = px.bar(data_filtrada, 
                              x='Anime', 
                              y='Vistas',
                              color='Genero',
                              labels={'Vistas':'Vistas de Anime'},
                              hover_data=['Anime', 'Vistas', 'Genero'],
                              color_discrete_map={
                                  "Aventura": palette["rosa_claro"],
                                  "Acción": palette["rosa"],
                                  "Drama": palette["rosa_piel"]
                              }
                             )
    st.plotly_chart(histogram_chart, use_container_width=True)

# Crear un mapa mundial con los países que tienen más vistas de anime
with column2:
    st.header("Mapa de Vistas de Anime por País")
    fig = px.choropleth(data_filtrada, 
                        locations='Localidad', 
                        color='Vistas',
                        color_continuous_scale=[(0, palette["rosa"]), (1, palette["blanco"])],
                        range_color=(0, data_filtrada['Vistas'].max()),
                        color_continuous_midpoint=data_filtrada['Vistas'].median(),
                        labels={'Vistas':'Vistas de Anime'},
                        locationmode='ISO-3',
                        hover_name='Localidad'
                       )
    fig.update_geos(showcountries=True, showcoastlines=True,
                    showland=True, fitbounds="locations")
    fig.update_layout(geo=dict(showframe=False, 
                               showcoastlines=False, 
                               projection_type='equirectangular'
                              )
                     )
    st.plotly_chart(fig, use_container_width=True)

# Crear un gráfico de pastel para representar las vistas de "Death Note"
vistas_death_note = data_filtrada[data_filtrada['Anime'] == 'Death Note']['Vistas'].values[0]
vistas_resto_animes = data_filtrada[data_filtrada['Anime'] != 'Death Note']['Vistas'].sum()

with st.container():
    st.header("Vistas de")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        st.image("death_note.png", use_column_width=True)
    with col2:
        fig_pie = px.pie(values=[vistas_death_note, vistas_resto_animes],
                         names=['Death Note', 'Otros Animes'],
                         hole=.9,
                         color_discrete_map={
                             "Death Note": palette["rosa_piel"],
                             "Otros Animes": palette["rosa_claro"]
                         }
                        )
        fig_pie.update_traces(hoverinfo="label+percent+name")
        st.plotly_chart(fig_pie, use_container_width=True)