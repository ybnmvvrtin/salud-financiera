import streamlit as st

st.set_page_config(page_title="Salud Financiera", page_icon="💚", layout="centered")


def clp(n):
    """Formatea un número como pesos chilenos: $1.000.000"""
    return f"${n:,.0f}".replace(",", ".")


def semaforo(valor, verde, amarillo, mayor_es_mejor=True):
    """Devuelve (emoji, puntos) según los umbrales."""
    if mayor_es_mejor:
        if valor >= verde:
            return "🟢", 2
        if valor >= amarillo:
            return "🟡", 1
        return "🔴", 0
    if valor <= verde:
        return "🟢", 2
    if valor <= amarillo:
        return "🟡", 1
    return "🔴", 0


# ---------- Encabezado ----------
st.title("💚 Mi salud financiera")
st.caption(
    "Descubre en 2 minutos cómo están tus finanzas. "
    "Herramienta educativa: no constituye asesoría financiera."
)

tab1, tab2 = st.tabs(["📊 Mi diagnóstico", "📚 Aprende"])

# ---------- Pestaña 1: Diagnóstico ----------
with tab1:
    with st.form("diagnostico"):
        col1, col2 = st.columns(2)
        with col1:
            ingreso = st.number_input("Ingreso mensual líquido ($)", min_value=0, step=10000)
            ahorro_total = st.number_input("Ahorro acumulado ($)", min_value=0, step=10000)
        with col2:
            gastos = st.number_input("Gastos mensuales totales ($)", min_value=0, step=10000)
            deuda_mensual = st.number_input("Pago mensual de deudas ($)", min_value=0, step=10000)

        enviado = st.form_submit_button(
            "Calcular mi diagnóstico", type="primary", use_container_width=True
        )

    if enviado:
        if ingreso <= 0:
            st.warning("Ingresa tu ingreso mensual para poder calcular.")
        else:
            tasa_ahorro = (ingreso - gastos) / ingreso * 100
            deuda_ingreso = deuda_mensual / ingreso * 100
            meses_fondo = ahorro_total / gastos if gastos > 0 else 0

            e1, p1 = semaforo(tasa_ahorro, 20, 10)
            e2, p2 = semaforo(deuda_ingreso, 20, 35, mayor_es_mejor=False)
            e3, p3 = semaforo(meses_fondo, 6, 3)

            st.subheader("Tus resultados")

            c1, c2, c3 = st.columns(3)
            with c1:
                with st.container(border=True):
                    st.markdown(f"### {e1}")
                    st.metric("Ahorro", f"{tasa_ahorro:.1f}%")
                    st.caption("Ideal: 20% o más del ingreso.")
            with c2:
                with st.container(border=True):
                    st.markdown(f"### {e2}")
                    st.metric("Deuda", f"{deuda_ingreso:.1f}%")
                    st.caption("Ideal: hasta 20%. Alerta sobre 35%.")
            with c3:
                with st.container(border=True):
                    st.markdown(f"### {e3}")
                    st.metric("Fondo", f"{meses_fondo:.1f} meses")
                    st.caption("Ideal: entre 3 y 6 meses de gastos.")

            total = p1 + p2 + p3
            st.subheader("Puntaje general")
            st.progress(total / 6)
            if total >= 5:
                st.success("¡Muy buena salud financiera! Sigue así.")
            elif total >= 3:
                st.info("Vas por buen camino. Hay áreas por mejorar.")
            else:
                st.error("Hay señales de alerta. Prioriza ordenar deudas y crear tu fondo de emergencia.")

            st.caption("Los umbrales son reglas generales de referencia, no normas oficiales.")

# ---------- Pestaña 2: Educación ----------
with tab2:
    st.subheader("Interés compuesto")
    st.write(
        "Es cuando los intereses que ganas (o pagas) también generan intereses. "
        "Con el tiempo el efecto crece cada vez más rápido: a tu favor hace crecer "
        "tus ahorros; en contra, hace crecer tus deudas."
    )

    with st.container(border=True):
        a, b, c = st.columns(3)
        with a:
            monto = st.number_input("Monto inicial ($)", min_value=0, value=1000000, step=100000)
        with b:
            tasa = st.slider("Tasa anual (%)", 0.0, 30.0, 5.0)
        with c:
            anios = st.slider("Años", 1, 30, 10)

        con_interes = [monto * (1 + tasa / 100) ** t for t in range(anios + 1)]
        sin_interes = [monto] * (anios + 1)

        st.line_chart({"Sin interés": sin_interes, "Con interés compuesto": con_interes})
        st.success(f"Después de **{anios} años**, {clp(monto)} se convertirían en **{clp(con_interes[-1])}**.")