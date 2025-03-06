import pandas as pd

import os

# Crear carpeta para guardar los archivos exportados
output_folder = "archivos_terceros"
os.makedirs(output_folder, exist_ok=True)


# Función genérica para comparar listas en cualquier par de columnas
def comparar_listas(row, col_id_pago, col_concepto_pago):
    # Convertir a string y manejar NaN reemplazándolos por una cadena vacía
    id_pago_str = str(row[col_id_pago]) if pd.notna(row[col_id_pago]) else ''
    concepto_pago_str = str(row[col_concepto_pago]) if pd.notna(row[col_concepto_pago]) else ''

    # Convertir en listas separadas por '-'
    id_pago_list = set(id_pago_str.split('-')) if id_pago_str else set()
    concepto_pago_list = concepto_pago_str.split('-') if concepto_pago_str else []

    # Comparar listas
    concepto_existente = [cp for cp in concepto_pago_list if cp in id_pago_list]
    concepto_no_existente = [cp for cp in concepto_pago_list if cp not in id_pago_list]
    
    return pd.Series({
        'ConceptoPagoE': '-'.join(concepto_existente) if concepto_existente else '',
        'ConceptoPagoN': '-'.join(concepto_no_existente) if concepto_no_existente else ''
    })


file_path = 'OCI_TERCEROS.xlsx'
df_terceros = pd.read_excel(file_path, dtype={
    'Departamento': str, 'Ciudad': str,
    'NumeroDocumento': str, 'NumeroCuenta': str,
    'NombreBanco': str, 'ConceptoPago': str, })
file_path = 'ADR_Info_Terceros_Direcciones_RP_ADR_Info_Terceros_Direcciones_RP.xlsx'
df_tercerosparal = pd.read_excel(file_path, dtype={
    'ID PROVEEDOR': str, 'CODIGO BANCO': str,
    'CUENTA BANCARIA': str, 'ID PAGO': str})
file_path = 'TerceroBusca.xlsx'
df_tercerosb = pd.read_excel(file_path, dtype={
    'NumeroDocumento': str, 'ConceptoPagoX': str,})


df_tercerose = df_tercerosparal.merge(df_tercerosb,
                                      left_on='ID PROVEEDOR',
                                      right_on='NumeroDocumento',
                                      how='inner')

df_tercerose.drop(columns=['NumeroDocumento'],
                  inplace=True)

# Aplicar la función en el DataFrame, indicando los nombres de las columnas que
# deseas comparar
df_tercerose[['ConceptoPagoE', 'ConceptoPagoN']] = df_tercerose.apply(
    lambda row: comparar_listas(row, 'ID PAGO', 'ConceptoPagoX'),
    axis=1
)


# Filtrar registros donde 'ConceptoPagoN' no sea NaN o vacío
df_filtrado = df_tercerose[df_tercerose['ConceptoPagoN'].notna() & (df_tercerose['ConceptoPagoN'] != '')]

# Expandir 'ConceptoPagoN' en filas separadas (cada valor se divide por '-')
df_exploded = df_filtrado.assign(ConceptoPagoN=df_filtrado['ConceptoPagoN'].str.split('-')).explode('ConceptoPagoN')

# Recorrer cada valor único de 'ConceptoPagoN' y exportar los registros correspondientes
for concepto in df_exploded['ConceptoPagoN'].unique():
    df_subset = df_exploded[df_exploded['ConceptoPagoN'] == concepto].drop_duplicates(subset=['ID PROVEEDOR'])

    # Crear nombre de archivo seguro
    nombre_archivo = f"{output_folder}/terceros_{concepto.replace(' ', '_').replace('/', '_')}.csv"
    
    # Exportar a CSV
    df_subset.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', sep=';', quoting=1)

print("Exportación Terceros Existentes completada.")

df_filtrado = df_tercerose[df_tercerose['ConceptoPagoE'].notna() & (df_tercerose['ConceptoPagoE'] != '')]
nombre_archivo = f"{output_folder}/TercerosExistentes.csv"
df_filtrado.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)


df_tercerosne = df_tercerosb.merge(df_tercerosparal,
                                   left_on='NumeroDocumento',
                                   right_on='ID PROVEEDOR',
                                   how='left',
                                   indicator=True)

# Filtrar los registros que no tienen coincidencia en df_tercerosparal
df_tercerosne = df_tercerosne[df_tercerosne['_merge'] == 'left_only']

# Eliminar la columna _merge si no la necesitas
df_tercerosne = df_tercerosne.drop(columns=['_merge'])
df_tercerosne = df_tercerosne[df_tercerosb.columns]

df_tercerosc = df_terceros.merge(df_tercerosne,
                                 left_on='NumeroDocumento',
                                 right_on='NumeroDocumento',
                                 how='inner')

nombre_archivo = f"{output_folder}/TercerosCargar.csv"
df_tercerosc.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)

df_tercerosne = df_tercerosne.merge(df_terceros,
                                    left_on='NumeroDocumento',
                                    right_on='NumeroDocumento',
                                    how='left',
                                    indicator=True)
df_tercerosne = df_tercerosne[df_tercerosne['_merge'] == 'left_only']

# Eliminar la columna _merge si no la necesitas
df_tercerosne = df_tercerosne.drop(columns=['_merge'])
df_tercerosne = df_tercerosne[df_tercerosb.columns]
nombre_archivo = f"{output_folder}/TercerosArmar.csv"
df_tercerosne.astype(str).to_csv(nombre_archivo,
                                 index=False, encoding="utf-8", quoting=1)
