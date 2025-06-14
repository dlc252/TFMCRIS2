import pandas as pd

def main():
    try:
        # Cargar el archivo
        df = pd.read_excel("recodificado.xlsx")
        
        # Identificar columnas dummy
        dummy_cols = [col for col in df.columns if '__' in col]
        
        # Obtener variables principales
        variables = set()
        for col in dummy_cols:
            if '__' in col:
                variable_principal = col.split('__')[0]
                variables.add(variable_principal)
        
        # Mostrar información
        print(f"Total de columnas en el DataFrame: {len(df.columns)}")
        print(f"Total de columnas dummy: {len(dummy_cols)}")
        print(f"Total de variables principales: {len(variables)}")
        print("\nVariables principales encontradas:")
        for var in sorted(list(variables)):
            print(f"- {var}")
            
        print("\nEjemplos de columnas dummy:")
        for col in dummy_cols[:20]:  # Mostrar solo las primeras 20
            print(f"- {col}")
            
    except Exception as e:
        print(f"Error al analizar datos: {e}")

if __name__ == "__main__":
    main()
