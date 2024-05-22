import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import streamlit.components.v1 as components
import base64
import pandas as pd
import streamlit as st

# Configura la página
st.set_page_config(
    page_title="Dashboard de Anime",
    page_icon=":tv:",
    layout="wide"
)
st.markdown("<h2 style='text-align: center;'>Dashboard Minitas Chinas</h1>", unsafe_allow_html=True)

top_10_anime_more_watch = pd.read_csv("./1.csv") 
top_genre_more_watch = pd.read_csv("./2.csv")
type_watch = pd.read_csv("./3.csv")
classification = pd.read_csv("./4.csv")
best_anime_genre = pd.read_csv("./5.csv")


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
        labels = [f'Tipo Tv con ({porcentaje_max_vistas:.2f}%) de vistas', f'Movie, OVA, Special, ONA, Music ({porcentaje_resto:.2f}%)']
        sizes = [porcentaje_max_vistas, porcentaje_resto]
        colors = ['#ff9999', '#66b3ff']  # Paleta de colores (ajusta según tu preferencia)

        # Crear el gráfico de pastel
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            sizes, 
            colors=colors, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=140, 
            wedgeprops=dict(width=0.3),  # Ajustar el tamaño del agujero
            pctdistance=0.85
        )

        # Resaltar la sección correspondiente al tipo de anime con más vistas
        wedges[0].set_edgecolor('black')
        wedges[0].set_linewidth(2)

        # Añadir un círculo en el centro para hacer el gráfico de donut
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig.gca().add_artist(centre_circle)

        # Asegurarse de que el gráfico es circular
        ax.axis('equal')

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig,use_container_width=True)

    with column2:
        st.markdown("<h2 style='text-align: center;'>Vistas por clasificación</h1>", unsafe_allow_html=True)
        # Crear el histograma con la paleta de colores
        fig, ax = plt.subplots()

        # Extraer los datos necesarios
        classification = classification.dropna()
        clases = classification['Clase']
        vistas = classification['Vistas']
        palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        # Crear las barras del histograma
        bars = ax.bar(clases, vistas, color=palette)

        # Añadir etiquetas y títulos
        ax.set_xlabel('Tipo')
        ax.set_ylabel('Vistas')
        ax.set_title('Histograma de Vistas por Tipo')
        ax.xaxis.set_tick_params(rotation=45)  # Rotar etiquetas del eje x para mejor visualización

        # Mostrar el histograma en Streamlit
        st.pyplot(fig,use_container_width=True)
st.subheader("Cantidad de animes por Año de cada genero")
df = pd.read_csv("./cant_genero_mes.csv")
fig = px.bar(df, x="GENRE", y="CANTIDAD", color="GENRE",
  animation_frame="anio",  range_y=[0,200])
st.plotly_chart(fig,use_container_width=True)

st.subheader("Cantidad de animes por mes de cada Source")
file_ = open("file_name.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="1000" height="400">',
    unsafe_allow_html=True,
)

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
