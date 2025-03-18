import pandas as pd
import numpy as np

# Expresión regular para validar correos electrónicos
regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

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
                                      'Supplier Site': 'Ciudad',
                                      'Remit Advice Email': 'Email'})

df_payees = df_payees.drop_duplicates(
    subset=['NumeroDocumento', 'UnidadNegocio'], keep='first')


df_merged = df_ADR_Supplier.merge(
    df_Address, on='NumeroDocumento', how='inner')

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
    'Ciudad', 'Pais', 'Email']

df_terceros = df_merged[columnas_terceros].copy()

df_terceros['Departamento'] = df_terceros['Ciudad'].astype(str).str[:2]
df_terceros['UnidadNegocio'] = df_terceros['UnidadNegocio'].replace(
    'fos', 'URA').str.upper()
df_terceros['Naturaleza'] = np.where(
    df_terceros['TipoDocumento'] == '31', 'J', 'N')
df_terceros['TipoProveedor'] = "Supplier"
# df_terceros['Email'] = ""

df_terceros['Nombre'] = df_terceros[['PrimerNombre', 'SegundoNombre',
                                     'PrimerApellido', 'SegundoApellido']] \
    .fillna('') \
    .astype(str) \
    .apply(lambda x: ' '.join(x).strip(), axis=1)

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

df_terceros['Nombre'] = df_terceros['Nombre'].replace(
    r'[ñÑ]', 'N', regex=True)

df_terceros['PrimerNombre'] = df_terceros['PrimerNombre'].replace(
    r'[ñÑ]', 'N', regex=True)
df_terceros['SegundoNombre'] = df_terceros['SegundoNombre'].replace(
    r'[ñÑ]', 'N', regex=True)
df_terceros['PrimerApellido'] = df_terceros['PrimerApellido'].replace(
    r'[ñÑ]', 'N', regex=True)
df_terceros['SegundoApellido'] = df_terceros['SegundoApellido'].replace(
    r'[ñÑ]', 'N', regex=True)

df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[$·ª=_~!¦§°<*ºØ&()/,?:>\`\"+\'@\]]', '', regex=True)

df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[#]', 'No', regex=True)
df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[¢]', 'O', regex=True)

df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[-]', ' ', regex=True)
df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[¡]', 'I', regex=True)
df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[¤]', 'N', regex=True)
df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[µ]', 'A', regex=True)
df_terceros['Direccion'] = df_terceros['Direccion'].replace(
    r'[£]', 'U', regex=True)


df_terceros['Direccion'] = df_terceros['Direccion'].str.replace(
    r'\s+', ' ', regex=True).str.strip()

# Asignar cadena vacía a los correos no válidos
df_terceros['Email'] = df_terceros['Email'].where(
    df_terceros['Email'].str.match(regex_email, na=False), "")

df_terceros_mail = df_terceros[df_terceros['Email'].notna() & (
    df_terceros['Email'] != '')]

df_filtro = df_terceros[df_terceros['NumeroDocumento'] == '901037916']

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
