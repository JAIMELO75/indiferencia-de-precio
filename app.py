import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador Comercial Pro", layout="wide")

# --- ESTILO Y TÍTULO ---
st.title("📊 Simulador de Elasticidad de Punto de Indiferencia")

# 1. NOMBRE DEL PRODUCTO EDITABLE
nombre_producto = st.text_input("Nombre del Producto/Proyecto:", value="Zapapico")

st.divider()

# --- ENTRADAS BASE ---
st.sidebar.header("1. Datos de Origen")
p_actual = st.sidebar.number_input("Precio Actual ($)", value=162000.00, format="%.2f")
q_actual = st.sidebar.number_input("Unidades Actuales", value=69000)
mb_actual_input = st.sidebar.number_input("Margen Bruto Actual (%)", value=26.00, format="%.2f")

# Cálculos Base
mb_actual = mb_actual_input / 100
costo_unitario = p_actual * (1 - mb_actual)
ub_actual_total = q_actual * (p_actual - costo_unitario)

# --- LÓGICA DE CÁLCULO CIRCULAR (Punto 2) ---
st.subheader(f"2. Simulación de Escenarios para: {nombre_producto}")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 Ajuste por Precio")
    nuevo_p = st.number_input("Definir Nuevo Precio ($)", value=p_actual, format="%.2f")
    
    # Cálculo automático de margen basado en el nuevo precio
    nuevo_mb_desde_p = (nuevo_p - costo_unitario) / nuevo_p if nuevo_p > 0 else 0
    q_necesaria_p = ub_total_actual = ub_actual_total / (nuevo_p - costo_unitario) if (nuevo_p - costo_unitario) > 0 else 0
    
    st.metric("Margen Resultante", f"{nuevo_mb_desde_p:.2%}")
    st.success(f"Ventas necesarias: **{int(q_necesaria_p):,}** unidades")

with col2:
    st.markdown("### 🔵 Ajuste por Margen")
    nuevo_mb_input = st.number_input("Definir Nuevo Margen (%)", value=mb_actual_input - 2, format="%.2f")
    
    # Cálculo automático de precio basado en el nuevo margen
    nuevo_mb_decimal = nuevo_mb_input / 100
    precio_sugerido = costo_unitario / (1 - nuevo_mb_decimal) if nuevo_mb_decimal < 1 else 0
    q_necesaria_m = ub_actual_total / (precio_sugerido - costo_unitario) if (precio_sugerido - costo_unitario) > 0 else 0
    
    st.metric("Precio Sugerido", f"${precio_sugerido:,.2f}")
    st.info(f"Ventas necesarias: **{int(q_necesaria_m):,}** unidades")

# --- RESUMEN Y EXPORTACIÓN (Punto 3) ---
st.divider()
st.subheader("3. Resumen del Análisis")

datos_resumen = {
    "Concepto": ["Producto", "Costo Unitario", "Utilidad Bruta a Mantener", "Esfuerzo Comercial (Var. Q)"],
    "Valor": [
        nombre_producto, 
        f"${costo_unitario:,.2f}", 
        f"${ub_actual_total:,.2f}", 
        f"{((q_necesaria_p / q_actual) - 1):.2%}" if q_actual > 0 else "0%"
    ]
}
df = pd.DataFrame(datos_resumen)
st.table(df)

# BOTÓN PARA PDF (Simulado mediante impresión de navegador)
st.write("💡 **Para guardar como PDF:** Presiona `Ctrl + P` (o `Cmd + P` en Mac) y selecciona 'Guardar como PDF'. La página está optimizada para mostrarse limpia.")
if st.button("Preparar vista de impresión"):
    st.balloons()
    st.write("### REPORTE FINAL DE ELASTICIDAD")
    st.write(f"Producto: {nombre_producto} | Precio Sugerido: ${precio_sugerido:,.2f} | Unidades Meta: {int(q_necesaria_m):,}")
