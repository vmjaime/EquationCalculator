import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Función para resolver ecuaciones cuadráticas
def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        x1 = (-b + discriminant ** 0.5) / (2 * a)
        x2 = (-b - discriminant ** 0.5) / (2 * a)
        return x1, x2
    elif discriminant == 0:
        x = -b / (2 * a)
        return x, None
    else:
        return None, None

# Configuración de la página
st.set_page_config(page_title="Calculadora de Ecuaciones Cuadráticas", page_icon=":1234:")

# Título de la aplicación
st.title("Calculadora de Ecuaciones Cuadráticas")

# Formulario para ingresar coeficientes
st.sidebar.header("Ingrese los coeficientes:")
a = st.sidebar.number_input("Coeficiente a", step=0.1)
b = st.sidebar.number_input("Coeficiente b", step=0.1)
c = st.sidebar.number_input("Coeficiente c", step=0.1)

# Resolver ecuación cuadrática y mostrar resultados
if st.sidebar.button("Resolver"):
    x1, x2 = solve_quadratic(a, b, c)
    if x1 is not None and x2 is not None:
        st.success(f"Las soluciones son: x1 = {x1} y x2 = {x2}")
    elif x1 is not None:
        st.success(f"La solución doble es: x = {x1}")
    else:
        st.error("La ecuación no tiene soluciones reales")

    # Graficar la ecuación cuadrática
    x = np.linspace(-10, 10, 400)
    y = a * x ** 2 + b * x + c
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, color='blue', label=f'{a}x^2 + {b}x + {c}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gráfica de la Ecuación Cuadrática')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    st.pyplot(plt)

