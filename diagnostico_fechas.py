import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_excel("analisis.xlsx")

# Verificar los formatos de fecha actuales
print("=== DIAGNÓSTICO DE FECHAS ===")
print(f"Total de filas: {len(df)}")

if 'Fecha' in df.columns:
    fechas_unicas = df['Fecha'].dropna().unique()
    print(f"Formatos de fecha encontrados (primeras 20):")
    for i, fecha in enumerate(fechas_unicas[:20]):
        print(f"  {i+1}. '{fecha}'")
    
    # Diagnóstico de la función actual
    def convertir_fecha_actual(fecha_str):
        try:
            if pd.isna(fecha_str):
                return None
            partes = str(fecha_str).lower().strip().split(' de ')
            if len(partes) < 2:
                return None
            
            dia = int(partes[0])
            mes_texto = partes[1].strip()
            # Mapeo de meses en español a números
            meses = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
                    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
            mes = meses.get(mes_texto, 1)
            return datetime(2023, mes, dia)
        except Exception as e:
            print(f"Error con fecha '{fecha_str}': {e}")
            return None
    
    # Función mejorada
    def convertir_fecha_mejorada(fecha_str):
        try:
            if pd.isna(fecha_str):
                return None
                
            # Normalizar texto
            fecha_str = str(fecha_str).lower().strip()
            
            # Extraer partes principales (día y mes)
            # Maneja varios formatos posibles
            if ' de ' in fecha_str:
                partes = fecha_str.split(' de ')
                dia_str = partes[0].strip()
                # Si hay más texto después del mes, ignorarlo
                mes_texto = partes[1].strip().split()[0]
            else:
                return None
            
            # Extraer el número del día
            import re
            dia_match = re.search(r'\d+', dia_str)
            if dia_match:
                dia = int(dia_match.group())
            else:
                return None
                
            # Mapeo de meses incluyendo abreviaturas y variaciones
            meses = {
                "ene": 1, "enero": 1,
                "feb": 2, "febrero": 2,
                "mar": 3, "marzo": 3,
                "abr": 4, "abril": 4,
                "may": 5, "mayo": 5,
                "jun": 6, "junio": 6,
                "jul": 7, "julio": 7,
                "ago": 8, "agosto": 8,
                "sep": 9, "sept": 9, "septiembre": 9,
                "oct": 10, "octubre": 10,
                "nov": 11, "noviembre": 11,
                "dic": 12, "diciembre": 12
            }
            
            # Buscar coincidencia del mes
            for clave, valor in meses.items():
                if clave in mes_texto:
                    mes = valor
                    break
            else:
                mes = None
                
            if mes is None:
                return None
                
            # Año académico 2023-2024
            if mes >= 9:  # septiembre a diciembre
                año = 2023
            else:  # enero a agosto
                año = 2024
                
            return datetime(año, mes, dia)
        except Exception as e:
            print(f"Error con fecha '{fecha_str}': {e}")
            return None
    
    # Aplicar ambas funciones y comparar
    df['Fecha_actual'] = df['Fecha'].apply(convertir_fecha_actual)
    df['Fecha_mejorada'] = df['Fecha'].apply(convertir_fecha_mejorada)
    
    # Resumen de resultados
    fechas_nulas_actual = df['Fecha_actual'].isna().sum()
    fechas_nulas_mejorada = df['Fecha_mejorada'].isna().sum()
    
    print("\n=== COMPARACIÓN DE RESULTADOS ===")
    print(f"Total de fechas: {len(df)}")
    print(f"Fechas convertidas (actual): {len(df) - fechas_nulas_actual} ({100*(len(df) - fechas_nulas_actual)/len(df):.1f}%)")
    print(f"Fechas convertidas (mejorada): {len(df) - fechas_nulas_mejorada} ({100*(len(df) - fechas_nulas_mejorada)/len(df):.1f}%)")
    
    # Análisis de distribución
    print("\n=== DISTRIBUCIÓN DE FECHAS ===")
    if len(df) - fechas_nulas_actual > 0:
        print("\nDistribución con función actual:")
        conteo_actual = df['Fecha_actual'].value_counts().sort_index()
        print(conteo_actual.head(10))
    
    if len(df) - fechas_nulas_mejorada > 0:
        print("\nDistribución con función mejorada:")
        conteo_mejorada = df['Fecha_mejorada'].value_counts().sort_index()
        print(conteo_mejorada.head(10))
        
    # Visualización
    plt.figure(figsize=(12, 6))
    
    # Graficamos si hay datos suficientes
    if len(df) - fechas_nulas_actual > 0:
        plt.subplot(1, 2, 1)
        df['Fecha_actual'].hist(bins=20, alpha=0.7)
        plt.title("Distribución con función actual")
        plt.xlabel("Fecha")
        plt.ylabel("Frecuencia")
    
    if len(df) - fechas_nulas_mejorada > 0:
        plt.subplot(1, 2, 2)
        df['Fecha_mejorada'].hist(bins=20, alpha=0.7)
        plt.title("Distribución con función mejorada")
        plt.xlabel("Fecha")
        plt.ylabel("Frecuencia")
    
    plt.tight_layout()
    plt.savefig("diagnostico_fechas.png")
    print("\nGráfico guardado como 'diagnostico_fechas.png'")

    # Verificar si hay desplazamiento en las fechas
    print("\n=== ANÁLISIS DE POSIBLE DESPLAZAMIENTO DE FECHAS ===")
    fechas_diferentes = df.dropna(subset=['Fecha_actual', 'Fecha_mejorada'])
    fechas_diferentes = fechas_diferentes[fechas_diferentes['Fecha_actual'] != fechas_diferentes['Fecha_mejorada']]
    
    if len(fechas_diferentes) > 0:
        print(f"Se encontraron {len(fechas_diferentes)} fechas con posible desplazamiento")
        print("\nMuestra de fechas con diferencias:")
        muestra = fechas_diferentes.sample(min(10, len(fechas_diferentes)))
        for _, row in muestra.iterrows():
            print(f"Original: '{row['Fecha']}' → Actual: {row['Fecha_actual'].strftime('%d/%m/%Y')} → Mejorada: {row['Fecha_mejorada'].strftime('%d/%m/%Y')}")
    else:
        print("No se encontraron diferencias entre las fechas convertidas")

    # Verificar publicaciones en el rango específico
    print("\n=== VERIFICACIÓN DEL RANGO PROBLEMÁTICO ===")
    rango_problema_inicio = datetime(2023, 4, 10)
    rango_problema_fin = datetime(2023, 5, 30)
    rango_correcto_inicio = datetime(2023, 3, 23)
    rango_correcto_fin = datetime(2023, 4, 10)
    
    publicaciones_problema = df[(df['Fecha_actual'] >= rango_problema_inicio) & 
                               (df['Fecha_actual'] <= rango_problema_fin)]
    print(f"Publicaciones en rango problemático (10/04 - 30/05): {len(publicaciones_problema)}")
    
    if len(publicaciones_problema) > 0:
        print("\nMuestra de publicaciones en rango problemático:")
        muestra = publicaciones_problema.sample(min(10, len(publicaciones_problema)))
        for _, row in muestra.iterrows():
            print(f"ID: {row.get('Nº Publi', 'N/A')} | Fecha original: '{row['Fecha']}' | Convertida: {row['Fecha_actual'].strftime('%d/%m/%Y')}")
            if not pd.isna(row['Fecha_mejorada']):
                print(f"  → Con función mejorada: {row['Fecha_mejorada'].strftime('%d/%m/%Y')}")
    
    # Sugerir corrección
    print("\n=== SOLUCIÓN PROPUESTA ===")
    print("1. Reemplazar la función convertir_fecha() actual por la versión mejorada")
    print("2. Actualizar el año utilizado (usar 2024 para fechas de enero a agosto)")
    print("3. Ejecutar nuevamente generar_dummies_desde_codigos.py para regenerar el archivo recodificado.xlsx")
    print("\nCódigo de la función mejorada:")
    print("""
def convertir_fecha(fecha_str):
    try:
        if pd.isna(fecha_str):
            return None
            
        # Normalizar texto
        fecha_str = str(fecha_str).lower().strip()
        
        # Extraer partes principales (día y mes)
        if ' de ' in fecha_str:
            partes = fecha_str.split(' de ')
            dia_str = partes[0].strip()
            # Si hay más texto después del mes, ignorarlo
            mes_texto = partes[1].strip().split()[0]
        else:
            return None
        
        # Extraer el número del día
        import re
        dia_match = re.search(r'\\d+', dia_str)
        if dia_match:
            dia = int(dia_match.group())
        else:
            return None
            
        # Mapeo de meses incluyendo abreviaturas
        meses = {
            "ene": 1, "enero": 1,
            "feb": 2, "febrero": 2,
            "mar": 3, "marzo": 3,
            "abr": 4, "abril": 4,
            "may": 5, "mayo": 5,
            "jun": 6, "junio": 6,
            "jul": 7, "julio": 7,
            "ago": 8, "agosto": 8,
            "sep": 9, "sept": 9, "septiembre": 9,
            "oct": 10, "octubre": 10,
            "nov": 11, "noviembre": 11,
            "dic": 12, "diciembre": 12
        }
        
        # Buscar coincidencia del mes
        for clave, valor in meses.items():
            if clave in mes_texto:
                mes = valor
                break
        else:
            mes = None
            
        if mes is None:
            return None
            
        # Año académico 2023-2024
        if mes >= 9:  # septiembre a diciembre
            año = 2023
        else:  # enero a agosto
            año = 2024
            
        return datetime(año, mes, dia)
    except Exception as e:
        return None
""")