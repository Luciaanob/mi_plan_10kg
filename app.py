import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Mi Plan 10kg - Tracker", page_icon="💪", layout="centered")

st.title("💪 Mi Tracker Personal: Meta -10kg")
st.write("Seguimiento diario para 96kg | 14.000 pasos | Cero Harinas")

# 1. SECCIÓN PASOS
st.header("🚶‍♂️ Tus 14.000 Pasos")
pasos = st.number_input("¿Cuántos pasos hiciste hoy?", min_value=0, value=14000, step=500)
if pasos >= 14000:
    st.success(f"¡Excelente! Quemaste aproximadamente {int(pasos * 0.055)} kcal extras.")
else:
    st.warning(f"¡Faltan {14000 - pasos} pasos para la meta diaria!")

# 2. SECCIÓN ALMUERZO GANADOR
st.header("🍽️ Almuerzo Ganador Check")
col1, col2 = st.columns(2)
with col1:
    proteina = st.checkbox("Proteína Sólida (Pollo/Cerdo/Huevo)")
    verdura = st.checkbox("Colchón de Verduras/Fibra")
with col2:
    carbo_limpio = st.checkbox("Carbohidrato Limpio o Fruta")
    sin_harina_azucar = st.checkbox("❌ Cero Harinas y Cero Azúcares")

if proteina and verdura and carbo_limpio and sin_harina_azucar:
    st.success("¡Almuerzo Perfecto de Manual! 🏆")

# 3. SECCIÓN MERIENDA Y CENA
st.header("🥛 Merienda y Cena")
whey = st.checkbox("Scoop de Whey Protein con leche descremada (19:00 hs)")
cena_limpia = st.checkbox("Cena Proteica y Limpia (Air Fryer)")

# 4. TEMPORIZADOR DE AYUNO (14 HS)
st.header("⏱️ Control de Ayuno (14hs)")
hora_cena = st.time_input("¿A qué hora terminás de cenar?", datetime.time(22, 0))
# Calcular hora de fin de ayuno
hora_fin_ayuno = (datetime.datetime.combine(datetime.date.today(), hora_cena) + datetime.timedelta(hours=14)).time()
st.info(f"🔒 Tu ayuno termina mañana a las: **{hora_fin_ayuno.strftime('%H:%M')} hs** (Recordá el mate con cáscara de mandarina).")

# 5. CÁLCULO DE BALANCE DIARIO
st.header("📊 Tu Balance del Día")
if st.button("Calcular Resultados de Hoy"):
    # Estimación calórica base
    gasto_total = 1920 + int(pasos * 0.055)
    
    # Consumo estimado según checks
    consumo = 0
    if proteina and carbo_limpio and verdura: consumo += 550
    if whey: consumo += 210
    if cena_limpia: consumo += 380
    
    deficit = gasto_total - consumo
    
    st.metric(label="Gasto Energético Total", value=f"{gasto_total} kcal")
    st.metric(label="Consumo Estimado", value=f"{consumo} kcal")
    st.metric(label="Déficit Logrado", value=f"{deficit} kcal", delta=f"{deficit} kcal", delta_color="normal")
    
    if deficit > 1200 and sin_harina_azucar:
        st.balloons()
        st.success("¡Día espectacular! Estás oxidando pura grasa y protegiendo tu músculo.")
