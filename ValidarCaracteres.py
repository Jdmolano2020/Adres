import pandas as pd
import re

# Función para verificar si hay caracteres especiales


def contiene_caracteres_especiales(nombre):
    # Detecta cualquier carácter que NO sea letra, número o espacio
    return bool(re.search(r'[^a-zA-Z0-9\s.-]', str(nombre)))


file_path = 'OCI_TERCEROS.xlsx'
df_terceros = pd.read_excel(file_path, dtype={
    'Departamento': str, 'Ciudad': str,
    'NumeroDocumento': str, 'NumeroCuenta': str,
    'NombreBanco': str, 'ConceptoPago': str, })

df_terceros['Nombre'] = df_terceros['Nombre'].replace(
    r'[&()/,?:>\`\"+\'@]', '', regex=True)

df_terceros['PrimerNombre'] = df_terceros['PrimerNombre'].replace(
    r'[&()/,?:>\`\"+\'@]', '', regex=True)
df_terceros['SegundoNombre'] = df_terceros['SegundoNombre'].replace(
    r'[&()/,?:>\`\"+\'@]', '', regex=True)
df_terceros['PrimerApellido'] = df_terceros['PrimerApellido'].replace(
    r'[&()/,?:>\`\"+\'@]', '', regex=True)
df_terceros['SegundoApellido'] = df_terceros['SegundoApellido'].replace(
    r'[&()/,?:>\`\"+\'@]', '', regex=True)
# Crear una nueva columna con la marca
df_terceros['Tiene_Caracteres_Especiales'] = df_terceros['Nombre'].apply(
    contiene_caracteres_especiales)

# Filtrar los registros que contienen caracteres especiales
df_con_especiales = df_terceros[df_terceros['Tiene_Caracteres_Especiales']]

df_terceros = df_terceros[~df_terceros['Tiene_Caracteres_Especiales']]

df_terceros.astype(str).to_csv(
    "OCI_TERCEROS.csv", index=False, encoding="utf-8", quoting=1)
