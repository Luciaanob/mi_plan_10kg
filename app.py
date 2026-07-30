import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Mi Plan 10kg - Tracker", page_icon="💪", layout="centered")

st.titlest.title("💪 Meta -10kg by Luciano Bravo")

st.write("Cálculo por Comidas | 96kg | 14.000 pasos | Cero Harinas")

# 📅 CALENDARIO
st.header("📅 Seleccionar Fecha")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())

# 🚶‍♂️ PASOS
st.header("🚶‍♂️ Tus 14.000 Pasos")
pasos = st.number_input("¿Cuántos pasos hiciste hoy?", min_value=0, value=14000, step=500)
kcal_pasos = int(pasos * 0.055)

# 🥑 BASE DE DATOS DE ALIMENTOS
base_alimentos = {
    "Pollo (Pechuga/Muslo)": {"kcal": 165, "prot": 31, "unidad": "100g"},
    "Carne de Vaca (Cortes magros)": {"kcal": 200, "prot": 26, "unidad": "100g"},
    "Carne de Cerdo (Costillita/Bondiola)": {"kcal": 240, "prot": 27, "unidad": "100g"},
    "Pescado de mar (Merluza/Gatuzo)": {"kcal": 90, "prot": 19, "unidad": "100g"},
    "Atún al natural (Lata)": {"kcal": 116, "prot": 26, "unidad": "100g"},
    "Huevo hervido (Unidad)": {"kcal": 70, "prot": 6, "unidad": "unidad"},
    "Papa o Batata hervida": {"kcal": 87, "prot": 2, "unidad": "100g"},
    "Calabaza/Zapallo al horno o puré": {"kcal": 30, "prot": 1, "unidad": "100g"},
    "Lentejas/Garbanzos/Porotos": {"kcal": 116, "prot": 9, "unidad": "100g"},
    "Quinoa cocida": {"kcal": 120, "prot": 4, "unidad": "100g"},
    "Mandarina (Unidad)": {"kcal": 45, "prot": 1, "unidad": "unidad"},
    "Banana (Unidad)": {"kcal": 105, "prot": 1, "unidad": "unidad"},
    "Manzana/Pera/Naranja (Unidad)": {"kcal": 60, "prot": 0.5, "unidad": "unidad"},
    "Brócoli/Zanahoria/Tomate/Zucchini": {"kcal": 30, "prot": 2, "unidad": "100g"},
    "Verduras de hoja (Lechuga/Acelga)": {"kcal": 15, "prot": 1, "unidad": "100g"},
    "Whey Protein (1 scoop)": {"kcal": 120, "prot": 24, "unidad": "unidad"},
    "Leche descremada (Vaso 200ml)": {"kcal": 90, "prot": 7, "unidad": "unidad"},
}

# Variables globales para sumar todo
total_kcal_dia = 0
total_prot_dia = 0

# Función secundaria para procesar alimentos por bloque de comida
def procesar_bloque_comida(titulo_bloque, key_sufijo):
    global total_kcal_dia, total_prot_dia
    st.subheader(titulo_bloque)
    elegidos = st.multiselect(f"¿Qué sumaste en tu {titulo_bloque.lower()}?", list(base_alimentos.keys()), key=f"select_{key_sufijo}")
    
    if elegidos:
        for alimento in elegidos:
            info = base_alimentos[alimento]
            if info["unidad"] == "100g":
                cantidad = st.number_input(f"Gramos de {alimento}:", min_value=0, value=150, step=50, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += (info["kcal"] * cantidad) / 100
                total_prot_dia += (info["prot"] * cantidad) / 100
            else:
                cantidad = st.number_input(f"Unidades de {alimento}:", min_value=0, value=1, step=1, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += info["kcal"] * cantidad
                total_prot_dia += info["prot"] * cantidad

# 📝 SECCIONES DE COMIDAS SEPARADAS
st.header("📝 Registro por Comidas")

# 1. Almuerzo
procesar_bloque_comida("📸 Almuerzo", "almuerzo")
st.markdown("---")

# 2. Merienda
procesar_bloque_comida("🥛 Merienda", "merienda")
st.markdown("---")

# 3. Cena
procesar_bloque_comida("🥩 Cena", "cena")
st.markdown("---")

# ⚠️ FILTRO ESTRICTO
st.subheader("⚠️ Filtro de Reglas")
sin_harina_azucar = st.checkbox("❌ Confirmo que comí CERO Harinas y Cero Azúcares hoy")

# ⏱️ CONTROL DE AYUNO
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
        st.warning(f"⚠️ Estás en {int(total_prot_dia)}g de proteína. Intentá llegar a más de 85g para cuidar el músculo.")
    else:
        st.success("💪 ¡Espectacular nivel de proteína! Masa muscular 100% protegida.")
        
    if not sin_harina_azucar:
        st.error("🚨 Cuidado con las harinas o azúcares anotados.")
        
    if deficit > 1000 and sin_harina_azucar and total_prot_dia >= 85:
        st.balloons()
        st.success(f"🏆 ¡Día Perfecto registrado para el {fecha_seleccionada.strftime('%d/%m/%Y')}!")
