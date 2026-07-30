import streamlit as st
import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Tracker Personal - Meta -10kg", page_icon="💪", layout="centered")

# CREAR MEMORIA DE SESIÓN
if "historial_progreso" not in st.session_state:
    st.session_state["historial_progreso"] = []

# TÍTULO PERSONALIZADO
st.title("💪 Meta -10kg by Luciano Bravo")
st.write("Versión Coach Analítico v6.1 | Tu Entrenador de Precisión IA")

# ==========================================
# 1. 📅 SECCIÓN MAESTRA: CALENDARIO Y NOMBRE
# ==========================================
st.header("📅 Identificación y Fecha")
nombre_usuario = st.text_input("¿Cómo querés que te llame la app?:", value="Luciano Bravo")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())
st.write(f"Hola **{nombre_usuario}**, registrando para el día: **{fecha_seleccionada.strftime('%d/%m/%Y')}**")
st.markdown("---")

# ==========================================
# 2. 🧬 PERFIL CORPORAL ABIERTO POR DEFECTO
# ==========================================
with st.expander(f"🧬 Perfil Corporal de {nombre_usuario}", expanded=True):
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        genero = st.radio("Seleccioná tu género:", ("Hombre", "Mujer"))
        peso_inicial = st.number_input("¿Peso Inicial? (Primer día):", min_value=40.0, max_value=200.0, value=96.0, step=0.1)
    with col_p2:
        altura = st.number_input("Ingresá tu altura (metros):", min_value=1.20, max_value=2.30, value=1.77, step=0.01)
        edad = st.number_input("Ingresá tu edad:", min_value=15, max_value=100, value=39, step=1)

if genero == "Hombre":
    bmr = 66.47 + (13.75 * peso_inicial) + (5.00 * (altura * 100)) - (6.75 * edad)
    deficit_ideal = 700  
else:
    bmr = 655.1 + (9.56 * peso_inicial) + (1.85 * (altura * 100)) - (4.68 * edad)
    deficit_ideal = 500  

st.info(f"🧬 Tu cuerpo quema **{int(bmr)} kcal** al día solo por existir (Metabolismo Basal).  \n🎯 Tu déficit ideal recomendado es de **-{deficit_ideal} kcal** diarios.")

# ==========================================
# 3. ⚖️ CONTROL DE PESO DIARIO Y PROGRESO
# ==========================================
st.header("⚖️ Control de Peso")
peso_actual = st.number_input("Ingresá tu peso de hoy (kg):", min_value=40.0, max_value=200.0, value=95.0, step=0.1)

meta_peso = peso_inicial - 10.0
kilos_bajados = peso_inicial - peso_actual

if kilos_bajados > 0:
    st.success(f"🎉 ¡Ya bajaste **{kilos_bajados:.1f} kg** desde que empezaste!")
    st.progress(min(kilos_bajados / 10.0, 1.0))
    st.write(f"Te faltan **{peso_actual - meta_peso:.1f} kg** para tu meta final de {meta_peso:.1f} kg.")
else:
    st.info(f"Punto de partida: {peso_inicial} kg. ¡Hoy arranca el cambio!")

# Gráfico interactivo
datos_peso = pd.DataFrame({
    "Días": ["Inicio", "Actual"],
    "Peso (kg)": [peso_inicial, peso_actual]
})
st.line_chart(datos_peso.set_index("Días"))
st.markdown("---")

# ==========================================
# 4. 🚶‍♂️ PASOS Y HIDRATACIÓN
# ==========================================
st.header("🚶‍♂️ Actividad del Día")
pasos = st.number_input("¿Cuántos pasos hiciste hoy?", min_value=0, value=14000, step=500)
kcal_pasos = int(pasos * 0.055)

st.subheader("💧 Control de Hidratación")
vasos_agua = st.slider("¿Cuántos vasos de agua (250ml) tomaste hoy?", 0, 12, 4)
st.markdown("---")

# ==========================================
# 5. 🥑 REGISTRO DE ALIMENTOS
# ==========================================
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

# Diccionario para trackear cantidades totales hoy
cantidades_totales = {}

