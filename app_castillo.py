import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta

# 1. Configuración de la página
st.set_page_config(
    page_title="Castillo S.A. - Control Operativo y Auditoría",
    page_icon="📈",
    layout="wide"
)

# 2. Estilos personalizados CSS High-End
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Cinzel:wght@700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #E5ECEF 0%, #D8E0E5 100%) !important;
    }

    span[data-baseweb="tag"] {
        background-color: #13293D !important;
        color: #E0A93B !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }

    /* REDISEÑO DE TABS */
    div[data-baseweb="tab-highlight-title"], 
    div[data-baseweb="tab-border"] {
        background-color: transparent !important;
        display: none !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: 2px solid #13293D !important;
        padding-bottom: 4px !important;
    }

    button[data-baseweb="tab"] {
        background-color: #1E3A52 !important;
        border: 1px solid #13293D !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 22px !important;
        transition: all 0.3s ease !important;
    }

    button[data-baseweb="tab"] p, 
    button[data-baseweb="tab"] div,
    button[data-baseweb="tab"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }

    button[data-baseweb="tab"]:hover {
        background-color: #2B4C6F !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #E0A93B 0%, #F5C258 100%) !important;
        border: 1px solid #E0A93B !important;
        box-shadow: 0px 4px 12px rgba(224, 169, 59, 0.4) !important;
        transform: translateY(-2px);
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] div,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: #13293D !important;
        font-weight: 800 !important;
        font-size: 13.5px !important;
    }

    /* BANNERS Y CONTENEDORES */
    .section-banner {
        background: linear-gradient(135deg, #13293D 0%, #1D3D5A 100%);
        color: #FFFFFF;
        padding: 14px 20px;
        border-radius: 10px;
        border-left: 8px solid #E0A93B;
        box-shadow: 0 4px 15px rgba(19, 41, 61, 0.2);
        margin-top: 10px;
        margin-bottom: 12px;
    }
    
    .section-banner-title {
        font-size: 16px;
        font-weight: 800;
        letter-spacing: 0.8px;
        color: #FFFFFF;
        text-transform: uppercase;
    }

    .objective-banner {
        background: linear-gradient(90deg, #13293D 0%, #203A52 100%);
        color: #E0A93B;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.4px;
        border: 1px solid rgba(224, 169, 59, 0.3);
        border-left: 6px solid #E0A93B;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 18px;
    }

    /* METRIC CARDS */
    .metric-card {
        background: linear-gradient(135deg, #13293D 0%, #1A3A54 100%);
        color: #FFFFFF;
        padding: 18px;
        border-radius: 10px;
        border-bottom: 4px solid #E0A93B;
        box-shadow: 0 6px 16px rgba(19, 41, 61, 0.18);
    }
    .metric-title {
        font-size: 11px;
        color: #E0A93B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 11px;
        color: #B0BEC5;
        margin-top: 2px;
    }

    /* LEYENDAS Y NOTAS ACLARATORIAS */
    .legend-box {
        background-color: #FFFFFF;
        padding: 12px 18px;
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        font-size: 12px;
        margin-bottom: 18px;
        display: flex;
        gap: 24px;
        align-items: center;
        flex-wrap: wrap;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        color: #13293D;
    }
    .color-badge {
        width: 14px;
        height: 14px;
        border-radius: 4px;
    }

    .chart-note {
        background-color: #FFFFFF;
        padding: 12px 16px;
        border-radius: 6px;
        border-left: 5px solid #E0A93B;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        margin-top: 8px;
        margin-bottom: 16px;
        font-size: 12.5px;
        color: #2D3748;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        line-height: 1.4;
    }
    .chart-note b {
        color: #13293D;
    }

    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        padding: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado Corporativo
col_logo, col_titulo = st.columns([1, 5])
logo_path = rhttps://drive.google.com/file/d/1uCri7BJnR9_rYxwMdl2SHp38FLlqGNtG/view?usp=drivesdk
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=130)
    else:
        st.markdown("<h2 style='font-family: \"Cinzel\", serif; color: #13293D; font-weight: 900; letter-spacing: 2px;'>CASTILLO</h2>", unsafe_allow_html=True)

with col_titulo:
    st.markdown("<h1 style='color: #13293D; font-size: 26px; font-weight: 800; margin-bottom: 0px;'>CASTILLO S.A. — AUDITORÍA Y CONTROL OPERATIVO</h1>", unsafe_allow_html=True)
    st.caption("Sistema de Monitoreo Continuo e Ingesta Diaria de Transacciones")

# 4. Generación del Dataset Base
@st.cache_data
def generar_dataset_base():
    np.random.seed(101)
    n_records = 30000

    sucursales = [
        "Av. Belgrano 1409 - S.M.T.", "25 de mayo 333 - S.M.T.", 
        "Av. Gregorio M. Diaz 211 - Bda. del Rio Sali", "Juan Bautista Alberdi 879 - Aguilares",
        "Av. Rayas esq. Ing. Tobar - Lomas de Tafi", "Av. Miguel Campero 403 - J.B. Alberdi",
        "25 de mayo 320 - S.M.T.", "Av. Alem 285 - Tafi Viejo", 
        "Bartolomé Mitre 358 - Famaillá", "San Martin 1276 - Concepción",
        "Av. Rivadavia 890 - Alderetes", "Lobo de la Vega esq. Magallanes - Yerba Buena",
        "Av. 9 de Julio 85 - Lules", "Leandro Araoz 97 - Monteros"
    ]

    vendedores = ["Ana M.", "Carlos G.", "Gonzalo R.", "Lucas J.", "María F.", "Roberto D.", "Sofía L."]
    canales = ["Presencial en Sucursal", "Venta Web (E-Commerce)"]
    lineas = ["Electrodomésticos", "Tecnología", "Mueblería", "Calefacción/Refrigeración"]

    start_date = datetime(2026, 8, 1, 8, 0, 0)
    end_date = datetime(2026, 8, 30, 20, 0, 0)
    seconds_between = int((end_date - start_date).total_seconds())
    random_seconds = np.random.randint(0, seconds_between, n_records)
    fechas = [start_date + timedelta(seconds=int(sec)) for sec in random_seconds]

    df_base = pd.DataFrame({
        'ID_Transaccion': range(1, n_records + 1),
        'Fecha_Hora': fechas,
        'Sucursal': np.random.choice(sucursales, n_records),
        'Vendedor': np.random.choice(vendedores, n_records),
        'Canal': np.random.choice(canales, n_records, p=[0.7, 0.3]),
        'Linea': np.random.choice(lineas, n_records),
        'Monto_Venta': np.random.uniform(15000, 350000, n_records),
        'Faltante_Stock_Valorado': np.random.choice([0, 5000, 18000, 45000], n_records, p=[0.92, 0.05, 0.02, 0.01]),
        'Dias_Entrega_Web': np.random.randint(1, 9, n_records)
    })

    factor_riesgo_caja = {
        "Lobo de la Vega esq. Magallanes - Yerba Buena": 0.85, 
        "Bartolomé Mitre 358 - Famaillá": 0.75,                
        "Av. Rayas esq. Ing. Tobar - Lomas de Tafi": 0.40,    
        "Av. 9 de Julio 85 - Lules": 0.35,                    
        "Av. Rivadavia 890 - Alderetes": 0.30,                 
        "Leandro Araoz 97 - Monteros": 0.15,                   
        "Av. Gregorio M. Diaz 211 - Bda. del Rio Sali": 0.12,  
        "Av. Alem 285 - Tafi Viejo": 0.10,                    
        "San Martin 1276 - Concepción": 0.08,                  
        "Av. Miguel Campero 403 - J.B. Alberdi": 0.05,        
        "25 de mayo 333 - S.M.T.": 0.04,                      
        "Juan Bautista Alberdi 879 - Aguilares": 0.03,        
        "Av. Belgrano 1409 - S.M.T.": 0.02,                   
        "25 de mayo 320 - S.M.T.": 0.01                       
    }

    df_base['Factor_Caja'] = df_base['Sucursal'].map(factor_riesgo_caja)
    df_base['Desvio_Caja'] = np.random.choice([0, 800, 2500, 12000], n_records, p=[0.94, 0.04, 0.015, 0.005]) * df_base['Factor_Caja']
    df_base['Fecha'] = df_base['Fecha_Hora'].dt.date
    
    return df_base

df_global = generar_dataset_base().copy()

# 5. Sidebar - Filtros y Simulación de Ingesta Diaria
st.sidebar.markdown("<h3 style='color: #13293D; font-weight: 800;'>PANEL DE CONTROL</h3>", unsafe_allow_html=True)

# SIMULADOR DE NUEVA INGESTA (31 de Agosto)
st.sidebar.markdown("---")
st.sidebar.markdown("**⚡ Simulación de Ingesta ETL**")
if st.sidebar.button("📥 Procesar Cierre Diario (31-Ago-2026)"):
    np.random.seed(202)
    n_nuevos = 1100
    sucursales_list = df_global['Sucursal'].unique().tolist()
    vendedores_list = df_global['Vendedor'].unique().tolist()
    lineas_list = df_global['Linea'].unique().tolist()
    
    fechas_nuevas = [datetime(2026, 8, 31, 8, 0, 0) + timedelta(seconds=int(s)) for s in np.random.randint(0, 43200, n_nuevos)]
    
    df_nuevo_dia = pd.DataFrame({
        'ID_Transaccion': range(len(df_global) + 1, len(df_global) + n_nuevos + 1),
        'Fecha_Hora': fechas_nuevas,
        'Sucursal': np.random.choice(sucursales_list, n_nuevos),
        'Vendedor': np.random.choice(vendedores_list, n_nuevos),
        'Canal': np.random.choice(["Presencial en Sucursal", "Venta Web (E-Commerce)"], n_nuevos, p=[0.7, 0.3]),
        'Linea': np.random.choice(lineas_list, n_nuevos),
        'Monto_Venta': np.random.uniform(15000, 350000, n_nuevos),
        'Faltante_Stock_Valorado': np.random.choice([0, 5000, 18000, 45000], n_nuevos, p=[0.90, 0.06, 0.03, 0.01]),
        'Dias_Entrega_Web': np.random.randint(1, 9, n_nuevos),
        'Factor_Caja': 0.5,
        'Desvio_Caja': np.random.choice([0, 1200, 3500, 15000], n_nuevos, p=[0.92, 0.05, 0.02, 0.01])
    })
    df_nuevo_dia['Fecha'] = df_nuevo_dia['Fecha_Hora'].dt.date
    df_global = pd.concat([df_global, df_nuevo_dia], ignore_index=True)
    st.sidebar.success("¡Lote del 31-Ago ingestado con éxito! (+1.100 transacciones)")

st.sidebar.markdown("---")
st.sidebar.markdown("**Filtros Ejecutivos**")

min_f = df_global['Fecha'].min()
max_f = df_global['Fecha'].max()

rango_fechas = st.sidebar.date_input(
    "Rango de Fechas a Auditar:",
    value=(min_f, max_f),
    min_value=min_f,
    max_value=max_f
)

selected_sucursales = st.sidebar.multiselect("Sucursales de Tucumán:", options=df_global['Sucursal'].unique().tolist(), default=df_global['Sucursal'].unique().tolist())
selected_lineas = st.sidebar.multiselect("Líneas de Producto:", options=df_global['Linea'].unique().tolist(), default=df_global['Linea'].unique().tolist())
selected_canal = st.sidebar.radio("Canal de Venta:", options=["Todos", "Presencial en Sucursal", "Venta Web (E-Commerce)"])

# Filtrado dinámico
if len(rango_fechas) == 2:
    f_inicio, f_fin = rango_fechas
    df_filtered = df_global[
        (df_global['Fecha'] >= f_inicio) & 
        (df_global['Fecha'] <= f_fin) &
        (df_global['Sucursal'].isin(selected_sucursales)) & 
        (df_global['Linea'].isin(selected_lineas))
    ]
else:
    df_filtered = df_global[
        (df_global['Sucursal'].isin(selected_sucursales)) & 
        (df_global['Linea'].isin(selected_lineas))
    ]

if selected_canal != "Todos":
    df_filtered = df_filtered[df_filtered['Canal'] == selected_canal]

# 6. Tarjetas KPIs
total_ventas = df_filtered['Monto_Venta'].sum()
total_desvio = df_filtered['Desvio_Caja'].sum()
total_faltante = df_filtered['Faltante_Stock_Valorado'].sum()
max_fecha_act = df_filtered['Fecha'].max().strftime('%d/%m/%Y')

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Ventas Totales Auditadas</div>
            <div class="metric-value">${total_ventas/1e6:,.2f} M ARS</div>
            <div class="metric-sub">{len(df_filtered):,} registros procesados</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Desvío en Cajas Detectado</div>
            <div class="metric-value">${total_desvio/1e3:,.1f} K ARS</div>
            <div class="metric-sub">Diferencia acumulada en arqueos</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Faltante de Stock Físico</div>
            <div class="metric-value">${total_faltante/1e6:,.2f} M ARS</div>
            <div class="metric-sub">Mercadería no localizada</div>
        </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Última Ingesta de Datos</div>
            <div class="metric-value" style="color: #E0A93B;">{max_fecha_act}</div>
            <div class="metric-sub">Actualización en tiempo real</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 7. Pestañas de Navegación
tab1, tab2, tab3, tab4 = st.tabs([
    "Cumplimiento de Metas (Vendedores)",
    "Auditoría de Caja y Desvíos",
    "Control de Stock y Entregas Web",
    "Exportación de Datos"
])

def style_tabla_metas(val):
    if val == "EXCEDIDO":
        return 'background-color: #D4EDDA; color: #155724; font-weight: bold;'
    elif val == "CUMPLIDO":
        return 'background-color: #E2E3E5; color: #383D41; font-weight: bold;'
    elif val == "DESVIACIÓN MODERADA":
        return 'background-color: #FFF3CD; color: #856404; font-weight: bold;'
    elif val == "DESVIACIÓN CRÍTICA":
        return 'background-color: #F8D7DA; color: #721C24; font-weight: bold;'
    return ''

def style_tabla_caja(val):
    if val == "CRÍTICO":
        return 'background-color: #F8D7DA; color: #721C24; font-weight: bold;'
    elif val == "PRECAUCIÓN":
        return 'background-color: #FFF3CD; color: #856404; font-weight: bold;'
    elif val == "CONFORME":
        return 'background-color: #E6F0FA; color: #13293D; font-weight: bold;'
    return ''

estilo_tabla_centrada = [
    {'selector': 'th', 'props': [('background-color', '#13293D'), ('color', '#E0A93B'), ('font-weight', '800'), ('text-align', 'center !important'), ('padding', '12px'), ('font-size', '12px'), ('text-transform', 'uppercase')]},
    {'selector': 'td', 'props': [('text-align', 'center !important'), ('padding', '10px'), ('font-size', '12px')]}
]

# ==========================================
# TAB 1: METAS VENDEDORES
# ==========================================
with tab1:
    st.markdown("""
        <div class="section-banner">
            <span class="section-banner-title">EVALUACIÓN DE CUMPLIMIENTO COMERCIAL POR VENDEDOR</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='objective-banner'><b>OBJETIVO ESTRATÉGICO:</b> Comparar las ventas logradas por cada vendedor contra sus cuotas asignadas e identificar la tendencia diaria de ventas.</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="legend-box">
            <span style="font-weight: 800; color: #13293D; text-transform: uppercase;">REFERENCIA DE CUMPLIMIENTO:</span>
            <div class="legend-item"><div class="color-badge" style="background-color: #D4EDDA; border:1px solid #155724;"></div> EXCEDIDO (≥ 100%)</div>
            <div class="legend-item"><div class="color-badge" style="background-color: #E2E3E5; border:1px solid #383D41;"></div> CUMPLIDO (90% - 99%)</div>
            <div class="legend-item"><div class="color-badge" style="background-color: #FFF3CD; border:1px solid #856404;"></div> DESVIACIÓN MODERADA (75% - 89%)</div>
            <div class="legend-item"><div class="color-badge" style="background-color: #F8D7DA; border:1px solid #721C24;"></div> DESVIACIÓN CRÍTICA (< 75%)</div>
        </div>
    """, unsafe_allow_html=True)

    df_vend = df_filtered.groupby('Vendedor')['Monto_Venta'].sum().reset_index()
    metas_dict = {
        "Ana M.": df_vend['Monto_Venta'].mean() * 0.98,
        "Carlos G.": df_vend['Monto_Venta'].mean() * 1.12,
        "Gonzalo R.": df_vend['Monto_Venta'].mean() * 1.25,
        "Lucas J.": df_vend['Monto_Venta'].mean() * 0.95,
        "María F.": df_vend['Monto_Venta'].mean() * 1.45,
        "Roberto D.": df_vend['Monto_Venta'].mean() * 1.08,
        "Sofía L.": df_vend['Monto_Venta'].mean() * 1.30
    }
    
    df_vend['Meta_ARS'] = df_vend['Vendedor'].map(metas_dict)
    df_vend['%_Cumplimiento'] = (df_vend['Monto_Venta'] / df_vend['Meta_ARS']) * 100

    def categorizar_cierre(pct):
        if pct >= 100:
            return "EXCEDIDO"
        elif pct >= 90:
            return "CUMPLIDO"
        elif pct >= 75:
            return "DESVIACIÓN MODERADA"
        else:
            return "DESVIACIÓN CRÍTICA"

    df_vend['Estado_Cierre'] = df_vend['%_Cumplimiento'].apply(categorizar_cierre)

    col_g1, col_g2 = st.columns([1.2, 1])
    
    with col_g1:
        st.markdown("**Comparativo de Ventas Reales vs Meta Asignada ($ ARS)**")
        df_chart_metas = pd.melt(
            df_vend, 
            id_vars=['Vendedor'], 
            value_vars=['Monto_Venta', 'Meta_ARS'],
            var_name='Tipo', 
            value_name='Monto'
        )
        df_chart_metas['Tipo'] = df_chart_metas['Tipo'].map({'Monto_Venta': 'Venta Lograda', 'Meta_ARS': 'Meta Asignada'})

        fig_metas = px.bar(
            df_chart_metas, 
            x='Vendedor', 
            y='Monto',
            color='Tipo',
            barmode='group',
            color_discrete_map={'Venta Lograda': '#13293D', 'Meta Asignada': '#E0A93B'},
            labels={'Monto': 'Monto en ARS', 'Vendedor': 'Vendedor'}
        )
        fig_metas.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
        st.plotly_chart(fig_metas, width="stretch")
        
        st.markdown("""
            <div class="chart-note">
                <b>Aclaración del gráfico:</b> Las barras oscuras representan lo vendido en pesos y las amarillas la meta fijada. Permite ver de un vistazo quién superó la barra objetivo y quién quedó por debajo.
            </div>
        """, unsafe_allow_html=True)
        
    with col_g2:
        st.markdown("**Matriz Comercial de Desempeño**")
        df_disp_vend = df_vend[['Vendedor', 'Estado_Cierre', '%_Cumplimiento', 'Monto_Venta', 'Meta_ARS']].copy()
        df_disp_vend['%_Cumplimiento'] = df_disp_vend['%_Cumplimiento'].map('{:.1f}%'.format)
        df_disp_vend['Monto_Venta'] = df_disp_vend['Monto_Venta'].map('${:,.0f}'.format)
        df_disp_vend['Meta_ARS'] = df_disp_vend['Meta_ARS'].map('${:,.0f}'.format)
        
        styled_df_metas = df_disp_vend.style.map(style_tabla_metas, subset=['Estado_Cierre']).set_table_styles(estilo_tabla_centrada)
        st.dataframe(styled_df_metas, hide_index=True, width="stretch")

        st.markdown("""
            <div class="chart-note">
                <b>Aclaración de la tabla:</b> Clasifica a cada vendedor según su porcentaje final. Las filas marcadas en rojo señalan a quienes no alcanzaron el 75% de su meta individual en el período.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("**Evolución Diaria de Ventas Totales ($ ARS)**")
    df_linea_ventas = df_filtered.groupby('Fecha')['Monto_Venta'].sum().reset_index()
    fig_linea_v = px.line(
        df_linea_ventas, 
        x='Fecha', 
        y='Monto_Venta', 
        markers=True,
        color_discrete_sequence=['#13293D'],
        labels={'Monto_Venta': 'Venta diaria ($)', 'Fecha': 'Día'}
    )
    fig_linea_v.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
    st.plotly_chart(fig_linea_v, width="stretch")

    st.markdown("""
        <div class="chart-note">
            <b>Aclaración del gráfico de línea:</b> Muestra la suma total facturada día por día dentro del rango elegido. Permite identificar qué días tuvieron los picos más altos de ventas y cuáles registraron caídas.
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 2: AUDITORÍA CAJA Y DESVÍOS
# ==========================================
with tab2:
    st.markdown("""
        <div class="section-banner">
            <span class="section-banner-title">AUDITORÍA DE ARQUEOS DE CAJA Y DÍAS CRÍTICOS</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='objective-banner'><b>OBJETIVO ESTRATÉGICO:</b> Ubicar en qué sucursales y en qué fechas se concentran las mayores diferencias de dinero al cierre de caja.</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="legend-box">
            <span style="font-weight: 800; color: #13293D; text-transform: uppercase;">REFERENCIA DE RIESGO OPERATIVO:</span>
            <div class="legend-item"><div class="color-badge" style="background-color: #7B1113;"></div> CRÍTICO (> $20.000 ARS)</div>
            <div class="legend-item"><div class="color-badge" style="background-color: #E0A93B;"></div> PRECAUCIÓN ($8.000 - $20.000 ARS)</div>
            <div class="legend-item"><div class="color-badge" style="background-color: #13293D;"></div> CONFORME (< $8.000 ARS)</div>
        </div>
    """, unsafe_allow_html=True)

    df_caja = df_filtered.groupby('Sucursal').agg(
        Desvio_Absoluto=('Desvio_Caja', 'sum'),
        Venta_Teorica=('Monto_Venta', 'sum')
    ).reset_index()

    def categorizar_caja(val):
        if val >= 20000:
            return "CRÍTICO"
        elif val >= 8000:
            return "PRECAUCIÓN"
        else:
            return "CONFORME"

    df_caja['Nivel_Riesgo'] = df_caja['Desvio_Absoluto'].apply(categorizar_caja)
    df_caja = df_caja.sort_values(by='Desvio_Absoluto', ascending=False)

    col_c1, col_c2 = st.columns([1.2, 1])

    with col_c1:
        st.markdown("**Desvíos de Caja Acumulados por Sucursal ($ ARS)**")
        fig_caja = px.bar(
            df_caja,
            y='Sucursal',
            x='Desvio_Absoluto',
            orientation='h',
            color='Nivel_Riesgo',
            color_discrete_map={"CRÍTICO": "#7B1113", "PRECAUCIÓN": "#E0A93B", "CONFORME": "#13293D"},
            labels={'Desvio_Absoluto': 'Faltante ($)', 'Sucursal': 'Punto de Venta'}
        )
        fig_caja.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20), yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
        st.plotly_chart(fig_caja, width="stretch")

        st.markdown("""
            <div class="chart-note">
                <b>Aclaración del gráfico:</b> Ordena las sucursales de mayor a menor según el monto faltante en caja. Las barras rojas indican las tiendas donde la diferencia de dinero superó el límite permitido.
            </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("**Informe de Arqueos por Sucursal**")
        df_caja_disp = df_caja[['Sucursal', 'Nivel_Riesgo', 'Desvio_Absoluto', 'Venta_Teorica']].copy()
        df_caja_disp['Desvio_Absoluto'] = df_caja_disp['Desvio_Absoluto'].map('${:,.0f}'.format)
        df_caja_disp['Venta_Teorica'] = df_caja_disp['Venta_Teorica'].map('${:,.0f}'.format)
        
        styled_df_caja = df_caja_disp.style.map(style_tabla_caja, subset=['Nivel_Riesgo']).set_table_styles(estilo_tabla_centrada)
        st.dataframe(styled_df_caja, hide_index=True, width="stretch")

        st.markdown("""
            <div class="chart-note">
                <b>Aclaración de la tabla:</b> Muestra el detalle numérico de cada sucursal, comparando el monto vendido contra la cifra total de faltantes registrados.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("**Línea de Tiempo: Días con Picos de Faltantes Monetarios ($ ARS)**")
    df_linea_caja = df_filtered.groupby('Fecha')['Desvio_Caja'].sum().reset_index()
    fig_linea_c = px.area(
        df_linea_caja, 
        x='Fecha', 
        y='Desvio_Caja',
        color_discrete_sequence=['#7B1113'],
        labels={'Desvio_Caja': 'Desvío Diario ($)', 'Fecha': 'Fecha de Operación'}
    )
    fig_linea_c.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
    st.plotly_chart(fig_linea_c, width="stretch")

    st.markdown("""
        <div class="chart-note">
            <b>Aclaración del gráfico de área:</b> Muestra la suma diaria de faltantes de caja. Las crestas más altas señalan los días específicos del mes donde hubo mayores descuadres en los arqueos.
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 3: CONTROL DE STOCK Y ENTREGAS WEB
# ==========================================
with tab3:
    st.markdown("""
        <div class="section-banner">
            <span class="section-banner-title">CONTROL OPERATIVO: STOCK FALTANTE Y LOGÍSTICA DE ENVÍOS</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='objective-banner'><b>OBJETIVO ESTRATÉGICO:</b> Medir la cantidad de faltantes de mercadería por sucursal y la velocidad de entrega en las compras web.</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="legend-box">
            <span style="font-weight: 800; color: #13293D; text-transform: uppercase;">REFERENCIA DE TIEMPO DE ENTREGA:</span>
            <div class="legend-item"><div class="color-badge" style="background-color: #13293D;"></div> EN TIEMPO (1 a 4 días)</div>
            <div class="legend-item"><div class="color-badge" style="background-color: #7B1113;"></div> DEMORADO (5 o más días)</div>
        </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("**Participación por Sucursal en el Faltante de Stock ($ ARS)**")
        df_stock = df_filtered.groupby('Sucursal')['Faltante_Stock_Valorado'].sum().reset_index()
        fig_dona = px.pie(
            df_stock, 
            values='Faltante_Stock_Valorado', 
            names='Sucursal', 
            hole=0.5,
            color_discrete_sequence=['#13293D', '#E0A93B', '#7B1113', '#2B4C7E', '#3A6B9C', '#7A8B99']
        )
        fig_dona.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='#FFFFFF')
        st.plotly_chart(fig_dona, width="stretch")

        st.markdown("""
            <div class="chart-note">
                <b>Aclaración del gráfico de dona:</b> Refleja la proporción del valor total de productos no localizados. Las porciones más grandes corresponden a las sucursales con mayor pérdida monetaria en inventario.
            </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown("**Cantidad de Pedidos Web según Días de Demora**")
        if selected_canal in ["Todos", "Venta Web (E-Commerce)"]:
            df_web = df_filtered[df_filtered['Canal'] == "Venta Web (E-Commerce)"]
            df_entrega = df_web.groupby('Dias_Entrega_Web').size().reset_index(name='Cantidad')
            
            df_entrega['Estado_SLA'] = df_entrega['Dias_Entrega_Web'].apply(
                lambda d: "EN TIEMPO (1-4 días)" if d < 5 else "DEMORADO (≥ 5 días)"
            )
            
            fig_web = px.bar(
                df_entrega,
                x='Dias_Entrega_Web',
                y='Cantidad',
                color='Estado_SLA',
                color_discrete_map={
                    "EN TIEMPO (1-4 días)": "#13293D",
                    "DEMORADO (≥ 5 días)": "#7B1113"
                },
                labels={
                    'Dias_Entrega_Web': 'Días hasta la entrega', 
                    'Cantidad': 'Cantidad de Pedidos',
                    'Estado_SLA': 'Estado del envío'
                }
            )
            fig_web.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
            st.plotly_chart(fig_web, width="stretch")

            st.markdown("""
                <div class="chart-note">
                    <b>Aclaración del gráfico de barras:</b> Muestra cuántos pedidos tardaron determinado número de días en entregarse. Las barras en rojo indican los envíos que demoraron 5 días o más.
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 4: EXPORTACIÓN DE DATOS
# ==========================================
with tab4:
    st.markdown("""
        <div class="section-banner">
            <span class="section-banner-title">EXPORTACIÓN DE REGISTROS CONSOLIDADOS DE AUDITORÍA</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='objective-banner'><b>OBJETIVO ESTRATÉGICO:</b> Descargar la lista de transacciones filtradas para armar informes o presentaciones.</div>", unsafe_allow_html=True)
    
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar Dataset Filtrado (.CSV)",
        data=csv_data,
        file_name=f"Audit_Castillo_{f_inicio}_al_{f_fin}.csv",
        mime="text/csv"
    )

    st.markdown("""
        <div class="chart-note">
            <b>Aclaración del archivo:</b> El archivo `.CSV` generado contiene únicamente los registros correspondientes al rango de fechas y filtros seleccionados en la barra lateral.
        </div>
    """, unsafe_allow_html=True)
