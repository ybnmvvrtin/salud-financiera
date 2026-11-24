import streamlit as st

st.title("Mi diagnóstico de salud financiera")

ingreso = st.number_input("Ingreso mensual líquido ($)", min_value=0, step=10000)
gastos = st.number_input("Gastos mensuales totales ($)", min_value=0, step=10000)
ahorro_total = st.number_input("Ahorro acumulado ($)", min_value=0, step=10000)
deuda_mensual = st.number_input("Pago mensual de deudas ($)", min_value=0, step=10000)

if st.button("Calcular") and ingreso > 0:
    tasa_ahorro = (ingreso - gastos) / ingreso * 100
    deuda_ingreso = deuda_mensual / ingreso * 100
    meses_fondo = ahorro_total / gastos if gastos > 0 else 0

    st.metric("Tasa de ahorro", f"{tasa_ahorro:.1f}%")
    st.metric("Deuda sobre ingreso", f"{deuda_ingreso:.1f}%")
    st.metric("Fondo de emergencia", f"{meses_fondo:.1f} meses de gastos")