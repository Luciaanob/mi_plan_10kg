import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="App de Nutrición", page_icon="🍏", layout="wide")

# 2. INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (SESSION STATE)
if 'calorias_totales' not in st.session_state:
    st.session_state['calorias_totales'] = 0.0
if 'unidades_totales_gr' not in st.session_state:
    st.session_state['unidades_totales_gr'] = 0.0
if 'volumen_ml_totales' not in st.session_state:
    st.session_state['volumen_ml_totales'] = 0.0
if 'objetivo_calorias' not in st.session_state:
    st.session_state['objetivo_calorias'] = 2000.0  # Meta predeterminada de calorías

# 3. TÍTULO PRINCIPAL DE LA APP
st.markdown("<h1 style='text-align: center;'>🍏 App de Nutrición</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Controle su consumo de alimentos y calorías</h3>", unsafe_allow_html=True)
st.write("---")

# 4. MENÚ LATERAL INTERACTIVO
st.sidebar.header("📊 Panel de Control")
opcion_menu = st.sidebar.selectbox(
    "Seleccione una opción del menú:", 
    ["Registro por alimentos", "Gráficos de Progreso", "Búsqueda por producto", "Recomendaciones con IA"]
)

# Configurar meta diaria desde la barra lateral
st.session_state['objetivo_calorias'] = st.sidebar.number_input(
    "Definir Meta de Calorías Diarias:", 
    min_value=500.0, 
    max_value=5000.0, 
    value=st.session_state['objetivo_calorias'], 
    step=50.0
)

# 5. DICCIONARIO DE ALIMENTOS Y EQUIVALENCIAS
alimentos_equivalencias = {
    "Leche entera (taza)": {"cant": 200, "unid": "ml", "cal": 120, "prot": 6, "gr": 6},
    "Leche descremada (taza)": {"cant": 200, "unid": "ml", "cal": 80, "prot": 6, "gr": 0},
    "Yogur entero (pote)": {"cant": 120, "unid": "gr", "cal": 90, "prot": 4, "gr": 4},
    "Queso blanco (cucharada)": {"cant": 30, "unid": "gr", "cal": 60, "prot": 3, "gr": 4},
    "Huevo (unidad)": {"cant": 50, "unid": "gr", "cal": 75, "prot": 6, "gr": 5},
    "Carne de vaca (bife)": {"cant": 150, "unid": "gr", "cal": 250, "prot": 30, "gr": 15},
    "Pechuga de pollo (unidad)": {"cant": 150, "unid": "gr", "cal": 165, "prot": 31, "gr": 4},
    "Arroz cocido (taza)": {"cant": 150, "unid": "gr", "cal": 200, "prot": 4, "gr": 0},
    "Fideos cocidos (taza)": {"cant": 150, "unid": "gr", "cal": 220, "prot": 5, "gr": 1},
    "Pan lactal (rodaja)": {"cant": 25, "unid": "gr", "cal": 65, "prot": 2, "gr": 1},
    "Manzana (unidad)": {"cant": 150, "unid": "gr", "cal": 80, "prot": 0, "gr": 0},
    "Banana (unidad)": {"cant": 100, "unid": "gr", "cal": 90, "prot": 1, "gr": 0},
    "Aceite de girasol (cucharada)": {"cant": 10, "unid": "ml", "cal": 90, "prot": 0, "gr": 10}
}

