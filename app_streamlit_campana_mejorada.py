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
    .apa-table {
        font-family: 'Times New Roman', serif;
        font-size: 12px;
        background-color: white;
        border-collapse: collapse;
    }
    .apa-table th {
        border-top: 2px solid black;
        border-bottom: 1px solid black;
        padding: 8px;
        text-align: center;
        font-weight: bold;
    }
    .apa-table td {
        padding: 6px;
        text-align: center;
        border-bottom: none;
    }
    .apa-table .final-row td {
        border-bottom: 1px solid black;
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

def mostrar_tabla_con_formato(df, titulo, formato_apa=False):
    """Muestra una tabla con el formato seleccionado"""
    if formato_apa:
        df_mostrar = aplicar_formato_apa_dataframe(df, titulo)
        st.markdown(f"**{titulo}**")
        st.dataframe(df_mostrar, use_container_width=True)
        if len(df) > 0:
            st.caption("*Nota*. Los valores están redondeados a dos decimales según estándares APA.")
    else:
        st.subheader(titulo)
        st.dataframe(df, use_container_width=True)

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
        st.error(f"Error al cargar datos: {e}")
        return None, []

def crear_ranking_por_variable(df, dummy_cols, variable_seleccionada=None, n_top=10, formato_apa=False):
    """Crea ranking de categorías dentro de una variable específica o de todas"""
    try:
        if variable_seleccionada and variable_seleccionada != "Todas las variables":
            # Filtrar solo las columnas de la variable seleccionada
            cols_variable = [col for col in dummy_cols if col.split('__')[0] == variable_seleccionada]
        else:
            cols_variable = dummy_cols
        
        # Calcular sumas
        sumas = {}
        for col in cols_variable:
            if col in df.columns:
                suma = df[col].sum()
                if suma > 0:  # Solo incluir categorías con al menos 1 uso
                    if '__' in col:
                        variable = col.split('__')[0].replace('_', ' ').title()
                        categoria = col.split('__')[1].replace('_', ' ').title()
                        nombre_completo = f"{variable} - {categoria}"
                    else:
                        nombre_completo = col
                    sumas[nombre_completo] = suma
        
        # Crear DataFrame y ordenar
        if sumas:
            df_ranking = pd.DataFrame(list(sumas.items()), columns=['Categoría', 'Frecuencia'])
            df_ranking = df_ranking.sort_values('Frecuencia', ascending=False).head(n_top)
            df_ranking = df_ranking.reset_index(drop=True)
            df_ranking.index += 1  # Comenzar numeración en 1
            
            # Agregar porcentaje
            total = df_ranking['Frecuencia'].sum()
            df_ranking['Porcentaje'] = (df_ranking['Frecuencia'] / len(df) * 100).round(2)
            
            return df_ranking
        else:
            return pd.DataFrame(columns=['Categoría', 'Frecuencia', 'Porcentaje'])
            
    except Exception as e:
        st.error(f"Error al crear ranking: {e}")
        return pd.DataFrame(columns=['Categoría', 'Frecuencia', 'Porcentaje'])

def crear_tabla_cruzada(df, var1, var2, formato_apa=False):
    """Crea una tabla cruzada entre dos variables"""
    try:
        # Crear tabla de contingencia
        tabla = pd.crosstab(df[var1], df[var2], margins=True)
        
        # Crear tabla de porcentajes
        tabla_pct = pd.crosstab(df[var1], df[var2], normalize='all') * 100
        tabla_pct = tabla_pct.round(2)
        
        # Estadística Chi-cuadrado
        chi2_stat, p_value = None, None
        try:
            if tabla.shape[0] > 1 and tabla.shape[1] > 1:
                # Excluir márgenes para el test
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

def analisis_evolucion_temporal(df, dummy_cols, variable_seleccionada=None, formato_apa=False):
    """Análisis de evolución temporal de estrategias"""
    if 'Fecha_convertida' not in df.columns:
        return None, []
    
    df_temporal = df.dropna(subset=['Fecha_convertida'])
    
    if variable_seleccionada and variable_seleccionada != "Todas las variables":
        # Filtrar columnas de la variable seleccionada
        estrategias_clave = [col for col in dummy_cols if col.split('__')[0] == variable_seleccionada][:6]
    else:
        # Estrategias clave para seguimiento temporal (todas las variables)
        estrategias_clave = [
            col for col in dummy_cols 
            if any(palabra in col.lower() for palabra in ['meme', 'logotipo', 'testimonio', 'plain_folks', 'orquestacion'])
        ][:6]
    
    if not estrategias_clave:
        return None, []
    
    # Agrupar por fecha
    df_agrupado = df_temporal.groupby('Fecha_convertida')[estrategias_clave].sum().reset_index()
    
    return df_agrupado, estrategias_clave

def analisis_propaganda_candidatos(df, dummy_cols, variable_seleccionada=None, formato_apa=False):
    """Análisis de técnicas de propaganda por candidato"""
    if variable_seleccionada and variable_seleccionada != "Todas las variables":
        propaganda_cols = [col for col in dummy_cols if col.split('__')[0] == variable_seleccionada]
    else:
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
                
                if '__' in col:
                    variable = col.split('__')[0].replace('_', ' ').title()
                    tecnica = col.split('__')[1].replace('_', ' ').title()
                    nombre_completo = f"{variable} - {tecnica}"
                else:
                    nombre_completo = col
                
                datos_propaganda.append({
                    'Candidato': candidato,
                    'Técnica': nombre_completo,
                    'Usos': usos,
                    'Porcentaje': porcentaje
                })
    
    return pd.DataFrame(datos_propaganda)

def analisis_plain_folks(df, dummy_cols, variable_seleccionada=None, formato_apa=False):
    """Análisis detallado de la estrategia Plain-folks"""
    if variable_seleccionada and variable_seleccionada != "Todas las variables":
        plain_folks_cols = [col for col in dummy_cols if col.split('__')[0] == variable_seleccionada and 'plain' in col.lower()]
    else:
        plain_folks_cols = [col for col in dummy_cols if 'plain' in col.lower() or 'pueblo' in col.lower()]
    
    if not plain_folks_cols:
        return None
    
    # Filtrar posts que usan Plain-folks
    df_plain = df[df[plain_folks_cols].sum(axis=1) > 0].copy()
    
    resultados = {}
    
    # Por candidato
    if 'Candidato' in df.columns and len(df_plain) > 0:
        candidatos_stats = []
        for candidato in df['Candidato'].unique():
            df_cand = df[df['Candidato'] == candidato]
            df_plain_cand = df_plain[df_plain['Candidato'] == candidato]
            
            total_posts = len(df_cand)
            plain_posts = len(df_plain_cand)
            porcentaje = (plain_posts / total_posts) * 100 if total_posts > 0 else 0
            
            candidatos_stats.append({
                'Candidato': candidato,
                'Total_Posts': total_posts,
                'Plain_Folks_Posts': plain_posts,
                'Porcentaje': porcentaje
            })
        
        resultados['candidatos'] = pd.DataFrame(candidatos_stats)
    
    return resultados

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def main():
    """Función principal de la aplicación Streamlit"""
    
    # =====================================================
    # CONFIGURACIÓN INICIAL
    # =====================================================
    
    st.markdown('<div class="main-header">📊 Análisis Avanzado de Campaña Electoral</div>', unsafe_allow_html=True)
    
    # Cargar datos
    df, dummy_cols = cargar_datos()
    
    if df is None or len(dummy_cols) == 0:
        st.error("❌ No se pudieron cargar los datos o no se encontraron columnas dummy.")
        st.info("Asegúrate de que el archivo 'recodificado.xlsx' esté en el directorio correcto.")
        return
    
    # =====================================================
    # CONFIGURACIÓN GLOBAL EN SIDEBAR
    # =====================================================
    
    st.sidebar.header("⚙️ Configuración General")
    
    # Toggle para formato APA
    formato_apa = st.sidebar.checkbox(
        "📋 Activar formato APA académico",
        value=False,
        help="Activa el formato de tablas según estándares APA para publicaciones académicas"
    )
    
    # Selección de variable principal
    variables_principales = obtener_variables_principales(dummy_cols)
    variable_seleccionada = st.sidebar.selectbox(
        "🔍 Seleccionar variable para análisis:",
        ["Todas las variables"] + variables_principales,
        help="Selecciona una variable específica para análisis univariado"
    )
    
    # Selección de categoría (si se seleccionó una variable específica)
    categoria_seleccionada = None
    if variable_seleccionada != "Todas las variables":
        categorias_disponibles = obtener_categorias_de_variable(dummy_cols, variable_seleccionada)
        if categorias_disponibles:
            nombres_categorias = ["Todas las categorías"] + [cat[1].replace('_', ' ').title() for cat in categorias_disponibles]
            categoria_display = st.sidebar.selectbox(
                f"📂 Categoría de {variable_seleccionada.replace('_', ' ').title()}:",
                nombres_categorias,
                help="Selecciona una categoría específica para análisis más granular"
            )
            
            if categoria_display != "Todas las categorías":
                # Encontrar la categoría original
                for cat_orig, cat_display in categorias_disponibles:
                    if cat_display.replace('_', ' ').title() == categoria_display:
                        categoria_seleccionada = cat_display
                        break
    
    # Filtros adicionales
    st.sidebar.header("🔧 Filtros Adicionales")
    
    candidatos_disponibles = ["Todos"] + list(df['Candidato'].unique()) if 'Candidato' in df.columns else ["Todos"]
    candidato_seleccionado = st.sidebar.selectbox("👤 Candidato:", candidatos_disponibles)
    
    # Filtro por fecha
    if 'Fecha_convertida' in df.columns:
        df_con_fecha = df.dropna(subset=['Fecha_convertida'])
        if len(df_con_fecha) > 0:
            fecha_min = df_con_fecha['Fecha_convertida'].min().date()
            fecha_max = df_con_fecha['Fecha_convertida'].max().date()
            
            rango_fechas = st.sidebar.date_input(
                "📅 Rango de fechas:",
                value=(fecha_min, fecha_max),
                min_value=fecha_min,
                max_value=fecha_max
            )
    
    # =====================================================
    # APLICAR FILTROS A LOS DATOS
    # =====================================================
    
    df_filtrado = df.copy()
    
    # Filtrar por candidato
    if candidato_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Candidato'] == candidato_seleccionado]
    
    # Filtrar por fecha
    if 'Fecha_convertida' in df.columns and 'rango_fechas' in locals() and len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
        df_filtrado = df_filtrado[
            (df_filtrado['Fecha_convertida'].dt.date >= fecha_inicio) &
            (df_filtrado['Fecha_convertida'].dt.date <= fecha_fin)
        ]
    
    # Aplicar filtro de variable/categoría
    df_filtrado, dummy_cols_filtradas = filtrar_datos_por_seleccion(
        df_filtrado, dummy_cols, variable_seleccionada, categoria_seleccionada
    )
    
    # Mostrar información de filtros aplicados
    st.sidebar.markdown("---")
    st.sidebar.markdown("📊 **Datos filtrados:**")
    st.sidebar.metric("Total de registros", len(df_filtrado))
    
    if variable_seleccionada != "Todas las variables":
        st.sidebar.info(f"🎯 **Análisis enfocado en:** {variable_seleccionada.replace('_', ' ').title()}")
        if categoria_seleccionada:
            st.sidebar.info(f"📂 **Categoría:** {categoria_seleccionada.replace('_', ' ').title()}")
    
    if formato_apa:
        st.sidebar.success("📋 Formato APA activo")
    
    # Verificar que hay datos después del filtrado
    if len(df_filtrado) == 0:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados.")
        return
    
    # =====================================================
    # SECCIÓN 1: RANKING DE CATEGORÍAS TOP
    # =====================================================
    
    st.markdown('<div class="section-header">🏆 Ranking de Categorías Más Utilizadas</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        n_top = st.slider(
            "Número de categorías a mostrar:",
            min_value=5,
            max_value=20,
            value=10,
            step=1
        )
    
    with col2:
        # Crear ranking según la selección de variable
        df_top = crear_ranking_por_variable(df_filtrado, dummy_cols_filtradas, variable_seleccionada, n_top, formato_apa)
        
        if len(df_top) > 0:
            # Mostrar tabla con formato seleccionado
            titulo_ranking = f"Top {n_top} Categorías"
            if variable_seleccionada != "Todas las variables":
                titulo_ranking += f" - {variable_seleccionada.replace('_', ' ').title()}"
            
            mostrar_tabla_con_formato(df_top, titulo_ranking, formato_apa)
            
            # Gráfico de barras
            fig = px.bar(
                df_top.head(10),
                x='Frecuencia',
                y='Categoría',
                orientation='h',
                title=titulo_ranking,
                labels={'Frecuencia': 'Número de Usos', 'Categoría': 'Categoría'}
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos para mostrar en el ranking.")
    
    # =====================================================
    # SECCIÓN 2: EVOLUCIÓN TEMPORAL
    # =====================================================
    
    st.markdown('<div class="section-header">📈 Evolución Temporal de Estrategias</div>', unsafe_allow_html=True)
    
    resultado_temporal = analisis_evolucion_temporal(df_filtrado, dummy_cols_filtradas, variable_seleccionada, formato_apa)
    
    if resultado_temporal[0] is not None:
        df_temporal, estrategias_clave = resultado_temporal
        
        if len(df_temporal) > 0 and len(estrategias_clave) > 0:
            # Gráfico de líneas interactivo
            fig = go.Figure()
            
            for estrategia in estrategias_clave:
                if estrategia in df_temporal.columns:
                    nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title() if '__' in estrategia else estrategia
                    fig.add_trace(go.Scatter(
                        x=df_temporal['Fecha_convertida'],
                        y=df_temporal[estrategia],
                        mode='lines+markers',
                        name=nombre_limpio,
                        line=dict(width=3),
                        marker=dict(size=8)
                    ))
            
            titulo_temporal = "Evolución Temporal de Estrategias"
            if variable_seleccionada != "Todas las variables":
                titulo_temporal += f" - {variable_seleccionada.replace('_', ' ').title()}"
            
            fig.update_layout(
                title=titulo_temporal,
                xaxis_title="Fecha",
                yaxis_title="Número de Usos",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas temporales
            col1, col2 = st.columns(2)
            
            with col1:
                estadisticas = []
                for estrategia in estrategias_clave:
                    if estrategia in df_temporal.columns:
                        valores = df_temporal[estrategia]
                        nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title() if '__' in estrategia else estrategia
                        
                        estadisticas.append({
                            'Estrategia': nombre_limpio,
                            'Total': int(valores.sum()),
                            'Promedio': round(valores.mean(), 2),
                            'Máximo': int(valores.max()),
                            'Mínimo': int(valores.min())
                        })
                
                df_stats = pd.DataFrame(estadisticas)
                mostrar_tabla_con_formato(df_stats, "📊 Estadísticas Descriptivas", formato_apa)
            
            with col2:
                st.subheader("📈 Tendencias")
                for estrategia in estrategias_clave:
                    if estrategia in df_temporal.columns:
                        nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title() if '__' in estrategia else estrategia
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
        variables_disponibles = [col for col in dummy_cols_filtradas if df_filtrado[col].sum() >= 3]
        
        if len(variables_disponibles) >= 2:
            var1 = st.selectbox(
                "Variable 1:",
                variables_disponibles,
                format_func=lambda x: f"{x.split('__')[0].replace('_', ' ').title()} - {x.split('__')[1].replace('_', ' ').title()}" if '__' in x else x
            )
            
            var2 = st.selectbox(
                "Variable 2:",
                [v for v in variables_disponibles if v != var1],
                format_func=lambda x: f"{x.split('__')[0].replace('_', ' ').title()} - {x.split('__')[1].replace('_', ' ').title()}" if '__' in x else x
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
            tabla, tabla_pct, chi2_stat, p_value = crear_tabla_cruzada(df_filtrado, var1, var2, formato_apa)
            
            if tabla is not None:
                st.subheader("Estadísticas del Cruce")
                
                # Mostrar estadísticas
                total_casos = tabla.iloc[:-1, :-1].sum().sum()
                st.metric("Total de casos analizados", int(total_casos))
                
                if chi2_stat is not None:
                    col_chi1, col_chi2 = st.columns(2)
                    with col_chi1:
                        st.metric("Chi-cuadrado", f"{chi2_stat:.3f}")
                    with col_chi2:
                        st.metric("Valor p", f"{p_value:.3f}")
                
                # Mostrar tablas
                if tipo_visualizacion in ["Tabla interactiva", "Ambos"]:
                    mostrar_tabla_con_formato(tabla, "Tabla de Contingencia", formato_apa)
                    mostrar_tabla_con_formato(tabla_pct, "Tabla de Porcentajes", formato_apa)
                
                # Mostrar heatmap
                if tipo_visualizacion in ["Heatmap", "Ambos"]:
                    fig = px.imshow(
                        tabla_pct.iloc[:-1, :-1],  # Excluir márgenes
                        labels=dict(x="Variable 2", y="Variable 1", color="Porcentaje"),
                        title="Heatmap de Porcentajes"
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # =====================================================
    # SECCIÓN 4: ANÁLISIS DE PROPAGANDA
    # =====================================================
    
    st.markdown('<div class="section-header">📢 Análisis de Técnicas de Propaganda</div>', unsafe_allow_html=True)
    
    datos_propaganda = analisis_propaganda_candidatos(df_filtrado, dummy_cols_filtradas, variable_seleccionada, formato_apa)
    
    if datos_propaganda is not None and len(datos_propaganda) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico por candidato
            fig = px.bar(
                datos_propaganda,
                x='Candidato',
                y='Porcentaje',
                color='Técnica',
                title="Uso de Técnicas por Candidato (%)",
                labels={'Porcentaje': 'Porcentaje de Posts (%)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            titulo_propaganda = "Técnicas de Propaganda por Candidato"
            if variable_seleccionada != "Todas las variables":
                titulo_propaganda += f" - {variable_seleccionada.replace('_', ' ').title()}"
            
            mostrar_tabla_con_formato(datos_propaganda.round(2), titulo_propaganda, formato_apa)
    else:
        st.info("No se encontraron datos de técnicas de propaganda.")
    
    # =====================================================
    # SECCIÓN 5: ANÁLISIS PLAIN-FOLKS
    # =====================================================
    
    st.markdown('<div class="section-header">👥 Análisis Detallado: Estrategia Plain-Folks</div>', unsafe_allow_html=True)
    
    resultados_plain = analisis_plain_folks(df_filtrado, dummy_cols_filtradas, variable_seleccionada, formato_apa)
    
    if resultados_plain:
        tab1, tab2 = st.tabs(["Por Candidato", "Detalles Contextuales"])
        
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
                    titulo_plain = "Plain-Folks por Candidato"
                    if variable_seleccionada != "Todas las variables":
                        titulo_plain += f" - {variable_seleccionada.replace('_', ' ').title()}"
                    
                    mostrar_tabla_con_formato(df_plain_cand.round(2), titulo_plain, formato_apa)
        
        with tab2:
            contextos_encontrados = [k for k in resultados_plain.keys() if k.startswith('contexto_')]
            
            if contextos_encontrados:
                for contexto_key in contextos_encontrados[:3]:  # Máximo 3 contextos
                    contexto_nombre = contexto_key.replace('contexto_', '')
                    titulo_contexto = f"Plain-Folks en {contexto_nombre}"
                    
                    tabla_contexto = resultados_plain[contexto_key]
                    mostrar_tabla_con_formato(tabla_contexto, titulo_contexto, formato_apa)
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
