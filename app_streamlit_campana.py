import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import base64
from scipy.stats import chi2_contingency

# =====================================================
# CONFIGURACIÓN VISUAL Y FORMATO APA
# =====================================================

# Configuración para cumplir con estándares APA
plt.style.use('default')  # Estilo base limpio
plt.rcParams.update({
    # FUENTES (APA recomienda Times New Roman 12pt, pero usaremos serif similar)
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 12,  # Tamaño base APA
    'axes.titlesize': 14,  # Títulos de ejes
    'axes.labelsize': 12,  # Etiquetas de ejes
    'xtick.labelsize': 11,  # Etiquetas del eje X
    'ytick.labelsize': 11,  # Etiquetas del eje Y
    'legend.fontsize': 11,  # Leyenda
    'figure.titlesize': 16,  # Título principal
    
    # COLORES Y ESTILOS (APA prefiere escala de grises, pero permitimos color moderado)
    'axes.spines.top': False,     # Sin borde superior
    'axes.spines.right': False,   # Sin borde derecho
    'axes.spines.left': True,     # Borde izquierdo
    'axes.spines.bottom': True,   # Borde inferior
    'axes.linewidth': 1.0,        # Grosor de bordes
    'axes.edgecolor': 'black',    # Color de bordes
    'axes.facecolor': 'white',    # Fondo blanco
    'figure.facecolor': 'white',  # Fondo de figura
    
    # GRILLAS (opcional, ajustar según preferencia)
    'axes.grid': True,            # Activar grillas
    'grid.alpha': 0.3,            # Transparencia de grillas
    'grid.linewidth': 0.5,        # Grosor de grillas
    'grid.color': 'gray',         # Color de grillas
    
    # TAMAÑOS DE FIGURA (ajustar según necesidad)
    'figure.figsize': (10, 6),    # Tamaño por defecto
    'figure.dpi': 300,            # Resolución alta para publicación
    'savefig.dpi': 300,           # DPI al guardar
    'savefig.bbox': 'tight',      # Recorte ajustado
    'savefig.facecolor': 'white', # Fondo blanco al guardar
})

# Paleta de colores profesional
COLORES_PRINCIPALES = [
    '#2E86AB',  # Azul profesional
    '#A23B72',  # Magenta
    '#F18F01',  # Naranja
    '#C73E1D',  # Rojo
    '#8B5A3C',  # Marrón
    '#4A4A4A',  # Gris oscuro
    '#7B68EE',  # Azul lavanda
    '#32CD32',  # Verde lima
]

# Configurar seaborn para que coincida
sns.set_palette(COLORES_PRINCIPALES)

def obtener_variables_principales(dummy_cols):
    """Obtiene la lista de variables principales (sin las subcategorías)"""
    variables = set()
    for col in dummy_cols:
        if '__' in col:
            variable_principal = col.split('__')[0]
            variables.add(variable_principal)
    return sorted(list(variables))

def obtener_categorias_de_variable(dummy_cols, variable_principal):
    """Obtiene las categorías de una variable específica"""
    categorias = []
    for col in dummy_cols:
        if '__' in col and col.split('__')[0] == variable_principal:
            categoria = col.split('__')[1]
            categorias.append((col, categoria))
    return categorias

def filtrar_datos_por_seleccion(df, dummy_cols, variable_seleccionada=None, categoria_seleccionada=None):
    """Filtra el DataFrame según la selección de variable/categoría"""
    if variable_seleccionada == "Todas las variables" or variable_seleccionada is None:
        return df, dummy_cols
    
    # Filtrar columnas dummy de la variable seleccionada
    if categoria_seleccionada == "Todas las categorías" or categoria_seleccionada is None:
        cols_filtradas = [col for col in dummy_cols if col.split('__')[0] == variable_seleccionada]
    else:
        cols_filtradas = [col for col in dummy_cols 
                         if col.split('__')[0] == variable_seleccionada and col.split('__')[1] == categoria_seleccionada]
    
    # Si se seleccionó una categoría específica, filtrar filas donde esa categoría = 1
    if categoria_seleccionada and categoria_seleccionada != "Todas las categorías":
        col_especifica = f"{variable_seleccionada}__{categoria_seleccionada}"
        if col_especifica in df.columns:
            df_filtrado = df[df[col_especifica] == 1].copy()
        else:
            df_filtrado = df.copy()
    else:
        df_filtrado = df.copy()
    
    return df_filtrado, cols_filtradas

