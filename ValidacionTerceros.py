import pandas as pd
import os
import numpy as np
import time
from datetime import datetime
import threading

# Crear carpeta para guardar los archivos exportados
output_folder = "archivos_terceros"
os.makedirs(output_folder, exist_ok=True)


# Medir el tiempo de ejecución
start_time = time.time()
print(f"inicio: ", {datetime.fromtimestamp(
    start_time).strftime('%Y-%m-%d %H:%M:%S')})


def Busca_conceptos(row, col_id_pago, col_concepto_pago):
    col_id_pago_value = str(row[col_id_pago]) if pd.notnull(
        row[col_id_pago]) else ''
    col_concepto_pago_value = str(row[col_concepto_pago]) if pd.notnull(
        row[col_concepto_pago]) else ''

    set_col_id_pago = set(col_id_pago_value.split('-'))
    set_col_concepto_pago = set(col_concepto_pago_value.split('-'))
    matching_numbers = set_col_id_pago.intersection(set_col_concepto_pago)
    return '-'.join(matching_numbers)


def find_different_numbers(row, col_concepto_pago, ConceptoPagoN):
    set_col_concepto_pago = set(row[col_concepto_pago].split('-'))
    set_ConceptoPagoN = set(row[ConceptoPagoN].split('-'))
    different_numbers = set_col_concepto_pago.symmetric_difference(
        set_ConceptoPagoN)
    return '-'.join(sorted(different_numbers))


def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def agregar_informe(df, nombre_archivo, columna, df_informe):

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

    df_informe = pd.concat(
        [df_informe, pd.DataFrame([nueva_fila])], ignore_index=True)

    return df_informe


def ordenar_numeros(conceptos):
    conceptos_unicos = set()
    for concepto in conceptos.split('-'):  # Separar los valores
        conceptos_unicos.add(concepto)
    return '-'.join(sorted(conceptos_unicos))  # Ordenarlos como números

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


def buscarcuentaterceros(df_tercerosb, df_cuentas):

    df_tercerosbc = df_tercerosb.copy()
    df_tercerocb = df_cuentas.copy()
    # Convertir en lista
    df_tercerosbc['ConceptoPagoX'] = df_tercerosbc['ConceptoPagoX'].str.split(
        '-')
    # Expandir en filas
    df_tercerosbf = df_tercerosbc.explode('ConceptoPagoX')

    df_tercerosbf = df_tercerosbf.rename(
        columns={'ConceptoPagoX': 'ConceptoPago', })

    df_tercerocbe = df_tercerosbf.merge(
        df_tercerocb,
        on=['NumeroDocumento', 'ConceptoPago'], how='left')

    return df_tercerocbe

def captura_opcion_Unidad(default="TODOS"):
    options = {
        1: "TODOS",
        2: "URA",
        3: "UGG"
    }
    attempts = 0
    max_attempts = 3
    choice_made = threading.Event()
    
    def timer():
        time.sleep(5)
        if not choice_made.is_set():
            print(f"\nTime's up! Defaulting to: {default}")
            choice_made.set()
    
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

    while attempts < max_attempts and not choice_made.is_set():
        print("Seleccione la Unidad de Negocio a Trabajar:")
        for key, value in options.items():
            print(f"{key}. {value}")
        
        try:
            choice = int(input("digite el numero de su eleccion: "))
            if choice in options:
                choice_made.set()
                return {"choice": choice, "text": options[choice]}
            else:
                print("Opcion invalida. Por favor seleccione una opcion valida.")
        except ValueError:
            print("Entrada Invalida. Digite un numero.")
        
        attempts += 1
    
    if not choice_made.is_set():
        print(f"Ha selecionado una opcion invalida. se realizara : {default}")
        return {"choice": 1, "text": default}

# Get the user's choice
Unidad_a_trabajar = captura_opcion_Unidad()
print(f"Selecciono: {Unidad_a_trabajar}")


df_informe = pd.DataFrame(
    columns=['archivo', 'Cantidad de registros', 'Cantidad de valores únicos'])

