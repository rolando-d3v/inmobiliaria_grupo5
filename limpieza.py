

import pandas as pd

# 1️⃣ Leer el archivo Excel
df = pd.read_excel("datos_actualizados7.xlsx")  # ← reemplaza con el nombre de tu archivo

kalen = "Área Social más valorada"
print("Valores vacíos antes:", df[kalen].isna().sum())


df[kalen] = df[kalen].fillna('No especifico')


df.to_excel("datos_actualizados8.xlsx", index=False)


print("Valores vacíos después:", df[kalen].isna().sum())
print("Columna actualizada:")
print(df[kalen].head())