def aplicar_formato_apa_dataframe(df, titulo="Tabla", incluir_nota=True):
    """Aplica formato APA a un DataFrame para visualización en Streamlit"""
    df_formateado = df.copy()
    
    # Redondear números decimales a 2 lugares
    for col in df_formateado.select_dtypes(include=[np.number]).columns:
        df_formateado[col] = df_formateado[col].round(2)
    
    return df_formateado

# =====================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Análisis de Campaña Electoral",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e86ab;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e6f3ff;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stDataFrame {
        border: 1px solid #e6e6e6;
        border-radius: 5px;
    }
    .download-button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

@st.cache_data
def cargar_datos():
    """Carga y procesa los datos del archivo Excel"""
    try:
        df = pd.read_excel("recodificado.xlsx")
        
        # Procesar fechas
        if 'Fecha' in df.columns:
            meses = {
                'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
                'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
            }
            
            def convertir_fecha(fecha_str):
                try:
                    if pd.isna(fecha_str):
                        return None
                    partes = str(fecha_str).lower().strip().split(' de ')
                    if len(partes) == 2:
                        dia = int(partes[0])
                        mes = meses.get(partes[1], 1)
                        return datetime(2025, mes, dia)
                except:
                    pass
                return None
            
            df['Fecha_convertida'] = df['Fecha'].apply(convertir_fecha)
        
        # Identificar columnas dummy
        dummy_cols = [col for col in df.columns if '__' in col]
        
        return df, dummy_cols
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None, None

def filtrar_datos(df, candidato_seleccionado, fecha_inicio, fecha_fin):
    """Filtra los datos según los criterios seleccionados"""
    df_filtrado = df.copy()
    
    if candidato_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Candidato'] == candidato_seleccionado]
    
    if 'Fecha_convertida' in df_filtrado.columns:
        df_filtrado = df_filtrado.dropna(subset=['Fecha_convertida'])
        df_filtrado = df_filtrado[
            (df_filtrado['Fecha_convertida'] >= fecha_inicio) & 
            (df_filtrado['Fecha_convertida'] <= fecha_fin)
        ]
    
    return df_filtrado

def crear_top_categorias(df, dummy_cols, top_n=10):
    """Crea análisis del top N de categorías más usadas"""
    resultados = []
    
    for col in dummy_cols:
        if col in df.columns:
            uso = df[col].sum()
            porcentaje = (uso / len(df)) * 100 if len(df) > 0 else 0
            
            # Extraer categoría y subcategoría
            partes = col.split('__')
            categoria_principal = partes[0].replace('_', ' ').title()
            subcategoria = partes[1].replace('_', ' ').title() if len(partes) > 1 else 'Sin especificar'
            
            resultados.append({
                'Categoría Principal': categoria_principal,
                'Subcategoría': subcategoria,
                'Usos': uso,
                'Porcentaje': porcentaje,
                'Variable': col
            })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados.sort_values('Usos', ascending=False).head(top_n)

def crear_ranking_por_variable(df, dummy_cols, variable_seleccionada=None):
    """Crea ranking de categorías dentro de una variable específica"""
    if variable_seleccionada is None:
        return crear_top_categorias(df, dummy_cols)
    
    # Filtrar solo las columnas dummy de la variable seleccionada
    cols_variable = [col for col in dummy_cols if col.startswith(variable_seleccionada + '__')]
    
    resultados = []
    for col in cols_variable:
        if col in df.columns:
            uso = df[col].sum()
            porcentaje = (uso / len(df)) * 100 if len(df) > 0 else 0
            
            subcategoria = col.split('__')[1].replace('_', ' ').title()
            
            resultados.append({
                'Categoría': subcategoria,
                'Usos': uso,
                'Porcentaje': porcentaje,
                'Variable': col
            })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados.sort_values('Usos', ascending=False)

