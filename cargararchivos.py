import pandas as pd

# Cargar el archivo Excel
file_path = '1.ADR_SupplierImportTemplate_ADR.xlsm'
df_ADR_Supplier = pd.read_excel(file_path, sheet_name="POZ_SUPPLIERS_INT", header=3 )

file_path = '2.ADR_SupplierAddressImportTemplate_ADR.xlsm'
df_Address = pd.read_excel(file_path, sheet_name="POZ_SUPPLIER_ADDRESSES_INT", header=3)

file_path = "7.ADR_SupplierBankAccountImportTemplate_ADR.xlsm"
# Cargar las hojas en DataFrames
df_payees = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_PAYEES", dtype=str, header=3)
df_bank_accts = pd.read_excel(file_path, sheet_name="IBY_TEMP_EXT_BANK_ACCTS ", dtype=str, header=3)

file_path = 'TerceroBusca.xlsx'
df_tercerosb = pd.read_excel(file_path, dtype={
    'NumeroDocumento': str, 'ConceptoPagoX': str,})

file_path = 'OCI_TERCEROS.xlsx'
df_terceros_v1 = pd.read_excel(file_path, dtype={
    'Departamento': str, 'Ciudad': str,
    'NumeroDocumento': str, 'NumeroCuenta': str,
    'NombreBanco': str, 'ConceptoPago': str, })

file_path = 'ADR_Info_Terceros_Direcciones_RP_ADR_Info_Terceros_Direcciones_RP.xlsx'
df_tercerosparal = pd.read_excel(file_path, dtype={
    'ID PROVEEDOR': str, 'CODIGO BANCO': str,
    'CUENTA BANCARIA': str, 'ID PAGO': str})
