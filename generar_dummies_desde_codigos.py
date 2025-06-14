import pandas as pd
import unicodedata
from datetime import datetime

# Reemplaza esto por la ruta a tu archivo
file_path = "analisis.xlsx"

# Leer las dos hojas del archivo Excel
print("Leyendo las hojas de Excel...")
df1 = pd.read_excel(file_path, sheet_name=0)  # Primera hoja
df2 = pd.read_excel(file_path, sheet_name=1)  # Segunda hoja

print(f"Primera hoja: {len(df1)} filas")
print(f"Segunda hoja: {len(df2)} filas")

# Combinar los dataframes - agregar la segunda hoja al final de la primera
df = pd.concat([df1, df2], ignore_index=True)
print(f"Dataset combinado: {len(df)} filas")

# Diccionario de categorías
category_mappings = {
    "Contenido visual del post": {
        "1": "Solo imagen",
        "2": "Vídeo",
        "3": "Sólo texto",
        "4": "Combinación de imagen y texto",
        "5": "Indeterminado",
        "6": "Otro"
    },
    "Formato del contenido": {
        "1": "Fotografía",
        "2": "Collage",
        "3": "Ilustración",
        "4": "Montaje",
        "5": "Meme",
        "6": "Indeterminado",
        "7": "Otro"
    },
    "Aparición del líder": {
        "1": "Sí",
        "2": "No",
        "3": "Indeterminado"
    },
    "Aparición de terceras personas": {
        "1": "Ninguna",
        "2": "Familiares",
        "3": "Líderes carismáticos",
        "4": "Compañeros de partido",
        "5": "Votantes",
        "6": "Candidato/rival",
        "7": "Políticos de la esfera nacional",
        "8": "Políticos de la esfera internacional",
        "9": "Indeterminado"
    },
    "Contexto de la imagen": {
        "1": "Contexto profesional",
        "2": "Contexto mediático",
        "3": "Contexto personal",
        "4": "Vía pública",
        "5": "Sarcastico",
        "6": "Indeterminado"
    },
    "Imagen corporativa": {
        "1": "Bandera de partido",
        "2": "Logotipo del partido",
        "3": "Música del partido",
        "4": "Color corporativo",
        "5": "Indeterminado"
    },
    "Tipo de propaganda": {
        "1": "Propaganda de afirmación",
        "2": "Propaganda de negación",
        "3": "Propaganda de reacción",
        "4": "Indeterminado"
    },
    "Recursos de propaganda según el Institute for propaganda": {
        "1": "Name-calling (Improperios)",
        "2": "Glittering-generalities (Generalidades brillantes)",
        "3": "Transfer (Transferencia)",
        "4": "Testimonial (Testimonio)",
        "5": "Plain-folks (Gente del pueblo)",
        "6": "Card-stacking (Cartas Trucadas)",
        "7": "Band-wagon (Imitación)"
    },
    "Reglas de la propaganda según Domenach": {
        "1": "Regla de simplificación y enemigo único",
        "2": "Regla de la exageración y desfiguración",
        "3": "Regla de la orquestación",
        "4": "Regla de la transfusión",
        "5": "Regla de la unanimidad"
    }
}

# Limpieza de etiquetas para nombres de columna
def clean_label(label):
    label = str(label)
    label = unicodedata.normalize("NFKD", label).encode("ASCII", "ignore").decode("ASCII")
    label = label.lower().strip().replace(" ", "_").replace("/", "_").replace("–", "-")
    return label

# Procesar fechas si existe la columna Fecha
if 'Fecha' in df.columns:
    print("Procesando fechas...")
      # Diccionario de meses en español
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
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
            dia_match = re.search(r'\d+', dia_str)
            if dia_match:
                dia = int(dia_match.group())
            else:
                return None
                
            # Obtener el mes
            mes = meses.get(mes_texto, None)
            if mes is None:
                return None
                
            # Todas las fechas se consideran de 2025
            return datetime(2025, mes, dia)
        except Exception as e:
            print(f"Error procesando fecha '{fecha_str}': {e}")
            return None
    
    # Crear columna de fecha convertida
    df['Fecha_convertida'] = df['Fecha'].apply(convertir_fecha)
    print(f"Fechas procesadas: {df['Fecha_convertida'].notna().sum()} de {len(df)} registros")

print("Generando variables dummy...")

# Procesar cada columna definida
for col, cat_dict in category_mappings.items():
    if col in df.columns:
        df[col] = df[col].astype(str)
        for code, label in cat_dict.items():
            dummy_col = f"{clean_label(col)}__{clean_label(label)}"
            df[dummy_col] = df[col].str.split("-").apply(
                lambda values: int(code in [v.strip() for v in values]) if isinstance(values, list) else 0
            )
    else:
        print(f"Advertencia: La columna '{col}' no fue encontrada en el dataset")

# Guardar resultado
df.to_excel("recodificado.xlsx", index=False)

print("Proceso completado!")
print(f"Las dos hojas han sido combinadas: {len(df)} filas totales")
print(f"Variables dummy generadas para {len(category_mappings)} categorías")
print("Archivo guardado como: recodificado.xlsx")