def procesar_bloque_comida(titulo_bloque, key_sufijo):
    global total_kcal_dia, total_prot_dia, cantidades_totales
    st.subheader(titulo_bloque)
    elegidos = st.multiselect(f"¿Qué sumaste en tu {titulo_bloque.lower()}?", list(base_alimentos.keys()), key=f"select_{key_sufijo}")
    
    if elegidos:
        for alimento in elegidos:
            info = base_alimentos[alimento]
            if info["unidad"] == "100g":
                cantidad = st.number_input(f"Gramos de {alimento}:", min_value=0, value=50 if "Queso" in alimento else 150, step=10 if "Queso" in alimento else 50, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += (info["kcal"] * cantidad) / 100
                total_prot_dia += (info["prot"] * cantidad) / 100
                cantidades_totales[alimento] = cantidades_totales.get(alimento, 0) + cantidad
            else:
                cantidad = st.number_input(f"Unidades de {alimento}:", min_value=0, value=1, step=1, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += info["kcal"] * cantidad
                total_prot_dia += info["prot"] * cantidad
                cantidades_totales[alimento] = cantidades_totales.get(alimento, 0) + cantidad

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

procesar_bloque_comida("📸 Cene", "cena")
st.markdown("---")

st.subheader("⚠️ Filtro de Reglas")
sin_harina_azucar = st.checkbox("❌ Confirmo que comí CERO Harinas y Cero Azúcares hoy")

st.header("⏱️ Control de Ayuno (14hs)")
hora_cena = st.time_input("¿A qué hora terminás de cenar?", datetime.time(22, 0))
hora_fin_ayuno = (datetime.datetime.combine(datetime.date.today(), hora_cena) + datetime.timedelta(hours=14)).time()
st.info(f"🔒 Tu ayuno termina mañana a las: **{hora_fin_ayuno.strftime('%H:%M')} hs**")

# ==========================================
# 6. 📊 BALANCE Y AUDITORÍA DE EXCESOS
# ==========================================
st.header("📊 Tu Balance del Día")
if st.button("Calcular y Registrar Día"):
    gasto_total = int(bmr) + kcal_pasos
    deficit_real = gasto_total - total_kcal_dia
    
    nuevo_registro = {
        "Fecha": fecha_seleccionada.strftime('%d/%m/%Y'),
        "Usuario": nombre_usuario,
        "Peso (kg)": peso_actual,
        "Pasos": pasos,
        "Consumo (kcal)": int(total_kcal_dia),
        "Proteínas (g)": int(total_prot_dia),
        "Déficit (kcal)": int(deficit_real)
    }
    st.session_state["historial_progreso"] = [r for r in st.session_state["historial_progreso"] if r["Fecha"] != nuevo_registro["Fecha"]]
    st.session_state["historial_progreso"].append(nuevo_registro)
    
    st.metric(label="Calorías Consumidas", value=f"{int(total_kcal_dia)} kcal")
    st.metric(label="Proteínas Totales", value=f"{int(total_prot_dia)} g")
    st.metric(label="Déficit Real Logrado", value=f"{int(deficit_real)} kcal")
    
    st.markdown("---")
    st.subheader(f"🤖 Análisis Específico del Coach IA para {nombre_usuario}:")
    
    excesos_detectados = []
    
    if cantidades_totales.get("Huevo hervido (Unidad)", 0) > 3:
        cant_h = cantidades_totales["Huevo hervido (Unidad)"]
        excesos_detectados.append(f"🥚 **Huevos ({int(cant_h)} unidades):** Te sobrepasaste. Deberías haber comido entre **2 y 3 unidades** como máximo. Ingerir tantos satura tu digestión.")
    
    for carne in ["Pollo (Pechuga/Muslo)", "Carne de Vaca (Cortes magros)", "Carne de Cerdo (Costillita/Bondiola)"]:
        if cantidades_totales.get(carne, 0) > 400:
            cant_c = cantidades_totales[carne]
            excesos_detectados.append(f"🥩 **{carne} ({int(cant_c)}g):** Te excediste con la porción. Comer más de 400g aporta más proteína de la que asimilás. Tu porción ideal sería de **150g a 250g** por comida.")
            
    if cantidades_totales.get("Queso Cremoso / Por Salut / Mozzarella", 0) > 150 or cantidades_totales.get("Queso Rallado / Reggianito / Hebras", 0) > 80:
        excesos_detectados.append(f"🧀 **Quesos:** Te pasaste con los lácteos grasos. Deberías limitar el queso rallado a **15g-30g** y el cremoso a **30g-50g**. El exceso suma muchas calorías ocultas.")

    if frutas > 3:
        excesos_detectados.append(f"🍎 **Frutas ({int(frutas)} unidades):** Te sobrepasaste. Comer más de 3 aporta exceso de fructosa (azúcar natural) que frena el déficit calórico. Lo ideal son **1 o 2 unidades** al día.")

    if excesos_detectados:
        st.error("🚨 **Análisis de porciones superadas hoy:**")
        for exceso in excesos_detectados:
            st.write(exceso)
        st.markdown("  \n*Consejo:* Si fue un error al tipear probando la app, ¡limpiá los campos y cargá tu porción real! 💪")
