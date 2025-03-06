import pandas as pd
import matplotlib.pyplot as plt
import re
from unidecode import unidecode

# Compilar expresiones regulares una vez
non_alpha_numeric_re = re.compile(r'[^a-zA-Z0-9ñÑ\s]')
digits_re = re.compile(r'\d+')
split_ñ_re = re.compile(r'([ñÑ])')
double_spaces_re = re.compile(r'\s+')


# Función para quitar tildes y preservar ñ
def quitar_tildes_y_preservar_n(texto):
    parts = split_ñ_re.split(texto)
    texto_sin_tildes = ''.join(
        [(unidecode(x)
          if x not in 'ñÑ'
          else x) for x in parts])
    return texto_sin_tildes


# Función para eliminar caracteres especiales
def eliminar_especiales(cadena):
    return non_alpha_numeric_re.sub('', cadena)


# Función para eliminar números
def eliminar_numeros(cadena):
    return digits_re.sub('', cadena)

# Función para eliminar espacios dobles


def eliminar_espacios_dobles(texto):
    return double_spaces_re.sub(' ', texto)


def normalizar_cadena(cadena):
    if cadena is None:
        cadena = ''
    cadena = quitar_tildes_y_preservar_n(cadena)
    cadena = eliminar_especiales(cadena)
    cadena = eliminar_espacios_dobles(cadena)
    return cadena.strip()

# Función para normalizar el texto en un DataFrame


def normalize_text(df, columns):

    for column in columns:
        df[column] = df[column].astype(str)
        # Convertir a mayúsculas
        df[column] = df[column].str.upper()
        # Aplicar normalización
        df[column] = df[column].apply(normalizar_cadena)
    return df


# Lista de palabras que pueden formar parte de un segundo nombre compuesto
preposiciones = {"de", "del", "la", "los", "las", "san", "santa"}


def organizar_nombres(nombre_completo):
    if not isinstance(nombre_completo, str):
        return pd.Series(["", "", "", "", ""])
    nombre_completo = double_spaces_re.sub(' ', nombre_completo)
    partes = nombre_completo.split()

    if len(partes) < 2:
        return pd.Series([partes[0], "", "", "", ""]) if partes else pd.Series(["", "", "", "", ""])

    # Asignación inicial de nombres y apellidos
    primer_nombre = partes[0]
    segundo_nombre = ""
    primer_apellido = ""
    segundo_apellido = ""
    nnombre_completo = ""
    # Buscar el primer apellido (penúltima palabra)
    primer_apellido_index = -2 if len(partes) > 3 else -1
    primer_apellido = partes[primer_apellido_index]

    # Palabras entre el primer y último nombre
    posible_segundo_nombre = partes[1:primer_apellido_index]
    # Unir palabras intermedias
    segundo_nombre = " ".join(posible_segundo_nombre)

    # Validar si hay un segundo apellido
    if len(partes) > 3:
        segundo_apellido = partes[-1]

    partes = [primer_nombre, segundo_nombre,
              primer_apellido, segundo_apellido]

    # Unir las partes no vacías en una cadena completa
    nnombre_completo = ' '.join(filter(None, partes))

    return pd.Series([primer_nombre, segundo_nombre,
                      primer_apellido, segundo_apellido,
                      nnombre_completo])

# Función para validar y generar la glosa


def generar_glosas(row):
    glosas = []

    if row['TIPO DE DOCUMENTO'] not in ['CEDULA DE CIUDADANIA', 'N.I.T.',
                                        'CEDULA EXTRANJERIA',
                                        'PERMISO POR PROTECCI¾N TEMPORAL',
                                        "PASAPORTE", "TARJETA IDENTIDAD O NIP",
                                        "PERMISO ESPECIAL",
                                        "REGISTRO CIVIL DE NACIMIENTO", "NUIP",
                                        "CARNU DIPLOMßTICO",
                                        "TARJETA DE EXTRANJERIA"]:
        glosas.append("Tipo de documento no válido")

    nombre = row.get('Nombre', '')
    nombre_completo = row.get('Supplier Name*', '')
    if pd.isna(nombre) or nombre.strip() == '' or pd.isna(nombre_completo) or nombre_completo.strip() == '':
        glosas.append("Nombre vacío")

    # Asegurarse de que las claves existen y limpiar los valores
    tipo_documento = str(row.get('TIPO DE DOCUMENTO', '')).strip()
    apellido = row.get('Apellido', '')
    # apellido = str(row.get('Apellido', '')).strip()

    # Condición corregida
    if tipo_documento != "N.I.T." and (pd.isna(apellido) or apellido.strip() == ''):
        # Depuración: Imprimir valores para identificar el problema
        # print(f"TIPO DE DOCUMENTO: '{tipo_documento}', Apellido: '{apellido}'")
        glosas.append("Apellido no válido")

    if row['Supplier Number'] == '':
        glosas.append("Numero Documento vacío")
    # Unir glosas con ';' y evitar valores vacíos
    return "; ".join(glosas) if glosas else None


