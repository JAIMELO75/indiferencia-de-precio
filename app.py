import streamlit.components.v1 as components
import streamlit as st
import time
import textwrap

# Configuración de la página
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# --- ESTILO ---
st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #1E1E1E;
    margin-bottom: -10px;
    line-height: 1.1;
}
.sub-title {
    font-size: 24px;
    font-weight: 300;
    color: #6C757D;
    margin-bottom: 25px;
    border-bottom: 1px solid #E0E0E0;
    padding-bottom: 10px;
}
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    color: gray;
    font-size: 12px;
    padding: 10px;
    background-color: white;
    border-top: 1px solid #eee;
}
.report-box {
    border: 2px solid #2e7d32;
    padding: 30px;
    border-radius: 15px;
    background-color: #fcfcfc;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<p class="main-title">Simulador de Punto de Indiferencia</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Sales Volume Break-even Simulator</p>', unsafe_allow_html=True)
st.caption("Herramienta desarrollada por **Jaime Loaiza** para uso gerencial en ventas.")

# --- NOMBRE DEL PRODUCTO ---
producto = st.text_input("Producto / Categoría a analizar:", value="Zapapicos")

st.divider()

# --- DATOS BASE (BARRA LATERAL) ---
st.sidebar.header("📝 Datos Base (Actuales)")
p_actual = st.sidebar.number_input("Precio de Venta Actual", min_value=0.0, value=162000.00, format="%.2f")
q_actual = st.sidebar.number_input("Unidades Vendidas Actuales", min_value=0, value=69000)
mb_actual_pct = st.sidebar.number_input("Margen Bruto Actual (%)", min_value=0.0, max_value=100.0, value=26.00, format="%.2f")

# --- CÁLCULOS BASE ---
costo_unitario = p_actual * (1 - (mb_actual_pct / 100))
ub_objetivo = q_actual * (p_actual - costo_unitario)

# --- SIMULACIÓN ---
st.subheader(f"Simulación de Escenario: {producto}")
col_input, col_res = st.columns([1, 2])

with col_input:
    st.markdown("### 🛠️ Ajuste de Precio")
    nuevo_p = st.number_input("Introduce el Nuevo Precio:", min_value=0.0, value=p_actual * 0.95, format="%.2f")

# --- CÁLCULOS AUTOMÁTICOS ---
ganancia_unitaria_nueva = nuevo_p - costo_unitario
nuevo_mb_pct = (ganancia_unitaria_nueva / nuevo_p) * 100 if nuevo_p > 0 else 0

if ganancia_unitaria_nueva > 0 and q_actual > 0:
    q_necesaria = ub_objetivo / ganancia_unitaria_nueva
    variacion_vol = ((q_necesaria / q_actual) - 1) * 100
else:
    q_necesaria = 0
    variacion_vol = 0

with col_res:
    res1, res2 = st.columns(2)
    res1.metric("Nuevo Margen Bruto", f"{nuevo_mb_pct:.2f}%", f"{nuevo_mb_pct - mb_actual_pct:.2f}%")
    res2.metric("Meta de Unidades", f"{int(q_necesaria):,}", f"{variacion_vol:.2f}% Vol.")

# --- ALERTA DE PRECIO INVÁLIDO ---
if nuevo_p <= costo_unitario:
    st.error(
        "El nuevo precio es igual o inferior al costo unitario estimado. "
        "En este escenario no existe punto de indiferencia rentable, porque cada unidad genera utilidad bruta cero o negativa."
    )

# --- GENERACIÓN DE REPORTE ---
st.divider()

if st.button("📄 Generar Reporte Gerencial de Punto de Indiferencia"):

    with st.status("Construyendo análisis de indiferencia...", expanded=True) as status:
        st.write("📍 Trazando ejes de Precio y Volumen...")
        time.sleep(0.5)
        st.write("📈 Dibujando curva de rentabilidad...")
        time.sleep(0.7)
        status.update(label="¡Análisis completado!", state="complete", expanded=False)

    if nuevo_p <= costo_unitario:
        st.warning(
            "No es posible generar un reporte de indiferencia válido porque el nuevo precio no deja utilidad bruta positiva por unidad."
        )
    else:
        reporte_html = textwrap.dedent(f"""
        <div class="report-box">
            <h2 style="margin-top:0; color:#1e1e1e; text-align:center;">
                Reporte Gerencial de Punto de Indiferencia
            </h2>
            <p style="text-align:center;"><strong>Desarrollado por Jaime Loaiza</strong></p>
            <hr>

            <p style="font-size:19px; line-height:1.6; text-align:justify;">
                Para mantener la <b>utilidad bruta</b> que arrojan las unidades actuales a precios actuales,
                la cual es de <span style="color:#2e7d32; font-weight:bold;">${ub_objetivo:,.2f}</span>,
                usted debe vender un total de
                <span style="color:#2e7d32; font-weight:bold;">{int(q_necesaria):,} unidades</span>
                con el fin de que la decisión de ajustar el precio a <b>${nuevo_p:,.2f}</b>
                sea <b>indiferente</b> para la rentabilidad de la compañía; es decir,
                que a pesar del cambio en el precio, el beneficio económico final en dinero permanezca inalterado.
            </p>

            <div style="font-size:19px; background-color:#e8f5e9; padding:15px; border-radius:8px; font-weight:500; margin-top:18px;">
                Lograr este objetivo requiere un incremento del <b>{variacion_vol:.2f}%</b> en el volumen de ventas.
                Cualquier cifra por debajo de este cumplimiento resultará en una pérdida de valor frente al escenario base.
            </div>

            <div style="background-color:#fff3cd; padding:20px; border-left:6px solid #ffca28; margin-top:20px; border-radius:8px;">
                <strong>⚠️ Consejo Gerencial:</strong><br>
                Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", sino procurar producir una mayor cantidad de dinero para que el riesgo valga la pena.
                Tenga en cuenta que este modelo es de utilidad bruta; no considera factores externos como el incremento en costos logísticos, operativos o de almacenamiento que implica vender un mayor volumen.
            </div>
        </div>
        """)
components.html(reporte_html, height=600, scrolling=True)
        st.info("💡 **Instrucciones:** Presiona Ctrl + P y guarda como PDF.")

# --- PIE DE PÁGINA ---
st.markdown(
    '<div class="footer">Simulador de Punto de Indiferencia | Developed by Jaime Loaiza</div>',
    unsafe_allow_html=True
)
