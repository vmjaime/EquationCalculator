import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# ------- FUNCIONES DE FORMATO --------
def format_term(coef, var="", is_first=False):
    if coef == 0:
        return ""
    if coef == 1:
        return f"{'' if is_first else '+ '}{var}"
    elif coef == -1:
        return f"{'-' if is_first else '- '}{var}"
    else:
        sign = "+" if coef > 0 else "-"
        return f"{'' if is_first and coef > 0 else sign + ' '}{abs(coef)}{var}"

def format_expression(a, b, c):
    return f"{format_term(a, 'x²', True)} {format_term(b, 'x')} {format_term(c)}".strip()

def format_sign(num):
    return f"+ {abs(num)}" if num > 0 else f"- {abs(num)}"

# ------- FACTORIZACIÓN --------
def factorize_quadratic(a, b, c):
    a, b, c = int(a), int(b), int(c)

    if c == 0:
        st.write("1. La ecuación tiene un término constante igual a 0.")
        return f"{a}x(x {format_sign(b / a)})"

    if a != 1 and b % a == 0 and c % a == 0:
        st.write(f"2. Extraemos el factor común {a} de la ecuación.")
        b_new, c_new = b // a, c // a
        st.write(f"Esto da: {a}(x² {format_sign(b_new)}x {format_sign(c_new)})")
        return factorize_quadratic(1, b_new, c_new)

    if b ** 2 - 4 * a * c == 0 and a != 1:
        raiz_a = math.isqrt(abs(a))
        raiz_c = math.isqrt(abs(c))
        st.write(f"3. La ecuación es una diferencia de cuadrados: ({raiz_a}x)^2 - ({raiz_c})^2")
        return f"({raiz_a}x + {raiz_c})({raiz_a}x - {raiz_c})"

    if a == 1:
        st.write("4. Trinomio de la forma x² + bx + c:")
        for i in range(-int(abs(c)), int(abs(c)) + 1):
            for j in range(-int(abs(b)), int(abs(b)) + 1):
                if i * j == c and i + j == b:
                    return f"(x {format_sign(i)})(x {format_sign(j)})"

    st.write("5. Trinomio con a ≠ 1:")
    for i in range(-int(abs(a * c)), int(abs(a * c)) + 1):
        for j in range(-int(abs(a * c)), int(abs(a * c)) + 1):
            if i * j == a * c and i + j == b:
                return f"({a}x {format_sign(j)})({a}x {format_sign(i)})"

    return "No se puede factorizar directamente."

# ------- FÓRMULA GENERAL --------
def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return x1, x2, discriminant, "fórmula general"
    elif discriminant == 0:
        x = -b / (2 * a)
        return x, None, discriminant, "fórmula general"
    else:
        return None, None, discriminant, None

# ------- CONFIGURACIÓN DE LA APP --------
st.set_page_config(page_title="Calculadora Cuadrática", page_icon="🧮")
st.title("🧮 Calculadora de Ecuaciones Cuadráticas")
st.markdown("Ingresa los coeficientes de la ecuación cuadrática en la barra lateral.")

# ------- ENTRADA DE DATOS --------
st.sidebar.header("🎯 Ingrese los coeficientes:")
st.sidebar.markdown("**Nota:** ubicar los coeficientes en números enteros.")
origen = st.sidebar.radio("¿De dónde provienen los coeficientes?", ('Fórmula', 'Valor dado'))

a = st.sidebar.number_input("Coeficiente a", step=1, format="%d")
b = st.sidebar.number_input("Coeficiente b", step=1, format="%d")
c = st.sidebar.number_input("Coeficiente c", step=1, format="%d")

st.sidebar.write(f"Los coeficientes provienen de: {origen}")

# ------- BOTÓN DE RESOLUCIÓN --------
if st.sidebar.button("Resolver"):
    a, b, c = int(a), int(b), int(c)

    st.divider()
    st.subheader("🧾 Paso a paso de la resolución")

    st.markdown(f"**Ecuación original:**")
    st.latex(format_expression(a, b, c) + "= 0")

    factored = factorize_quadratic(a, b, c)

    if "No se puede" not in factored:
        st.success(f"✨ Factorización: {factored}")
    else:
        st.warning("No se pudo factorizar directamente. Usaremos la fórmula general:")
        st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
        x1, x2, discriminant, method = solve_quadratic(a, b, c)

        st.write(f"Discriminante: {discriminant}")
        if discriminant > 0:
            st.info(f"Soluciones reales distintas: x₁ = {x1}, x₂ = {x2}")
        elif discriminant == 0:
            st.info(f"Solución doble: x = {x1}")
        else:
            st.error("La ecuación no tiene soluciones reales.")

    # ------- GRÁFICO --------
    st.divider()
    st.subheader("📈 Gráfica de la función")

    x_vals = np.arange(-10, 11, 1)
    y_vals = a * x_vals ** 2 + b * x_vals + c

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, color='#1f77b4', linewidth=2.5, label=f'{format_expression(a, b, c)}')
    plt.fill_between(x_vals, y_vals, alpha=0.1, color='#1f77b4')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gráfica de la Ecuación Cuadrática')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(np.arange(-10, 11, 1))
    plt.legend()
    st.pyplot(plt)

    # ------- RAÍCES --------
    st.divider()
    st.subheader("📌 Raíces de la Ecuación:")
    x1, x2, _, _ = solve_quadratic(a, b, c)
    if x1 is not None:
        if x2 is None:
            st.write(f"La solución doble es: x = {x1}")
        else:
            st.write(f"Las soluciones reales son: x₁ = {x1}, x₂ = {x2}")
    else:
        st.write("No hay raíces reales (soluciones imaginarias).")
