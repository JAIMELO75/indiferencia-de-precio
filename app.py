import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# 1. NOMBRE DEL PRODUCTO (Editable para múltiples ejercicios)
st.title("📊 Simulador de Elasticidad")
nombre_producto = st.text_input("Producto a analizar:", value="Zapapico")

st.divider()

# --- DATOS DE ORIGEN (Barra Lateral) ---
st.sidebar.header("1. Datos Actuales (Base)")
p_actual = st.sidebar.number_input("Precio de Venta Actual", value=162000.00, format="%.2f")
q_actual = st.sidebar.number_input("Cantidad Vendida Actual", value=69000)
mb_actual_pct = st.sidebar.number_input("Margen Bruto Actual (%)", value=26.00, format="%.2f")

# Cálculos Base Internos
mb_actual_decimal = mb_actual_pct / 100
costo_unitario = p_actual * (1 - mb_actual_decimal)
utilidad_bruta_objetivo = q_actual * (p_actual - costo_unitario)

# --- SIMULADOR AUTOMÁTICO ---
st.subheader(f"2. Simulación de Escenario: {nombre_producto}")

# Entrada del nuevo precio
nuevo_p = st.number_input("Introduce el Nuevo Precio de Venta:", value=p_actual - 4263.16, format="%.2f")

# Cálculos Automáticos Basados en el Precio
# 1. Nuevo Margen: (Precio - Costo) / Precio
nuevo_mb_decimal = (nuevo_p - costo_unitario) / nuevo_p if nuevo_p > 0 else 0
nuevo_mb_pct = nuevo_mb_decimal * 100

# 2. Unidades Necesarias: Utilidad Objetivo / (Nuevo Precio - Costo)
ganancia_por_unidad = nuevo_p - costo_unitario
if ganancia_por_unidad > 0:
    q_necesaria = utilidad_bruta_objetivo / ganancia_por_unidad
else:
    q_necesaria = 0

# Visualización de Resultados
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Nuevo Margen Bruto", f"{nuevo_mb_pct:.2f}%", f"{nuevo_mb_pct - mb_actual_pct:.2f}%")

with col2:
    st.metric("Ventas Necesarias", f"{int(q_necesaria):,} un.")
    esfuerzo = ((q_necesaria / q_actual) - 1) * 100 if q_actual > 0 else 0
    st.write(f"**Esfuerzo extra:** {esfuerzo:.2f}% en volumen")

with col3:
    precio_var = ((nuevo_p / p_actual) - 1) * 100 if p_actual > 0 else 0
    st.metric("Variación de Precio", f"{precio_var:.2f}%")

# --- RESUMEN PARA PDF/IMPRESIÓN ---
st.divider()
if st.button("Preparar Reporte para PDF"):
    st.balloons()
    st.markdown(f"""
    ### 📝 Reporte de Estrategia Comercial
    **Producto:** {nombre_producto}  
    **Precio Anterior:** ${p_actual:,.2f}  | **Precio Nuevo:** ${nuevo_p:,.2f}  
    **Margen Anterior:** {mb_actual_pct:.2f}% | **Margen Nuevo:** {nuevo_mb_pct:.2f}%  
    
    ---
    **CONCLUSIÓN:** Para mantener la utilidad bruta actual de **${utilidad_bruta_objetivo:,.2f}**, el equipo comercial 
    debe lograr una venta mínima de **{int(q_necesaria):,} unidades**.
    
    *Costo unitario de referencia: ${costo_unitario:,.2f}*
    """)
    st.info("💡 Tip: Presiona 'Ctrl+P' para guardar este reporte como PDF.")