# Cargar el archivo Excel
file_path = '1.ADR_SupplierImportTemplate_ADR.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')
df['id_unico'] = pd.util.hash_pandas_object(df).astype(str)
# Mostrar las primeras filas del dataframe
print(df.head())
file_path = '2.ADR_SupplierAddressImportTemplate_ADR.xlsx'
df2 = pd.read_excel(file_path, engine='openpyxl')
print(df2.head())
df_merged = df.merge(df2[['Supplier Number', 'TIPO DE DOCUMENTO']],
                     on='Supplier Number', how='left')
df_merged = df_merged.drop_duplicates()
df_duplicados = df_merged[df_merged.duplicated(
    subset=['id_unico'], keep=False)]

df_nit = df_merged[df_merged['TIPO DE DOCUMENTO'] == "N.I.T."].copy()

df_sin_nit = df_merged[df_merged['TIPO DE DOCUMENTO'] != "N.I.T."].copy()

df_sin_nit[['Primer_Nombre', 'Segundo_Nombre',
            'Primer_Apellido', 'Segundo_Apellido',
            'nombre_completo']
           ] = df_sin_nit['Supplier Name*'].apply(organizar_nombres)

df_sin_nit['Supplier Name*'] = df_sin_nit['nombre_completo']
df_sin_nit['Nombre'] = df_sin_nit['Primer_Nombre']
df_sin_nit['Segundo Nombre'] = df_sin_nit['Segundo_Nombre']
df_sin_nit['Apellido'] = df_sin_nit['Primer_Apellido']
df_sin_nit['Segundo Apellido'] = df_sin_nit['Segundo_Apellido']


# Eliminamos las columnas extra
df_sin_nit.drop(columns=['Primer_Nombre', 'Segundo_Nombre',
                         'Primer_Apellido', 'Segundo_Apellido',
                         'nombre_completo'],
                inplace=True)

# Si quieres que df se actualice con los cambios
# df = df_actualizado.copy()

# supplier_id = "900798865"

# df_filtered = df[df['Supplier Number'] == supplier_id]
# df2_filtered = df2[df2['Supplier Number'] == supplier_id]
# column_names = ["Supplier Name*", "Nombre", "Segundo Nombre", "Apellido",
#                 "Segundo Apellido"]
# dfcorr = normalize_text(df, column_names)
# Encontrar las diferencias entre los dos DataFrames
# diferencias = pd.concat([df, dfcorr]).drop_duplicates(keep=False)

# Obtener un resumen estadístico
# summary = df.describe(include='all')
# print(summary)
# suppliers = df[df['Supplier Type'] == 'Supplier']
# print(suppliers)
# payment_methods = df['Payment Method'].value_counts()
# print(payment_methods)

df_actualizado = pd.concat([df_sin_nit, df_nit], ignore_index=True)
# Aplicar la función al DataFrame
df_actualizado['Nombre'] = df_actualizado['Nombre'].apply(
    str)
df_actualizado['Nombre'] = df_actualizado['Nombre'].str.strip()
df_actualizado['TIPO DE DOCUMENTO'] = df_actualizado['TIPO DE DOCUMENTO'].apply(
    str)
df_actualizado['TIPO DE DOCUMENTO'] = df_actualizado['TIPO DE DOCUMENTO'].str.strip()
df_actualizado['Glosas'] = df_actualizado.apply(generar_glosas, axis=1)
df_filtradoglosa = df_actualizado[df_actualizado['Glosas'].notna() & (
    df_actualizado['Glosas'].str.strip() != "")]
df_filtradoglosa.to_csv("archivo.csv", sep=";", index=False)

df_filtradosglosa = df_actualizado[df_actualizado['Glosas'].isna()]
df_filtradosfinal = df_filtradosglosa.drop_duplicates(
    subset=['Supplier Number'], keep='first')
df_filtradosfinal.to_csv("tercerosfinal.csv", sep=";", index=False)
# df_actualizado['Glosas'].value_counts()
#  Filtrar los registros donde la columna 'Glosas' contiene "Apellido no válido"
# df_filtrado = df_actualizado[df_actualizado['Glosas'].str.contains(
#     "Apellido no válido", na=False)]

# Mostrar resultados
# print(df_actualizado)
