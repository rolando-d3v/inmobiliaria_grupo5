import pandas as pd
import numpy as np

def analizar_e_imputar_categoricas(df, valor_imputacion='Desconocido'):
    """
    Obtiene valores únicos por columna categórica e imputa un valor textual donde hay NaNs
    
    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame a analizar
    valor_imputacion : str, default='Desconocido'
        Valor textual para imputar en los NaNs
    
    Retorna:
    --------
    tuple: (DataFrame imputado, diccionario con valores únicos)
    """
    
    # Crear copia del dataframe
    df_imputado = df.copy()
    
    # Identificar columnas categóricas (object y category)
    cols_categoricas = df.select_dtypes(include=['object', 'category']).columns
    
    # Diccionario para almacenar valores únicos
    valores_unicos = {}
    
    # Diccionario para almacenar información de NaNs
    info_nans = {}
    
    print("=" * 60)
    print("ANÁLISIS DE COLUMNAS CATEGÓRICAS")
    print("=" * 60)
    
    for col in cols_categoricas:
        # Contar NaNs
        num_nans = df[col].isna().sum()
        total = len(df[col])
        porcentaje_nans = (num_nans / total) * 100
        
        # Obtener valores únicos (excluyendo NaN)
        
        unicos = df[col].dropna().unique()
        valores_unicos[col] = unicos
        info_nans[col] = {
            'num_nans': num_nans,
            'porcentaje': porcentaje_nans
        }
        
        # Imputar NaNs con el valor especificado
        df_imputado[col] = df_imputado[col].fillna(valor_imputacion)
        
        # Mostrar información
        print(f"\nColumna: {col}")
        print(f"  - Total registros: {total}")
        print(f"  - NaNs encontrados: {num_nans} ({porcentaje_nans:.2f}%)")
        print(f"  - Valores únicos (sin NaN): {len(unicos)}")
        print(f"  - Valores: {list(unicos)[:10]}")  # Mostrar máximo 10
        if len(unicos) > 10:
            print(f"    ... y {len(unicos) - 10} más")
    
    print("\n" + "=" * 60)
    print(f"IMPUTACIÓN COMPLETADA con valor: '{valor_imputacion}'")
    print("=" * 60)
    
    return df_imputado, valores_unicos, info_nans