# 6. LÓGICA DE LAS VISTAS SEGÚN EL MENÚ
if opcion_menu == "Registro por alimentos":
    st.header("📋 Registro Diario de Alimentos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        alimento_seleccionado = st.selectbox("Seleccione el alimento consumido:", list(alimentos_equivalencias.keys()))
        porciones = st.number_input("Cantidad de porciones/unidades:", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        
        if st.button("Añadir Alimento al Día ➕"):
            datos_alimento = alimentos_equivalencias[alimento_seleccionado]
            
            # Calcular valores según las porciones ingeridas
            calorias_ganadas = datos_alimento["cal"] * porciones
            peso_ganado = datos_alimento["cant"] * porciones if datos_alimento["unid"] == "gr" else 0
            volumen_ganado = datos_alimento["cant"] * porciones if datos_alimento["unid"] == "ml" else 0
            
            # Sumar al estado general
            st.session_state['calorias_totales'] += calorias_ganadas
            st.session_state['unidades_totales_gr'] += peso_ganado
            st.session_state['volumen_ml_totales'] += volumen_ganado
            st.success(f"Se añadieron {calorias_ganadas:.1f} kcal con éxito.")

    with col2:
        st.subheader("Resumen de Consumo Actual")
        st.metric("Calorías Totales", f"{st.session_state['calorias_totales']:.1f} kcal")
        st.metric("Total Peso Alimentos", f"{st.session_state['unidades_totales_gr']:.1f} gr")
        st.metric("Total Líquidos", f"{st.session_state['volumen_ml_totales']:.1f} ml")

elif opcion_menu == "Gráficos de Progreso":
    st.header("📉 Estadísticas y Gráficos")
    st.info("Aquí verás el comportamiento de tus consumos mediante gráficos dinámicos.")
    # Datos simulados para demostración gráfica
    df_progreso = pd.DataFrame({
        'Métricas': ['Gramos Totales', 'Mililitros Totales'],
        'Valores': [st.session_state['unidades_totales_gr'], st.session_state['volumen_ml_totales']]
    })
    st.bar_chart(df_progreso.set_index('Métricas'))

elif opcion_menu == "Búsqueda por producto":
    st.header("🔍 Buscador de Equivalencias")
    busqueda = st.text_input("Escriba el nombre de un alimento para buscar:")
    if busqueda:
        resultados = {k: v for k, v in alimentos_equivalencias.items() if busqueda.lower() in k.lower()}
        if resultados:
            st.write(resultados)
        else:
            st.warning("No se encontraron coincidencias para ese alimento.")

elif opcion_menu == "Recomendaciones con IA":
    st.header("🤖 Asistente de Nutrición Inteligente")
    st.write("Tu consumo actual de calorías es óptimo para mantener tus metas según tus indicadores.")

# 7. REVISAR SI SE CUMPLIERON REQUISITOS DIARIOS (BARRA DE PROGRESO Y FESTEJO)
st.write("---")
st.subheader("🎯 Progreso hacia la Meta Diaria")

# Calcular porcentaje de progreso (máximo 1.0 que equivale al 100%)
porcentaje_progreso = min(st.session_state['calorias_totales'] / st.session_state['objetivo_calorias'], 1.0)

# Mostrar barra de progreso visual
st.progress(porcentaje_progreso)
st.write(f"Has alcanzado el **{porcentaje_progreso * 100:.1f}%** de tu meta diaria.")

# --- COMPROBACIÓN REQUISITO: FESTEJO DE GLOBOS ---
if porcentaje_progreso >= 1.0:
    st.balloons()
    st.success("¡Felicitaciones! Cumpliste con tus requisitos de consumo de calorías para hoy. 🎈🎉")

# Botón para reiniciar el día en la barra lateral
if st.sidebar.button("🔄 Reiniciar Progreso del Día"):
    st.session_state['calorias_totales'] = 0.0
    st.session_state['unidades_totales_gr'] = 0.0
    st.session_state['volumen_ml_totales'] = 0.0
    st.rerun()

# --- AGREGÁ SOLO ESTO AL FINAL DE TU ARCHIVO ACTUAL ---
try:
    # Esto busca de forma automática si tu barra llegó al 100%
    if 'barra_progreso' in locals() and barra_progreso >= 1.0:
        st.balloons()
        st.success("¡Felicitaciones! Cumpliste con tus requisitos de consumo de calorías para hoy. 🎈🎉")
except:
    pass