df_informe = agregar_informe(
    df_tercerosb, 'Terceros_Buscar', 'NumeroDocumento', df_informe)

df_terceros_control= df_tercerosb.copy()

df_tercerosb = df_tercerosb.groupby('NumeroDocumento')['ConceptoPagoX'].apply(
    lambda x: '-'.join(map(str, x))).reset_index()

# Aplicar la función a la columna col2
df_tercerosb['ConceptoPagoX'] = df_tercerosb['ConceptoPagoX'].apply(
    ordenar_numeros)

df_tercerose = df_tercerosparal.merge(df_tercerosb,
                                      left_on='ID PROVEEDOR',
                                      right_on='NumeroDocumento',
                                      how='inner')

df_tercerose.drop(columns=['NumeroDocumento'],
                  inplace=True)


# Aplicar la función en el DataFrame, indicando los nombres de las columnas que
# deseas comparar
df_tercerose['ConceptoPagoE'] = df_tercerose.apply(
    Busca_conceptos, axis=1, col_id_pago="ID PAGO", col_concepto_pago="ConceptoPagoX")
df_tercerose['ConceptoPagoE'] = df_tercerose.groupby('ID PROVEEDOR')[
    'ConceptoPagoE'].transform(lambda x: '-'.join(sorted(set(filter(None, x)))))
df_tercerose['ConceptoPagoN'] = df_tercerose.apply(
    find_different_numbers, axis=1, col_concepto_pago="ConceptoPagoX", ConceptoPagoN='ConceptoPagoE')
df_tercerose['ConceptoPagoN'] = df_tercerose['ConceptoPagoN'] .apply(
    lambda x: x.lstrip('-'))

df_filtradoe = df_tercerose[df_tercerose['ConceptoPagoE'].notna() & (
    df_tercerose['ConceptoPagoE'] != '') & (
    df_tercerose['ConceptoPagoE'] != 'nan')]

nombre_archivo = f"{output_folder}/TercerosExistentes.csv"
df_filtradoe.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)


df_terceros_control= df_terceros_control.merge(df_tercerose[['ID PROVEEDOR']], left_on='NumeroDocumento', right_on='ID PROVEEDOR', how='left', indicator=True)
df_terceros_control=df_terceros_control[df_terceros_control['_merge'] == 'left_only'].drop(columns=['_merge','ID PROVEEDOR'])

df_informe = agregar_informe(
    df_tercerose, 'TercerosExistentes', 'ID PROVEEDOR', df_informe)

#
df_filtradon = df_tercerose[df_tercerose['ConceptoPagoN'].notna() & (
    df_tercerose['ConceptoPagoN'] != '') & (
    df_tercerose['ConceptoPagoN'] != 'nan') & (
    df_tercerose['ConceptoPagoN'].str.len() > 0)]

df_filtradon = df_filtradon.drop(columns=['ADRES OPERAC RECIPROCA', 'ID PAGO',
                                          'CUENTA BANCARIA', 'TIPO CUENTA',
                                          'UBICACION ENVIO', 'BANCO',
                                          'CODIGO BANCO', 'ConceptoPagoX',
                                          'ConceptoPagoE', 'CIUDAD',
                                          'DEPARTAMENTO']).drop_duplicates()

if Unidad_a_trabajar['text'] != "TODOS":
    df_filtradon=df_filtradon[['UNIDAD NEGOCIO']==Unidad_a_trabajar['text']]
    df_filtradon['UNIDAD NEGOCIO'] = df_filtradon['UNIDAD NEGOCIO'].replace([np.nan, '', None], Unidad_a_trabajar['text'])
else:
    df_filtradon['UNIDAD NEGOCIO'] = df_filtradon['UNIDAD NEGOCIO'].replace([np.nan, '', None], 'URA')    

# Terceros existentes que no contienen el concepto se Consultan las cuentas
df_tercerosc_cuentas = buscarcuentaterceros(df_filtradon[['ID PROVEEDOR', 'ConceptoPagoN']]
                                            .rename(columns={'ID PROVEEDOR': 'NumeroDocumento', 'ConceptoPagoN': 'ConceptoPagoX'}), df_cuentas).drop_duplicates()

