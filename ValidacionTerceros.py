import pandas as pd
import os

import time
from datetime import datetime

# Crear carpeta para guardar los archivos exportados
output_folder = "archivos_terceros"
os.makedirs(output_folder, exist_ok=True)


# Medir el tiempo de ejecución
start_time = time.time()
print(f"inicio: ", {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')})

def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def agregar_informe(df, nombre_archivo,columna, df_informe):
    
    if columna in df.columns:
        num_registros = len(df)
        valores_unicos = df[columna].unique()
        cantidad_valores_unicos = len(valores_unicos)
        nueva_fila = {
            'archivo': nombre_archivo,
            'Cantidad de registros': num_registros,
            'Cantidad de valores únicos': cantidad_valores_unicos
        }
    else:
        nueva_fila = {
            'archivo': nombre_archivo,
            'Cantidad de registros': len(df),
            'Cantidad de valores únicos': 0
        }
    
    df_informe = pd.concat([df_informe, pd.DataFrame([nueva_fila])], ignore_index=True)
    
    return df_informe

def ordenar_numeros(conceptos):
    conceptos_unicos = set()
    for concepto in conceptos.split('-'): # Separar los valores
        conceptos_unicos.add(concepto)
    return '-'.join(sorted(conceptos_unicos)) # Ordenarlos como números

# Función para comparar dos columnas con listas de valores separados por guiones
def compare_columns(row):
    set_x = set(row['ConceptoPagoX'].split('-'))
    set_e = set(row['ConceptoPagoE'].split('-'))
    diff_x = set_x - set_e
    diff_e = set_e - set_x
    concepton = diff_x.union(diff_e)
    return pd.Series(['-'.join(concepton)]).str.strip()


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


def buscarinformacionterceros(df_terceros, df_tercerosb):
    
    df_tercerosbc = df_tercerosb.copy()
    df_tercerosma = df_terceros.copy()
    # Convertir en lista
    
    df_tercerosmae = df_tercerosbc.merge(
        df_tercerosma,
        on=['NumeroDocumento'], how='inner')
    columnas_terceros = ['Nombre', 'TipoDocumento', 'NumeroDocumento',
                      'Email', 'Naturaleza', 'TipoProveedor',
                      'PrimerNombre', 'SegundoNombre',
                      'PrimerApellido', 'SegundoApellido',
                      'Actividad Economica', 'TipoContribuyente',
                      'UnidadNegocio', 'Direccion',
                      'Departamento', 'Ciudad', 'Pais']
    df_tercerosmae = df_tercerosmae[columnas_terceros].copy()
    return df_tercerosmae

def buscarcuentaterceros (df_tercerosb, df_cuentas):

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

    return df_tercerocbe


df_informe = pd.DataFrame(columns=['archivo', 'Cantidad de registros', 'Cantidad de valores únicos'])

# file_path = 'OCI_TERCEROS.xlsx'
# df_terceros_v1 = pd.read_excel(file_path, dtype={
#     'Departamento': str, 'Ciudad': str,
#     'NumeroDocumento': str, 'NumeroCuenta': str,
#     'NombreBanco': str, 'ConceptoPago': str })
# file_path = 'ADR_Info_Terceros_Direcciones_RP_ADR_Info_Terceros_Direcciones_RP.xlsx'
# df_tercerosparal = pd.read_excel(file_path, dtype={
#     'ID PROVEEDOR': str, 'CODIGO BANCO': str,
#     'CUENTA BANCARIA': str, 'ID PAGO': str},header=1)
# file_path = 'TerceroBusca.xlsx'
# df_tercerosb = pd.read_excel(file_path, dtype={
#     'NumeroDocumento': str, 'ConceptoPagoX': str,})

df_tercerosb=df_tercerosb.groupby('NumeroDocumento')['ConceptoPagoX'].apply(lambda x: '-'.join(map(str, x))).reset_index()

# Aplicar la función a la columna col2
df_tercerosb['ConceptoPagoX'] = df_tercerosb['ConceptoPagoX'].apply(ordenar_numeros)

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

df_tercerose['ConceptoPagoE'] = df_tercerose.groupby('ID PROVEEDOR')['ConceptoPagoE'].transform(lambda x: '-'.join(sorted(set(x))))
df_tercerose['ConceptoPagoN'] = df_tercerose.apply(compare_columns, axis=1)
# Filtrar registros donde 'ConceptoPagoN' no sea NaN o vacío
df_filtradon = df_tercerose[df_tercerose['ConceptoPagoN'].notna() & (df_tercerose['ConceptoPagoN'] != '')]

df_filtradoe = df_tercerose[df_tercerose['ConceptoPagoE'].notna() & (df_tercerose['ConceptoPagoE'] != '')]
#df_filtradoe['ConceptoPagoE'] = df_filtradoe.groupby('ID PROVEEDOR')['ConceptoPagoE'].transform(lambda x: '-'.join(sorted(set(x))))
#df_filtradoe['ConceptoPagoE']=df_filtradoe['ConceptoPagoT'].apply(ordenar_numeros)  # columna innecesarea

#df_filtradoe.to_excel("df_filtradoe.xlsx") 

#df_filtradoe.drop ('ConceptoPagoT', axis = 1)
df_iguales = df_filtradoe[df_filtradoe['ConceptoPagoX'] == df_filtradoe['ConceptoPagoE']]
df_filtradon = df_filtradon[~df_filtradon['ID PROVEEDOR'].isin(df_iguales['ID PROVEEDOR'])]

#df_filtradon.to_excel("df_filtradon.xlsx") 
# Expandir 'ConceptoPagoN' en filas separadas (cada valor se divide por '-')
df_exploded = df_filtradon.assign(ConceptoPagoN=df_filtradon['ConceptoPagoN'].str.split('-')).explode('ConceptoPagoN')

# ## archivo de directorios y divipola
# excel_TI_df = pd.read_excel('DIRECTORIO ERP DINAMICS.xlsx',sheet_name='Tipo Identificacion', dtype={
#     'Número': str, 'TipoIdentificacion (CITAIdentificationType)': str})
# excel_TI_df['TipoIdentificacion (CITAIdentificationType)']=excel_TI_df['TipoIdentificacion (CITAIdentificationType)'].astype('str').str.replace(r".", r"", regex=False)

# ## archivo Grupo de proveedores
# excel_DP_df = pd.read_excel('DIRECTORIO ERP DINAMICS.xlsx',sheet_name='Grupo de proveedores', usecols="A:C", dtype={
#     'Grupo de proveedores': str, 'Descripción': str,'Condiciones de pago': str})

# ## archivo Grupo de proveedores
# df1 = pd.read_excel('TERCEROS SISTEMAS 1.xlsx',usecols="C,M", dtype={
#     'Número documento': str, 'Grupo': str})

# df2 = pd.read_excel('TERCEROS SISTEMAS 2.xlsx',usecols="C,M", dtype={
#     'Número documento': str, 'Grupo': str})

# df3 = pd.read_excel('terceros a migrar.xlsx',usecols="C,F", dtype={
#     'Tercero': str, 'GrupoProveedor': str})
# df3.rename(columns={'Tercero': 'Número documento', 'GrupoProveedor': 'Grupo'}, inplace=True)

# # Combinar los DataFrames
# df_G_Proveedores = pd.concat([df1, df2, df3], ignore_index=True)

# Asegurarse de que los valores en la primera columna sean únicos
# Suponiendo que la primera columna se llama 'Número documento'
# df_G_Proveedores = df_G_Proveedores.drop_duplicates(subset=['Número documento'])

# Recorrer cada valor único de 'ConceptoPagoN' y exportar los registros correspondientes
conceptos=df_exploded['ConceptoPagoN'].unique()
conceptos=sorted([elemento for elemento in conceptos if elemento])
print(conceptos)
for concepto in conceptos:
    df_subset = df_exploded[df_exploded['ConceptoPagoN'] == concepto].drop_duplicates(subset=['ID PROVEEDOR'])

    # Cambia el Tipo de Identificacion para la SUBSET
    df_subset = df_subset.merge(df_terceros_v1[['NumeroDocumento','Direccion','Departamento','Ciudad']], left_on='ID PROVEEDOR', right_on='NumeroDocumento', how='left')

    # Cambia el Tipo de direccion, deparatamento y municipio a numero para la SUBSET
    df_subset['DIRECCION1']=df_subset['Direccion']
    df_subset['DEPARTAMENTO']=df_subset['Departamento']
    df_subset['CIUDAD']=df_subset['Ciudad'].str[2:5] 
    df_subset.drop(columns=['NumeroDocumento','Direccion','Departamento','Ciudad'], inplace=True)
    
    # Crear nombre de archivo seguro
    nombre_archivo = f"{output_folder}/terceros_{concepto.replace(' ', '_').replace('/', '_')}.csv"
    # Generar el informe y añadir las filas al DataFrame de informe inicial
    df_informe = agregar_informe(df_subset, f"terceros_{concepto.replace(' ', '_').replace('/', '_')}",'ID PROVEEDOR' , df_informe)
    
    # Exportar a CSV
    df_subset.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', quoting=1)

    ###############################   DATAFRAME PLANTILLA

    # df_plantilla= pd.DataFrame(columns=['IdProceso','TipoProceso','LineaNegocio','UnidadNegocio','NumeroIdentificacion','PrimerNombreRazonSocial','SegundoNombre','PrimerApellido','SegundoApellido','TipoIdentificacion','GrupoClienteProveedor','DimensionCentro','Direccion','Departamento','Municipio','Pais','Correo','CodigoCIIU','Reciproco','GrupoImpuesto','NumeroCuentaBancaria','TipoCuenta','CodigoBanco','NombreCuenta','ConceptoPago','FormaPago','NombreBanco','NumeroRuta'])
    # df_plantilla[['NumeroIdentificacion','PrimerNombreRazonSocial','TipoIdentificacion','TipoCuenta','ConceptoPago','Direccion','Departamento','Municipio']]=df_subset[['ID PROVEEDOR','NOMBRE PROVEEDOR','TIPO DOCUMENTO','TIPO CUENTA','ConceptoPagoX','DIRECCION1','DEPARTAMENTO','CIUDAD']]
    # df_plantilla['PrimerNombreRazonSocial']=df_plantilla['PrimerNombreRazonSocial'].str.extract(r'^[^-\n]*-[^-\n]*-(.*)$')
    # df_plantilla['TipoProceso']='44'
    # df_plantilla['LineaNegocio']='14'
    # df_plantilla['UnidadNegocio']='FOS'
    # #df_plantilla['DimensionCentro']='2'
    # #df_plantilla['Direccion']='Oficina Central URA'
    # #df_plantilla['Departamento']='11'
    # #df_plantilla['Municipio']='001'
    # df_plantilla['Pais']='COL'
    # df_plantilla['GrupoImpuesto']='RC'

    # # Cambiar las palabras Ahorro y Corriente por los tipos [0,1] para la plantilla
    # df_plantilla['TipoCuenta'] = "" #df_plantilla['TipoCuenta'].apply(lambda x: '0' if x=='Corriente' else 1 if x=='Ahorro' else "")

    # # Cambia el Tipo de Identificacion para la plantilla
    # df_plantilla = df_plantilla.merge(excel_TI_df, left_on='TipoIdentificacion', right_on='TipoIdentificacion (CITAIdentificationType)', how='left')
    # df_plantilla['TipoIdentificacion']=df_plantilla['Número']

    # # Cambia el Tipo de Identificacion para la plantilla
    # df_plantilla = df_plantilla.merge(df_terceros_v1[['NumeroDocumento','Direccion','Departamento','Ciudad',]], left_on='NumeroIdentificacion', right_on='NumeroDocumento', how='left')

    # # Cambia el Tipo de direccion, deparatamento y municipio a numero EN PLANTILLA
    # df_plantilla['Direccion_x']=df_plantilla['Direccion_y']
    # df_plantilla['Departamento_x']=df_plantilla['Departamento_y']
    # df_plantilla['Municipio']=df_plantilla['Ciudad'].str[2:5] 

    # df_plantilla.rename(columns={'Direccion_x': 'Direccion', 'Departamento_x': 'Departamento'}, inplace=True)

    # # Obtener el Grupo de profevedores df_G_Proveedores PLANTILLA
    # df_plantilla = df_plantilla.merge(df_G_Proveedores, left_on='NumeroIdentificacion', right_on='Número documento', how='left')
    # df_plantilla['GrupoClienteProveedor']=df_plantilla['Grupo']

    # # Buscar DimensionCentro
    # df_plantilla = df_plantilla.merge(excel_DP_df, left_on='GrupoClienteProveedor', right_on='Grupo de proveedores', how='left')
    # df_plantilla['DimensionCentro']=df_plantilla['Condiciones de pago']

    # #Eliminar Columnas 
    # df_plantilla.drop(columns=['Número', 'TipoIdentificacion (CITAIdentificationType)', 'NumeroDocumento','Direccion_y',
    #                            'Departamento_y','Ciudad','Número documento','Grupo','Condiciones de pago','Descripción',
    #                            'Grupo de proveedores'], inplace=True)

    # df_plantilla.to_csv(f"{output_folder}/pl_terceros_{concepto.replace(' ', '_').replace('/', '_')}.csv", index=False, encoding='utf-8-sig', quoting=1)

print("Exportación Terceros Existentes completada.")

nombre_archivo = f"{output_folder}/TercerosExistentes.csv"
df_filtradoe.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)
df_informe = agregar_informe(df_filtradoe, 'TercerosExistentes','ID PROVEEDOR' , df_informe)

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

df_tercerosc = df_terceros_v1.merge(df_tercerosne,
                                 left_on='NumeroDocumento',
                                 right_on='NumeroDocumento',
                                 how='inner')

nombre_archivo = f"{output_folder}/TercerosCargar.csv"
df_tercerosc.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)

