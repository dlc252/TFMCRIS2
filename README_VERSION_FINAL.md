# 📊 Análisis Avanzado de Campaña Electoral - VERSIÓN FINAL

## 🎯 Descripción General

Este proyecto proporciona un conjunto completo de herramientas para el análisis avanzado de datos de campañas electorales, con enfoque en técnicas de propaganda y comunicación política. La versión final incluye funcionalidades avanzadas para análisis académico y profesional.

## ✨ Nuevas Funcionalidades Principales

### 1. 📋 Toggle de Formato APA Académico
- **Activación/desactivación** de formato según estándares APA
- **Tablas académicas** con redondeo a 2 decimales
- **Notas explicativas** según normas de publicación
- **Exportación compatible** con revistas científicas

### 2. 🔍 Selección de Variable/Categoría Específica
- **Análisis univariado** enfocado en variables específicas
- **Filtrado granular** por categoría individual
- **Rankings especializados** sin mezcla de variables
- **Análisis temporal** de variables seleccionadas

### 3. ⚙️ Sistema de Filtros Avanzado
- **Filtros múltiples** combinables (candidato, fecha, variable)
- **Interfaz intuitiva** en sidebar de Streamlit
- **Feedback visual** del estado de filtros aplicados
- **Análisis dinámico** que respeta todas las configuraciones

## 📁 Archivos del Proyecto

### Scripts Principales
- `analisis_campana_electoral.py` - Script de análisis con formato APA y selección de variables
- `app_streamlit_campana_mejorada.py` - **APLICACIÓN PRINCIPAL** con todas las funcionalidades
- `generar_dummies_desde_codigos.py` - Generación de variables dummy desde datos originales

### Archivos de Configuración
- `requirements.txt` - Dependencias del proyecto
- `instalar_dependencias.ps1` - Script de instalación para Windows
- `demo_funcionalidades_finales.py` - Demostración de nuevas funcionalidades

### Datos
- `recodificado.xlsx` - Archivo de datos procesados con variables dummy
- `Análisis de contanido acabado.xlsx` - Datos originales del análisis de contenido

## 🚀 Guía de Inicio Rápido

### Paso 1: Instalación
```powershell
# Instalar dependencias
pip install -r requirements.txt

# O usar el script automatizado (Windows)
.\instalar_dependencias.ps1
```

### Paso 2: Ejecutar Aplicación Principal
```powershell
streamlit run app_streamlit_campana_mejorada.py
```

### Paso 3: Configuración en Streamlit
1. **Formato APA**: Activa el checkbox "📋 Activar formato APA académico"
2. **Variable Específica**: Selecciona una variable en "🔍 Seleccionar variable para análisis"
3. **Categoría**: Si deseas análisis más granular, selecciona una categoría específica
4. **Filtros Adicionales**: Configura candidato, rango de fechas según necesidad

## 📖 Funcionalidades Detalladas

### 🏆 Ranking de Categorías
- **Análisis global**: Todas las variables y categorías
- **Análisis por variable**: Solo categorías de una variable específica
- **Análisis granular**: Una categoría específica
- **Formato APA**: Tablas académicas con notas explicativas

### 📈 Análisis Temporal
- **Evolución general**: Estrategias clave predefinidas
- **Evolución específica**: Variable seleccionada por el usuario
- **Visualizaciones**: Gráficos interactivos con Plotly
- **Estadísticas**: Descriptivos con formato APA opcional

### 🔄 Tablas Cruzadas
- **Variables disponibles**: Filtradas según selección del usuario
- **Visualizaciones**: Heatmaps y tablas interactivas
- **Estadísticas**: Chi-cuadrado con interpretación
- **Exportación**: Excel con formato académico

### 📢 Análisis de Propaganda
- **Técnicas por candidato**: Uso porcentual de cada técnica
- **Filtrado por variable**: Análisis especializado
- **Visualizaciones**: Gráficos de barras comparativos
- **Exportación**: Datos listos para publicación

### 👥 Análisis Plain-Folks
- **Análisis por candidato**: Uso de estrategia populista
- **Contextos**: Detalles de implementación
- **Formato académico**: Tablas APA opcionales
- **Comparaciones**: Entre candidatos y períodos

## 🎨 Casos de Uso Específicos

### Para Investigadores Académicos
```
✅ Configuración Recomendada:
- Formato APA: ACTIVADO
- Variable específica: Según hipótesis de investigación
- Exportación: Tablas listas para publicación
```

### Para Analistas de Campaña
```
✅ Configuración Recomendada:
- Formato APA: Opcional
- Filtro por candidato: ACTIVADO
- Variable específica: Técnicas de interés
- Análisis temporal: Para seguimiento de estrategias
```

