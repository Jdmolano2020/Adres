import pandas as pd

file_path = 'bancos.xlsx'
df_bancos = pd.read_excel(file_path, dtype={
    'CodigoBanco': str, 'NombreBanco': str, }, engine='openpyxl')

file_path = 'CuentasUGG.xlsx'
df_Cuentasugg = pd.read_excel(file_path,  dtype={
    'Identificación del tercero (NIT)': str }, engine='openpyxl')

df_Cuentasugg = df_Cuentasugg.rename(
    columns={'Identificación del tercero (NIT)': 'NumeroDocumento',
             'N° de cuenta bancaria': 'NumeroCuenta', })


df_bank_acctscuenta = df_bank_accts.copy()
df_bank_acctscuenta = df_bank_acctscuenta.rename(
    columns={'*Payee Identifier': 'NumeroDocumento',
             '**Bank Name': 'NombreBanco',
             'Id Concepto de pago': 'ConceptoPago',
             '*Account Number': 'NumeroCuenta',
             'Account Type Code': 'TipoCuenta'})

# Diccionario con los valores a reemplazar
cambios_banco = {
    'BBVA COLOMBIA': 'BANCO BBVA',
    'BANCO CAJA SOCIAL BCSC SA': 'BANCO CAJA SOCIAL',
    'BANCO DAVIVIENDA S.A.': 'BANCO DAVIVIENDA',
    'BANCO AV VILLAS': 'AV VILLAS',
    'COOMEVA': 'BANCO COOMEVA',
    'NEQUI': 'BANCO NEQUI',
    'BANCO GNB SUDAMERIS': 'GNB SUDAMERIS',
    'COOPCENTRAL': 'BANCO COOPCENTRAL',
    'Banco Nubank': 'NU BANK',
    'SCOTIABANK COLPATRIA S.A': 'BANCO SCOTIABANK COLPATRIA',
    'NUBANK COLOMBIA': 'NU BANK',
    'LULO BANK S.A.': 'LULO BANK',
    'BANCO SERFINANZA': 'BANCO SERFINANZA SA',
    'MIBANCO': 'MI BANCO',
    'BANCOOMEVA': 'BANCO COOMEVA',
    'BANCO COOPERATIVO COOPCENTRAL': 'BANCO COOPCENTRAL',
    'LULO BANK S.A': 'LULO BANK',
    'CONFIAR': 'CONFIAR SA',
    'BNP PARIBAS': 'BNP Paribas Colombia',
    'ITAÚ CORPBANCA/HELM BANK': 'ITAU',
    'HELM BANK': 'ITAU',
    'GRANBANCO S.A.BANCAFE': 'BANCO DAVIVIENDA',
    'RappiPay': 'RAPPIPAY',
    'CORPBANCA/SANTANDER': 'BANCO SANTANDER',
    'santander': 'BANCO SANTANDER',
}


# Aplicar los cambios en la columna 'NombreBanco'
df_bank_acctscuenta['NombreBanco'] = df_bank_acctscuenta['NombreBanco'].replace(
    cambios_banco)

cambios_tipo = {
    'CURRENT': '0',
    'SAVINGS': '1', }

df_bank_acctscuenta['TipoCuenta'] = df_bank_acctscuenta['TipoCuenta'].replace(
    cambios_tipo)

df_mergedcuentas = df_bank_acctscuenta.merge(
    df_bancos, on='NombreBanco', how='left')

df_mergedcuentas = df_mergedcuentas.dropna(subset=['CodigoBanco'])

# ['NumeroDocumento', 'NumeroCuenta', 'UnidadNegocio']
df_mergedcuentas = df_mergedcuentas.merge(
    df_Cuentasugg,
    on=['NumeroDocumento', 'NumeroCuenta'], how='left')

df_mergedcuentas['UnidadNegocio'] = df_mergedcuentas['UnidadNegocio'].fillna('URA').str.upper()

# print(df_mergedcuentas.columns)

campos_cuentas = ['NumeroDocumento', 'NumeroCuenta', 'CodigoBanco',
                  'NombreBanco', 'TipoCuenta', 'ConceptoPago', 'UnidadNegocio']

df_cuentas = df_mergedcuentas[campos_cuentas].copy()

nombre_archivo = "TercerosCuentasrevisar.csv"
df_cuentas.astype(str).to_csv(nombre_archivo,
                              index=False, encoding="utf-8", quoting=1)
