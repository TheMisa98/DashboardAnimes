import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd
import streamlit as st
repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
# Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()

# Establecer el ancho completo del dashboard
st.set_page_config(layout="wide")

data = {'estado': {
    1: "Aguascalientes",
    2: "Baja California",
    3: "Baja California Sur",
    4: "Campeche",
    5: "Coahuila",
    6: "Colima",
    7: "Chiapas",
    8: "Chihuahua",
    9: "Ciudad de México",
    10: "Durango",
    11: "Guanajuato",
    12: "Guerrero",
    13: "Hidalgo",
    14: "Jalisco",
    15: "México",
    16: "Michoacán",
    17: "Morelos",
    18: "Nayarit",
    19: "Nuevo León",
    20: "Oaxaca",
    21: "Puebla",
    22: "Querétaro",
    23: "Quintana Roo",
    24: "San Luis Potosí",
    25: "Sinaloa",
    26: "Sonora",
    27: "Tabasco",
    28: "Tamaulipas",
    29: "Tlaxcala",
    30: "Veracruz",
    31: "Yucatán",
    32: "Zacatecas"
},
    'population': {
    1:  1425607,
    2:  3769020,
    3:  798447,
    4:  928363,
    5:  3146771,
    6:  731391,
    7:  5543828,
    8:  3741869,
    9:  9209944,
    10: 1832650,
    11: 6166934,
    12: 3540685,
    13: 3082841,
    14: 8348151,
    15: 16992418,
    16: 4748846,
    17: 1971520,
    18: 1235456,
    19: 5784442,
    20: 4132148,
    21: 6583278,
    22: 2368467,
    23: 1857985,
    24: 2822255,
    25: 3026943,
    26: 2944840,
    27: 2402598,
    28: 3527735,
    29: 1342977,
    30: 8062579,
    31: 2320898,
    32: 1622138
}}

df = pd.DataFrame({'estado': data['estado'].values(), 'population':   data['population'].values()})
# Calcular la población total
poblacion_total = df['population'].sum()

# Formatear la población total para mostrarla en millones con un decimal
poblacion_total_millones = "{:.1f}".format(poblacion_total / 1e6)

# Obtener los 10 estados más poblados
df_top10 = df.nlargest(10, 'population')

# Obtener el estado más poblado
estado_mas_poblado = df.loc[df['population'].idxmax()]

# Crear un gráfico de pastel para representar visualmente la población del estado más poblado
fig_pie = px.pie(values=[estado_mas_poblado['population'], poblacion_total - estado_mas_poblado['population']],
                 names=[estado_mas_poblado['estado'], 'Resto de estados'],
                 hole=.9)
fig_pie.update_traces(pull=[0.1, 0], hoverinfo="label+percent+name", marker=dict(colors=['blue', 'gray']))

# Dividir el espacio horizontalmente
col1, col2 = st.columns([1, 2])

# Mostrar el gráfico de pastel y el mapa en columnas separadas
with col1:
    # Mostrar el estado más poblado como un KPI con una barra de progreso circular
    st.subheader("Estado más poblado:")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Mapa de calor de la población por estado en México")
    fig_mapa = px.choropleth(data_frame=df,
                              geojson=mx_regions_geo,
                              # nombre de la columna del Dataframe
                              locations=df['estado'],
                              # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                              featureidkey="properties.name",
                              # El color depende de las cantidades
                              color=df['population'],
                              color_continuous_scale="burg",
                              projection="stereographic"  # Cambia la proyección según lo deseado
                              # scope="north america"
                              ).update_geos(showcountries=True, showcoastlines=True,
                                            showland=True, fitbounds="locations")

    # Ajusta el tamaño del mapa
    fig_mapa.update_layout(width=800, height=600)

    st.plotly_chart(fig_mapa, use_container_width=True)

# Mostrar tabla con los 10 estados más poblados y progresos de población
st.subheader("Los 10 estados más poblados:")
for index, row in df_top10.iterrows():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.write(row['estado'])
    with col2:
        progress = st.progress(row['population'] / estado_mas_poblado["population"])
    with col3:
        st.write(f"{row['population']:,}")


st.sidebar.title("Información")
st.sidebar.subheader("Población Total")
st.sidebar.write(f'{poblacion_total_millones} (millones)')

# Crear un gráfico de barra circular para representar la población por estado
fig_planet = go.Figure()

# Agregar una barra para cada estado
for index, row in df.iterrows():
    fig_planet.add_trace(go.Barpolar(
        r=[row['population']],
        theta=[row['estado']],
        name=row['estado'],
        marker_color='rgb(106, 90, 205)'  # Color de la barra
    ))
# Establecer el tamaño y título del gráfico
fig_planet.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, showticklabels=False, showgrid=False),
        angularaxis=dict(showticklabels=True, tickangle=45)
    ),
    title='Población por estado en México (en millones)',
)

# Mostrar el gráfico de barra circular
st.plotly_chart(fig_planet, use_container_width=True)


# ['airy', 'aitoff', 'albers', 'albers usa', 'august', 'azimuthal equal area', 'azimuthal equidistant', 'baker', 'bertin1953', 'boggs', 'bonne', 'bottomley', 'bromley', 'collignon', 'conic conformal', 'conic equal area', 'conic equidistant', 'craig', 'craster', 'cylindrical equal area', 'cylindrical stereographic', 'eckert1', 'eckert2', 'eckert3', 'eckert4', 'eckert5', 'eckert6', 'eisenlohr', 'equal earth', 'equirectangular', 'fahey', 'foucaut', 'foucaut sinusoidal', 'ginzburg4', 'ginzburg5', 'ginzburg6', 'ginzburg8', 'ginzburg9', 'gnomonic', 'gringorten', 'gringorten quincuncial', 'guyou', 'hammer', 'hill', 'homolosine', 'hufnagel', 'hyperelliptical', 'kavrayskiy7', 'lagrange', 'larrivee', 'laskowski', 'loximuthal', 'mercator', 'miller', 'mollweide', 'mt flat polar parabolic', 'mt flat polar quartic', 'mt flat polar sinusoidal', 'natural earth', 'natural earth1', 'natural earth2', 'nell hammer', 'nicolosi', 'orthographic', 'patterson', 'peirce quincuncial', 'polyconic', 'rectangular polyconic', 'robinson', 'satellite', 'sinu mollweide', 'sinusoidal', 'stereographic', 'times', 'transverse mercator', 'van der grinten', 'van der grinten2', 'van der grinten3', 'van der grinten4', 'wagner4', 'wagner6', 'wiechel', 'winkel tripel', 'winkel3']