def obtener_variables_principales(dummy_cols):
    """Obtiene la lista de variables principales (sin las subcategorías)"""
    variables = set()
    for col in dummy_cols:
        if '__' in col:
            variable_principal = col.split('__')[0]
            variables.add(variable_principal)
    
    return sorted(list(variables))

def crear_tabla_cruzada(df, var1, var2):
    """Crea tabla cruzada entre dos variables dummy"""
    try:
        # Crear tabla de contingencia
        tabla = pd.crosstab(df[var1], df[var2], margins=True)
        
        # Calcular porcentajes
        tabla_pct = pd.crosstab(df[var1], df[var2], normalize='all') * 100
        
        # Test de chi-cuadrado si es posible
        chi2_stat = None
        p_value = None
        
        if tabla.shape[0] > 1 and tabla.shape[1] > 1:
            try:
                # Eliminar márgenes para el test
                tabla_test = tabla.iloc[:-1, :-1]
                if tabla_test.sum().sum() > 0:
                    chi2_stat, p_value, _, _ = chi2_contingency(tabla_test)
            except:
                pass
        
        return tabla, tabla_pct, chi2_stat, p_value
    except Exception as e:
        st.error(f"Error al crear tabla cruzada: {e}")
        return None, None, None, None

def exportar_a_excel(dataframes_dict, nombre_archivo):
    """Exporta múltiples DataFrames a un archivo Excel"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Límite de 31 caracteres para nombres de hojas
    
    output.seek(0)
    return output

def crear_boton_descarga(dataframes_dict, nombre_archivo):
    """Crea botón de descarga para Excel"""
    excel_data = exportar_a_excel(dataframes_dict, nombre_archivo)
    
    b64 = base64.b64encode(excel_data.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{nombre_archivo}.xlsx" class="download-button">📥 Descargar Excel</a>'
    
    st.markdown(href, unsafe_allow_html=True)

# =====================================================
# ANÁLISIS AVANZADOS (Basados en analisis_campana_electoral.py)
# =====================================================

def analisis_evolucion_temporal(df, dummy_cols):
    """Análisis de evolución temporal de estrategias"""
    if 'Fecha_convertida' not in df.columns:
        return None
    
    df_temporal = df.dropna(subset=['Fecha_convertida'])
    
    # Estrategias clave para seguimiento temporal
    estrategias_clave = [
        col for col in dummy_cols 
        if any(palabra in col.lower() for palabra in ['meme', 'logotipo', 'testimonio', 'plain_folks', 'orquestacion'])
    ][:6]
    
    if not estrategias_clave:
        return None
    
    # Agrupar por fecha
    df_agrupado = df_temporal.groupby('Fecha_convertida')[estrategias_clave].sum().reset_index()
    
    return df_agrupado, estrategias_clave

def analisis_propaganda_candidatos(df, dummy_cols):
    """Análisis de técnicas de propaganda por candidato"""
    propaganda_cols = [col for col in dummy_cols if 'institute' in col.lower() or 'propaganda' in col.lower()]
    
    if not propaganda_cols or 'Candidato' not in df.columns:
        return None
    
    candidatos = df['Candidato'].unique()
    datos_propaganda = []
    
    for candidato in candidatos:
        df_cand = df[df['Candidato'] == candidato]
        total_posts = len(df_cand)
        
        for col in propaganda_cols:
            if col in df.columns:
                usos = df_cand[col].sum()
                porcentaje = (usos / total_posts) * 100 if total_posts > 0 else 0
                tecnica = col.split('__')[1].replace('_', ' ').title()
                
                datos_propaganda.append({
                    'Candidato': candidato,
                    'Técnica': tecnica,
                    'Usos': usos,
                    'Porcentaje': porcentaje
                })
    
    return pd.DataFrame(datos_propaganda)

def analisis_plain_folks(df, dummy_cols):
    """Análisis detallado de la estrategia Plain-folks"""
    plain_folks_cols = [col for col in dummy_cols if 'plain' in col.lower() or 'pueblo' in col.lower()]
    contexto_cols = [col for col in dummy_cols if 'contexto' in col.lower()]
    aparicion_cols = [col for col in dummy_cols if 'aparicion' in col.lower()]
    
    if not plain_folks_cols:
        return None
    
    # Filtrar posts que usan Plain-folks
    df_plain = df[df[plain_folks_cols].sum(axis=1) > 0].copy()
    
    resultados = {}
    
    # Por candidato
    if 'Candidato' in df.columns and len(df_plain) > 0:
        plain_candidatos = df_plain.groupby('Candidato').size().reset_index(name='Usos_Plain_Folks')
        total_candidatos = df.groupby('Candidato').size().reset_index(name='Total_Posts')
        
        resultados['candidatos'] = pd.merge(plain_candidatos, total_candidatos, on='Candidato')
        resultados['candidatos']['Porcentaje'] = (
            resultados['candidatos']['Usos_Plain_Folks'] / resultados['candidatos']['Total_Posts'] * 100
        )
    
    # Por contexto
    if contexto_cols and len(df_plain) > 0:
        for contexto_col in contexto_cols[:3]:  # Primeros 3 contextos
            if contexto_col in df.columns:
                nombre_contexto = contexto_col.split('__')[1].replace('_', ' ').title()
                tabla_contexto = pd.crosstab(df_plain[contexto_col], 
                                           df_plain['Candidato'] if 'Candidato' in df.columns else 'Total')
                resultados[f'contexto_{nombre_contexto}'] = tabla_contexto
    
    return resultados

# =====================================================
# INTERFAZ PRINCIPAL
# =====================================================

def main():
    # Título principal
    st.markdown('<div class="main-header">📊 Análisis de Campaña Electoral</div>', unsafe_allow_html=True)
    
    # Cargar datos
    df, dummy_cols = cargar_datos()
    
    if df is None:
        st.error("No se pudieron cargar los datos. Verifica que el archivo 'ereip_unificado_dummies_corregido.xlsx' existe.")
        return
    
    # =====================================================
    # SIDEBAR - FILTROS
    # =====================================================
    
    st.sidebar.header("🔍 Filtros de Análisis")
    
    # Filtro de candidato
    candidatos = ["Todos"] + list(df['Candidato'].unique()) if 'Candidato' in df.columns else ["Todos"]
    candidato_seleccionado = st.sidebar.selectbox("Seleccionar Candidato:", candidatos)
    
    # Filtro de fechas
    if 'Fecha_convertida' in df.columns:
        fechas_validas = df['Fecha_convertida'].dropna()
        if len(fechas_validas) > 0:
            fecha_min = fechas_validas.min()
            fecha_max = fechas_validas.max()
            
            fecha_inicio = st.sidebar.date_input(
                "Fecha de inicio:",
                value=fecha_min,
                min_value=fecha_min,
                max_value=fecha_max
            )
            
            fecha_fin = st.sidebar.date_input(
                "Fecha de fin:",
                value=fecha_max,
                min_value=fecha_min,
                max_value=fecha_max
            )
            
            fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
            fecha_fin = datetime.combine(fecha_fin, datetime.max.time())
        else:
            fecha_inicio = datetime(2025, 1, 1)
            fecha_fin = datetime(2025, 12, 31)
    else:
        fecha_inicio = datetime(2025, 1, 1)
        fecha_fin = datetime(2025, 12, 31)
    
    # Aplicar filtros
    df_filtrado = filtrar_datos(df, candidato_seleccionado, fecha_inicio, fecha_fin)
    
    # Mostrar información básica
    st.sidebar.markdown("---")
    st.sidebar.markdown("📈 **Información del Dataset:**")
    st.sidebar.markdown(f"- **Total registros:** {len(df):,}")
    st.sidebar.markdown(f"- **Registros filtrados:** {len(df_filtrado):,}")
    st.sidebar.markdown(f"- **Variables dummy:** {len(dummy_cols)}")
    if 'Candidato' in df.columns:
        st.sidebar.markdown(f"- **Candidatos:** {df['Candidato'].nunique()}")
      # =====================================================
    # SECCIÓN 1: TOP CATEGORÍAS MÁS USADAS
    # =====================================================
    
    st.markdown('<div class="section-header">🏆 Ranking de Categorías por Variable</div>', unsafe_allow_html=True)
    
    # Obtener variables principales
    variables_principales = obtener_variables_principales(dummy_cols)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Selector de variable
        modo_analisis = st.radio(
            "Tipo de análisis:",
            ["Top general (todas las variables)", "Ranking por variable específica"],
            index=0
        )
        
        variable_seleccionada = None
        if modo_analisis == "Ranking por variable específica":
            variable_seleccionada = st.selectbox(
                "Seleccionar variable:",
                variables_principales,
                format_func=lambda x: x.replace('_', ' ').title()
            )
    
    with col2:
        if modo_analisis == "Top general (todas las variables)":
            top_n = st.selectbox("Número de categorías:", [5, 10, 15, 20], index=1)
        else:
            top_n = st.selectbox("Número de categorías:", [3, 5, 8, 10], index=2)
    
    with col3:
        mostrar_tabla = st.checkbox("Mostrar tabla detallada", value=True)
    
    # Crear análisis según el modo seleccionado
    if modo_analisis == "Top general (todas las variables)":
        df_top = crear_top_categorias(df_filtrado, dummy_cols, top_n)
        titulo_grafico = f"Top {top_n} Estrategias Más Utilizadas (Todas las Variables)"
        columnas_tabla = ['Categoría Principal', 'Subcategoría', 'Usos', 'Porcentaje']
        y_col = 'Subcategoría'
    else:
        df_top = crear_ranking_por_variable(df_filtrado, dummy_cols, variable_seleccionada)
        if len(df_top) > top_n:
            df_top = df_top.head(top_n)
        
        variable_nombre = variable_seleccionada.replace('_', ' ').title() if variable_seleccionada else ""
        titulo_grafico = f"Ranking de {variable_nombre} (Top {len(df_top)})"
        columnas_tabla = ['Categoría', 'Usos', 'Porcentaje']
        y_col = 'Categoría'
    
    if len(df_top) > 0:
        # Gráfico
        fig = px.bar(
            df_top, 
            x='Usos', 
            y=y_col,
            color='Porcentaje',
            orientation='h',
            title=titulo_grafico,
            labels={'Usos': 'Número de Usos', y_col: 'Categoría'},
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=max(400, len(df_top) * 40), yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla si se solicita
        if mostrar_tabla:
            st.subheader("📋 Tabla Detallada")
            df_display = df_top[columnas_tabla].round(2).reset_index(drop=True)
            df_display.index = df_display.index + 1  # Empezar numeración en 1
            df_display.index.name = "Ranking"
            st.dataframe(df_display, use_container_width=True)
            
            # Mostrar estadísticas adicionales
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("Total de Usos", int(df_top['Usos'].sum()))
            
            with col_stat2:
                st.metric("Promedio de Usos", f"{df_top['Usos'].mean():.1f}")
            
            with col_stat3:
                if modo_analisis == "Ranking por variable específica":
                    # Calcular el porcentaje de cobertura de la variable
                    variable_cols = [col for col in dummy_cols if col.startswith(variable_seleccionada + '__')]
                    cobertura = (df_filtrado[variable_cols].sum(axis=1) > 0).sum()
                    porcentaje_cobertura = (cobertura / len(df_filtrado)) * 100 if len(df_filtrado) > 0 else 0
                    st.metric("Cobertura de Variable", f"{porcentaje_cobertura:.1f}%")
                else:
                    st.metric("Máximo de Usos", int(df_top['Usos'].max()))
    else:
        st.warning("No hay datos para mostrar con los filtros aplicados.")
    
    # =====================================================
    # SECCIÓN 2: ANÁLISIS TEMPORAL
    # =====================================================
    
    st.markdown('<div class="section-header">📅 Evolución Temporal de Estrategias</div>', unsafe_allow_html=True)
    
    evolucion_data = analisis_evolucion_temporal(df_filtrado, dummy_cols)
    
    if evolucion_data:
        df_temporal, estrategias_clave = evolucion_data
        
        if len(df_temporal) > 0:
            # Gráfico temporal
            fig = go.Figure()
            
            for estrategia in estrategias_clave:
                nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title()
                fig.add_trace(go.Scatter(
                    x=df_temporal['Fecha_convertida'],
                    y=df_temporal[estrategia],
                    mode='lines+markers',
                    name=nombre_limpio,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title="Evolución Temporal de Estrategias Clave",
                xaxis_title="Fecha",
                yaxis_title="Número de Usos",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas temporales
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Estadísticas Descriptivas")
                estadisticas = []
                for estrategia in estrategias_clave:
                    valores = df_temporal[estrategia]
                    nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title()
                    
                    estadisticas.append({
                        'Estrategia': nombre_limpio,
                        'Total': int(valores.sum()),
                        'Promedio': round(valores.mean(), 2),
                        'Máximo': int(valores.max()),
                        'Mínimo': int(valores.min())
                    })
                
                st.dataframe(pd.DataFrame(estadisticas), use_container_width=True)
            
            with col2:
                st.subheader("📈 Tendencias")
                for estrategia in estrategias_clave:
                    nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title()
                    total_usos = df_temporal[estrategia].sum()
                    tendencia = "📈" if df_temporal[estrategia].iloc[-1] > df_temporal[estrategia].iloc[0] else "📉"
                    
                    st.metric(
                        label=nombre_limpio,
                        value=int(total_usos),
                        delta=f"{tendencia} Tendencia"
                    )
        else:
            st.info("No hay datos temporales suficientes para el análisis.")
    else:
        st.info("No se encontraron estrategias clave para el análisis temporal.")
    
    # =====================================================
    # SECCIÓN 3: TABLA CRUZADA ENTRE VARIABLES
    # =====================================================
    
    st.markdown('<div class="section-header">🔄 Análisis de Cruces entre Variables</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Seleccionar Variables para Cruce")
        
        # Filtrar variables con suficientes datos
        variables_disponibles = [col for col in dummy_cols if df_filtrado[col].sum() >= 3]
        
        if len(variables_disponibles) >= 2:
            var1 = st.selectbox(
                "Variable 1:",
                variables_disponibles,
                format_func=lambda x: f"{x.split('__')[0].replace('_', ' ').title()} - {x.split('__')[1].replace('_', ' ').title()}"
            )
            
            var2 = st.selectbox(
                "Variable 2:",
                [v for v in variables_disponibles if v != var1],
                format_func=lambda x: f"{x.split('__')[0].replace('_', ' ').title()} - {x.split('__')[1].replace('_', ' ').title()}"
            )
            
            tipo_visualizacion = st.radio(
                "Tipo de visualización:",
                ["Heatmap", "Tabla interactiva", "Ambos"]
            )
        else:
            st.warning("No hay suficientes variables con datos para realizar cruces.")
            var1, var2 = None, None
    
    with col2:
        if len(variables_disponibles) >= 2 and var1 and var2:
            tabla, tabla_pct, chi2_stat, p_value = crear_tabla_cruzada(df_filtrado, var1, var2)
            
            if tabla is not None:
                st.subheader("Estadísticas del Cruce")
                
                # Mostrar estadísticas
                total_casos = tabla.iloc[:-1, :-1].sum().sum()
                st.metric("Total de casos analizados", int(total_casos))
                
                if chi2_stat is not None and p_value is not None:
                    st.metric("Chi-cuadrado", f"{chi2_stat:.3f}")
                    st.metric("Valor p", f"{p_value:.3f}")
                    
                    if p_value < 0.05:
                        st.success("✅ Asociación estadísticamente significativa (p < 0.05)")
                    else:
                        st.info("ℹ️ No hay asociación estadísticamente significativa")
    
    # Mostrar visualizaciones del cruce
    if len(variables_disponibles) >= 2 and var1 and var2 and 'tabla' in locals():
        if tipo_visualizacion in ["Heatmap", "Ambos"]:
            st.subheader("🔥 Heatmap de Cruces")
            
            # Eliminar márgenes para el heatmap
            tabla_heat = tabla_pct.iloc[:-1, :-1] if tabla_pct.shape[0] > 1 and tabla_pct.shape[1] > 1 else tabla_pct
            
            if tabla_heat.shape[0] > 0 and tabla_heat.shape[1] > 0:
                fig = px.imshow(
                    tabla_heat.values,
                    x=tabla_heat.columns,
                    y=tabla_heat.index,
                    color_continuous_scale='RdYlBu_r',
                    aspect='auto',
                    title=f"Cruce: {var1.split('__')[1].replace('_', ' ').title()} vs {var2.split('__')[1].replace('_', ' ').title()}"
                )
                
                # Añadir texto con porcentajes
                for i in range(tabla_heat.shape[0]):
                    for j in range(tabla_heat.shape[1]):
                        fig.add_annotation(
                            x=j, y=i,
                            text=f"{tabla_heat.iloc[i, j]:.1f}%",
                            showarrow=False,
                            font=dict(color="white" if tabla_heat.iloc[i, j] > tabla_heat.values.mean() else "black")
                        )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        if tipo_visualizacion in ["Tabla interactiva", "Ambos"]:
            st.subheader("📋 Tabla de Contingencia")
            
            tab1, tab2 = st.tabs(["Frecuencias", "Porcentajes"])
            
            with tab1:
                st.dataframe(tabla, use_container_width=True)
            
            with tab2:
                st.dataframe(tabla_pct.round(2), use_container_width=True)
    
    # =====================================================
    # SECCIÓN 4: ANÁLISIS DE PROPAGANDA
    # =====================================================
    
    st.markdown('<div class="section-header">🎯 Análisis de Técnicas de Propaganda</div>', unsafe_allow_html=True)
    
    datos_propaganda = analisis_propaganda_candidatos(df_filtrado, dummy_cols)
    
    if datos_propaganda is not None and len(datos_propaganda) > 0:
        # Gráfico de barras agrupadas
        fig = px.bar(
            datos_propaganda,
            x='Candidato',
            y='Porcentaje',
            color='Técnica',
            title="Uso de Técnicas de Propaganda por Candidato",
            labels={'Porcentaje': 'Porcentaje de Uso (%)', 'Candidato': 'Candidato'},
            barmode='group'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla resumen
        st.subheader("📊 Tabla Resumen - Propaganda por Candidato")
        pivot_propaganda = datos_propaganda.pivot(index='Técnica', columns='Candidato', values='Porcentaje').fillna(0)
        st.dataframe(pivot_propaganda.round(2), use_container_width=True)
        
    else:
        st.info("No se encontraron técnicas de propaganda en los datos filtrados.")
    
    # =====================================================
    # SECCIÓN 5: ANÁLISIS PLAIN-FOLKS
    # =====================================================
    
    st.markdown('<div class="section-header">👥 Análisis Estrategia Plain-Folks</div>', unsafe_allow_html=True)
    
    resultados_plain = analisis_plain_folks(df_filtrado, dummy_cols)
    
    if resultados_plain:
        tab1, tab2 = st.tabs(["Por Candidato", "Por Contexto"])
        
        with tab1:
            if 'candidatos' in resultados_plain:
                df_plain_cand = resultados_plain['candidatos']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        df_plain_cand,
                        x='Candidato',
                        y='Porcentaje',
                        title="Uso de Estrategia Plain-Folks por Candidato",
                        labels={'Porcentaje': 'Porcentaje de Posts (%)'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(df_plain_cand.round(2), use_container_width=True)
        
        with tab2:
            contextos_encontrados = [k for k in resultados_plain.keys() if k.startswith('contexto_')]
            
            if contextos_encontrados:
                for contexto_key in contextos_encontrados[:3]:  # Máximo 3 contextos
                    contexto_nombre = contexto_key.replace('contexto_', '')
                    st.subheader(f"Plain-Folks en {contexto_nombre}")
                    
                    tabla_contexto = resultados_plain[contexto_key]
                    st.dataframe(tabla_contexto, use_container_width=True)
            else:
                st.info("No se encontraron datos de contexto para Plain-Folks.")
    else:
        st.info("No se encontraron datos de la estrategia Plain-Folks.")
    
    # =====================================================
    # SECCIÓN 6: EXPORTACIÓN DE DATOS
    # =====================================================
    
    st.markdown('<div class="section-header">💾 Exportar Resultados</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Exportar Top Categorías", use_container_width=True):
            if 'df_top' in locals() and len(df_top) > 0:
                excel_data = exportar_a_excel(
                    {"Top_Categorias": df_top},
                    "top_categorias_campana"
                )
                
                st.download_button(
                    label="Descargar Excel - Top Categorías",
                    data=excel_data,
                    file_name="top_categorias_campana.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col2:
        if st.button("📥 Exportar Tabla Cruzada", use_container_width=True):
            if 'tabla' in locals() and tabla is not None:
                excel_data = exportar_a_excel(
                    {
                        "Tabla_Contingencia": tabla,
                        "Tabla_Porcentajes": tabla_pct
                    },
                    "tabla_cruzada_campana"
                )
                
                st.download_button(
                    label="Descargar Excel - Tabla Cruzada",
                    data=excel_data,
                    file_name="tabla_cruzada_campana.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col3:
        if st.button("📥 Exportar Análisis Propaganda", use_container_width=True):
            if 'datos_propaganda' in locals() and datos_propaganda is not None:
                excel_data = exportar_a_excel(
                    {"Propaganda_Candidatos": datos_propaganda},
                    "propaganda_campana"
                )
                
                st.download_button(
                    label="Descargar Excel - Propaganda",
                    data=excel_data,
                    file_name="propaganda_campana.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    # Botón para exportar todo
    st.markdown("---")
    if st.button("📦 Exportar Análisis Completo", use_container_width=True):
        dataframes_completo = {}
        
        if 'df_top' in locals() and len(df_top) > 0:
            dataframes_completo["Top_Categorias"] = df_top
        
        if 'tabla' in locals() and tabla is not None:
            dataframes_completo["Tabla_Contingencia"] = tabla
            dataframes_completo["Tabla_Porcentajes"] = tabla_pct
        
        if 'datos_propaganda' in locals() and datos_propaganda is not None:
            dataframes_completo["Propaganda"] = datos_propaganda
        
        if 'df_temporal' in locals() and len(df_temporal) > 0:
            dataframes_completo["Evolucion_Temporal"] = df_temporal
        
        if dataframes_completo:
            excel_data = exportar_a_excel(dataframes_completo, "analisis_completo_campana")
            
            st.download_button(
                label="Descargar Excel - Análisis Completo",
                data=excel_data,
                file_name="analisis_completo_campana.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No hay datos para exportar.")

# =====================================================
# EJECUTAR LA APLICACIÓN
# =====================================================

if __name__ == "__main__":
    main()
