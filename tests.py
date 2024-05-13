import plotly.express as px

# Obtener la lista de nombres de países reconocidos por Plotly
paises_reconocidos = px.data.gapminder()['country'].unique()

# Imprimir la lista de nombres de países reconocidos
print(paises_reconocidos)