# 📊 Análisis de Campaña Electoral - Nuevas Funcionalidades

## 🎯 Nuevas Características Añadidas

### 1. **Ranking por Variable Específica**
Ahora puedes analizar cada variable de forma independiente, sin mezclar categorías de diferentes variables.

### 2. **Formato APA Académico**
Toggle para activar un formato académico estricto según normas APA para tablas profesionales.

## 🚀 Cómo Usar las Nuevas Funcionalidades

### **Opción 1: Análisis Interactivo (Recomendado)**

```powershell
# Ejecutar el análisis principal con opciones interactivas
python analisis_campana_electoral.py
```

El script te preguntará:
1. **¿Activar formato APA académico?** (s/n)
2. **¿Realizar análisis por variable específica?** (s/n)
3. **Seleccionar variable** (si elegiste análisis específico)

### **Opción 2: Modificar Variables Directamente**

Edita las variables al inicio del archivo `analisis_campana_electoral.py`:

```python
# Configuración manual (líneas ~280-285)
USAR_FORMATO_APA = True  # True para formato académico, False para estándar
USAR_ANALISIS_ESPECIFICO = True  # True para variable específica, False para general
VARIABLE_ESPECIFICA = "formato_del_contenido"  # Nombre de la variable
```

### **Opción 3: Usar Funciones Directamente**

```python
import pandas as pd
from analisis_campana_electoral import *

# Cargar datos
df = pd.read_excel("recodificado.xlsx")
dummy_cols = [col for col in df.columns if '__' in col]

# Activar formato APA
activar_formato_apa()

# Obtener variables disponibles
variables = obtener_variables_principales(dummy_cols)
print("Variables disponibles:", variables)

# Análisis por variable específica
df_ranking = crear_ranking_por_variable(df, dummy_cols, "formato_del_contenido", "Candidato1")

# Exportar tabla
exportar_tabla_apa(df_ranking.head(5), "Mi Tabla", "mi_archivo")
```

## 📋 Tipos de Análisis Disponibles

### **Análisis General (Original)**
- Mezcla todas las categorías de todas las variables
- Muestra el top N global
- Útil para panorama general

**Ejemplo de salida:**
```
1. Formato Del Contenido - Fotografía: 45 usos
2. Recursos De Propaganda - Testimonio: 32 usos
3. Imagen Corporativa - Logotipo: 28 usos
```

### **Análisis por Variable Específica (Nuevo)**
- Analiza solo una variable a la vez
- No mezcla categorías de diferentes variables
- Más específico y detallado

**Ejemplo de salida para "Formato del Contenido":**
```
1. Fotografía: 45 usos (67.2%)
2. Meme: 15 usos (22.4%)
3. Collage: 7 usos (10.4%)
```

## 🎨 Formatos de Tabla Disponibles

### **Formato Estándar**
- Colorido y visual
- Mejor para presentaciones
- Filas alternadas en colores
- Encabezados con fondo gris

### **Formato APA Académico**
- Cumple normas APA estrictas
- Solo bordes horizontales
- Fondo blanco
- Numeración de ranking incluida
- Apto para publicaciones académicas

## 📊 Variables Principales Detectadas Automáticamente

El sistema detecta automáticamente variables como:
- `formato_del_contenido`
- `aparicion_de_terceras_personas`
- `contexto_de_la_imagen`
- `imagen_corporativa`
- `recursos_de_propaganda_segun_el_institute_for_propaganda`
- `reglas_de_la_propaganda_segun_domenach`

## 📁 Archivos Generados

### **Análisis General:**
- `tabla_1_top_estrategias_general.png`
- `figura_1_comparacion_estrategias.png`

### **Análisis por Variable Específica:**
- `tabla_ranking_[variable]_[candidato].png`
- `tabla_comparativa_[variable]_todos_candidatos.png`

### **Formatos:**
- **Estándar:** Colorido, visual
- **APA:** Profesional, académico

## 🔧 Configuración Avanzada

### **Cambiar Tamaño de Tablas:**
```python
exportar_tabla_apa(df, "Título", "archivo", figsize=(16, 10))  # Más grande
```

### **Forzar Formato Específico:**
```python
exportar_tabla_apa(df, "Título", "archivo", formato_academico=True)  # Forzar APA
```

### **Cambiar Número de Rankings:**
```python
df_ranking = crear_ranking_por_variable(df, dummy_cols, "variable", "candidato")
top_10 = df_ranking.head(10)  # Solo top 10
```

## 📚 Ejemplos de Uso Prácticos

### **Caso 1: Análisis de Formatos por Candidato**
```python
# Ver qué formatos usa más cada candidato
for candidato in df['Candidato'].unique():
    ranking = crear_ranking_por_variable(df, dummy_cols, "formato_del_contenido", candidato)
    print(f"\n{candidato}:")
    print(ranking.head(3)[['Categoria', 'Usos', 'Porcentaje']])
```

### **Caso 2: Comparar Técnicas de Propaganda**
```python
# Analizar solo técnicas de propaganda
activar_formato_apa()
ranking_propaganda = crear_ranking_por_variable(df, dummy_cols, "recursos_de_propaganda_segun_el_institute_for_propaganda")
exportar_tabla_apa(ranking_propaganda, "Técnicas de Propaganda", "propaganda_ranking")
```

### **Caso 3: Análisis de Contextos**
```python
# Ver en qué contextos aparecen más
ranking_contextos = crear_ranking_por_variable(df, dummy_cols, "contexto_de_la_imagen")
exportar_tabla_apa(ranking_contextos, "Análisis de Contextos", "contextos_ranking")
```

## ⚠️ Notas Importantes

1. **Archivo requerido:** `recodificado.xlsx` debe estar en el mismo directorio
2. **Columnas dummy:** Deben seguir el formato `variable__categoria`
3. **Formato APA:** Se recomienda para publicaciones académicas
4. **Análisis específico:** Más preciso para estudios detallados
5. **Rendimiento:** Variables específicas son más rápidas de procesar

## 🆘 Solución de Problemas

### **Error: Variable no encontrada**
```python
# Verificar variables disponibles
variables = obtener_variables_principales(dummy_cols)
print("Variables disponibles:", variables)
```

### **Error: Archivo no encontrado**
- Verificar que `recodificado.xlsx` existe
- Verificar que estás en el directorio correcto

### **Error: Sin datos para candidato**
```python
# Verificar candidatos disponibles
print("Candidatos disponibles:", df['Candidato'].unique())
```

## 📞 Soporte

Para problemas o sugerencias, revisa:
1. Los archivos de ejemplo generados
2. Los mensajes de consola durante la ejecución
3. La estructura de tu archivo Excel
