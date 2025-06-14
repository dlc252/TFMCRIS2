import pandas as pd
import numpy as np

def analizar_variables():
    """Analiza las variables en el dataframe y muestra información diagnóstica"""
    print("Cargando datos...")
    
    try:
        df = pd.read_excel("recodificado.xlsx")
        
        print("\n=== INFORMACIÓN BÁSICA DEL DATAFRAME ===")
        print(f"Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        # Identificar columnas dummy y variables principales
        dummy_cols = [col for col in df.columns if '__' in col]
        
        variables_principales = set()
        for col in dummy_cols:
            if '__' in col:
                variable_principal = col.split('__')[0]
                variables_principales.add(variable_principal)
        
        print(f"\n=== VARIABLES PRINCIPALES ENCONTRADAS: {len(variables_principales)} ===")
        for var in sorted(variables_principales):
            print(f"- {var}")
        
        print(f"\n=== COLUMNAS DUMMY ENCONTRADAS: {len(dummy_cols)} ===")
        print("Primeras 10 columnas dummy:", dummy_cols[:10])
        
        print("\n=== TODAS LAS COLUMNAS DEL DATAFRAME ===")
        print(df.columns.tolist())
        
        print("\n=== VERIFICANDO VARIABLES ESPERADAS ===")
        variables_esperadas = [
            "contenido_visual_del_post",
            "formato_del_contenido",
            "aparicion_del_lider",
            "aparicion_de_terceras_personas",
            "contexto_de_la_imagen",
            "imagen_corporativa",
            "tipo_de_propaganda",
            "recursos_de_propaganda_segun_el_institute_for_propaganda",
            "reglas_de_la_propaganda_segun_domenach"
        ]
        
        for var in variables_esperadas:
            encontrada = False
            for col in df.columns:
                if col.startswith(var + "__") or col == var:
                    encontrada = True
                    break
            
            cols_relacionadas = [col for col in df.columns if col.startswith(var)]
            print(f"Variable '{var}': {'✓' if encontrada else '✗'} - Columnas relacionadas: {len(cols_relacionadas)}")
            
        # Análisis adicional: buscar columnas que podrían contener estas variables con otro formato
        print("\n=== ANÁLISIS ADICIONAL DE POSIBLES COLUMNAS RELEVANTES ===")
        palabras_clave = ["contenido", "formato", "lider", "aparicion", "terceras", "contexto", 
                         "imagen", "corporativa", "propaganda", "recursos", "reglas"]
        
        for palabra in palabras_clave:
            cols_relacionadas = [col for col in df.columns if palabra.lower() in col.lower()]
            if cols_relacionadas:
                print(f"Columnas con '{palabra}': {cols_relacionadas}")
                
    except Exception as e:
        print(f"Error al cargar o analizar los datos: {e}")

if __name__ == "__main__":
    analizar_variables()
