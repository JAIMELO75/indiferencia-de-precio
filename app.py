import streamlit as st
import pandas as pd
import time

# Configuración de la página
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# --- ESTILOS CSS PROFESIONALES ---
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E1E1E; margin-bottom: -15px; line-height: 1.1; }
    .sub-title { font-size: 26px; font-weight: 300; color: #6C757D; margin-bottom: 25px; border-bottom: 1px solid #E0E0E0; padding-bottom: 10px; }
    .report-box { border: 2px solid #2e7d32; padding: 30px; border-radius: 15px; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: gray; font-size: 12px; padding: 10px; background-color: white; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado Bilingüe
st.markdown('<p class="main-title">Simulador de Punto de Indiferencia</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Sales Volume Break-even Simulator</p>', unsafe_allow_html=True)
st.caption("Herramienta desarrollada por **Jaime Loaiza** para uso gerencial en ventas.")

# 1. NOMBRE DEL PRODUCTO EDITABLE
producto = st.text_input("Nombre del producto / proyecto a analizar:", value="Zapapicos")

st.divider()

# --- DATOS BASE (RECUPERADOS Y ROBUSTOS) ---
st.sidebar.header("📝 Datos Base (Situación Actual)")
p_actual = st.sidebar.number_input("Precio de Venta Actual", value=162000.00, format="%.2f")
q_actual = st.sidebar.number_input("Unidades Vendidas Actuales", value=69000)
mb_actual_pct = st.sidebar.number_input("Margen Bruto Actual (%)", value=26.00, format="%.2f")

# Cálculos Base Internos (Infalibles)
mb_actual_decimal = mb_actual_pct / 100
costo_unitario = p_actual * (1 - mb_actual_decimal)
ub_actual_total = q_actual * (p_actual - costo_unitario)

# --- SIMULADOR DE ESCENARIO ---
st.subheader(f"Análisis de Sensibilidad: {producto}")
col_input, col_res = st.columns([1, 2])

with col_input:
    st.markdown("### 🛠️ Ajuste de Precio")
    # El usuario define el nuevo precio como driver principal
    nuevo_p = st.number_input("Define el Nuevo Precio:", value=157736.84, format="%.2f")

# Cálculos de Indiferencia (Automáticos)
ganancia_unitaria_nueva = nuevo_p - costo_unitario
nuevo_mb_pct = (ganancia_unitaria_nueva / nuevo_p) * 100 if nuevo_p > 0 else 0

if ganancia_unitaria_nueva > 0:
    q_necesaria = ub_actual_total / ganancia_unitaria_nueva
    variacion_vol = ((q_necesaria / q_actual) - 1) * 100 if q_actual > 0 else 0
else:
    q_necesaria = 0
    variacion_vol = 0

with col_res:
    res1, res2 = st.columns(2)
    res1.metric("Nuevo Margen Bruto", f"{nuevo_mb_pct:.2f}%", f"{nuevo_mb_pct - mb_actual_pct:.2f}%")
    res2.metric("Meta de Unidades", f"{int(q_necesaria):,}", f"{variacion_vol:.2f}% Vol.")

# --- GENERACIÓN DE REPORTE CON EFECTO DE TRAZADO ---
st.divider()
if st.button("📊 Generar Reporte Gerencial de Punto de Indiferencia"):
    
    # EFECTO DE TRAZOS DE PLANO CARTESIANO (Simulación visual)
    with st.status("Construyendo plano cartesiano de indiferencia...", expanded=True) as status:
        st.write("📍 Trazando ejes de coordenadas (Precio vs Volumen)...")
        time.sleep(0.6)
        st.write("📈 Dibujando curva de indiferencia de rentabilidad...")
        time.sleep(0.8)
        st.write("🎯 Identificando punto de equilibrio proyectado...")
        time.sleep(0.6)
        status.update(label="¡Análisis completado!", state="complete", expanded=False)

    # REPORTE FINAL
    st.markdown(f"""
    <div class="report-box">
        <h2 style="text-align: center; color: #1e1e1e; margin-top: 0;">Reporte Gerencial de Punto de Indiferencia</h2>
        <p style="text-align: center; color: #666; font-weight: bold;">Analizado por: Jaime Loaiza</p>
        <hr>
        <p style="font-size: 20px; line-height: 1.6; text-align: justify;">
            Para mantener la <b>utilidad bruta</b> que arrojan las unidades actuales a precios actuales, la cual asciende a 
            <span style="color: #2e7d32; font-weight: bold;">${ub_actual_total:,.2f}</span>, 
            usted debe vender un total de <span style="color: #2e7d32; font-weight: bold;">{int(q_necesaria):,} unidades</span> 
            con el fin de que la decisión de ajustar el precio sea <b>indiferente</b> para los resultados financieros de la operación.
        </p>
        
        <p style="font-size: 20px; background-color: #f1f8e9; padding: 20px; border-radius: 10px; border: 1px solid #c8e6c9;">
            Esto significa que el equipo de ventas tiene el reto de lograr un incremento del <b>{variacion_vol:.2f}%</b> en el volumen de unidades vendidas. 
            Cualquier resultado por debajo de esta meta implicará una destrucción de valor comparada con el escenario actual.
        </p>
        
        <br>
        <div style="background-color: #fffde7; padding: 25px; border-left: 8px solid #fbc02d; border-radius: 5px;">
            <strong style="font-size: 18px;">⚠️ Consejo Gerencial:</strong><br>
            <p style="font-style: italic; font-size: 17px; margin-top: 10px;">
                Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", sino procurar producir una mayor cantidad de dinero para que el riesgo estratégico valga la pena. 
                Tenga en cuenta que este modelo se basa en utilidad bruta; vender un {variacion_vol:.2f}% más de volumen implica presiones logísticas, operativas y de capital de trabajo que este cálculo primario no contempla y que podrían afectar su utilidad neta real.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Para exportar:** Presione Ctrl+P (o Cmd+P) y guarde este reporte como PDF.")

# Pie de página
st.markdown(f'<div class="footer">Simulador de Punto de Indiferencia | Desarrollado por Jaime Loaiza</div>', unsafe_allow_html=True)
