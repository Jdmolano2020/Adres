import pandas as pd


file_path = 'OCI_TERCEROS.xlsx'
df_terceros = pd.read_excel(file_path, dtype={
    'Departamento': str, 'Ciudad': str,
    'NumeroDocumento': str, 'NumeroCuenta': str,
    'NombreBanco': str, 'ConceptoPago': str, })
file_path = '1.ADR_SupplierImportTemplate_ADR.xlsx'
df_tercerosini = pd.read_excel(file_path, engine='openpyxl')
file_path = 'TercerosBalance.xlsx'
df_tercerosb = pd.read_excel(file_path, dtype={'NumeroDocumento': str})


df_tercerosbal = df_terceros.merge(df_tercerosb,
                                   left_on='NumeroDocumento',
                                   right_on='NumeroDocumento',
                                   how='inner')
# Unir los DataFrames por las columnas correspondientes
df_comparado = df_tercerosbal.merge(df_tercerosini,
                                    left_on='NumeroDocumento',
                                    right_on='Supplier Number',
                                    how='inner')

# Filtrar registros donde 'Nombre' y 'Supplier Name*' sean diferentes
df_diferencias = df_comparado[df_comparado['Nombre_x']
                              != df_comparado['Supplier Name*']]
df_diferencias_seleccion = df_diferencias[['NumeroDocumento', 'Supplier Name*',
                                           'Nombre_x', 'PrimerNombre',
                                           'SegundoNombre', 'PrimerApellido',
                                           'SegundoApellido']]
