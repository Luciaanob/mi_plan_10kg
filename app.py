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
st.write("Versión Coach Sincero v5.3 | Tu Entrenador Personal IA")

# ==========================================
# 1. 📅 SECCIÓN MAESTRA: CALENDARIO Y NOMBRE
# ==========================================
st.header("📅 Identificación y Fecha")
nombre_usuario = st.text_input("¿Cómo querés que te llame la app?:", value="Luciano Bravo")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())
st.write(f"Hola **{nombre_usuario}**, registrando para el día: **{fecha_seleccionada.strftime('%d/%m/%Y')}**")
st.markdown("---")

# ==========================================
# 2. 🧬 PERFIL CORPORAL ABIERTO POR DEFECTO (CORREGIDO)
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

# ==========================================
# 6. 📊 BALANCE Y FUNCIÓN DE GUARDADO/DESCARGA
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
    st.subheader(f"🤖 Recomendaciones de tu Coach IA para {nombre_usuario}:")
    
    if deficit_real > 1200:
        st.error(f"🚨 **¡Cuidado, {nombre_usuario}! El déficit es peligrosamente alto ({int(deficit_real)} kcal).**  \nEsto suele pasar porque comiste extremadamente poco hoy o por un error al cargar las cantidades de comida. ¡Mañana asegurate de comer buen volumen de comida limpia!")
    elif deficit_real >= deficit_ideal:
        st.success(f"🔥 ¡Espectacular! Lograste un déficit de {int(deficit_real)} kcal, cumpliendo tu meta ideal de -{deficit_ideal} kcal.")
    else:
        st.warning(f"⚠️ Hoy tu déficit fue menor al ideal recomendado. Intentá ajustar un poco más las porciones mañana.")

    if not sin_harina_azucar:
        st.error(f"⚠️ **Reglas:** Hoy se escapó alguna harina o azúcar. ¡Mañana volvemos al camino limpio!")
    else:
        st.success(f"✅ **Reglas:** Mantuviste las harinas y azúcares en CERO absoluto.")

    meta_proteina = peso_actual * 1.2
    if total_prot_dia < meta_proteina:
        st.warning(f"🍗 **Proteína baja:** Llegaste a {int(total_prot_dia)}g. Tu cuerpo te pide {int(meta_proteina)}g. Mañana reforzá sumando carnes, huevos o Whey Protein.")

# MOSTRAR HISTORIAL
if st.session_state["historial_progreso"]:
    st.markdown("---")
    st.header("🗂️ Historial Guardado (Esta Sesión)")
    df_historial = pd.DataFrame(st.session_state["historial_progreso"])
    st.dataframe(df_historial)
    
    csv = df_historial.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar todo mi Historial (.csv)",
        data=csv,
        file_name=f"historial_peso_{nombre_usuario}.csv",
        mime="text/csv",
    )
