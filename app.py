import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# Estilo para mejorar la visualización
st.markdown("""
    <style>
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: gray; font-size: 12px; padding: 10px; }
    .report-box { border: 1px solid #e6e9ef; padding: 20px; border-radius: 10px; background-color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO Y CRÉDITOS ---
st.title("📊 Simulador de Punto de Indiferencia de Ventas")
st.caption("Herramienta desarrollada por **Jaime Loaiza** para uso gerencial en ventas.")

# 1. NOMBRE DEL PRODUCTO
producto = st.text_input("Producto / Categoría a analizar:", value="un producto cualquiera")

st.divider()

# --- DATOS BASE (BARRA LATERAL) ---
st.sidebar.header("📝 Datos Base (Actuales)")
p_actual = st.sidebar.number_input("Precio de Venta Actual", value=1.00, format="%.2f")
q_actual = st.sidebar.number_input("Unidades Vendidas Actuales", value=1000)
mb_actual_pct = st.sidebar.number_input("Margen Bruto Actual (%)", value=26.00, format="%.2f")

# Cálculos Base Internos
costo_unitario = p_actual * (1 - (mb_actual_pct / 100))
ub_objetivo = q_actual * (p_actual - costo_unitario)

# --- SIMULACIÓN ---
st.subheader(f"Simulación de Escenario: {producto}")
col_input, col_res = st.columns([1, 2])

with col_input:
    st.markdown("### 🛠️ Ajuste de Precio")
    nuevo_p = st.number_input("Introduce el Nuevo Precio:", value=p_actual - 4263.16, format="%.2f")

# Cálculos Automáticos
ganancia_unitaria_nueva = nuevo_p - costo_unitario
nuevo_mb_pct = (ganancia_unitaria_nueva / nuevo_p) * 100 if nuevo_p > 0 else 0

if ganancia_unitaria_nueva > 0:
    q_necesaria = ub_objetivo / ganancia_unitaria_nueva
    variacion_vol = ((q_necesaria / q_actual) - 1) * 100 if q_actual > 0 else 0
else:
    q_necesaria = 0
    variacion_vol = 0

with col_res:
    res1, res2 = st.columns(2)
    res1.metric("Nuevo Margen Bruto", f"{nuevo_mb_pct:.2f}%", f"{nuevo_mb_pct - mb_actual_pct:.2f}%")
    res2.metric("Meta de Unidades", f"{int(q_necesaria):,}", f"{variacion_vol:.2f}% Vol.")

# --- GENERACIÓN DE REPORTE Y PDF ---
st.divider()
if st.button("📄 Generar Reporte para PDF"):
    st.balloons()
    
    st.markdown(f"""
    <div class="report-box">
        <h2>Reporte Gerencial de Elasticidad</h2>
        <p><strong>Desarrollado por Jaime Loaiza</strong></p>
        <hr>
        <p><strong>Producto:</strong> {producto}</p>
        <table style="width:100%">
            <tr>
                <td><strong>Precio Anterior:</strong> ${p_actual:,.2f}</td>
                <td><strong>Precio Nuevo:</strong> ${nuevo_p:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Margen Anterior:</strong> {mb_actual_pct:.2f}%</td>
                <td><strong>Margen Nuevo:</strong> {nuevo_mb_pct:.2f}%</td>
            </tr>
        </table>
        <h3 style="color: #2e7d32;">Meta Obligatoria: {int(q_necesaria):,} unidades</h3>
        <p>Para mantener la utilidad bruta de <strong>${ub_objetivo:,.2f}</strong>, se requiere un incremento del <strong>{variacion_vol:.2f}%</strong> en el volumen de ventas.</p>
        <br>
        <blockquote style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffca28;">
            <strong>⚠️ Consejo Gerencial:</strong><br>
            Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", sino procurar producir una mayor cantidad de dinero para que el riesgo valga la pena. 
            Tenga en cuenta que este modelo es de utilidad bruta; no considera factores externos como el incremento en costos logísticos, operativos o de almacenamiento que implica vender un mayor volumen.
        </blockquote>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Instrucciones para PDF:** Ahora que el reporte aparece arriba, presiona **Ctrl + P** (o Cmd + P en Mac) y selecciona 'Guardar como PDF' en tu impresora.")

# Pie de página fijo
st.markdown('<div class="footer">Simulador de Punto de Indiferencia | Autor: Jaime Loaiza</div>', unsafe_allow_html=True)
