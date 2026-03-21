import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main-title { font-size: 40px; font-weight: 800; color: #1E1E1E; margin-bottom: -10px; line-height: 1.1; }
    .sub-title { font-size: 24px; font-weight: 300; color: #6C757D; margin-bottom: 25px; border-bottom: 1px solid #E0E0E0; padding-bottom: 10px; }
    .report-box { border: 2px solid #2e7d32; padding: 25px; border-radius: 15px; background-color: #fcfcfc; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: gray; font-size: 12px; padding: 10px; background-color: white; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado Bilingüe
st.markdown('<p class="main-title">Simulador de Punto de Indiferencia</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Sales Volume Break-even Simulator</p>', unsafe_allow_html=True)
st.caption("Herramienta desarrollada por **Jaime Loaiza** para uso gerencial en ventas.")

# --- DATOS BASE ---
producto = st.text_input("Producto / Categoría a analizar:", value="Zapapicos")
st.sidebar.header("📝 Datos Base")
p_actual = st.sidebar.number_input("Precio Actual", value=162000.00, format="%.2f")
q_actual = st.sidebar.number_input("Unidades Actuales", value=69000)
mb_actual_pct = st.sidebar.number_input("Margen Bruto Actual (%)", value=26.00, format="%.2f")

costo_unitario = p_actual * (1 - (mb_actual_pct / 100))
ub_actual_total = q_actual * (p_actual - costo_unitario)

# --- SIMULACIÓN ---
st.divider()
nuevo_p = st.number_input(f"Ajustar Nuevo Precio para {producto}:", value=p_actual * 0.95, format="%.2f")

# Cálculos de Indiferencia
ganancia_unitaria_nueva = nuevo_p - costo_unitario
nuevo_mb_pct = (ganancia_unitaria_nueva / nuevo_p) * 100 if nuevo_p > 0 else 0

if ganancia_unitaria_nueva > 0:
    q_necesaria = ub_actual_total / ganancia_unitaria_nueva
    variacion_vol = ((q_necesaria / q_actual) - 1) * 100
else:
    q_necesaria = 0
    variacion_vol = 0

# --- BOTÓN DE REPORTE ---
if st.button("📊 Generar Reporte Gerencial de Punto de Indiferencia"):
    st.balloons()
    
    # 1. TRAZOS DE PLANO CARTESIANO (GRÁFICA)
    st.subheader("Análisis Visual de Sensibilidad (Indiferencia)")
    
    # Generar datos para la curva
    precios_test = [nuevo_p * (1 + i/100) for i in range(-10, 11)]
    unidades_test = [ub_actual_total / (p - costo_unitario) if (p - costo_unitario) > 0 else None for p in precios_test]
    
    fig = go.Figure()
    # Línea de Indiferencia
    fig.add_trace(go.Scatter(x=precios_test, y=unidades_test, mode='lines+markers', 
                             name='Curva de Indiferencia', line=dict(color='#2e7d32', width=3)))
    # Punto Actual
    fig.add_trace(go.Scatter(x=[p_actual], y=[q_actual], mode='markers', 
                             name='Punto Actual', marker=dict(color='black', size=12, symbol='x')))
    # Punto Nuevo
    fig.add_trace(go.Scatter(x=[nuevo_p], y=[q_necesaria], mode='markers', 
                             name='Punto de Decisión', marker=dict(color='red', size=15)))
    
    fig.update_layout(title="Relación Precio vs. Volumen Necesario",
                      xaxis_title="Precio ($)", yaxis_title="Unidades (Q)",
                      template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # 2. CUADRO DE REPORTE REFINADO
    st.markdown(f"""
    <div class="report-box">
        <h2 style="text-align: center; color: #1e1e1e;">Reporte Gerencial de Punto de Indiferencia</h2>
        <p style="text-align: center; color: #666;">Analizado por: Jaime Loaiza</p>
        <hr>
        <p style="font-size: 18px; line-height: 1.6;">
            Para mantener la <b>Utilidad Bruta</b> que arrojan las unidades actuales a precios actuales, la cual asciende a 
            <span style="color: #2e7d32; font-weight: bold;">${ub_actual_total:,.2f}</span>, 
            usted debe vender un total de <span style="color: #2e7d32; font-weight: bold;">{int(q_necesaria):,} unidades</span> 
            al nuevo precio de <span style="color: #1e1e1e; font-weight: bold;">${nuevo_p:,.2f}</span>.
        </p>
        <p style="font-size: 18px; background-color: #e8f5e9; padding: 10px; border-radius: 5px;">
            Este volumen representa un incremento del <b>{variacion_vol:.2f}%</b> en unidades vendidas. 
            Solo alcanzando esta cifra la decisión será <b>indiferente</b> en términos de rentabilidad bruta.
        </p>
        <br>
        <blockquote style="background-color: #fff3cd; padding: 20px; border-left: 6px solid #ffca28; font-style: italic;">
            <b>⚠️ Consejo Gerencial:</b><br>
            Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", sino procurar producir una mayor cantidad de dinero para que el riesgo estratégico valga la pena. 
            Recuerde que este análisis se basa en margen de contribución primario; vender un {variacion_vol:.2f}% más de volumen implica presiones logísticas, operativas y de capital de trabajo que podrían reducir su utilidad neta real.
        </blockquote>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Vista de Impresión:** Presione Ctrl+P para guardar este análisis gráfico en PDF.")

st.markdown('<div class="footer">Developed by Jaime Loaiza | Sales Management Tool</div>', unsafe_allow_html=True)
