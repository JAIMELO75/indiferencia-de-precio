import streamlit as st

st.set_page_config(page_title="Simulador de Precios", layout="wide")

st.title("📊 Simulador de Elasticidad: Zapapicos")

# --- VALORES BASE ---
st.sidebar.header("Datos Actuales")
p_actual = st.sidebar.number_input("Precio Actual", value=162000)
q_actual = st.sidebar.number_input("Unidades Actuales", value=69000)
mb_actual = st.sidebar.slider("Margen Bruto Actual (%)", 0, 100, 26) / 100

costo = p_actual * (1 - mb_actual)
ub_actual = q_actual * (p_actual - costo)

# --- INTERFAZ DE CUADROS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 Escenario: Mover Precio")
    nuevo_p = st.number_input("Nuevo Precio", value=157737)
    
    # Cálculos
    n_margen = (nuevo_p - costo) / nuevo_p
    q_nec = ub_actual / (nuevo_p - costo)
    
    st.metric("Nuevo Margen", f"{n_margen:.2%}")
    st.success(f"Ventas necesarias: {int(q_nec):,} unidades")
    st.caption(f"Incremento requerido: {((q_nec/q_actual)-1):.2%}")

with col2:
    st.subheader("🔵 Escenario: Mover Margen")
    n_mb_input = st.slider("Nuevo Margen Objetivo (%)", 0, 100, 24) / 100
    
    # Cálculos
    n_p_calc = costo / (1 - n_mb_input)
    q_nec_mb = ub_actual / (n_p_calc - costo)
    
    st.metric("Precio Resultante", f"${n_p_calc:,.0f}")
    st.info(f"Ventas necesarias: {int(q_nec_mb):,} unidades")

st.divider()
st.write(f"Costo unitario calculado: ${costo:,.2f} | Utilidad Bruta a proteger: ${ub_actual:,.0f}")
