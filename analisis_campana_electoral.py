import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# CONFIGURACIÓN VISUAL GLOBAL
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

# Paleta de colores profesional (puedes cambiar estos colores)
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
# CONFIGURACIÓN DE FORMATO ACADÉMICO
# =====================================================

# Variable global para controlar el formato APA
FORMATO_APA_ACADEMICO = False

def activar_formato_apa():
    """Activa el formato académico APA estricto"""
    global FORMATO_APA_ACADEMICO
    FORMATO_APA_ACADEMICO = True
    print("✅ Formato APA académico activado")

def desactivar_formato_apa():
    """Desactiva el formato académico APA estricto"""
    global FORMATO_APA_ACADEMICO
    FORMATO_APA_ACADEMICO = False
    print("❌ Formato APA académico desactivado")

# =====================================================
# FUNCIONES PARA RANKING POR VARIABLE ESPECÍFICA
# =====================================================

def obtener_variables_principales(dummy_cols):
    """Obtiene la lista de variables principales (sin las subcategorías)"""
    variables = set()
    for col in dummy_cols:
        if '__' in col:
            variable_principal = col.split('__')[0]
            variables.add(variable_principal)
    return sorted(list(variables))

def crear_ranking_por_variable(df, dummy_cols, variable_seleccionada=None, candidato=None):
    """
    Crea ranking de categorías dentro de una variable específica
    
    Parámetros:
    - df: DataFrame con los datos
    - dummy_cols: Lista de columnas dummy
    - variable_seleccionada: Variable específica a analizar (ej: 'formato_del_contenido')
    - candidato: Candidato específico (opcional)
    """
    if variable_seleccionada is None:
        # Si no se especifica variable, devolver análisis general
        return crear_analisis_general(df, dummy_cols, candidato)
    
    # Filtrar por candidato si se especifica
    df_analisis = df.copy()
    if candidato and candidato != "Todos" and 'Candidato' in df.columns:
        df_analisis = df_analisis[df_analisis['Candidato'] == candidato]
    
    # Filtrar solo las columnas dummy de la variable seleccionada
    cols_variable = [col for col in dummy_cols if col.startswith(variable_seleccionada + '__')]
    
    resultados = []
    total_posts = len(df_analisis)
    
    for col in cols_variable:
        if col in df_analisis.columns:
            uso = df_analisis[col].sum()
            porcentaje = (uso / total_posts) * 100 if total_posts > 0 else 0
            
            subcategoria = col.split('__')[1].replace('_', ' ').title()
            
            resultados.append({
                'Variable_Principal': variable_seleccionada.replace('_', ' ').title(),
                'Categoria': subcategoria,
                'Usos': uso,
                'Porcentaje': porcentaje,
                'Variable_Completa': col
            })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados.sort_values('Usos', ascending=False)

def crear_analisis_general(df, dummy_cols, candidato=None, top_n=10):
    """Crea análisis general de todas las variables (comportamiento original)"""
    # Filtrar por candidato si se especifica
    df_analisis = df.copy()
    if candidato and candidato != "Todos" and 'Candidato' in df.columns:
        df_analisis = df_analisis[df_analisis['Candidato'] == candidato]
    
    resultados = []
    total_posts = len(df_analisis)
    
    for col in dummy_cols:
        if col in df_analisis.columns:
            uso = df_analisis[col].sum()
            porcentaje = (uso / total_posts) * 100 if total_posts > 0 else 0
            
            # Extraer categoría y subcategoría
            partes = col.split('__')
            categoria_principal = partes[0].replace('_', ' ').title()
            subcategoria = partes[1].replace('_', ' ').title() if len(partes) > 1 else 'Sin especificar'
            
            resultados.append({
                'Variable_Principal': categoria_principal,
                'Categoria': subcategoria,
                'Usos': uso,
                'Porcentaje': porcentaje,
                'Variable_Completa': col
            })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados.sort_values('Usos', ascending=False).head(top_n)

# =====================================================
# FUNCIONES AUXILIARES PARA EXPORTAR TABLAS
# =====================================================

