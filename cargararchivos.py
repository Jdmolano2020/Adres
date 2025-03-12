import pandas as pd

# Cargar el archivo Excel
file_path = '1.ADR_SupplierImportTemplate_ADR.xlsx'
df_ADR_Supplier = pd.read_excel(file_path, engine='openpyxl')
df_ADR_Supplier['id_unico'] = pd.util.hash_pandas_object(df_ADR_Supplier).astype(str)

file_path = '2.ADR_SupplierAddressImportTemplate_ADR.xlsx'
df_Address = pd.read_excel(file_path, engine='openpyxl')

file_path = "7.ADR_SupplierBankAccountImportTemplate_ADR.xlsx"
# Cargar las hojas en DataFrames
df_payees = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_PAYEES", dtype=str)
df_bank_accts = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_BANK_ACCTS", dtype=str)

file_path = 'TerceroBusca.xlsx'
df_tercerosb = pd.read_excel(file_path, dtype={
    'NumeroDocumento': str, 'ConceptoPagoX': str,})

file_path = 'OCI_TERCEROS.xlsx'
df_terceros = pd.read_excel(file_path, dtype={
    'Departamento': str, 'Ciudad': str,
    'NumeroDocumento': str, 'NumeroCuenta': str,
    'NombreBanco': str, 'ConceptoPago': str, })

file_path = 'ADR_Info_Terceros_Direcciones_RP_ADR_Info_Terceros_Direcciones_RP.xlsx'
df_tercerosparal = pd.read_excel(file_path, dtype={
    'ID PROVEEDOR': str, 'CODIGO BANCO': str,
    'CUENTA BANCARIA': str, 'ID PAGO': str})