df_informe = agregar_informe(df_tercerosc, 'TercerosCargar','NumeroDocumento' , df_informe)

df_tercerosne = df_tercerosne.merge(df_terceros_v1,
                                    left_on='NumeroDocumento',
                                    right_on='NumeroDocumento',
                                    how='left',
                                    indicator=True)
df_tercerosne = df_tercerosne[df_tercerosne['_merge'] == 'left_only']

# Eliminar la columna _merge si no la necesitas
df_tercerosne = df_tercerosne.drop(columns=['_merge'])
df_tercerosne = df_tercerosne[df_tercerosb.columns]
nombre_archivo = f"{output_folder}/TercerosArmar.csv"
df_terceros_armar = buscarinformacionterceros(df_terceros, df_tercerosne)
df_terceros_cuentas = buscarcuentaterceros(df_tercerosne, df_cuentas)

df_terceros_armar = df_terceros_armar.merge(df_terceros_cuentas,
                                  on=['NumeroDocumento', 'UnidadNegocio'], how='left')



df_tercerosne.astype(str).to_csv(nombre_archivo,
                                 index=False, encoding="utf-8", quoting=1)
df_informe = agregar_informe(df_tercerosne, 'TercerosArmar','ID PROVEEDOR' , df_informe)

print(df_informe)

## captura hora de finalizacion
end_time = time.time()
print(f"fin: ", {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')})

# Calcular el tiempo total de ejecución
tiempo_total = end_time - start_time
print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos", segundos_a_segundos_minutos_y_horas(int(round(tiempo_total,0))))

nombre_archivo = f"{output_folder}/TercerosNoExistentes.csv"
df_exploded.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)