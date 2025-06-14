# =====================================================
# EJEMPLO DE USO DE LAS NUEVAS FUNCIONALIDADES
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Ejecutar el script principal con configuraciones específicas
exec(open('analisis_campana_electoral.py').read())

# =====================================================
# SCRIPT SIMPLIFICADO PARA DEMOS RÁPIDAS
# =====================================================

def demo_analisis_interactivo():
    """
    Función demo que muestra cómo usar las nuevas funcionalidades
    """
    print("\n" + "🎯 DEMO DE NUEVAS FUNCIONALIDADES")
    print("="*60)
    
    # Cargar datos
    print("Cargando datos...")
    df = pd.read_excel("recodificado.xlsx")
    dummy_cols = [col for col in df.columns if '__' in col]
    variables_principales = obtener_variables_principales(dummy_cols)
    
    print(f"✅ Datos cargados: {len(df)} registros")
    print(f"✅ Variables encontradas: {len(variables_principales)}")
    
    # Mostrar variables disponibles
    print("\n📋 Variables principales disponibles:")
    for i, var in enumerate(variables_principales, 1):
        print(f"  {i}. {var.replace('_', ' ').title()}")
    
    # Demo 1: Formato APA vs Estándar
    print("\n" + "="*40)
    print("DEMO 1: COMPARACIÓN DE FORMATOS")
    print("="*40)
    
    # Crear datos de ejemplo
    if 'Candidato' in df.columns:
        candidato_ejemplo = df['Candidato'].iloc[0]
        variable_ejemplo = variables_principales[0]
        
        print(f"🔍 Analizando variable: {variable_ejemplo.replace('_', ' ').title()}")
        print(f"🏛️ Candidato ejemplo: {candidato_ejemplo}")
        
        # Análisis con formato estándar
        desactivar_formato_apa()
        df_ranking_std = crear_ranking_por_variable(df, dummy_cols, variable_ejemplo, candidato_ejemplo)
        
        if len(df_ranking_std) > 0:
            print("\n📊 FORMATO ESTÁNDAR:")
            df_export_std = df_ranking_std.head(5)[['Categoria', 'Usos', 'Porcentaje']].copy()
            exportar_tabla_apa(df_export_std, 
                              f"Ranking {variable_ejemplo.replace('_', ' ').title()} - {candidato_ejemplo}",
                              f"demo_formato_estandar_{variable_ejemplo}",
                              figsize=(10, 6))
        
        # Análisis con formato APA
        activar_formato_apa()
        df_ranking_apa = crear_ranking_por_variable(df, dummy_cols, variable_ejemplo, candidato_ejemplo)
        
        if len(df_ranking_apa) > 0:
            print("\n📚 FORMATO APA ACADÉMICO:")
            df_export_apa = df_ranking_apa.head(5)[['Categoria', 'Usos', 'Porcentaje']].copy()
            df_export_apa.index = range(1, len(df_export_apa) + 1)
            df_export_apa.index.name = "Ranking"
            
            exportar_tabla_apa(df_export_apa, 
                              f"Ranking {variable_ejemplo.replace('_', ' ').title()} - {candidato_ejemplo}",
                              f"demo_formato_apa_{variable_ejemplo}",
                              figsize=(10, 6))
    
    # Demo 2: Análisis por variable específica vs general
    print("\n" + "="*40)
    print("DEMO 2: ANÁLISIS ESPECÍFICO VS GENERAL")
    print("="*40)
    
    if len(variables_principales) >= 2:
        variable1 = variables_principales[0]
        variable2 = variables_principales[1]
        
        print(f"🎯 Variable 1: {variable1.replace('_', ' ').title()}")
        print(f"🎯 Variable 2: {variable2.replace('_', ' ').title()}")
        
        # Análisis específico de variable 1
        df_var1 = crear_ranking_por_variable(df, dummy_cols, variable1)
        print(f"\n📊 Top 3 de {variable1.replace('_', ' ').title()}:")
        for i, (_, row) in enumerate(df_var1.head(3).iterrows(), 1):
            print(f"  {i}. {row['Categoria']}: {row['Usos']} usos ({row['Porcentaje']:.1f}%)")
        
        # Análisis específico de variable 2
        df_var2 = crear_ranking_por_variable(df, dummy_cols, variable2)
        print(f"\n📊 Top 3 de {variable2.replace('_', ' ').title()}:")
        for i, (_, row) in enumerate(df_var2.head(3).iterrows(), 1):
            print(f"  {i}. {row['Categoria']}: {row['Usos']} usos ({row['Porcentaje']:.1f}%)")
        
        # Análisis general
        df_general = crear_analisis_general(df, dummy_cols, top_n=6)
        print(f"\n📊 Top 6 General (todas las variables mezcladas):")
        for i, (_, row) in enumerate(df_general.head(6).iterrows(), 1):
            print(f"  {i}. {row['Variable_Principal']} - {row['Categoria']}: {row['Usos']} usos")
    
    # Demo 3: Comparación entre candidatos
    print("\n" + "="*40)
    print("DEMO 3: COMPARACIÓN ENTRE CANDIDATOS")
    print("="*40)
    
    if 'Candidato' in df.columns and len(variables_principales) > 0:
        candidatos = df['Candidato'].unique()[:3]  # Máximo 3 candidatos para la demo
        variable_demo = variables_principales[0]
        
        print(f"🎯 Variable analizada: {variable_demo.replace('_', ' ').title()}")
        print(f"👥 Candidatos: {', '.join(candidatos)}")
        
        tabla_comparacion = []
        
        for candidato in candidatos:
            df_cand_ranking = crear_ranking_por_variable(df, dummy_cols, variable_demo, candidato)
            
            if len(df_cand_ranking) > 0:
                top_categoria = df_cand_ranking.iloc[0]
                tabla_comparacion.append({
                    'Candidato': candidato,
                    'Top_Categoria': top_categoria['Categoria'],
                    'Usos': int(top_categoria['Usos']),
                    'Porcentaje': round(top_categoria['Porcentaje'], 1)
                })
        
        if tabla_comparacion:
            df_comparacion = pd.DataFrame(tabla_comparacion)
            print(f"\n📊 Comparación - Top categoría de {variable_demo.replace('_', ' ').title()} por candidato:")
            print(df_comparacion.to_string(index=False))
            
            # Exportar tabla de comparación
            exportar_tabla_apa(df_comparacion,
                              f"Comparación Top {variable_demo.replace('_', ' ').title()} por Candidato",
                              f"demo_comparacion_{variable_demo}",
                              figsize=(12, 6))
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETADA")
    print("📁 Revisa los archivos PNG generados para ver las diferencias")
    print("📚 Formato APA: Más limpio, profesional, apto para publicaciones")
    print("🎨 Formato Estándar: Más colorido, visual, mejor para presentaciones")
    print("="*60)

# Ejecutar demo si se llama directamente
if __name__ == "__main__":
    try:
        demo_analisis_interactivo()
    except Exception as e:
        print(f"❌ Error en la demo: {e}")
        print("📋 Asegúrate de tener el archivo 'recodificado.xlsx' en el directorio")
