import streamlit as st
import datetime
import pandas as pd

# --- [EL CÓDIGO HA SIDO REVISADO Y CORREGIDO PARA STREAMLIT] ---
# Configuración de la página
st.set_page_config(page_title="Meta -10kg by Luciano Bravo", page_icon="💪", layout="centered")

# CREAR MEMORIA DE SESIÓN
if "historial_progreso" not in st.session_state:
    st.session_state["historial_progreso"] = []

# TÍTULO PERSONALIZADO
st.title("💪 Meta -10kg by Luciano Bravo")
st.write("Versión Estable v8.5 | Tu Entrenador de Precisión IA")

# 1. 📅 SECCIÓN MAESTRA: CALENDARIO Y NOMBRE
st.header("📅 Identificación y Fecha")
nombre_usuario = st.text_input("¿Cómo querés que te llame la app?", value="Luciano Bravo")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())
st.markdown("---")

# 2. 🧬 PERFIL CORPORAL
with st.expander(f"🧬 Perfil Corporal de {nombre_usuario}", expanded=True):
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        genero = st.radio("Seleccioná tu género:", ("Hombre", "Mujer"))
        peso_inicial = st.number_input("¿Peso Inicial? (kg):", min_value=40.0, max_value=200.0, value=96.0)
        peso_actual = st.number_input("Ingresá tu peso de hoy (kg):", min_value=40.0, max_value=200.0, value=95.0)
    with col_p2:
        altura = st.number_input("Altura (metros):", min_value=1.20, max_value=2.30, value=1.77, step=0.01)
        edad = st.number_input("Edad:", min_value=15, max_value=100, value=39)

# Cálculo BMR
if genero == "Hombre":
    bmr = 66.47 + (13.75 * peso_inicial) + (5.00 * (altura * 100)) - (6.75 * edad)
    deficit_ideal = 700  
else:
    bmr = 655.1 + (9.56 * peso_inicial) + (1.85 * (altura * 100)) - (4.68 * edad)
    deficit_ideal = 500  
st.info(f"🧬 Metabolismo Basal: ~{int(bmr)} kcal/día. 🎯 Déficit sugerido: -{deficit_ideal} kcal.")

# 3. ⚖️ PROGRESO DE PESO
kilos_bajados = peso_inicial - peso_actual
if kilos_bajados > 0:
    st.success(f"🎉 ¡Bajaste **{kilos_bajados:.1f} kg**! Meta: -10kg.")
    st.progress(min(kilos_bajados / 10.0, 1.0))
else:
    st.info(f"Punto de partida: {peso_inicial} kg. ¡Arranca el cambio!")

# 4. 🚶‍♂️ PASOS Y AGUA
st.header("🚶‍♂️ Actividad")
pasos = st.number_input("¿Pasos hoy?", min_value=0, value=14000, step=500)
vasos_agua = st.slider("💧 Vasos de agua (250ml)", 0, 12, 4)

# 5. 🥑 REGISTRO DE ALIMENTOS
base_alimentos = {
    "Pollo": {"kcal": 165, "prot": 31, "unidad": "100g"},
    "Carne Magra": {"kcal": 200, "prot": 26, "unidad": "100g"},
    "Huevo": {"kcal": 70, "prot": 6, "unidad": "unidad"},
    "Verduras": {"kcal": 30, "prot": 2, "unidad": "100g"},
    "Fruta": {"kcal": 60, "prot": 0.5, "unidad": "unidad"}
}
st.header("📝 Registro de Comidas")
total_kcal = 0
total_prot = 0
items = st.multiselect("Seleccioná qué comiste hoy:", list(base_alimentos.keys()))

for item in items:
    info = base_alimentos[item]
    if info["unidad"] == "100g":
        cant = st.number_input(f"Gramos de {item}:", min_value=0, value=100, step=10, key=f"{item}_g")
        total_kcal += (info["kcal"] * cant) / 100
        total_prot += (info["prot"] * cant) / 100
    else:
        cant = st.number_input(f"Cantidad de {item}:", min_value=0, value=1, step=1, key=f"{item}_u")
        total_kcal += info["kcal"] * cant
        total_prot += info["prot"] * cant

st.markdown("---")
sin_harina = st.checkbox("❌ CERO Harinas y Azúcares")

# 6. 📊 BALANCE FINAL
if st.button("📊 CALCULAR DÍA"):
    gasto_pasos = int(pasos * 0.055)
    deficit_real = (int(bmr) + gasto_pasos) - int(total_kcal)
    st.metric(label="Déficit Calórico Final", value=f"{deficit_real} kcal")
    
    if deficit_real > 1200:
        st.error("⚠️ Déficit extremo. ¡Comé un poco más!")
    elif deficit_real >= deficit_ideal:
        st.success("🔥 ¡Excelente balance! Objetivo cumplido.")
    else:
        st.warning("⚠️ Ajustá las porciones mañana.")

    if not sin_harina:
        st.error("🚨 ¡Se escaparon harinas/azúcar! Fuerza mañana.")
    else:
        st.success("✅ Disciplina impecable.")

# 7. 💾 HISTORIAL
if st.session_state["historial_progreso"]:
    st.markdown("---")
    st.header("🗂️ Historial")
    st.dataframe(pd.DataFrame(st.session_state["historial_progreso"]))