df_filtradon = df_filtradon.rename(columns={'UNIDAD NEGOCIO': 'UnidadNegocio', 'ID PROVEEDOR': 'NumeroDocumento'}
                                   ).merge(df_tercerosc_cuentas, on=['NumeroDocumento', 'UnidadNegocio'], how='left'
                                           ).drop_duplicates()

df_filtradon = df_filtradon.merge(df_terceros, on=['NumeroDocumento', 'UnidadNegocio'],  how='left'
                                         ).drop_duplicates()

df_filtradon=df_filtradon[df_filtradon['ConceptoPago'].notna() & (df_filtradon['ConceptoPago'] != '')]

df_filtradon['rank'] = df_filtradon.groupby('NumeroDocumento')['ConceptoPago'].rank(method='dense', ascending=False)

df_informe = agregar_informe(
    df_filtradon, 'TercerosSinConcepto', 'NumeroDocumento', df_informe)

df_terceros_control= df_terceros_control.merge(df_filtradon[['NumeroDocumento']], left_on='NumeroDocumento', right_on='NumeroDocumento', how='left', indicator=True)
df_terceros_control=df_terceros_control[df_terceros_control['_merge'] == 'left_only'].drop(columns=['_merge'])

campos_tercero = ['Nombre',
                  'TipoDocumento',
                  'NumeroDocumento',
                  'Email',
                  'Naturaleza',
                  'TipoProveedor',
                  'PrimerNombre',
                  'SegundoNombre',
                  'PrimerApellido',
                  'SegundoApellido',
                  'UnidadNegocio',
                  'Actividad Economica',
                  'TipoContribuyente',
                  'Direccion',
                  'Departamento',
                  'Ciudad',
                  'Pais',
                  'NumeroCuenta',
                  'NombreBanco',
                  'TipoCuenta',
                  'ConceptoPago'
                  ]

#for para gerenar archivo Json por grupos
conceptos = df_filtradon['rank'].unique()
conceptos = sorted([elemento for elemento in conceptos if elemento])
print(conceptos)
for concepto in conceptos:
    df_subset=df_filtradon[df_filtradon['rank']==concepto]

    df_subset['NombreBanco']=df_subset['CodigoBanco']

    #crea df con los campos para contruir Json
    df_subset=df_subset[campos_tercero]   

    # Crear nombre de archivo seguro
    nombre_archivo = f"{output_folder}/terceros_e_" + f"{concepto:.0f}".replace(' ', '_').replace('/', '_') + ".csv"

    # Generar el informe y añadir las filas al DataFrame de informe inicial
    df_informe = agregar_informe(
        df_subset, f"terceros_e_{concepto:.0f}", 'NumeroDocumento', df_informe)

    # Exportar a CSV
    df_subset.to_csv(nombre_archivo, index=False,
                     encoding='utf-8-sig', quoting=1)
    
    # Generar el JSON con la función
    json_resultado = construir_json(df_subset)

    # Guardar el JSON en un archivo
    with open(nombre_archivo.replace("csv","json"), "w", encoding="utf-8") as f:
        json.dump(json_resultado, f, indent=4, ensure_ascii=False)

    print(f"El archivo JSON se ha guardado como terceros_{concepto:.0f}.json")

    #Envio_integracion(json_resultado)

print("Exportación Terceros Existentes sin concepto completada.")

df_tercerosne = df_tercerosb[['NumeroDocumento','ConceptoPagoX']].merge(df_tercerosparal[['ID PROVEEDOR']],
                                   left_on='NumeroDocumento',
                                   right_on='ID PROVEEDOR',
                                   how='left',
                                   indicator=True)

# Filtrar los registros que no tienen coincidencia en df_tercerosparal
df_tercerosne = df_tercerosne[df_tercerosne['_merge'] == 'left_only']

# Eliminar la columna _merge si no la necesitas
df_tercerosne = df_tercerosne.drop(columns=['_merge'])
df_tercerosne = df_tercerosne[df_tercerosb.columns]