### Para Consultores Políticos
```
✅ Configuración Recomendada:
- Filtros múltiples: Candidato + Período específico
- Variables: Técnicas de mayor impacto
- Exportación: Reportes ejecutivos
```

### Para Estudiantes
```
✅ Configuración Recomendada:
- Formato APA: ACTIVADO (para trabajos académicos)
- Análisis exploratorio: Todas las variables
- Comparaciones: Entre diferentes enfoques
```

## 📊 Tipos de Análisis Disponibles

### 1. Análisis Descriptivo Univariado
- Frecuencias por variable/categoría
- Estadísticos descriptivos
- Distribuciones temporales

### 2. Análisis Descriptivo Bivariado
- Tablas de contingencia
- Pruebas de asociación (Chi-cuadrado)
- Correlaciones temporales

### 3. Análisis Comparativo
- Entre candidatos
- Entre períodos temporales
- Entre técnicas de propaganda

### 4. Análisis Temporal
- Evolución de estrategias
- Tendencias por variable
- Análisis de picos de actividad

## 💾 Exportación y Formato

### Formatos de Exportación
- **Excel (.xlsx)**: Múltiples hojas con diferentes análisis
- **Tablas APA**: Formato académico estricto
- **Gráficos**: PNG de alta resolución (300 DPI)

### Estructura de Exportación
```
analisis_completo_campana.xlsx
├── Top_Categorias (Rankings)
├── Tabla_Contingencia (Cruces)
├── Tabla_Porcentajes (Cruces %)
├── Propaganda (Por candidato)
├── Evolucion_Temporal (Series de tiempo)
└── Plain_Folks (Análisis específico)
```

## 🔧 Configuración Técnica

### Requisitos del Sistema
- Python 3.8+
- Streamlit 1.25+
- Pandas, NumPy, Matplotlib, Seaborn, Plotly
- Openpyxl para manejo de Excel

### Configuración APA
- Fuente: Times New Roman (serif)
- Tamaño: 12pt base
- Decimales: 2 lugares
- Bordes: Superior e inferior en encabezados
- Notas: Formato estándar APA

### Estructura de Datos Esperada
```
Columnas requeridas:
- Candidato: Nombre del candidato
- Fecha: Fecha en formato "DD de MMMM"
- [Variable]__[Categoría]: Variables dummy (0/1)

Ejemplo:
- Tecnicas_Propaganda__Plain_Folks
- Contexto_Aparicion__Evento_Publico
- Elementos_Visuales__Logotipo
```

## 🚨 Solución de Problemas

### Error: "No se pudieron cargar los datos"
- Verificar que `recodificado.xlsx` esté en el directorio
- Comprobar que el archivo no esté abierto en Excel
- Revisar permisos de lectura del archivo

### Error: "No se encontraron columnas dummy"
- Las columnas deben seguir formato `Variable__Categoria`
- Verificar que existan columnas con doble guión bajo `__`
- Revisar el archivo con `generar_dummies_desde_codigos.py`

### Problemas de Rendimiento
- Filtrar datos antes de análisis complejos
- Limitar número de categorías en rankings
- Usar análisis por variable específica

## 📝 Notas Técnicas

### Funciones Clave Añadidas
- `obtener_variables_principales()` - Extrae variables únicas
- `filtrar_datos_por_seleccion()` - Aplica filtros granulares
- `aplicar_formato_apa_dataframe()` - Formatea según APA
- `mostrar_tabla_con_formato()` - Muestra tablas con formato seleccionado

### Mejoras de Rendimiento
- Cache de datos con `@st.cache_data`
- Filtrado eficiente de columnas
- Carga condicional de análisis

### Configuración Visual
- Paleta de colores profesional
- Estilos CSS personalizados
- Configuración matplotlib para APA
- Responsive design para diferentes pantallas

## 📞 Soporte

Para dudas sobre funcionalidades específicas:
1. Revisar `demo_funcionalidades_finales.py`
2. Consultar comentarios en el código
3. Verificar configuración en sidebar de Streamlit

## 🎉 Changelog - Versión Final

### ✅ Nuevas Funcionalidades
- Toggle de formato APA en todas las secciones
- Selección de variable/categoría específica
- Filtros avanzados combinables
- Análisis univariado granular
- Exportación mejorada con formato académico

### 🔧 Mejoras Técnicas
- Refactorización completa de la aplicación Streamlit
- Funciones modulares para análisis específicos
- Optimización de rendimiento
- Mejor manejo de errores

### 🎨 Mejoras de UI/UX
- Controles organizados en sidebar
- Feedback visual de filtros aplicados
- Indicadores de estado claros
- Diseño responsive mejorado

---

**Versión**: Final (Enero 2025)  
**Autor**: GitHub Copilot  
**Licencia**: Proyecto Académico
