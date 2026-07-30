import streamlit as st
import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Meta -10kg by Luciano Bravo", page_icon="💪", layout="centered")

# TÍTULO PERSONALIZADO
st.title("💪 Meta -10kg by Luciano Bravo")
st.write("Versión Universal | Cálculo de Déficit Personalizado")

# 🧬 CONFIGURACIÓN DE TIPO DE CUERPO Y PERFIL
st.header("🧬 Perfil Corporal")
col_p1, col_p2 = st.columns(2)

with col_p1:
    genero = st.radio("Seleccioná tu género:", ("Hombre", "Mujer"))
    peso_inicial = st.number_input("¿Cuánto pesabas el primer día? (Peso Inicial):", min_value=40.0, max_value=200.0, value=96.0, step=0.1)
    peso_actual = st.number_input("Ingresá tu peso de hoy (kg):", min_value=40.0, max_value=200.0, value=96.0, step=0.1)

with col_p2:
    altura = st.number_input("Ingresá tu altura (metros):", min_value=1.20, max_value=2.30, value=1.77, step=0.01)
    edad = st.number_input("Ingresá tu edad:", min_value=15, max_value=100, value=30, step=1)

# 🧠 CÁLCULO CIENTÍFICO AUTOMÁTICO (Fórmula Harris-Benedict)
if genero == "Hombre":
    bmr = 66.47 + (13.75 * peso_actual) + (5.00 * (altura * 100)) - (6.75 * edad)
    deficit_ideal = 700  
else:
    bmr = 655.1 + (9.56 * peso_actual) + (1.85 * (altura * 100)) - (4.68 * edad)
    deficit_ideal = 500  

st.info(f"🧬 Tu cuerpo quema **{int(bmr)} kcal** al día solo por existir (Metabolismo Basal).  \n🎯 Tu déficit ideal recomendado es de **-{deficit_ideal} kcal** diarios.")

# ⚖️ BARRA DE PROGRESO DE PESO UNIVERSAL
meta_peso = peso_inicial - 10.0
kilos_bajados = peso_inicial - peso_actual

if kilos_bajados > 0:
    st.success(f"🎉 ¡Ya bajaste **{kilos_bajados:.1f} kg** desde que empezaste!")
    st.progress(min(kilos_bajados / 10.0, 1.0))
    st.write(f"Te faltan **{peso_actual - meta_peso:.1f} kg** para tu meta final de {meta_peso:.1f} kg.")
elif kilos_bajados == 0:
    st.info(f"Punto de partida: {peso_inicial} kg. ¡Hoy arranca el cambio!")
else:
    st.warning("Mantené la calma, el peso fluctúa por retención de agua. ¡Seguí firme!")

# Gráfico de peso interactivo adaptado
st.subheader("📉 Tu Curva de Descenso")
datos_peso = pd.DataFrame({
    "Días": ["Inicio", "Actual"],
    "Peso (kg)": [peso_inicial, peso_actual]
})
st.line_chart(datos_peso.set_index("Días"))

# 📅 CALENDARIO Y PASOS
st.header("📅 Registro del Día")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())

pasos = st.number_input("¿Cuántos pasos hiciste hoy?", min_value=0, value=14000, step=500)
kcal_pasos = int(pasos * 0.055)

# 💧 CONTROL DE HIDRATACIÓN
st.subheader("💧 Control de Hidratación")
vasos_agua = st.slider("¿Cuántos vasos de agua pura (250ml) tomaste hoy?", 0, 12, 4)

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
                character_id = f"{alimento}_{key_sufijo}"
                cantidad = st.number_input(f"Unidades de {alimento}:", min_value=0, value=1, step=1, key=character_id)
                total_kcal_dia += info["kcal"] * cantidad
                total_prot_dia += info["prot"] * cantidad

st.header("📝 Registro por Comidas")
procesar_bloque_comida("📸 Almuerzo", "almuerzo")
st.markdown("---")
procesar_bloque_comida("🥛 Merienda", "merienda")
st.markdown("---")

st.subheader("🍎 Registro de Frutas")
frutas = st.number_input("¿Cuántas frutas enteras comiste hoy?", min_value=0, value=0, step=1)
total_kcal_dia += (frutas * 60)
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
    gasto_total = int(bmr) + kcal_pasos
    deficit_real = gasto_total - total_kcal_dia
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Calorías Consumidas", value=f"{int(total_kcal_dia)} kcal")
        st.metric(label="Proteínas Totales", value=f"{int(total_prot_dia)} g")
    with col_b:
        st.metric(label="Gasto Diario Total", value=f"{gasto_total} kcal")
        st.metric(label="Déficit Real Logrado", value=f"{int(deficit_real)} kcal")
    
    st.subheader("💡 Análisis de tu IA:")
    st.write(f"🎯 Tu meta de déficit ideal es de: **{deficit_ideal} kcal**.")
    
    if deficit_real >= deficit_ideal:
        st.success(f"🔥 ¡Espectacular! Lograste un déficit de {int(deficit_real)} kcal, superando tu meta ideal de {deficit_ideal} kcal.")
    else:
        st.warning(f"⚠️ Hoy tu déficit fue de {int(deficit_real)} kcal (menor al ideal de {deficit_ideal} kcal).")
        
    if total_prot_dia < (peso_actual * 1.2):
        st.warning(f"⚠️ Estás bajo en proteínas ({int(total_prot_dia)}g). Intentá subir el consumo de carnes o huevos para proteger tu masa muscular.")
    else:
        st.success("💪 ¡Nivel de proteína óptimo! Tus músculos están blindados según tu tipo de cuerpo.")
        
    if deficit_real >= deficit_ideal and sin_harina_azucar and total_prot_dia >= (peso_actual * 1.2):
        st.balloons()
        st.success(f"🏆 ¡Día Perfecto de Recomposición registrado para el {fecha_seleccionada.strftime('%d/%m/%Y')}!")

