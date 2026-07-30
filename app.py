import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuración de la página
st.set_page_config(page_title="Meta -10kg by Luciano Bravo", page_icon="💪", layout="centered")

# TÍTULO PERSONALIZADO
st.title("💪 Meta -10kg by Luciano Bravo")
st.write("Versión Base de Datos v11.0 | Guardado Permanente y Comparación Semanal")

# Conexión automática con Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_historico_real = conn.read(ttl="0m") # Lee los datos guardados en vivo
except Exception:
    df_historico_real = pd.DataFrame()

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
        peso_actual = st.number_input("Ingresá tu peso de hoy (kg):", min_value=40.0, max_value=200.0, value=95.0, step=0.1)
    with col_p2:
        altura = st.number_input("Ingresá tu altura (metros):", min_value=1.20, max_value=2.30, value=1.77, step=0.01)
        edad = st.number_input("Ingresá tu edad:", min_value=15, max_value=100, value=39, step=1)

if genero == "Hombre":
    bmr = 66.47 + (13.75 * peso_inicial) + (5.00 * (altura * 100)) - (6.75 * edad)
    deficit_ideal = 700  
else:
    bmr = 655.1 + (9.56 * peso_inicial) + (1.85 * (altura * 100)) - (4.68 * edad)
    deficit_ideal = 500  

st.info(f"🧬 **{nombre_usuario}**, tu cuerpo quema **{int(bmr)} kcal** al día **solo por existir, respirar y estar quieto en la cama**. ¡Esa es tu base antes de meter un solo paso! \n\n🎯 Para bajar esos 10kg cuidando tus músculos, tu déficit ideal recomendado es de **-{deficit_ideal} kcal** diarios.")

# ==========================================
# 3. ⚖️ PROGRESO DE PESO
# ==========================================
meta_peso = peso_inicial - 10.0
kilos_bajados = peso_inicial - peso_actual

if kilos_bajados > 0:
    st.success(f"🎉 ¡Ya bajaste **{kilos_bajados:.1f} kg** desde que empezaste!")
    st.progress(min(kilos_bajados / 10.0, 1.0))
    st.write(f"Te faltan **{peso_actual - meta_peso:.1f} kg** para tu meta final de {meta_peso:.1f} kg.")
else:
    st.info(f"Punto de partida: {peso_inicial} kg. ¡Hoy arranca el cambio!")

# Gráfico interactivo diario
st.subheader("📉 Tu Curva de Descenso Histórica")
if not df_historico_real.empty and "Peso (kg)" in df_historico_real.columns:
    st.line_chart(df_historico_real.set_index("Fecha")["Peso (kg)"])
else:
    datos_peso = pd.DataFrame({"Días": ["Inicio", "Actual"], "Peso (kg)": [peso_inicial, peso_actual]})
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
# 5. 🥑 BASE DE DATOS DE ALIMENTOS
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

st.header("📝 Registro por Comidas")
total_kcal_dia = 0
total_prot_dia = 0
cantidades_totales = {}

def procesar_bloque_comida(titulo_bloque, key_sufijo):
    global total_kcal_dia, total_prot_dia, cantidades_totales
    st.subheader(titulo_bloque)
    elegidos = st.multiselect(f"¿Qué sumaste en tu {titulo_bloque.lower()}?", list(base_alimentos.keys()), key=f"select_{key_sufijo}")
    
    if elegidos:
        for alimento in elegidos:
            info = base_alimentos[alimento]
            if info["unidad"] == "100g":
                cantidad = st.number_input(f"Gramos de {alimento} ({titulo_bloque}):", min_value=0, value=50 if "Queso" in alimento else 150, step=10, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += (info["kcal"] * cantidad) / 100
                total_prot_dia += (info["prot"] * cantidad) / 100
                cantidades_totales[alimento] = cantidades_totales.get(alimento, 0) + cantidad
            else:
                cantidad = st.number_input(f"Unidades de {alimento} ({titulo_bloque}):", min_value=0, value=1, step=1, key=f"{alimento}_{key_sufijo}")
                total_kcal_dia += info["kcal"] * cantidad
                total_prot_dia += info["prot"] * cantidad
                cantidades_totales[alimento] = cantidades_totales.get(alimento, 0) + cantidad

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
hora_fin_ayuno = (datetime.datetime.combine(datetime.date.today(), hora_cena) + datetime.timedelta(hours=14))
st.info(f"🔒 Tu ayuno termina mañana a las: **{hora_fin_ayuno.strftime('%H:%M')} hs**")

# ==========================================
# 6. 📊 BALANCE DIARIO E INFORME
# ==========================================
st.header("📊 Tu Balance del Día")

gasto_total = int(bmr) + kcal_pasos
deficit_real = gasto_total - total_kcal_dia
calorias_objetivo = gasto_total - deficit_ideal
calorias_faltantes = deficit_real - deficit_ideal
meta_proteina = peso_actual * 1.2

st.metric(label="Calorías Consumidas", value=f"{int(total_kcal_dia)} kcal")
st.metric(label="Proteínas Totales", value=f"{int(total_prot_dia)} g")

# BOTÓN DE GUARDADO PRINCIPAL EN LA NUBE PERMANENTE
if st.button("💾 Guardar y Comparar mi Día en la NUBE"):
    nuevo_registro = pd.DataFrame([{
        "Fecha": fecha_seleccionada.strftime('%d/%m/%Y'),
        "Usuario": nombre_usuario,
        "Peso (kg)": peso_actual,
        "Pasos": pasos,
        "Consumo (kcal)": int(total_kcal_dia),
        "Proteínas (g)": int(total_prot_dia),
        "Déficit (kcal)": int(deficit_real)
    }])
    
    # Intenta actualizar la planilla de Google Sheets de forma permanente
    try:
        df_actualizado = pd.concat([df_historico_real, nuevo_registro]).drop_duplicates(subset=["Fecha"], keep="last")
        conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=df_actualizado)
        st.success("📊 ¡Día guardado de forma PERMANENTE en la Nube! Ya podés cerrar la app sin perder nada.")
    except Exception as e:
        st.warning("⚠️ Los datos se calcularon pero la hoja de Google Sheets no está conectada todavía. Pasá al Paso 2.")

    st.metric(label="Déficit Real Logrado", value=f"{int(deficit_real)} kcal")
    
    st.markdown("---")
    st.subheader(f"🤖 El Consejo de tu Coach para {nombre_usuario}:")
    
    if deficit_real > 1200:
        st.error(f"⚠️ **¡Cuidado {nombre_usuario}, estás comiendo muy poco!** Hoy lograste un déficit tremendo de {int(deficit_real)} kcal. Te faltaron ingerir exactamente **{int(calorias_faltantes)} kcal** para alcanzar tu meta ideal de manera saludable, que sería consumir **{int(calorias_objetivo)} kcal** en el día. Cortar tanto la comida obliga a tu cuerpo de {int(peso_actual)}kg a quemar masa muscular para aguantar los {pasos} pasos. \n\n💡 **Cómo solucionarlo:** ¡No dejes de comer! Mañana asegurate de sumarle a tus platos una buena porción de carbohidratos sanos (como **200g de papa o batata**) o un buen refuerzo de carne o pollo en la cena.")
    
