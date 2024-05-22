import numpy as np
import pandas as pd

# Definir los pesos iniciales y el bias
w = np.array([0.2, 0.3, 0.4])
b = 0.01

# Definir la tasa de aprendizaje
alpha = 0.1

# Definir la tabla de datos como un DataFrame vacío
columns = ['epoch', 'X1', 'X2', 'X3', 'valor_esperado',
           'y_pred', 'error', 'w1', 'w2', 'w3']
tabla_datos = pd.DataFrame(columns=columns)

# Definir la función de activación step


def step(z):
    return 1 if z >= 0 else 0

# Definir la función para calcular el valor predicho


def predecir(x):
    z = np.dot(w, x) + b
    return step(z)


# Definir los datos de entrada para la puerta AND de 3 entradas
datos_entrada = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
])

# Definir los valores esperados para la puerta AND de 3 entradas
valores_esperados = np.array([0, 0, 0, 0, 0, 0, 0, 1])

# Entrenamiento del perceptrón
for epoch in range(20000000):  # Número máximo de epochs
    todos_correctos = True
    for i, entrada in enumerate(datos_entrada):
        # Calcular predicción
        y_pred = predecir(entrada)

        # Calcular error
        error = valores_esperados[i] - y_pred

        # Actualizar pesos si hay error
        if error != 0:
            w += alpha * error * entrada
            todos_correctos = False

        # Guardar en la tabla de datos como un nuevo registro en el DataFrame
        fila = pd.DataFrame([[epoch, entrada[0], entrada[1], entrada[2],
                            valores_esperados[i], y_pred, error, w[0], w[1], w[2]]], columns=columns)
        tabla_datos = pd.concat([tabla_datos, fila], ignore_index=True)

    # Si todos los ejemplos están clasificados correctamente, detener el entrenamiento
    if todos_correctos:
        break

# Mostrar la tabla de datos al finalizar
print("Tabla de datos (epoch, X1, X2, X3, valor esperado, real, error, w1, w2, w3):")
print(tabla_datos)
