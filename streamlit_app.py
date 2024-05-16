import plotly.express as px
import pandas as pd
import streamlit as st
from queries_olap import Queries
# queries a la bd
qr = Queries()

# Configura la página
st.set_page_config(
    page_title="Dashboard de Anime",
    page_icon=":tv:",
    layout="wide"
)
st.markdown("<h2 style='text-align: center;'>Dashboard Minitas Chinas</h1>", unsafe_allow_html=True)

top_10_anime_more_watch = qr.get_top_10_anime_more_watch() 
top_genre_more_watch = qr.get_top_10_genre_more_watch()
type_watch = qr.get_top_types_mor_watch()
classification = qr.get_top_classification_mor_watch()
best_anime_genre = qr.best_anime_genre()


# Define la paleta de colores
palette = {
    "blanco": "#F3F3F3",
    "gris": "#A3A3A3",
    "rosa_piel": "#FFD6BA",
    "rosa_claro": "#FFAD9F",
    "rosa": "#FF8C9D"
}
# Dividir la página en dos columnas
column1, column2 = st.columns(2)
with column1:
    
    # Crear el histograma con la paleta de colores
    # st.subheader("")
    st.markdown("<h2 style='text-align: center;'>Animes más vistos</h1>", unsafe_allow_html=True)
    fig = px.bar(top_10_anime_more_watch, x="Anime", y="Vistas", color="Anime", 
                color_discrete_map=palette)
    fig.update_xaxes(title="Anime")
    fig.update_yaxes(title="Vistas")
    fig.update_layout(xaxis={'categoryorder':'total descending'}) # Ordenar las barras de mayor a menor
    # Mostrar el histograma en Streamlit
    st.plotly_chart(fig, use_container_width=True)

with column2:
    
    # Crear el pie
    st.markdown("<h2 style='text-align: center;'>Géneros más vistos</h1>", unsafe_allow_html=True)
    fig = px.pie(top_genre_more_watch, values='Vistas', names='Genero', color='Genero', 
                color_discrete_map=palette,hole=.6)
    fig.update_traces(textposition='inside', textinfo='percent+label')  # Mostrar porcentaje y etiqueta dentro de cada sector
    # Mostrar el gráfico de pastel en Streamlit
    fig.update_layout(
        {
            'annotations': [
                {
                    'font': {'size': 20}  # Ajusta el tamaño de los labels
                }
            ]
        }
    )
    fig.update_traces(
    pull=[0.1] + [0] * (len(top_genre_more_watch) - 1),  # Separa el primer sector
    textposition='inside',
    textinfo='percent+label'  # Mostrar porcentaje y etiqueta dentro de cada sector
    )
    st.plotly_chart(fig, use_container_width=True)
    

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Con mas de 10K vistas!!!")
        st.image("death_note.png", width=400,  output_format='PNG',caption='Death Note')
    with col2:
        st.subheader("Con mas de 1M vistas!!!")
        st.image("comedy.png",width=400,  output_format='PNG',caption='Comedy')

with st.container():
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("<h2 style='text-align: center;'>Tipos de animes más importantes</h1>", unsafe_allow_html=True)
        
        # Calcular el porcentaje que el tipo de anime con más vistas representa del resto de tipos
        total_vistas = type_watch['Vistas'].sum()
        max_vistas = type_watch['Vistas'].max()
        porcentaje_max_vistas = (max_vistas / total_vistas) * 100
        porcentaje_resto = 100 - porcentaje_max_vistas

        # Crear las etiquetas para el gráfico de pastel
        labels = [f'Tipo más visto ({porcentaje_max_vistas:.2f}%)', f'Resto de tipos ({porcentaje_resto:.2f}%)']

        # Crear el gráfico de pastel con la paleta de colores
        fig_pie = px.pie(type_watch, values='Vistas', names='Tipo', color='Tipo', 
                        color_discrete_map=palette, hole=0.6, labels=labels)  # Define el tamaño del agujero y las etiquetas

        # Resaltar la sección correspondiente al tipo de anime con más vistas
        fig_pie.update_traces(pull=[0.1, 0], textinfo='percent+label')  # Ajusta el pull para resaltar la sección

        # Mostrar el gráfico de pastel en Streamlit
        st.plotly_chart(fig_pie, use_container_width=True)

    with column2:
        st.markdown("<h2 style='text-align: center;'>Vistas por clasificación</h1>", unsafe_allow_html=True)
        # Crear el histograma con la paleta de colores
        fig = px.bar(classification, x="Clase", y="Vistas", color="Clase", 
                    color_discrete_map=palette)
        fig.update_xaxes(title="Tipo")
        fig.update_yaxes(title="Vistas")
        fig.update_layout(xaxis={'categoryorder':'total descending'}) # Ordenar las barras de mayor a menor
        # Mostrar el histograma en Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
st.subheader("Mejores animes por género:")
best_anime_genre = best_anime_genre.sort_values(by='Vistas', ascending=False)
for index, row in best_anime_genre.iterrows():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.write(f"{row['Anime']} -:- {row['Genero']}")  # Muestra el nombre del anime
    with col2:
        progress = st.progress(row['Vistas'] / best_anime_genre['Vistas'].max())  # Calcula la longitud de la barra de progreso
    with col3:
        st.write(f"{row['Vistas']:,}")  # Muestra el número de vistas
# Ordena los datos de menor a mayor según las vistas
