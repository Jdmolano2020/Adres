import pandas as pd

# Cargar el archivo Excel
# file_path = '../ArmandoTerceros/1.ADR_SupplierImportTemplate_ADR.xlsm'
# df_ADR_Supplier = pd.read_excel(file_path, sheet_name="POZ_SUPPLIERS_INT", header=3 )
# df_ADR_Supplier['id_unico'] = pd.util.hash_pandas_object(df_ADR_Supplier).astype(str)
# # Mostrar las primeras filas del dataframe

# file_path = '../ArmandoTerceros/2.ADR_SupplierAddressImportTemplate_ADR.xlsm'
# df_Address = pd.read_excel(file_path, sheet_name="POZ_SUPPLIER_ADDRESSES_INT", header=3)

# file_path = "../ArmandoTerceros/7.ADR_SupplierBankAccountImportTemplate_ADR.xlsm"

# # Cargar las hojas en DataFrames
# df_payees = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_PAYEES", dtype=str)
# df_bank_accts = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_BANK_ACCTS ", dtype=str, header=4)


# file_path = 'TerceroBusca.xlsx'
# df_tercerosb = pd.read_excel(file_path, dtype={
#     'NumeroDocumento': str, 'ConceptoPagoX': str,})

df_ADR_Supplier = df_ADR_Supplier.rename(columns={'Supplier Number': 'NumeroDocumento',
                                                  'Taxpayer Country': 'Pais',
                                                  'Nombre': 'PrimerNombre',
                                                  'Segundo Nombre': 'SegundoNombre',
                                                  'Apellido': 'PrimerApellido',
                                                  'Segundo Apellido': 'SegundoApellido',
                                                  'Grupo de impuestos': 'TipoContribuyente'})

df_ADR_Supplier = df_ADR_Supplier.drop_duplicates(
    subset=['NumeroDocumento'], keep='first')

df_Address = df_Address.rename(columns={'Supplier Number': 'NumeroDocumento',
                                        'Address Line 1': 'Direccion',
                                        'TIPO DE DOCUMENTO': 'TipoDocumentoDesc',
                                        'ACTIVIDAD ECONOMICA': 'Actividad Economica',
                                        'ID TIPO DE DOCUMENTO': 'TipoDocumento'})
df_Address = df_Address.drop_duplicates(
    subset=['NumeroDocumento'], keep='first')

df_payees = df_payees.rename(columns={'*Supplier Number': 'NumeroDocumento',
                                      'Business Unit Name': 'UnidadNegocio',
                                      'Supplier Site': 'Ciudad'})

df_payees = df_payees.drop_duplicates(
    subset=['NumeroDocumento', 'UnidadNegocio'], keep='first')

# df_bank_accts = df_bank_accts.rename(columns={'*Payee Identifier': 'NumeroDocumento',
#                               '**Branch Name': 'NombreBanco',
#                               'Id Concepto de pago': 'ConceptoPago',
#                               '*Account Number': 'NumeroCuenta',
#                               'Account Type Code': 'TipoCuenta'})


df_merged = df_ADR_Supplier.merge(df_Address, on='NumeroDocumento', how='inner')

columnas_terceros = [
    'TipoDocumento', 'NumeroDocumento',  'PrimerNombre',
    'SegundoNombre', 'PrimerApellido', 'SegundoApellido',
    'Actividad Economica', 'TipoContribuyente', 'Direccion', 'Pais',
    'TipoDocumentoDesc']

# Crear el nuevo dataframe
df_terceros = df_merged[columnas_terceros].copy()

df_merged = df_terceros.merge(df_payees, on='NumeroDocumento', how='left')

columnas_terceros = [
    'TipoDocumento', 'NumeroDocumento', 'PrimerNombre',
    'SegundoNombre', 'PrimerApellido', 'SegundoApellido',
    'Actividad Economica', 'TipoContribuyente', 'Direccion', 'UnidadNegocio',
    'Ciudad', 'Pais']

df_terceros = df_merged[columnas_terceros].copy()

df_terceros['Departamento'] = df_terceros['Ciudad'].astype(str).str[:2]
df_terceros['UnidadNegocio'] = df_terceros['UnidadNegocio'].replace('fos', 'URA').str.upper()

df_duplicados = df_terceros[df_terceros.duplicated(
    subset=['NumeroDocumento'], keep=False)]

# columnas_cuentas = [
#     'NumeroDocumento', 'NumeroCuenta', 'NombreBanco',
#     'TipoCuenta', 'ConceptoPago']

# df_bank_accts = df_bank_accts[columnas_cuentas].copy()


# df_mergedcuentas = df_tercerosb.merge(
#     df_bank_accts, on='NumeroDocumento', how='left')

# nombre_archivo = "TercerosCuentas.csv"
# df_mergedcuentas.astype(str).to_csv(nombre_archivo,
#                                     index=False, encoding="utf-8", quoting=1)

# campos_terceso = ['Nombre',
#                   'TipoDocumento',
#                   'NumeroDocumento',
#                   'Email',
#                   'Naturaleza',
#                   'TipoProveedor',
#                   'PrimerNombre',
#                   'SegundoNombre',
#                   'PrimerApellido',
#                   'SegundoApellido',
#                   'Actividad Economica',
#                   'TipoContribuyente',
#                   'UnidadNegocio',
#                   'Direccion',
#                   'Departamento',
#                   'Ciudad',
#                   'Pais']