df_informe = agregar_informe(
    df_tercerosne, 'TercerosNoEncontrados', 'NumeroDocumento', df_informe)

df_tercerosc = df_terceros.merge(df_tercerosne,
                                    left_on='NumeroDocumento',
                                    right_on='NumeroDocumento',
                                    how='inner')

df_tercerosc_cuentas = buscarcuentaterceros(df_tercerosne, df_cuentas)

df_tercerosc = df_tercerosc.merge(df_tercerosc_cuentas,
                                  on=['NumeroDocumento', 'UnidadNegocio'], how='left')

df_tercerosc = df_tercerosc.drop(columns=['ConceptoPagoX'])

#crea df con los campos para contruir Json
df_tercerosc=df_tercerosc[campos_tercero]  

if Unidad_a_trabajar['text'] != "TODOS":
    df_tercerosc=df_tercerosc[['UnidadNegocio']==Unidad_a_trabajar['text']]
    df_tercerosc['UnidadNegocio'] = df_tercerosc['UnidadNegocio'].replace([np.nan, '', None], Unidad_a_trabajar['text'])

df_informe = agregar_informe(
    df_tercerosc, 'TercerosCargar', 'NumeroDocumento', df_informe)

df_terceros_control= df_terceros_control.merge(df_tercerosc[['NumeroDocumento']], left_on='NumeroDocumento', right_on='NumeroDocumento', how='left', indicator=True)
df_terceros_control=df_terceros_control[df_terceros_control['_merge'] == 'left_only'].drop(columns=['_merge'])

nombre_archivo = f"{output_folder}/TercerosCargar.csv"
df_tercerosc.astype(str).to_csv(nombre_archivo,
                                index=False, encoding="utf-8", quoting=1)

df_tercerosc['rank'] = df_tercerosc.groupby('NumeroDocumento')['ConceptoPago'].rank(method='dense', ascending=False)

archivos = df_tercerosc['rank'].unique()
archivos = sorted([elemento for elemento in archivos if elemento])
print(archivos)
for archivo in archivos:
    df_subset=df_filtradon[df_filtradon['rank']==archivo]

    df_subset['NombreBanco']=df_subset['CodigoBanco']

    # Generar el JSON con la función
    json_resultado = construir_json(df_tercerosc)

    # Guardar el JSON en un archivo
    with open(nombre_archivo.replace(".csv",f"_c_{archivo:.0f}.json"), "w", encoding="utf-8") as f:
        json.dump(json_resultado, f, indent=4, ensure_ascii=False)

    print(f"El archivo JSON se ha guardado como terceros_c_{archivo:.0f}.json")

    #Envio_integracion(json_resultado)

print("Exportación Terceros a Cargar completada.")

#df_tercerosne = df_terceros_control
nombre_archivo = f"{output_folder}/TercerosArmar.csv"
df_terceros_armar = df_terceros.merge(df_terceros_control, on='NumeroDocumento', how='right')
df_terceros_cuentas = buscarcuentaterceros(df_terceros_control, df_cuentas)

df_terceros_armar = df_terceros_armar.drop(columns=['UnidadNegocio']).merge(df_terceros_cuentas,
                                            on='NumeroDocumento', how='left')

df_terceros_armar.astype(str).to_csv(nombre_archivo,
                                     index=False, encoding="utf-8", quoting=1)
df_informe = agregar_informe(
    df_terceros_armar, 'TercerosArmar', 'NumeroDocumento', df_informe)

print(df_informe)

# captura hora de finalizacion
end_time = time.time()

df_informe.to_excel(f"{output_folder}\Informe_{datetime.fromtimestamp(end_time).strftime('%d%m%Y_%H_%M')}.xlsx", index=False)

print(f"fin: ", {datetime.fromtimestamp(
    end_time).strftime('%Y-%m-%d %H:%M:%S')})

# Calcular el tiempo total de ejecución
tiempo_total = end_time - start_time
print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos",
      segundos_a_segundos_minutos_y_horas(int(round(tiempo_total, 0))))

