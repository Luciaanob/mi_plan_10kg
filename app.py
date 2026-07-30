import streamlit as st
import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Meta -10kg by Luciano Bravo", page_icon="💪", layout="centered")

# TÍTULO PERSONALIZADO
st.title("💪 Meta -10kg by Luciano Bravo")
st.write("Versión Premium v2.1 | 96kg Inicial | 14.000 pasos | Cero Harinas")

# 📅 CALENDARIO
st.header("📅 Seleccionar Fecha")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())

# ⚖️ CONTROL DE PESO DIARIO Y GRÁFICO
st.header("⚖️ Control de Peso")
peso_actual = st.number_input("Ingresá tu peso de hoy (kg):", min_value=50.0, max_value=150.0, value=96.0, step=0.1)

peso_inicial = 96.0
meta_peso = 86.0
kilos_bajados = peso_inicial - peso_actual

if kilos_bajados > 0:
    st.success(f"🎉 ¡Ya bajaste **{kilos_bajados:.1f} kg** desde que empezaste!")
    st.progress(min(kilos_bajados / 10.0, 1.0))
    st.write(f"Te faltan **{peso_actual - meta_peso:.1f} kg** para tu meta final de 86 kg.")
elif kilos_bajados == 0:
    st.info("Punto de partida: 96 kg. ¡Hoy arranca el cambio!")
else:
    st.warning("Mantené la calma y seguí firme con el déficit, el peso fluctúa por agua.")

# Gráfico de peso
st.subheader("📉 Tu Curva de Descenso")
datos_peso = pd.DataFrame({
    "Días": ["Inicio", "Actual"],
    "Peso (kg)": [peso_inicial, peso_actual]
})
st.line_chart(datos_peso.set_index("Días"))

# 🚶‍♂️ PASOS
st.header("🚶‍♂️ Tus 14.000 Pasos")
pasos = st.number_input("¿Cuántos pasos hiciste hoy?", min_value=0, value=14000, step=500)
kcal_pasos = int(pasos * 0.055)

# 💧 CONTROL DE HIDRATACIÓN
st.header("💧 Control de Hidratación")
vasos_agua = st.slider("¿Cuántos vasos de agua pura (250ml) tomaste hoy?", 0, 12, 4)
if vasos_agua < 8:
    st.warning("⚠️ Intentá llegar a 8 vasos diarios para limpiar tu organismo y rendir más al caminar.")
else:
    st.success("😎 ¡Excelente nivel de hidratación para tus riñones!")

# 🥑 BASE DE DATOS DE ALIMENTOS
base_alimentos = {
    "Pollo (Pechuga/Muslo)": {"kcal": 165, "prot": 31, "unidad": "100g"},
    "Carne de Vaca (Cortes magros)": {"kcal": 200, "prot": 26, "unidad": "100g"},
    "Carne de Cerdo (Costillita/Bondiola)": {"kcal": 240, "prot": 27, "unidad": "100g"},
    "Pescado de mar (Merluza/Gatuzo)": {"kcal": 90, "prot": 19, "unidad": "100g"},
    "Atún al natural (Lata)": {"kcal": 116, "prot": 26, "unidad": "100g"},
    "Huevo hervido (Unidad)": {"kcal": 70, "prot": 6, "unidad": "unidad"},
    "Queso Cremoso / Por Salut / Mozzarella": {"kcal": 260, "prot": 20, "unidad": "100g"},
    "Queso Rallado / Reggianito / Hebras": {"kcal": 390, "prot": 35, "unidad": "100g"},
    "Queso crema / Untable descremado": {"kcal": 100, "prot": 7, "unidad": "100g"},
    "Leche descremada (Vaso 200ml)": {"kcal": 90, "prot": 7, "unidad": "unidad"},
    "Whey Protein (1 scoop)": {"kcal": 120, "prot": 24, "unidad": "unidad"},
    "Papa o Batata hervida": {"kcal": 87, "prot": 2, "unidad": "100g"},
    "Calabaza/Zapallo al horno o puré": {"kcal": 30, "prot": 1, "unidad": "100g"},
    "Lentejas/Garbanzos/Porotos": {"kcal": 116, "prot": 9, "unidad": "100g"},
    "Quinoa cocida": {"kcal": 120, "prot": 4, "unidad": "100g"},
    "Brócoli/Zanahoria/Tomate/Zucchini": {"kcal": 30, "prot": 2, "unidad": "100g"},
    "Verduras de hoja (Lechuga/Acelga)": {"kcal": 15, "prot": 1, "unidad": "100g"},
}

