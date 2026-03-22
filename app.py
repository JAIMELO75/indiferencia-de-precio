import io
import time
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Simulador de Punto de Indiferencia", layout="wide")

# -------------------------------------------------
# ESTILOS
# -------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 4rem;
    max-width: 900px;
}
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
}
.step-box {
    background:#F8F9FA;
    padding:14px;
    border-radius:12px;
    margin-bottom:10px;
}
.green-box {
    background:#E8F5E9;
    padding:15px;
    border-radius:10px;
}
.yellow-box {
    background:#FFF8E1;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FUNCIONES
# -------------------------------------------------
def fmt_money(v): return f"${v:,.2f}"
def fmt_units(v): return f"{int(round(v)):,}"

def precio_limite_estructural(costo, ub_objetivo, q_actual):
    q_max = q_actual * 1.18  # límite estructural
    return (ub_objetivo / q_max) + costo

def build_pdf(producto, p_actual, q_actual, nuevo_p, ub_objetivo, q_necesaria, variacion_vol):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)

    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        alignment=TA_JUSTIFY,
        fontSize=11,
        leading=16
    )

    elements = []

    texto = f"""
    Para mantener la utilidad bruta de {fmt_money(ub_objetivo)},
    debe vender {fmt_units(q_necesaria)} unidades con precio {fmt_money(nuevo_p)}.
    Esto implica una variación de {variacion_vol:.2f}% en volumen.
    """

    elements.append(Paragraph(texto, body))
    elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# -------------------------------------------------
# UI
# -------------------------------------------------
st.markdown('<div class="main-title">Simulador de Punto de Indiferencia</div>', unsafe_allow_html=True)

st.info("1) Ingresa datos actuales → 2) define nuevo precio → 3) analiza → 4) descarga")

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
st.markdown('<div class="step-box"><b>Paso 1.</b> Datos actuales</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    producto = st.text_input("Producto", value="Producto")
    p_actual = st.number_input("Precio actual", value=100.0)

with col2:
    q_actual = st.number_input("Unidades actuales", value=1000)
    mb_actual_pct = st.number_input("Margen bruto (%)", value=30.0)

# -------------------------------------------------
# NUEVO PRECIO
# -------------------------------------------------
st.markdown('<div class="step-box"><b>Paso 2.</b> Nuevo precio</div>', unsafe_allow_html=True)

nuevo_p = st.number_input("Nuevo precio", value=p_actual * 0.95)

# -------------------------------------------------
# CÁLCULOS
# -------------------------------------------------
costo = p_actual * (1 - mb_actual_pct / 100)
ub_objetivo = q_actual * (p_actual - costo)
ganancia_nueva = nuevo_p - costo

if ganancia_nueva > 0:
    q_necesaria = ub_objetivo / ganancia_nueva
    variacion = ((q_necesaria / q_actual) - 1) * 100
else:
    q_necesaria = 0
    variacion = 0

# -------------------------------------------------
# RESULTADOS
# -------------------------------------------------
st.markdown('<div class="step-box"><b>Paso 3.</b> Resultado</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Costo", fmt_money(costo))
m2.metric("Nuevo margen", f"{(ganancia_nueva/nuevo_p)*100:.2f}%" if nuevo_p else "0%")
m3.metric("Unidades necesarias", fmt_units(q_necesaria), f"{variacion:.2f}%")

# -------------------------------------------------
# DIAGNÓSTICO
# -------------------------------------------------
if nuevo_p <= costo:
    st.error("Zona de destrucción inmediata")
else:
    if variacion <= 6:
        st.success("Zona óptima")
    elif variacion <= 12:
        st.warning("Zona de gestión")
    elif variacion <= 18:
        st.warning("Zona exigente")
    else:
        st.error("Zona estructural")

# -------------------------------------------------
# 🔥 PRECIO LÍMITE
# -------------------------------------------------
precio_limite = precio_limite_estructural(costo, ub_objetivo, q_actual)

st.markdown(f"""
<div class="yellow-box">
<b>Precio máximo sin entrar en zona estructural:</b><br><br>
{fmt_money(precio_limite)}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# BOTÓN
# -------------------------------------------------
generar = st.button("📊 Evaluar decisión")

if generar:

    if nuevo_p <= costo:
        st.error("Precio inválido")
    else:

        # CONCLUSIÓN
        if variacion <= 6:
            conclusion = "Decisión óptima"
        elif variacion <= 12:
            conclusion = "Viable con gestión"
        elif variacion <= 18:
            conclusion = "Exigente"
        else:
            conclusion = "Estructural"

        st.markdown(f"""
        <div class="green-box">
        <b>Conclusión:</b><br><br>
        {conclusion}
        </div>
        """, unsafe_allow_html=True)

        # PDF
        pdf = build_pdf(producto, p_actual, q_actual, nuevo_p, ub_objetivo, q_necesaria, variacion)

        st.download_button("⬇️ Descargar PDF", pdf, file_name="reporte.pdf")
