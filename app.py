import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# --- ESTILO BILINGÜE PROFESIONAL (NUEVO) ---
st.markdown("""
    <style>
    /* Estilo para los títulos gerenciales */
    .main-title { 
        font-size: 40px; 
        font-weight: 800; 
        color: #1E1E1E; 
        margin-bottom: -10px; /* Pegar un poco el inglés */
        line-height: 1.1;
    }
    .sub-title { 
        font-size: 24px; 
        font-weight: 300; 
        color: #6C757D; /* Gris azulado elegante */
        margin-bottom: 25px; /* Espacio antes del caption */
        border-bottom: 1px solid #E0E0E0; /* Línea divisoria sutil */
        padding-bottom: 10px;
    }
    
    /* Mantener tus estilos anteriores */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: gray; font-size: 12px; padding: 10px; background-color: white; border-top: 1px solid #eee; }
    .report-box { border: 2px solid #e6e9ef; padding: 25px; border-radius: 15px; background-color: #fcfcfc; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO APLICADO ---
st.markdown('<p class="main-title">Simulador de Punto de Indiferencia</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Sales Volume Break-even Simulator</p>', unsafe_allow_html=True)

# Mantenemos tus créditos Gerenciales
st.caption("Herramienta desarrollada por **Jaime Loaiza** para uso gerencial en ventas.")

# ... (Aquí sigue el resto de tu código sin cambios) ...

# 1. NOMBRE DEL PRODUCTO
producto = st.text_input("Producto / Categoría a analizar:", value="Un producto cualquiera")

st.divider()

# --- DATOS BASE (BARRA LATERAL) ---
st.sidebar.header("📝 Datos Base (Actuales)")
p_actual = st.sidebar.number_input("Precio de Venta Actual", value=10.00, format="%.2f")
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
    # Valor por defecto sugerido con una pequeña baja
    nuevo_p = st.number_input("Introduce el Nuevo Precio:", value=p_actual * 1.00, format="%.2f")

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
        <h2 style="margin-top:0;">Reporte Gerencial de Elasticidad</h2>
        <p><strong>Desarrollado por Jaime Loaiza</strong></p>
        <hr>
        <p><strong>Producto:</strong> {producto}</p>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #f2f2f2;">
                <td style="padding:10px;"><strong>Precio Anterior:</strong> ${p_actual:,.2f}</td>
                <td style="padding:10px;"><strong>Precio Nuevo:</strong> ${nuevo_p:,.2f}</td>
            </tr>
            <tr>
                <td style="padding:10px;"><strong>Margen Anterior:</strong> {mb_actual_pct:.2f}%</td>
                <td style="padding:10px;"><strong>Margen Nuevo:</strong> {nuevo_mb_pct:.2f}%</td>
            </tr>
        </table>
        <h3 style="color: #2e7d32; margin-bottom: 5px;">Meta Obligatoria: {int(q_necesaria):,} unidades</h3>
        <p>Para mantener la utilidad bruta de <strong>${ub_objetivo:,.2f}</strong>, se requiere un incremento del <strong>{variacion_vol:.2f}%</strong> en el volumen de ventas.</p>
        <br>
        <blockquote style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffca28; margin: 0;">
            <strong>⚠️ Consejo Gerencial:</strong><br>
            Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", sino procurar producir una mayor cantidad de dinero para que el riesgo valga la pena. 
            Tenga en cuenta que este modelo es de utilidad bruta; no considera factores externos como el incremento en costos logísticos, operativos o de almacenamiento que implica vender un mayor volumen.
        </blockquote>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Instrucciones para PDF:** Presiona **Ctrl + P** (o Cmd + P en Mac) y selecciona 'Guardar como PDF'.")

# Pie de página fijo
st.markdown(f'<div class="footer">Simulador de Punto de Indiferencia | Developed by Jaime Loaiza</div>', unsafe_allow_html=True)
