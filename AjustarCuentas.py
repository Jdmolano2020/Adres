import pandas as pd

file_path = 'Cuentas.xlsx'
df_cuentas = pd.read_excel(file_path, dtype={
                           'NumeroDocumento': str, 'NumeroCuenta': str,
                           'NombreBanco': str, 'ConceptoPago': str, })
df_unificado = df_cuentas.groupby(['NumeroDocumento', 'NumeroCuenta',
                                   'NombreBanco', 'TipoCuenta'],
                                  as_index=False) \
    .agg({'ConceptoPago': lambda x: '-'.join(x.unique())})

df_unificado['ConceptoPago'].value_counts()
df_unificado.to_csv("cuentas.csv", sep=";", index=False)
df_unificado.astype(str).to_csv(
    "cuentas.csv", index=False, encoding="utf-8", quoting=1)
