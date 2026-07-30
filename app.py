import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Mi Plan 10kg - Tracker", page_icon="💪", layout="centered")

st.title("💪 Mi Tracker Inteligente: Meta -10kg")
st.write("Cálculo Automático de Calorías y Proteínas para 96kg | 14.000 pasos")

# 📅 CALENDARIO
st.header("📅 Seleccionar Fecha")
fecha_seleccionada = st.date_input("¿Qué día querés registrar?", datetime.date.today())

# 🚶‍♂️ PASOS
st.header("🚶‍♂️ Tus 14.000 Pasos")
pasos = st.number_input("¿Cuántos pasos hiciste hoy?", min_value=0, value=14000, step=500)
kcal_pasos = int(pasos * 0.055)

# 🥑 BASE DE DATOS AMPLIADA (Carnes, pescados, huevos, frutas y verduras)
base_alimentos = {
    # PROTEÍNAS ANIMALES
    "Pollo (Pechuga/Muslo)": {"kcal": 165, "prot": 31, "unidad": "100g"},
    "Carne de Vaca (Cortes magros)": {"kcal": 200, "prot": 26, "unidad": "100g"},
    "Carne de Cerdo (Costillita/Bondiola)": {"kcal": 240, "prot": 27, "unidad": "100g"},
    "Pescado de mar (Merluza/Gatuzo)": {"kcal": 90, "prot": 19, "unidad": "100g"},
    "Atún al natural (Lata)": {"kcal": 116, "prot": 26, "unidad": "100g"},
    "Huevo hervido (Unidad)": {"kcal": 70, "prot": 6, "unidad": "unidad"},
    
    # CARBOHIDRATOS LIMPIOS Y LEGUMBRES
    "Papa o Batata hervida": {"kcal": 87, "prot": 2, "unidad": "100g"},
    "Calabaza/Zapallo al horno o puré": {"kcal": 30, "prot": 1, "unidad": "100g"},
    "Lentejas/Garbanzos/Porotos": {"kcal": 116, "prot": 9, "unidad": "100g"},
    "Quinoa cocida": {"kcal": 120, "prot": 4, "unidad": "100g"},
    
    # FRUTAS
    "Mandarina (Unidad)": {"kcal": 45, "prot": 1, "unidad": "unidad"},
    "Banana (Unidad)": {"kcal": 105, "prot": 1, "unidad": "unidad"},
    "Manzana/Pera/Naranja (Unidad)": {"kcal": 60, "prot": 0.5, "unidad": "unidad"},
    "Frutillas/Arándanos (Porción 150g)": {"kcal": 50, "prot": 1, "unidad": "unidad"},
    
    # VEGETALES Y SUPLEMENTOS
    "Brócoli/Zanahoria/Tomate/Zucchini": {"kcal": 30, "prot": 2, "unidad": "100g"},
    "Verduras de hoja (Lechuga/Acelga/Espinaca)": {"kcal": 15, "prot": 1, "unidad": "100g"},
    "Whey Protein (1 scoop)": {"kcal": 120, "prot": 24, "unidad": "unidad"},
    "Leche descremada (Vaso 200ml)": {"kcal": 90, "prot": 7, "unidad": "unidad"},
}

# 📝 REGISTRO DE ALIMENTOS
st.header("📝 ¿Qué comiste hoy?")
st.write("Seleccioná los alimentos de tu ventana de comida:")

total_kcal_comida = 0
total_prot_comida = 0

# Buscador multiselect
alimentos_elegidos = st.multiselect("Elegí todo lo que consumiste hoy:", list(base_alimentos.keys()))

if alimentos_elegidos:
    st.subheader("⚖️ Ingresá las cantidades:")
    for alimento in alimentos_elegidos:
        info = base_alimentos[alimento]
        tipo_unidad = info["unidad"]
        
        if tipo_unidad == "100g":
            cantidad = st.number_input(f"¿Cuántos gramos de {alimento}?", min_value=0, value=150, step=50, key=alimento)
            total_kcal_comida += (info["kcal"] * cantidad) / 100
            total_prot_comida += (info["prot"] * cantidad) / 100
        else:
            cantidad = st.number_input(f"¿Cuántas unidades de {alimento}?", min_value=0, value=1, step=1, key=alimento)
            total_kcal_comida += info["kcal"] * cantidad
            total_prot_comida += info["prot"] * cantidad

# Nota extra por si come algo raro
st.subheader("✍️ Notas o Extras")
notas_extras = st.text_input("¿Comiste algo que no está en la lista? Anotalo acá:", placeholder="Ej: Condimentos, un chorrito de aceite de oliva, etc.")

# ❌ REGLA DE ORO CHECK
st.subheader("⚠️ Filtro Estricto")
sin_harina_azucar = st.checkbox("❌ Confirmo que comí CERO Harinas y Cero Azúcares hoy")

# ⏱️ CONTROL DE AYUNO (14 HS)
st.header("⏱️ Control de Ayuno (14hs)")
hora_cena = st.time_input("¿A qué hora terminás de cenar?", datetime.time(22, 0))
hora_fin_ayuno = (datetime.datetime.combine(datetime.date.today(), hora_cena) + datetime.timedelta(hours=14)).time()
st.info(f"🔒 Tu ayuno termina mañana a las: **{hora_fin_ayuno.strftime('%H:%M')} hs**")

# 📊 BALANCE FINAL AUTOMÁTICO
st.header("📊 Tu Balance del Día")
if st.button("Calcular Resultados de Hoy"):
    gasto_total = 1920 + kcal_pasos
    deficit = gasto_total - total_kcal_comida
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Calorías Consumidas", value=f"{int(total_kcal_comida)} kcal")
        st.metric(label="Proteínas Totales", value=f"{int(total_prot_comida)} g")
    with col_b:
        st.metric(label="Gasto Diario Total", value=f"{gasto_total} kcal")
        st.metric(label="Déficit Logrado", value=f"{int(deficit)} kcal", delta=f"{int(deficit)} kcal")
    
    st.subheader("💡 Análisis de tu IA:")
    if total_prot_comida < 85:
        st.warning(f"⚠️ Estás en {int(total_prot_comida)}g de proteína. Para tus 96kg, intentá subir a más de 85g para blindar tus músculos.")
    else:
        st.success("💪 ¡Espectacular! Buen nivel de proteína para mantener tu masa muscular intacta.")
        
    if not sin_harina_azucar:
        st.error("🚨 Ojo con las harinas o azúcares. Mantenelas en cero para que no te dé ansiedad matutina.")
        
    if deficit > 1000 and sin_harina_azucar and total_prot_comida >= 85:
        st.balloons()
        st.success(f"🏆 ¡Día Impecable registrado para el {fecha_seleccionada.strftime('%d/%m/%Y')}!")


