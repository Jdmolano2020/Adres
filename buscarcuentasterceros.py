import pandas as pd


df_tercerosbc = df_tercerosb.copy()
df_tercerocb = df_cuentas.copy()
# Convertir en lista
df_tercerosbc['ConceptoPagoX'] = df_tercerosbc['ConceptoPagoX'].str.split('-')
# Expandir en filas  
df_tercerosbf = df_tercerosbc.explode('ConceptoPagoX')  

df_tercerosbf = df_tercerosbf.rename(
    columns={'ConceptoPagoX': 'ConceptoPago',})


df_tercerocbe = df_tercerosbf.merge(
    df_tercerocb,
    on=['NumeroDocumento', 'ConceptoPago'], how='left')

nombre_archivo = "TercerosCuentasEncontradas.csv"
df_tercerocbe.astype(str).to_csv(nombre_archivo,
                              index=False, encoding="utf-8", quoting=1)