total_kcal_dia = 0
total_prot_dia = 0

def procesar_bloque_comida(titulo_bloque, key_sufijo):
    global total_kcal_dia, total_prot_dia
    st.subheader(titulo_bloque)
    elegidos = st.multiselect(f"¿Qué sumaste en tu {titulo_bloque.lower()}?", list(base_alimentos.keys()), key=f"select_{key_sufijo}")
    
    if elegidos:
        for alimento in elegidos:
            info = base_alimentos[alimento]
            if info["unidad"] == "100g":
                cantidad = st.number_input(f"Gramos de {alimento}:", min_value=0, value=50 if "Queso" in alimento else 150, step=10 if "Queso" in alimento else 50, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += (info["kcal"] * cantidad) / 100
                total_prot_dia += (info["prot"] * cantidad) / 100
            else:
                cantidad = st.number_input(f"Unidades de {alimento}:", min_value=0, value=1, step=1, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += info["kcal"] * cantidad
                total_prot_dia += info["prot"] * cantidad

st.header("📝 Registro por Comidas")
procesar_bloque_comida("📸 Almuerzo", "almuerzo")
st.markdown("---")
procesar_bloque_comida("🥛 Merienda", "merienda")
st.markdown("---")

# 🍎 SECCIÓN CORREGIDA: CONTADOR GENERAL DE FRUTAS
st.subheader("🍎 Registro de Frutas")
frutas = st.number_input("¿Cuántas frutas enteras comiste hoy? (Mandarinas, manzanas, etc.)", min_value=0, value=0, step=1)
total_kcal_dia += (frutas * 60) # Promedio de calorías por fruta común
total_prot_dia += (frutas * 0.5)
st.markdown("---")

procesar_bloque_comida("📸 Cena", "cena")
st.markdown("---")

st.subheader("⚠️ Filtro de Reglas")
sin_harina_azucar = st.checkbox("❌ Confirmo que comí CERO Harinas y Cero Azúcares hoy")

st.header("⏱️ Control de Ayuno (14hs)")
hora_cena = st.time_input("¿A qué hora terminás de cenar?", datetime.time(22, 0))
hora_fin_ayuno = (datetime.datetime.combine(datetime.date.today(), hora_cena) + datetime.timedelta(hours=14)).time()
st.info(f"🔒 Tu ayuno termina mañana a las: **{hora_fin_ayuno.strftime('%H:%M')} hs**")

# 📊 BALANCE FINAL AUTOMÁTICO
st.header("📊 Tu Balance del Día")
if st.button("Calcular Resultados de Hoy"):
    gasto_total = 1920 + kcal_pasos
    deficit = gasto_total - total_kcal_dia
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Calorías Consumidas", value=f"{int(total_kcal_dia)} kcal")
        st.metric(label="Proteínas Totales", value=f"{int(total_prot_dia)} g")
    with col_b:
        st.metric(label="Gasto Diario Total", value=f"{gasto_total} kcal")
        st.metric(label="Déficit Logrado", value=f"{int(deficit)} kcal", delta=f"{int(deficit)} kcal")
    
    st.subheader("💡 Análisis de tu IA:")
    if total_prot_dia < 85:
        st.warning(f"⚠️ Estás bajo en proteínas ({int(total_prot_dia)}g). Recordá cuidar el músculo.")
    else:
        st.success("💪 ¡Nivel de proteína espectacular! Tus músculos están blindados.")
        
    if frutas > 4:
        st.warning("⚠️ Recordá que aunque las frutas sean sanas, comer más de 4 unidades al día suma azúcares naturales que pueden recortar tu déficit.")
        
    if deficit > 1000 and sin_harina_azucar and total_prot_dia >= 85:
        st.balloons()
        st.success(f"🏆 ¡Día Perfecto registrado para el {fecha_seleccionada.strftime('%d/%m/%Y')}! Estás quemando grasa a ritmo máximo.")