def exportar_tabla_apa(df, titulo, nombre_archivo, figsize=(12, 8), formato_academico=None):
    """
    Exporta una tabla en formato APA como imagen PNG
    
    Parámetros:
    - df: DataFrame a exportar
    - titulo: Título de la tabla
    - nombre_archivo: Nombre del archivo (sin extensión)
    - figsize: Tamaño de la figura (ancho, alto)
    - formato_academico: Si None, usa la variable global FORMATO_APA_ACADEMICO
    """
    global FORMATO_APA_ACADEMICO
    usar_apa = FORMATO_APA_ACADEMICO if formato_academico is None else formato_academico
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('tight')
    ax.axis('off')
    
    # Preparar datos para la tabla
    df_tabla = df.copy()
    
    if usar_apa:
        # Formato APA académico estricto
        # Añadir números de ranking si no existen
        if df_tabla.index.name != "Ranking" and not df_tabla.index.equals(pd.RangeIndex(len(df_tabla))):
            df_tabla = df_tabla.reset_index(drop=True)
            df_tabla.index = df_tabla.index + 1
            df_tabla.index.name = "Ranking"
        
        # Formatear columnas numéricas según APA
        for col in df_tabla.columns:
            if df_tabla[col].dtype in ['float64', 'float32']:
                if 'Porcentaje' in col or 'porcentaje' in col.lower():
                    df_tabla[col] = df_tabla[col].apply(lambda x: f"{x:.1f}")
                else:
                    df_tabla[col] = df_tabla[col].apply(lambda x: f"{x:.2f}")
            elif df_tabla[col].dtype in ['int64', 'int32']:
                df_tabla[col] = df_tabla[col].apply(lambda x: f"{x:,}")
        
        # Ajustar nombres de columnas para formato APA
        columnas_apa = []
        for col in df_tabla.columns:
            if col.lower() in ['usos', 'uso']:
                columnas_apa.append('Frecuencia')
            elif col.lower() in ['porcentaje']:
                columnas_apa.append('Porcentaje (%)')
            elif col.lower() in ['categoria', 'categoría']:
                columnas_apa.append('Categoría')
            elif col.lower() in ['variable_principal']:
                columnas_apa.append('Variable')
            else:
                columnas_apa.append(col)
        df_tabla.columns = columnas_apa
    
    # Crear la tabla
    if usar_apa and df_tabla.index.name:
        # Incluir el índice como primera columna
        cellText = []
        for idx, row in df_tabla.iterrows():
            cellText.append([str(idx)] + [str(val) for val in row.values])
        colLabels = [df_tabla.index.name] + list(df_tabla.columns)
    else:
        cellText = df_tabla.values
        colLabels = df_tabla.columns
    
    tabla = ax.table(cellText=cellText,
                     colLabels=colLabels,
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    
    # Estilo según formato
    if usar_apa:
        # Estilo APA académico estricto
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)  # Tamaño de fuente APA más pequeño
        tabla.scale(1, 1.8)     # Escalar para mejor legibilidad
        
        # Formatear encabezados (solo borde inferior, sin fondo)
        for i in range(len(colLabels)):
            tabla[(0, i)].set_facecolor('white')
            tabla[(0, i)].set_text_props(weight='bold')
            tabla[(0, i)].set_height(0.08)
            # Agregar borde inferior grueso (estilo APA)
            tabla[(0, i)].get_path().set_linewidth(2)
        
        # Formatear celdas de datos (sin bordes laterales, estilo APA)
        for i in range(1, len(cellText) + 1):
            for j in range(len(colLabels)):
                tabla[(i, j)].set_facecolor('white')
                tabla[(i, j)].set_height(0.06)
                # Quitar bordes laterales (estilo APA)
                tabla[(i, j)].get_path().set_linewidth(0.5)
        
        # Título en formato APA (Tabla N. Título descriptivo)
        titulo_apa = f"Tabla. {titulo}" if not titulo.startswith("Tabla") else titulo
        plt.title(titulo_apa, fontsize=12, fontweight='bold', pad=20, loc='left')
        
    else:
        # Estilo original más colorido
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(11)
        tabla.scale(1, 2)
        
        # Formatear encabezados (negrita y fondo gris claro)
        for i in range(len(colLabels)):
            tabla[(0, i)].set_facecolor('#E6E6E6')
            tabla[(0, i)].set_text_props(weight='bold')
            tabla[(0, i)].set_height(0.08)
        
        # Alternar colores de filas para mejor legibilidad
        for i in range(1, len(cellText) + 1):
            for j in range(len(colLabels)):
                if i % 2 == 0:
                    tabla[(i, j)].set_facecolor('#F8F9FA')
                tabla[(i, j)].set_height(0.06)
        
        # Título normal
        plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    # Guardar con alta calidad
    plt.savefig(f'{nombre_archivo}.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()
    plt.close()
    
    # Alternar colores de filas para mejor legibilidad
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                tabla[(i, j)].set_facecolor('#F8F8F8')  # Gris muy claro
            tabla[(i, j)].set_height(0.06)
    
    # Título en formato APA
    plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    # Guardar con alta calidad
    plt.savefig(f'{nombre_archivo}.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()
    plt.close()

def crear_grafico_barras_mejorado(df, x_col, y_col, titulo, nombre_archivo, 
                                 color_col=None, figsize=(12, 8), rotar_x=45):
    """
    Crear gráfico de barras con estilo mejorado
    
    Parámetros ajustables:
    - figsize: Tamaño del gráfico
    - rotar_x: Grados de rotación para etiquetas X
    - color_col: Columna para colorear barras
    """
    plt.figure(figsize=figsize)
    
    if color_col and color_col in df.columns:
        # Gráfico con colores por categoría
        for i, categoria in enumerate(df[color_col].unique()):
            datos_cat = df[df[color_col] == categoria]
            plt.bar(datos_cat[x_col], datos_cat[y_col], 
                   label=categoria, color=COLORES_PRINCIPALES[i % len(COLORES_PRINCIPALES)],
                   alpha=0.8, edgecolor='black', linewidth=0.5)
    else:
        # Gráfico simple
        plt.bar(df[x_col], df[y_col], color=COLORES_PRINCIPALES[0], 
               alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Formateo APA
    plt.title(titulo, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel(x_col.replace('_', ' ').title(), fontsize=12)
    plt.ylabel(y_col.replace('_', ' ').title(), fontsize=12)
    
    if rotar_x:
        plt.xticks(rotation=rotar_x, ha='right')
    
    if color_col:
        plt.legend(frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig(f'{nombre_archivo}.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

# =====================================================
# CARGA Y PREPARACIÓN DE DATOS
# =====================================================

print("Cargando datos...")
df = pd.read_excel("recodificado.xlsx")
print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")

# Identificar columnas dummy automáticamente
dummy_cols = [col for col in df.columns if '__' in col]
print(f"Columnas dummy encontradas: {len(dummy_cols)}")

# =====================================================
# CONFIGURACIÓN INICIAL Y OPCIONES DE USUARIO
# =====================================================

print("\n" + "🔧 CONFIGURACIÓN DEL ANÁLISIS")
print("="*50)

# Opciones de configuración
print("Opciones disponibles:")
print("1. Activar formato APA académico estricto")
print("2. Mantener formato estándar con colores")
print("3. Análisis por variable específica")
print("4. Análisis general (todas las variables)")

# Aquí puedes cambiar estas opciones manualmente
USAR_FORMATO_APA = input("¿Activar formato APA académico? (s/n): ").lower().startswith('s')
USAR_ANALISIS_ESPECIFICO = input("¿Realizar análisis por variable específica? (s/n): ").lower().startswith('s')

if USAR_FORMATO_APA:
    activar_formato_apa()
else:
    desactivar_formato_apa()

# Si se elige análisis específico, preguntar qué variable
VARIABLE_ESPECIFICA = None
if USAR_ANALISIS_ESPECIFICO:
    variables_disponibles = obtener_variables_principales(dummy_cols)
    print("\nVariables disponibles:")
    for i, var in enumerate(variables_disponibles, 1):
        print(f"{i}. {var.replace('_', ' ').title()}")
    
    try:
        opcion = int(input(f"Seleccionar variable (1-{len(variables_disponibles)}): ")) - 1
        if 0 <= opcion < len(variables_disponibles):
            VARIABLE_ESPECIFICA = variables_disponibles[opcion]
            print(f"✅ Variable seleccionada: {VARIABLE_ESPECIFICA.replace('_', ' ').title()}")
        else:
            print("❌ Opción inválida, se usará análisis general")
            USAR_ANALISIS_ESPECIFICO = False
    except:
        print("❌ Entrada inválida, se usará análisis general")
        USAR_ANALISIS_ESPECIFICO = False

# =====================================================
# 1. ANÁLISIS POR CANDIDATO CON NUEVAS OPCIONES
# =====================================================

print("\n" + "="*50)
print("1. ANÁLISIS POR CANDIDATO")
print("="*50)

if 'Candidato' in df.columns:
    candidatos = df['Candidato'].unique()
    print(f"Candidatos encontrados: {candidatos}")
    
    if USAR_ANALISIS_ESPECIFICO:
        print(f"📊 Analizando variable específica: {VARIABLE_ESPECIFICA.replace('_', ' ').title()}")
        
        # Análisis por variable específica para cada candidato
        for candidato in candidatos:
            print(f"\n--- Análisis para {candidato} ---")
            
            df_ranking = crear_ranking_por_variable(df, dummy_cols, VARIABLE_ESPECIFICA, candidato)
            
            if len(df_ranking) > 0:
                # Mostrar ranking
                print(f"Ranking de {VARIABLE_ESPECIFICA.replace('_', ' ').title()} para {candidato}:")
                for i, (_, row) in enumerate(df_ranking.head(10).iterrows(), 1):
                    print(f"  {i}. {row['Categoria']}: {row['Usos']} usos ({row['Porcentaje']:.1f}%)")
                
                # Exportar tabla individual
                df_export = df_ranking.head(10)[['Categoria', 'Usos', 'Porcentaje']].copy()
                df_export.index = range(1, len(df_export) + 1)
                df_export.index.name = "Ranking"
                
                nombre_archivo = f"tabla_ranking_{VARIABLE_ESPECIFICA}_{candidato.replace(' ', '_')}"
                titulo_tabla = f"Ranking de {VARIABLE_ESPECIFICA.replace('_', ' ').title()} - {candidato}"
                
                exportar_tabla_apa(df_export, titulo_tabla, nombre_archivo, figsize=(12, 8))
        
        # Tabla comparativa entre candidatos para la variable específica
        print(f"\n=== TABLA COMPARATIVA: {VARIABLE_ESPECIFICA.replace('_', ' ').title().upper()} ===")
        
        tabla_comparativa = []
        for candidato in candidatos:
            df_ranking = crear_ranking_por_variable(df, dummy_cols, VARIABLE_ESPECIFICA, candidato)
            
            for i, (_, row) in enumerate(df_ranking.head(5).iterrows(), 1):
                tabla_comparativa.append({
                    'Candidato': candidato,
                    'Ranking': i,
                    'Categoria': row['Categoria'],
                    'Usos': int(row['Usos']),
                    'Porcentaje': row['Porcentaje']
                })
        
        df_tabla_comparativa = pd.DataFrame(tabla_comparativa)
        
        if len(df_tabla_comparativa) > 0:
            nombre_archivo_comp = f"tabla_comparativa_{VARIABLE_ESPECIFICA}_todos_candidatos"
            titulo_comp = f"Comparativa de {VARIABLE_ESPECIFICA.replace('_', ' ').title()} por Candidato"
            
            exportar_tabla_apa(df_tabla_comparativa, titulo_comp, nombre_archivo_comp, figsize=(16, 12))
    
    else:
        # Análisis general original (todas las variables)
        print("📊 Realizando análisis general de todas las variables")
        
        # Crear DataFrame de resultados (código original)
        resultados_candidato = []
        
        for candidato in candidatos:
            df_candidato = df[df['Candidato'] == candidato]
            total_posts = len(df_candidato)
            
            for col in dummy_cols:
                if col in df.columns:
                    uso = df_candidato[col].sum()
                    porcentaje = (uso / total_posts) * 100 if total_posts > 0 else 0
                    
                    # Extraer nombres limpios
                    partes = col.split('__')
                    categoria_principal = partes[0].replace('_', ' ').title()
                    subcategoria = partes[1].replace('_', ' ').title() if len(partes) > 1 else 'Sin especificar'
                    
                    resultados_candidato.append({
                        'Candidato': candidato,
                        'Variable_Principal': categoria_principal,
                        'Categoria': subcategoria,
                        'Usos': uso,
                        'Total_Posts': total_posts,
                        'Porcentaje': round(porcentaje, 2),
                        'Variable_Completa': col
                    })
        
        df_resultados = pd.DataFrame(resultados_candidato)
        
        # TABLA 1: Top estrategias por candidato (todas las variables)
        print("\n=== CREANDO TABLA 1: TOP ESTRATEGIAS GENERALES POR CANDIDATO ===")
        
        tabla_top_estrategias = []
        for candidato in candidatos:
            df_cand = df_resultados[df_resultados['Candidato'] == candidato]
            top_5 = df_cand.nlargest(5, 'Porcentaje')
            
            for i, (_, row) in enumerate(top_5.iterrows()):
                tabla_top_estrategias.append({
                    'Candidato': candidato if i == 0 else '',
                    'Ranking': i+1,
                    'Variable': row['Variable_Principal'],
                    'Categoria': row['Categoria'],
                    'Usos': int(row['Usos']),
                    'Porcentaje': row['Porcentaje']
                })
            
            # Agregar fila separadora si no es el último candidato
            if candidato != candidatos[-1]:
                tabla_top_estrategias.append({
                    'Candidato': '—', 'Ranking': '—', 'Variable': '—', 
                    'Categoria': '—', 'Usos': '—', 'Porcentaje': '—'
                })
        
        df_tabla_top = pd.DataFrame(tabla_top_estrategias)
        exportar_tabla_apa(df_tabla_top, 
                          "Top 5 Estrategias Más Utilizadas por Candidato (Análisis General)",
                          "tabla_1_top_estrategias_general",
                          figsize=(16, 12))
    
    # GRÁFICO 1: Comparación de estrategias principales
    print("\n=== CREANDO GRÁFICO 1: COMPARACIÓN ESTRATEGIAS PRINCIPALES ===")
    
    # Seleccionar las 8 estrategias más usadas globalmente
    estrategias_principales = (df_resultados.groupby('Subcategoria')['Usos']
                             .sum().nlargest(8).index.tolist())
    
    # Crear datos para gráfico comparativo
    datos_grafico = []
    for candidato in candidatos:
        for estrategia in estrategias_principales:
            porcentaje = df_resultados[
                (df_resultados['Candidato'] == candidato) & 
                (df_resultados['Subcategoria'] == estrategia)
            ]['Porcentaje'].sum()
            
            datos_grafico.append({
                'Candidato': candidato,
                'Estrategia': estrategia,
                'Porcentaje': porcentaje
            })
    
    df_grafico = pd.DataFrame(datos_grafico)
    
    # Crear gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Configurar posiciones de barras
    x = np.arange(len(estrategias_principales))
    ancho_barra = 0.35
    multiplicador = 0
    
    for i, candidato in enumerate(candidatos):
        datos_candidato = df_grafico[df_grafico['Candidato'] == candidato]
        valores = [datos_candidato[datos_candidato['Estrategia'] == est]['Porcentaje'].iloc[0] 
                  if len(datos_candidato[datos_candidato['Estrategia'] == est]) > 0 else 0 
                  for est in estrategias_principales]
        
        offset = ancho_barra * multiplicador
        barras = ax.bar(x + offset, valores, ancho_barra, 
                       label=candidato, color=COLORES_PRINCIPALES[i],
                       alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # Añadir valores en las barras
        for j, barra in enumerate(barras):
            altura = barra.get_height()
            if altura > 0:
                ax.text(barra.get_x() + barra.get_width()/2., altura + 0.5,
                       f'{altura:.1f}%', ha='center', va='bottom', fontsize=10)
        
        multiplicador += 1
    
    # Formateo del gráfico
    ax.set_xlabel('Estrategias de Comunicación', fontsize=14)
    ax.set_ylabel('Porcentaje de Uso (%)', fontsize=14)
    ax.set_title('Figura 1. Comparación de Estrategias Principales por Candidato', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x + ancho_barra * (len(candidatos) - 1) / 2)
    ax.set_xticklabels([est.replace(' ', '\n') for est in estrategias_principales], 
                      rotation=0, ha='center')
    ax.legend(frameon=True, fancybox=True, shadow=True)
    ax.set_ylim(0, max([max(df_grafico[df_grafico['Candidato'] == c]['Porcentaje']) 
                       for c in candidatos]) * 1.15)
    
    plt.tight_layout()
    plt.savefig('figura_1_comparacion_estrategias.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

# =====================================================
# 2. EVOLUCIÓN TEMPORAL MEJORADA
# =====================================================

print("\n" + "="*50)
print("2. EVOLUCIÓN TEMPORAL")
print("="*50)

if 'Fecha' in df.columns:
    # Diccionario de meses en español
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    def convertir_fecha(fecha_str):
        """Convierte fechas en formato 'DD de MES' a datetime"""
        try:
            if pd.isna(fecha_str):
                return None
            partes = str(fecha_str).lower().split(' de ')
            if len(partes) == 2:
                dia = int(partes[0])
                mes = meses.get(partes[1], 1)
                return datetime(2024, mes, dia)  # AJUSTAR AÑO SEGÚN DATOS
        except:
            pass
        return None
    
    df['Fecha_convertida'] = df['Fecha'].apply(convertir_fecha)
    df_temporal = df.dropna(subset=['Fecha_convertida']).copy()
    
    # Seleccionar estrategias clave para seguimiento (AJUSTAR SEGÚN INTERÉS)
    estrategias_temporales = [
        col for col in dummy_cols 
        if any(palabra in col.lower() for palabra in [
            'meme', 'logotipo', 'testimonio', 'plain_folks', 'orquestacion',
            'celebrity', 'bandwagon', 'transfer'  # Añadir más según necesidad
        ])
    ][:6]  # Máximo 6 líneas para claridad
    
    if estrategias_temporales:
        print(f"Analizando evolución de {len(estrategias_temporales)} estrategias")
        
        # Agrupar por fecha
        df_temp_agrupado = df_temporal.groupby('Fecha_convertida')[estrategias_temporales].sum().reset_index()
        
        # GRÁFICO 2: Evolución temporal
        fig, ax = plt.subplots(figsize=(16, 10))
        
        for i, estrategia in enumerate(estrategias_temporales):
            nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title()
            ax.plot(df_temp_agrupado['Fecha_convertida'], 
                   df_temp_agrupado[estrategia], 
                   marker='o', markersize=6, linewidth=2.5, 
                   label=nombre_limpio, color=COLORES_PRINCIPALES[i],
                   alpha=0.8)
        
        # Formateo
        ax.set_title('Figura 2. Evolución Temporal de Estrategias Comunicativas Clave', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Fecha', fontsize=14)
        ax.set_ylabel('Frecuencia de Uso', fontsize=14)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
        ax.tick_params(axis='x', rotation=45)
        
        # Mejorar formato de fechas en eje X
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        
        plt.tight_layout()
        plt.savefig('figura_2_evolucion_temporal.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
        
        # TABLA 2: Resumen estadístico temporal
        estadisticas_temporales = []
        for estrategia in estrategias_temporales:
            valores = df_temp_agrupado[estrategia]
            nombre_limpio = estrategia.split('__')[1].replace('_', ' ').title()
            
            estadisticas_temporales.append({
                'Estrategia': nombre_limpio,
                'Total': int(valores.sum()),
                'Promedio': round(valores.mean(), 2),
                'Máximo': int(valores.max()),
                'Mínimo': int(valores.min()),
                'Desv. Estándar': round(valores.std(), 2)
            })
        
        df_estadisticas = pd.DataFrame(estadisticas_temporales)
        exportar_tabla_apa(df_estadisticas,
                          "Tabla 2. Estadísticas Descriptivas de Uso Temporal por Estrategia",
                          "tabla_2_estadisticas_temporales",
                          figsize=(14, 8))

# =====================================================
# 3. ANÁLISIS DE CRUCES MEJORADO
# =====================================================

print("\n" + "="*50)
print("3. ANÁLISIS DE CRUCES: APARICIÓN vs IMAGEN CORPORATIVA")
print("="*50)

aparicion_cols = [col for col in dummy_cols if 'aparicion' in col.lower()]
imagen_cols = [col for col in dummy_cols if 'imagen_corporativa' in col.lower()]

if aparicion_cols and imagen_cols:
    print(f"Variables de aparición: {len(aparicion_cols)}")
    print(f"Variables de imagen corporativa: {len(imagen_cols)}")
    
    # Crear análisis de cruces más sistemático
    cruces_significativos = []
    
    for aparicion_col in aparicion_cols:
        for imagen_col in imagen_cols:
            # Crear tabla de contingencia
            tabla = pd.crosstab(df[aparicion_col], df[imagen_col], margins=False)
            
            # Solo analizar si hay variación suficiente
            if tabla.shape[0] > 1 and tabla.shape[1] > 1 and tabla.sum().sum() > 10:
                aparicion_nombre = aparicion_col.split('__')[1].replace('_', ' ').title()
                imagen_nombre = imagen_col.split('__')[1].replace('_', ' ').title()
                
                # Calcular porcentajes
                total = tabla.sum().sum()
                
                # Buscar combinaciones más frecuentes
                for i in tabla.index:
                    for j in tabla.columns:
                        if tabla.loc[i, j] > 0:
                            cruces_significativos.append({
                                'Aparición': aparicion_nombre,
                                'Imagen_Corporativa': imagen_nombre,
                                'Aparición_Valor': 'Sí' if i == 1 else 'No',
                                'Imagen_Valor': 'Sí' if j == 1 else 'No',
                                'Frecuencia': int(tabla.loc[i, j]),
                                'Porcentaje': round((tabla.loc[i, j] / total) * 100, 2)
                            })
    
    if cruces_significativos:
        df_cruces = pd.DataFrame(cruces_significativos)
        
        # Filtrar solo combinaciones con ambos=Sí y frecuencia > 0
        df_cruces_positivos = df_cruces[
            (df_cruces['Aparición_Valor'] == 'Sí') & 
            (df_cruces['Imagen_Valor'] == 'Sí') &
            (df_cruces['Frecuencia'] > 0)
        ].sort_values('Frecuencia', ascending=False)
        
        if len(df_cruces_positivos) > 0:
            # TABLA 3: Cruces más significativos
            tabla_cruces_exportar = df_cruces_positivos[
                ['Aparición', 'Imagen_Corporativa', 'Frecuencia', 'Porcentaje']
            ].head(15)  # Top 15 cruces
            
            exportar_tabla_apa(tabla_cruces_exportar,
                              "Tabla 3. Cruces Más Frecuentes: Aparición e Imagen Corporativa",
                              "tabla_3_cruces_aparicion_imagen",
                              figsize=(16, 10))
            
            # GRÁFICO 3: Heatmap de cruces principales
            print("\n=== CREANDO GRÁFICO 3: HEATMAP DE CRUCES ===")
            
            # Crear matriz para heatmap (tomar top combinaciones)
            top_apariciones = df_cruces_positivos['Aparición'].value_counts().head(5).index
            top_imagenes = df_cruces_positivos['Imagen_Corporativa'].value_counts().head(5).index
            
            matriz_heatmap = np.zeros((len(top_apariciones), len(top_imagenes)))
            
            for i, aparicion in enumerate(top_apariciones):
                for j, imagen in enumerate(top_imagenes):
                    valor = df_cruces_positivos[
                        (df_cruces_positivos['Aparición'] == aparicion) &
                        (df_cruces_positivos['Imagen_Corporativa'] == imagen)
                    ]['Frecuencia'].sum()
                    matriz_heatmap[i, j] = valor
            
            # Crear heatmap
            fig, ax = plt.subplots(figsize=(12, 8))
            
            heatmap = sns.heatmap(matriz_heatmap, 
                                 xticklabels=[img.replace(' ', '\n') for img in top_imagenes],
                                 yticklabels=[ap.replace(' ', '\n') for ap in top_apariciones],
                                 annot=True, fmt='.0f', cmap='Blues',
                                 cbar_kws={'label': 'Frecuencia'},
                                 square=True, linewidths=0.5)
            
            ax.set_title('Figura 3. Mapa de Calor: Cruces Aparición e Imagen Corporativa', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Estrategias de Imagen Corporativa', fontsize=14)
            ax.set_ylabel('Estrategias de Aparición', fontsize=14)
            
            plt.tight_layout()
            plt.savefig('figura_3_heatmap_cruces.png', dpi=300, bbox_inches='tight')
            plt.show()
            plt.close()

# =====================================================
# 4. PROPAGANDA POR CANDIDATO (MEJORADO)
# =====================================================

print("\n" + "="*50)
print("4. ANÁLISIS DE TÉCNICAS DE PROPAGANDA")
print("="*50)

propaganda_cols = [col for col in dummy_cols if 'institute' in col.lower() or 'propaganda' in col.lower()]

if propaganda_cols and 'Candidato' in df.columns:
    print(f"Técnicas de propaganda encontradas: {len(propaganda_cols)}")
    
    # Crear datos para análisis
    candidatos = df['Candidato'].unique()
    datos_propaganda = []
    
    for candidato in candidatos:
        df_cand = df[df['Candidato'] == candidato]
        total_posts = len(df_cand)
        
        for col in propaganda_cols:
            if col in df.columns:
                usos = df_cand[col].sum()
                porcentaje = (usos / total_posts) * 100 if total_posts > 0 else 0
                nombre_tecnica = col.split('__')[1].replace('_', ' ').title()
                
                datos_propaganda.append({
                    'Candidato': candidato,
                    'Técnica': nombre_tecnica,
                    'Usos': int(usos),
                    'Total_Posts': total_posts,
                    'Porcentaje': round(porcentaje, 2)
                })
    
    df_propaganda = pd.DataFrame(datos_propaganda)
    
    # TABLA 4: Resumen de propaganda por candidato
    tabla_propaganda_resumen = df_propaganda.pivot(index='Técnica', 
                                                  columns='Candidato', 
                                                  values='Porcentaje').fillna(0)
    tabla_propaganda_resumen['Total'] = df_propaganda.groupby('Técnica')['Usos'].sum()
    tabla_propaganda_resumen = tabla_propaganda_resumen.sort_values('Total', ascending=False)
    
    # Formatear para exportar
    tabla_propaganda_exportar = tabla_propaganda_resumen.copy()
    for col in tabla_propaganda_exportar.columns:
        if col != 'Total':
            tabla_propaganda_exportar[col] = tabla_propaganda_exportar[col].apply(lambda x: f"{x:.1f}%")
    
    tabla_propaganda_exportar = tabla_propaganda_exportar.reset_index()
    
    exportar_tabla_apa(tabla_propaganda_exportar,
                      "Tabla 4. Uso de Técnicas de Propaganda por Candidato (Porcentajes)",
                      "tabla_4_propaganda_candidatos",
                      figsize=(16, 12))
    
    # GRÁFICO 4: Barras apiladas mejorado
    print("\n=== CREANDO GRÁFICO 4: PROPAGANDA POR CANDIDATO ===")
    
    # Seleccionar las 8 técnicas más usadas
    top_tecnicas = tabla_propaganda_resumen.head(8).index
    
    # Preparar datos para gráfico apilado
    datos_grafico_prop = df_propaganda[df_propaganda['Técnica'].isin(top_tecnicas)]
    pivot_propaganda = datos_grafico_prop.pivot(index='Candidato', 
                                               columns='Técnica', 
                                               values='Usos').fillna(0)
    
    # Crear gráfico apilado
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Crear barras apiladas
    pivot_propaganda.plot(kind='bar', stacked=True, ax=ax, 
                         color=COLORES_PRINCIPALES[:len(pivot_propaganda.columns)],
                         alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_title('Figura 4. Distribución de Técnicas de Propaganda por Candidato', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Candidato', fontsize=14)
    ax.set_ylabel('Frecuencia de Uso', fontsize=14)
    ax.legend(title='Técnicas de Propaganda', bbox_to_anchor=(1.05, 1), 
             loc='upper left', frameon=True)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('figura_4_propaganda_apilada.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

# =====================================================
# 5. ANÁLISIS PLAIN-FOLKS DETALLADO
# =====================================================

print("\n" + "="*50)
print("5. ANÁLISIS DETALLADO: ESTRATEGIA PLAIN-FOLKS")
print("="*50)

# Buscar columnas relacionadas con Plain-folks
plain_folks_cols = [col for col in dummy_cols if 'plain' in col.lower() or 'pueblo' in col.lower()]
contexto_cols = [col for col in dummy_cols if 'contexto' in col.lower()]
aparicion_cols = [col for col in dummy_cols if 'aparicion' in col.lower()]

if plain_folks_cols:
    print(f"Variables Plain-folks encontradas: {len(plain_folks_cols)}")
    
    # Filtrar posts que usan Plain-folks
    df_plain = df[df[plain_folks_cols].sum(axis=1) > 0].copy()
    
    if len(df_plain) > 0:
        print(f"Posts con estrategia Plain-folks: {len(df_plain)}")
        
        # ANÁLISIS 1: Plain-folks por candidato
        if 'Candidato' in df.columns:
            plain_por_candidato = []
            
            for candidato in df['Candidato'].unique():
                df_cand = df[df['Candidato'] == candidato]
                df_cand_plain = df_cand[df_cand[plain_folks_cols].sum(axis=1) > 0]
                
                total_posts = len(df_cand)
                posts_plain = len(df_cand_plain)
                porcentaje = (posts_plain / total_posts) * 100 if total_posts > 0 else 0
                
                plain_por_candidato.append({
                    'Candidato': candidato,
                    'Posts_Totales': total_posts,
                    'Posts_Plain_Folks': posts_plain,
                    'Porcentaje_Uso': round(porcentaje, 2),
                    'Intensidad_Promedio': round(df_cand[plain_folks_cols].sum(axis=1).mean(), 2)
                })
            
            df_plain_candidatos = pd.DataFrame(plain_por_candidato)
            
            # TABLA 5: Plain-folks por candidato
            exportar_tabla_apa(df_plain_candidatos,
                              "Tabla 5. Uso de Estrategia Plain-Folks por Candidato",
                              "tabla_5_plain_folks_candidatos",
                              figsize=(14, 6))
        
        # ANÁLISIS 2: Plain-folks por contexto
        if contexto_cols:
            print("\n=== ANALIZANDO PLAIN-FOLKS POR CONTEXTO ===")
            
            cruces_contexto = []
            
            for contexto_col in contexto_cols:
                if contexto_col in df.columns:
                    contexto_nombre = contexto_col.split('__')[1].replace('_', ' ').title()
                    
                    # Crear tabla de contingencia
                    tabla_contexto = pd.crosstab(
                        df_plain[contexto_col], 
                        df_plain['Candidato'] if 'Candidato' in df.columns else pd.Series(['Total'] * len(df_plain)),
                        margins=True
                    )
                    
                    # Convertir a formato exportable
                    if tabla_contexto.shape[0] > 2 and tabla_contexto.shape[1] > 2:
                        tabla_exportar = tabla_contexto.copy()
                        tabla_exportar.index = ['No usa ' + contexto_nombre if x == 0 
                                              else 'Usa ' + contexto_nombre if x == 1 
                                              else str(x) for x in tabla_exportar.index]
                        
                        # Guardar tabla
                        exportar_tabla_apa(tabla_exportar,
                                          f"Tabla 6. Plain-Folks por {contexto_nombre}",
                                          f"tabla_6_plain_folks_{contexto_nombre.lower().replace(' ', '_')}",
                                          figsize=(12, 6))
        
        # ANÁLISIS 3: Plain-folks por tipo de compañía/aparición
        if aparicion_cols:
            print("\n=== ANALIZANDO PLAIN-FOLKS POR TIPO DE COMPAÑÍA ===")
            
            for aparicion_col in aparicion_cols:
                if aparicion_col in df.columns:
                    aparicion_nombre = aparicion_col.split('__')[1].replace('_', ' ').title()
                    
                    # Solo analizar apariciones relevantes para Plain-folks
                    if any(palabra in aparicion_nombre.lower() for palabra in 
                          ['familiar', 'votante', 'ciudadano', 'pueblo', 'gente', 'persona']):
                        
                        tabla_aparicion = pd.crosstab(
                            df_plain[aparicion_col],
                            df_plain['Candidato'] if 'Candidato' in df.columns else pd.Series(['Total'] * len(df_plain)),
                            margins=True
                        )
                        
                        if tabla_aparicion.shape[0] > 2 and tabla_aparicion.shape[1] > 2:
                            tabla_aparicion.index = ['Sin ' + aparicion_nombre if x == 0 
                                                   else 'Con ' + aparicion_nombre if x == 1 
                                                   else str(x) for x in tabla_aparicion.index]
                            
                            exportar_tabla_apa(tabla_aparicion,
                                              f"Tabla 7. Plain-Folks con {aparicion_nombre}",
                                              f"tabla_7_plain_folks_{aparicion_nombre.lower().replace(' ', '_')}",
                                              figsize=(12, 6))
        
        # GRÁFICO 5: Análisis visual de Plain-folks
        print("\n=== CREANDO GRÁFICO 5: ANÁLISIS VISUAL PLAIN-FOLKS ===")
        
        if 'Candidato' in df.columns and len(df_plain_candidatos) > 0:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # Subgráfico 1: Porcentaje de uso por candidato
            bars1 = ax1.bar(df_plain_candidatos['Candidato'], 
                           df_plain_candidatos['Porcentaje_Uso'],
                           color=COLORES_PRINCIPALES[:len(df_plain_candidatos)],
                           alpha=0.8, edgecolor='black', linewidth=0.5)
            
            ax1.set_title('Porcentaje de Uso de Plain-Folks', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Candidato', fontsize=12)
            ax1.set_ylabel('Porcentaje (%)', fontsize=12)
            ax1.tick_params(axis='x', rotation=45)
            
            # Añadir valores en las barras
            for bar in bars1:
                altura = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., altura + 0.5,
                        f'{altura:.1f}%', ha='center', va='bottom', fontsize=10)
            
            # Subgráfico 2: Número absoluto de posts
            bars2 = ax2.bar(df_plain_candidatos['Candidato'], 
                           df_plain_candidatos['Posts_Plain_Folks'],
                           color=COLORES_PRINCIPALES[:len(df_plain_candidatos)],
                           alpha=0.8, edgecolor='black', linewidth=0.5)
            
            ax2.set_title('Número Absoluto de Posts Plain-Folks', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Candidato', fontsize=12)
            ax2.set_ylabel('Número de Posts', fontsize=12)
            ax2.tick_params(axis='x', rotation=45)
            
            # Añadir valores en las barras
            for bar in bars2:
                altura = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., altura + 0.2,
                        f'{int(altura)}', ha='center', va='bottom', fontsize=10)
            
            fig.suptitle('Figura 5. Análisis de Estrategia Plain-Folks por Candidato', 
                        fontsize=16, fontweight='bold', y=1.02)
            
            plt.tight_layout()
            plt.savefig('figura_5_plain_folks_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            plt.close()

# =====================================================
# 6. ANÁLISIS DE CORRELACIONES AVANZADO
# =====================================================

print("\n" + "="*50)
print("6. ANÁLISIS DE CORRELACIONES ENTRE ESTRATEGIAS")
print("="*50)

# Seleccionar las estrategias más relevantes para análisis de correlación
estrategias_principales = [col for col in dummy_cols if df[col].sum() >= 5]  # Mínimo 5 usos
print(f"Estrategias con uso significativo: {len(estrategias_principales)}")

if len(estrategias_principales) >= 4:  # Mínimo para análisis de correlación
    
    # Calcular matriz de correlación
    matriz_correlacion = df[estrategias_principales].corr()
    
    # GRÁFICO 6: Heatmap de correlaciones
    print("\n=== CREANDO GRÁFICO 6: MAPA DE CORRELACIONES ===")
    
    # Seleccionar las 15 estrategias más usadas para el heatmap
    top_15_estrategias = df[estrategias_principales].sum().nlargest(15).index.tolist()
    matriz_top15 = df[top_15_estrategias].corr()
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Crear máscara para la matriz triangular superior
    mask = np.triu(np.ones_like(matriz_top15, dtype=bool))
    
    # Crear heatmap
    heatmap_corr = sns.heatmap(matriz_top15, mask=mask, annot=True, fmt='.2f',
                              cmap='RdBu_r', center=0, square=True, linewidths=0.5,
                              cbar_kws={"shrink": 0.8, "label": "Coeficiente de Correlación"})
    
    # Formatear etiquetas
    etiquetas_limpias = [col.split('__')[1].replace('_', ' ').title() 
                        for col in top_15_estrategias]
    heatmap_corr.set_xticklabels(etiquetas_limpias, rotation=45, ha='right')
    heatmap_corr.set_yticklabels(etiquetas_limpias, rotation=0)
    
    ax.set_title('Figura 6. Matriz de Correlaciones entre Estrategias Comunicativas', 
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('figura_6_correlaciones_estrategias.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # TABLA 8: Correlaciones más fuertes (positivas y negativas)
    print("\n=== CREANDO TABLA 8: CORRELACIONES SIGNIFICATIVAS ===")
    
    correlaciones_significativas = []
    
    for i in range(len(matriz_top15.columns)):
        for j in range(i+1, len(matriz_top15.columns)):
            estrategia1 = matriz_top15.columns[i]
            estrategia2 = matriz_top15.columns[j]
            correlacion = matriz_top15.iloc[i, j]
            
            # Solo incluir correlaciones moderadas o fuertes
            if abs(correlacion) >= 0.3:  # AJUSTAR UMBRAL SEGÚN NECESIDAD
                correlaciones_significativas.append({
                    'Estrategia_1': estrategia1.split('__')[1].replace('_', ' ').title(),
                    'Estrategia_2': estrategia2.split('__')[1].replace('_', ' ').title(),
                    'Correlación': round(correlacion, 3),
                    'Fuerza': 'Fuerte' if abs(correlacion) >= 0.7 
                             else 'Moderada' if abs(correlacion) >= 0.5
                             else 'Débil',
                    'Dirección': 'Positiva' if correlacion > 0 else 'Negativa'
                })
    
    if correlaciones_significativas:
        df_correlaciones = pd.DataFrame(correlaciones_significativas)
        df_correlaciones = df_correlaciones.sort_values('Correlación', 
                                                       key=abs, ascending=False)
        
        exportar_tabla_apa(df_correlaciones,
                          "Tabla 8. Correlaciones Significativas entre Estrategias (|r| ≥ 0.3)",
                          "tabla_8_correlaciones_significativas",
                          figsize=(16, 10))

# =====================================================
# RESUMEN EJECUTIVO MEJORADO
# =====================================================

print("\n" + "="*70)
print("RESUMEN EJECUTIVO - ANÁLISIS COMPLETADO")
print("="*70)

# Estadísticas generales
print(f"📊 DATOS PROCESADOS:")
print(f"   • Total de publicaciones analizadas: {df.shape[0]:,}")
print(f"   • Variables dummy identificadas: {len(dummy_cols)}")

if 'Candidato' in df.columns:
    candidatos_unicos = df['Candidato'].nunique()
    print(f"   • Candidatos analizados: {candidatos_unicos}")

# Estrategia más común
if dummy_cols:
    uso_total = df[dummy_cols].sum().sort_values(ascending=False)
    estrategia_top = uso_total.index[0].split('__')[1].replace('_', ' ').title()
    print(f"   • Estrategia más utilizada: {estrategia_top} ({uso_total.iloc[0]} usos)")

# Archivos generados
archivos_generados = [
    "📈 GRÁFICOS GENERADOS:",
    "   • figura_1_comparacion_estrategias.png",
    "   • figura_2_evolucion_temporal.png",
    "   • figura_3_heatmap_cruces.png",
    "   • figura_4_propaganda_apilada.png",
    "   • figura_5_plain_folks_analysis.png",
    "   • figura_6_correlaciones_estrategias.png",
    "",
    "📋 TABLAS EXPORTADAS:",
    "   • tabla_1_top_estrategias.png",
    "   • tabla_2_estadisticas_temporales.png",
    "   • tabla_3_cruces_aparicion_imagen.png",
    "   • tabla_4_propaganda_candidatos.png",
    "   • tabla_5_plain_folks_candidatos.png",
    "   • tabla_6_[contexto]_plain_folks.png",
    "   • tabla_7_[aparicion]_plain_folks.png",
    "   • tabla_8_correlaciones_significativas.png"
]

for archivo in archivos_generados:
    print(archivo)

print("\n" + "="*70)
print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
print("   Todos los gráficos y tablas han sido exportados en formato PNG")
print("   con estándares de calidad para publicación académica (APA).")
print("="*70)

# =====================================================
# CONFIGURACIÓN DE FORMATO ACADÉMICO
# =====================================================

# Variable global para controlar el formato APA
FORMATO_APA_ACADEMICO = False

def activar_formato_apa():
    """Activa el formato académico APA estricto"""
    global FORMATO_APA_ACADEMICO
    FORMATO_APA_ACADEMICO = True
    print("✅ Formato APA académico activado")

def desactivar_formato_apa():
    """Desactiva el formato académico APA estricto"""
    global FORMATO_APA_ACADEMICO
    FORMATO_APA_ACADEMICO = False
    print("❌ Formato APA académico desactivado")

# =====================================================
# FUNCIONES PARA RANKING POR VARIABLE ESPECÍFICA
# =====================================================

def obtener_variables_principales(dummy_cols):
    """Obtiene la lista de variables principales (sin las subcategorías)"""
    variables = set()
    for col in dummy_cols:
        if '__' in col:
            variable_principal = col.split('__')[0]
            variables.add(variable_principal)
    return sorted(list(variables))

def crear_ranking_por_variable(df, dummy_cols, variable_seleccionada=None, candidato=None):
    """
    Crea ranking de categorías dentro de una variable específica
    
    Parámetros:
    - df: DataFrame con los datos
    - dummy_cols: Lista de columnas dummy
    - variable_seleccionada: Variable específica a analizar (ej: 'formato_del_contenido')
    - candidato: Candidato específico (opcional)
    """
    if variable_seleccionada is None:
        # Si no se especifica variable, devolver análisis general
        return crear_analisis_general(df, dummy_cols, candidato)
    
    # Filtrar por candidato si se especifica
    df_analisis = df.copy()
    if candidato and candidato != "Todos" and 'Candidato' in df.columns:
        df_analisis = df_analisis[df_analisis['Candidato'] == candidato]
    
    # Filtrar solo las columnas dummy de la variable seleccionada
    cols_variable = [col for col in dummy_cols if col.startswith(variable_seleccionada + '__')]
    
    resultados = []
    total_posts = len(df_analisis)
    
    for col in cols_variable:
        if col in df_analisis.columns:
            uso = df_analisis[col].sum()
            porcentaje = (uso / total_posts) * 100 if total_posts > 0 else 0
            
            subcategoria = col.split('__')[1].replace('_', ' ').title()
            
            resultados.append({
                'Variable_Principal': variable_seleccionada.replace('_', ' ').title(),
                'Categoria': subcategoria,
                'Usos': uso,
                'Porcentaje': porcentaje,
                'Variable_Completa': col
            })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados.sort_values('Usos', ascending=False)

def crear_analisis_general(df, dummy_cols, candidato=None, top_n=10):
    """Crea análisis general de todas las variables (comportamiento original)"""
    # Filtrar por candidato si se especifica
    df_analisis = df.copy()
    if candidato and candidato != "Todos" and 'Candidato' in df.columns:
        df_analisis = df_analisis[df_analisis['Candidato'] == candidato]
    
    resultados = []
    total_posts = len(df_analisis)
    
    for col in dummy_cols:
        if col in df_analisis.columns:
            uso = df_analisis[col].sum()
            porcentaje = (uso / total_posts) * 100 if total_posts > 0 else 0
            
            # Extraer categoría y subcategoría
            partes = col.split('__')
            categoria_principal = partes[0].replace('_', ' ').title()
            subcategoria = partes[1].replace('_', ' ').title() if len(partes) > 1 else 'Sin especificar'
            
            resultados.append({
                'Variable_Principal': categoria_principal,
                'Categoria': subcategoria,
                'Usos': uso,
                'Porcentaje': porcentaje,
                'Variable_Completa': col
            })
    
    df_resultados = pd.DataFrame(resultados)
    return df_resultados.sort_values('Usos', ascending=False).head(top_n)

# =====================================================
# FUNCIONES AUXILIARES PARA EXPORTAR TABLAS MEJORADAS
# =====================================================