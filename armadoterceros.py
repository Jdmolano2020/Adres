import pandas as pd

# Cargar el archivo Excel
file_path = '1.ADR_SupplierImportTemplate_ADR.xlsx'
df_p1 = pd.read_excel(file_path, engine='openpyxl')
df_p1['id_unico'] = pd.util.hash_pandas_object(df_p1).astype(str)
# Mostrar las primeras filas del dataframe

file_path = '2.ADR_SupplierAddressImportTemplate_ADR.xlsx'
df_p2 = pd.read_excel(file_path, engine='openpyxl')

file_path = "7.ADR_SupplierBankAccountImportTemplate_ADR.xlsx"

# Cargar las hojas en DataFrames
df_payees = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_PAYEES", dtype=str)
df_bank_accts = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_BANK_ACCTS", dtype=str)

file_path = 'TerceroBusca.xlsx'
df_tercerosb = pd.read_excel(file_path, dtype={
    'NumeroDocumento': str, 'ConceptoPagoX': str,})

df_p1 = df_p1.rename(columns={'Supplier Number': 'NumeroDocumento',
                              'Taxpayer Country': 'Pais',
                              'Nombre': 'PrimerNombre',
                              'Segundo Nombre': 'SegundoNombre',
                              'Apellido': 'PrimerApellido',
                              'Segundo Apellido': 'SegundoApellido',
                              'Grupo de impuesto': 'TipoContribuyente'})

df_p1 = df_p1.drop_duplicates(subset=['NumeroDocumento'], keep='first')

df_p2 = df_p2.rename(columns={'Supplier Number': 'NumeroDocumento',
                              'Address Line 1': 'Direccion',
                              'TIPO DE DOCUMENTO': 'TipoDocumentoDesc',
                              'ACTIVIDAD ECONOMICA': 'Actividad Economica',
                              'NATURALEZA': 'Naturaleza',
                              'ID TIPO DE DOCUMENTO': 'TipoDocumento'})
df_p2 = df_p2.drop_duplicates(subset=['NumeroDocumento'], keep='first')

df_payees = df_payees.rename(columns={'*Supplier Number': 'NumeroDocumento',
                              'Business Unit Name': 'UnidadNegocio',
                              'Supplier Site': 'Ciudad'})
 
df_payees = df_payees.drop_duplicates(subset=['NumeroDocumento','UnidadNegocio'], keep='first')

df_bank_accts = df_bank_accts.rename(columns={'*Payee Identifier': 'NumeroDocumento',
                              '**Branch Name': 'NombreBanco',
                              'Id Concepto de pago': 'ConceptoPago',
                              '*Account Number': 'NumeroCuenta',
                              'Account Type Code': 'TipoCuenta'})
   

df_merged = df_p1.merge(df_p2, on='NumeroDocumento', how='left')

columnas_terceros = [
    'TipoDocumento', 'NumeroDocumento', 'Naturaleza', 'PrimerNombre',
    'SegundoNombre', 'PrimerApellido', 'SegundoApellido',
    'Actividad Economica', 'TipoContribuyente', 'Direccion', 'Pais']

# Crear el nuevo dataframe
df_terceros = df_merged[columnas_terceros].copy()

df_merged = df_terceros.merge(df_payees, on='NumeroDocumento', how='left')

columnas_terceros = [
    'TipoDocumento', 'NumeroDocumento', 'Naturaleza', 'PrimerNombre',
    'SegundoNombre', 'PrimerApellido', 'SegundoApellido',
    'Actividad Economica', 'TipoContribuyente', 'Direccion', 'UnidadNegocio',
    'Ciudad', 'Pais' ]

df_terceros = df_merged[columnas_terceros].copy()

df_duplicados = df_terceros[df_terceros.duplicated(subset=['NumeroDocumento'], keep=False)]

columnas_cuentas = [
    'NumeroDocumento', 'NumeroCuenta', 'NombreBanco',
    'TipoCuenta', 'ConceptoPago']

df_bank_accts = df_bank_accts[columnas_cuentas].copy()


df_mergedcuentas = df_tercerosb.merge(df_bank_accts, on='NumeroDocumento', how='left')

nombre_archivo = "TercerosCuentas.csv"
df_mergedcuentas.astype(str).to_csv(nombre_archivo,
                                 index=False, encoding="utf-8", quoting=1)

campos_terceso = ['Nombre',	
'TipoDocumento',	
'NumeroDocumento',	
'Email',	
'Naturaleza',	
'TipoProveedor',	
'PrimerNombre',	
'SegundoNombre',	
'PrimerApellido',	
'SegundoApellido',
'Actividad Economica',	
'TipoContribuyente',
'UnidadNegocio',	
'Direccion',	
'Departamento',	
'Ciudad',	
'Pais']
			


