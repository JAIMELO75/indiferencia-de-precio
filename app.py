import io
import time
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Simulador de Punto de Indiferencia",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------
# ESTILOS
# -------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 4.5rem;
    padding-bottom: 4rem;
    max-width: 980px;
}
@media (max-width: 768px) {
    .block-container {
        padding-top: 6rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1E1E1E;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.sub-title {
    font-size: 1.05rem;
    color: #6C757D;
    margin-bottom: 1rem;
}

.step-box {
    background: #F8F9FA;
    border: 1px solid #E9ECEF;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 12px;
}

.report-box {
    border: 1px solid #DDE5DB;
    border-left: 6px solid #2E7D32;
    background: #FCFCFC;
    padding: 22px;
    border-radius: 14px;
    margin-top: 10px;
}

.green-box {
    background-color: #E8F5E9;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #CFE8D1;
}

.yellow-box {
    background-color: #FFF8E1;
    padding: 16px;
    border-radius: 10px;
    border-left: 6px solid #F9A825;
}

.small-muted {
    color: #6C757D;
    font-size: 0.95rem;
}

.footer-note {
    color: #7A7A7A;
    font-size: 0.85rem;
    text-align: center;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FUNCIONES
# -------------------------------------------------
def fmt_money(value):
    return f"${value:,.2f}"

def fmt_units(value):
    return f"{int(round(value)):,}"

def build_pdf(producto, p_actual, q_actual, mb_actual_pct, nuevo_p, costo_unitario,
              ub_objetivo, nuevo_mb_pct, q_necesaria, variacion_vol):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#1E1E1E"),
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.HexColor("#444444"),
        spaceAfter=16
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontName="Helvetica",
        fontSize=11.3,
        leading=17,
        textColor=colors.HexColor("#1E1E1E"),
        spaceAfter=10
    )

    box_style = ParagraphStyle(
        "BoxCustom",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontName="Helvetica",
        fontSize=10.8,
        leading=16,
        textColor=colors.HexColor("#1E1E1E"),
    )

    elements = []

    elements.append(Paragraph("Reporte Gerencial de Punto de Indiferencia", title_style))
    elements.append(Paragraph("Desarrollado por Jaime Loaiza", subtitle_style))
    elements.append(Spacer(1, 8))

    resumen = f"""
    Para mantener la <b>utilidad bruta</b> que arrojan las unidades actuales a precios actuales,
    la cual es de <b>{fmt_money(ub_objetivo)}</b>, usted debe vender un total de
    <b>{fmt_units(q_necesaria)} unidades</b> con el fin de que la decisión de ajustar el precio a
    <b>{fmt_money(nuevo_p)}</b> sea <b>indiferente</b> para la rentabilidad de la compañía;
    es decir, que a pesar del cambio en el precio, el beneficio económico final en dinero permanezca inalterado.
    """
    elements.append(Paragraph(resumen, body_style))
    elements.append(Spacer(1, 8))

    data_1 = [[Paragraph(
        f"Lograr este objetivo requiere un incremento del <b>{variacion_vol:.2f}%</b> en el volumen de ventas. "
        "Cualquier cifra por debajo de este cumplimiento resultará en una pérdida de valor frente al escenario base.",
        box_style
    )]]

    table_1 = Table(data_1, colWidths=[16.5 * cm])
    table_1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CFE8D1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(table_1)
    elements.append(Spacer(1, 12))

    data_2 = [[Paragraph(
        "<b>Consejo Gerencial:</b><br/><br/>"
        'Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", '
        "sino procurar producir una mayor cantidad de dinero para que el riesgo valga la pena. "
        "Tenga en cuenta que este modelo es de utilidad bruta; no considera factores externos "
        "como el incremento en costos logísticos, operativos o de almacenamiento que implica vender un mayor volumen.",
        box_style
    )]]

    table_2 = Table(data_2, colWidths=[16.5 * cm])
    table_2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E1")),
        ("LINEBEFORE", (0, 0), (0, -1), 4, colors.HexColor("#F9A825")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#F1D98A")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(table_2)
    elements.append(Spacer(1, 16))

    datos = [
        ["Producto", producto],
        ["Precio actual", fmt_money(p_actual)],
        ["Unidades actuales", fmt_units(q_actual)],
        ["Margen bruto actual", f"{mb_actual_pct:.2f}%"],
        ["Nuevo precio", fmt_money(nuevo_p)],
        ["Costo unitario estimado", fmt_money(costo_unitario)],
        ["Nuevo margen bruto", f"{nuevo_mb_pct:.2f}%"],
        ["Meta de unidades", fmt_units(q_necesaria)],
        ["Variación requerida de volumen", f"{variacion_vol:.2f}%"],
    ]

    summary_table = Table(datos, colWidths=[6 * cm, 10.5 * cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1E1E1E")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9D9D9")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elements.append(summary_table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# -------------------------------------------------
# ENCABEZADO
# -------------------------------------------------
st.markdown('<div class="main-title">Simulador de Punto de Indiferencia</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Calcula cuántas unidades necesitas vender para bajar precio sin sacrificar la utilidad bruta.</div>',
    unsafe_allow_html=True
)

st.info(
    "Uso sugerido: 1) ingresa los datos actuales, 2) escribe el nuevo precio deseado, "
    "3) la plataforma calcula sola, 4) genera y descarga el reporte."
)

# -------------------------------------------------
# PASO 1
# -------------------------------------------------
st.markdown('<div class="step-box"><b>Paso 1.</b> Ingresa los datos actuales del producto.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    producto = st.text_input("Producto o categoría", value="Zapapicos")
    p_actual = st.number_input(
        "Precio de venta actual",
        min_value=0.0,
        value=162000.00,
        format="%.2f",
        help="Es el precio actual al que hoy vendes el producto."
    )

with col2:
    q_actual = st.number_input(
        "Unidades vendidas actuales",
        min_value=1,
        value=69000,
        step=1,
        help="Cantidad actual vendida en el período que estás analizando."
    )
    mb_actual_pct = st.number_input(
        "Margen bruto actual (%)",
        min_value=0.0,
        max_value=100.0,
        value=26.00,
        format="%.2f",
        help="Margen bruto estimado del producto en el escenario actual."
    )

# -------------------------------------------------
# PASO 2
# -------------------------------------------------
st.markdown('<div class="step-box"><b>Paso 2.</b> Escribe el nuevo precio que quieres evaluar.</div>', unsafe_allow_html=True)

nuevo_p = st.number_input(
    "Nuevo precio propuesto",
    min_value=0.0,
    value=round(p_actual * 0.95, 2),
    format="%.2f",
    help="La plataforma calculará automáticamente cuántas unidades debes vender para conservar la misma utilidad bruta."
)

# -------------------------------------------------
# CÁLCULOS
# -------------------------------------------------
costo_unitario = p_actual * (1 - (mb_actual_pct / 100))
ub_objetivo = q_actual * (p_actual - costo_unitario)
ganancia_unitaria_nueva = nuevo_p - costo_unitario
nuevo_mb_pct = (ganancia_unitaria_nueva / nuevo_p) * 100 if nuevo_p > 0 else 0

if ganancia_unitaria_nueva > 0 and q_actual > 0:
    q_necesaria = ub_objetivo / ganancia_unitaria_nueva
    variacion_vol = ((q_necesaria / q_actual) - 1) * 100
else:
    q_necesaria = 0
    variacion_vol = 0

# -------------------------------------------------
# PASO 3
# -------------------------------------------------
st.markdown('<div class="step-box"><b>Paso 3.</b> Revisa el cálculo automático y genera el reporte.</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Costo unitario estimado", fmt_money(costo_unitario))
m2.metric("Nuevo margen bruto", f"{nuevo_mb_pct:.2f}%", f"{nuevo_mb_pct - mb_actual_pct:.2f}%")
m3.metric("Meta de unidades", fmt_units(q_necesaria), f"{variacion_vol:.2f}% Vol.")
# -----------------------------------
# DIAGNÓSTICO COMERCIAL
# -----------------------------------
if nuevo_p > costo_unitario:

    if variacion_vol <= 5:
        st.success("🟢 Decisión altamente viable: el crecimiento requerido es bajo y manejable comercialmente.")

    elif variacion_vol <= 15:
        st.warning("🟡 Decisión viable con gestión: se requiere un esfuerzo comercial relevante para sostener la rentabilidad.")

    else:
        st.error("🔴 Decisión de alto riesgo: el crecimiento requerido es muy alto y puede no ser sostenible.")

if nuevo_p <= costo_unitario:
    st.error(
        "El nuevo precio es igual o inferior al costo unitario estimado. "
        "Así no existe punto de indiferencia rentable, porque cada unidad deja utilidad bruta cero o negativa."
    )

generar = st.button("📄 Generar reporte gerencial", use_container_width=True)

if generar:
    with st.status("Construyendo reporte...", expanded=True) as status:
        st.write("Calculando punto de indiferencia...")
        time.sleep(0.5)
        st.write("Preparando resumen ejecutivo...")
        time.sleep(0.6)
        st.write("Generando versión descargable...")
        time.sleep(0.6)
        status.update(label="Reporte listo", state="complete", expanded=False)

    if nuevo_p <= costo_unitario:
        st.warning("No se puede generar un reporte válido porque el nuevo precio no deja utilidad bruta positiva.")
    else:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown("## Reporte Gerencial de Punto de Indiferencia")
        st.markdown("**Desarrollado por Jaime Loaiza**")
        st.divider()

        st.write(
            f"""
Para mantener la **utilidad bruta** que arrojan las unidades actuales a precios actuales, la cual es de
**{fmt_money(ub_objetivo)}**, usted debe vender un total de **{fmt_units(q_necesaria)} unidades**
con el fin de que la decisión de ajustar el precio a **{fmt_money(nuevo_p)}** sea **indiferente**
para la rentabilidad de la compañía; es decir, que a pesar del cambio en el precio,
el beneficio económico final en dinero permanezca inalterado.
"""
        )

        st.markdown(
            f"""
<div class="green-box">
Lograr este objetivo requiere un incremento del <b>{variacion_vol:.2f}%</b> en el volumen de ventas.
Cualquier cifra por debajo de este cumplimiento resultará en una pérdida de valor frente al escenario base.
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
<div class="yellow-box">
<b>Consejo Gerencial:</b><br><br>
Al mover precios y cantidades, el objetivo no debe ser solo "quedar igual", sino procurar producir una mayor cantidad de dinero para que el riesgo valga la pena.
Tenga en cuenta que este modelo es de utilidad bruta; no considera factores externos como el incremento en costos logísticos, operativos o de almacenamiento que implica vender un mayor volumen.
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.caption("Resumen técnico del escenario")
        resumen_col1, resumen_col2 = st.columns(2)

        with resumen_col1:
            st.write(f"**Producto:** {producto}")
            st.write(f"**Precio actual:** {fmt_money(p_actual)}")
            st.write(f"**Unidades actuales:** {fmt_units(q_actual)}")
            st.write(f"**Margen bruto actual:** {mb_actual_pct:.2f}%")

        with resumen_col2:
            st.write(f"**Nuevo precio:** {fmt_money(nuevo_p)}")
            st.write(f"**Costo unitario estimado:** {fmt_money(costo_unitario)}")
            st.write(f"**Nuevo margen bruto:** {nuevo_mb_pct:.2f}%")
            st.write(f"**Meta de unidades:** {fmt_units(q_necesaria)}")

        st.markdown('</div>', unsafe_allow_html=True)

        pdf_bytes = build_pdf(
            producto=producto,
            p_actual=p_actual,
            q_actual=q_actual,
            mb_actual_pct=mb_actual_pct,
            nuevo_p=nuevo_p,
            costo_unitario=costo_unitario,
            ub_objetivo=ub_objetivo,
            nuevo_mb_pct=nuevo_mb_pct,
            q_necesaria=q_necesaria,
            variacion_vol=variacion_vol
        )

        st.download_button(
            label="⬇️ Descargar reporte en PDF",
            data=pdf_bytes,
            file_name=f"reporte_punto_indiferencia_{producto.lower().replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown('<div class="footer-note">Simulador de Punto de Indiferencia | Developed by Jaime Loaiza</div>', unsafe_allow_html=True)
