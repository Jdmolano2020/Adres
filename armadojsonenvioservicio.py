import pandas as pd
import json
import requests
import datetime


TAMANO_LOTE = 100


# Función para buscar cuentas de terceros
def buscarcuentaterceros(df_tercerosb, df_cuentas):

    df_tercerosbc = df_tercerosb[['NumeroDocumento', 'UnidadNegocio']].copy()
    df_tercerocb = df_cuentas.copy()

    df_tercerocbe = df_tercerosbc.merge(df_tercerocb,
                                        on=['NumeroDocumento',
                                            'UnidadNegocio'], how='inner')
    df_tercerocbe.drop(columns=['NombreBanco'], inplace=True)
    df_tercerocbe.rename(
        columns={'CodigoBanco': 'NombreBanco'}, inplace=True)
    df_tercerocbe = df_tercerocbe.groupby(['NumeroDocumento', 'NumeroCuenta',
                                           'NombreBanco', 'TipoCuenta',
                                           'UnidadNegocio'],
                                          as_index=False) \
        .agg({'ConceptoPago': lambda x: '-'.join(x.unique())})
    return df_tercerocbe


# Función para construir el JSON
def envio_integracion(dev=2, json_resultado={"DATA": []}):
    # URL del servicio
    if dev == 1:
        url = "https://desarrrollo-adr-axstgrwlxen2-px.integration.us-phoenix-1.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/ADR_CREARACTUA_TERCERO/1.0/data"
    if dev == 2:
        url = "https://desarrollo2-adr-axstgrwlxen2-px.integration.us-phoenix-1.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/ADR_CREARACTUA_TERCERO/1.0/data"
    # Credenciales de autenticación (Basic Auth)
    username = "INTEGRACION_ADR"
    password = "4Dr3s2024**.."

    # Asegúrate de tener la función de generación del JSON
    json_data = json.dumps(json_resultado, ensure_ascii=False)
    # Convertir a string JSON

    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Enviar la solicitud POST
    response = requests.post(url, auth=(username, password),
                             headers=headers, data=json_data)

    # Verificar respuesta del servidor
    if response.status_code == 200 or response.status_code == 201:
        return print("✅ Éxito:", response.json())  # Mostrar respuesta en JSON
    else:
        # Mostrar error en caso de fallo
        return print("❌ Error:", response.status_code, response.text)


def construir_json(df):
    resultado = {"DATA": []}

    # Agrupar por NumeroDocumento
    for num_doc, doc_group in df.groupby("NumeroDocumento"):
        documento = {
            "NumeroDocumento": num_doc,
            "Nombre": doc_group["Nombre"].iloc[0],
            "TipoDocumento": doc_group["TipoDocumento"].iloc[0],
            "Email": doc_group["Email"].iloc[0],
            "Naturaleza": doc_group["Naturaleza"].iloc[0],
            "TipoProveedor": doc_group["TipoProveedor"].iloc[0],
            "PrimerNombre": doc_group["PrimerNombre"].iloc[0],
            "SegundoNombre": doc_group["SegundoNombre"].iloc[0],
            "PrimerApellido": doc_group["PrimerApellido"].iloc[0],
            "SegundoApellido": doc_group["SegundoApellido"].iloc[0],
            "Actividad Economica": doc_group["Actividad Economica"].iloc[0],
            "TipoContribuyente": doc_group["TipoContribuyente"].iloc[0],
            "Direcciones": []
        }

        # Agrupar dentro del documento por UnidadNegocio, Direccion,
        # Departamento, Ciudad, Pais
        for _, dir_group in doc_group.groupby(["UnidadNegocio",
                                               "Direccion",
                                               "Departamento",
                                               "Ciudad",
                                               "Pais"], dropna=False):
            direccion = {
                "UnidadNegocio": dir_group["UnidadNegocio"].iloc[0],
                "Direccion": dir_group["Direccion"].iloc[0],
                "Departamento": dir_group["Departamento"].iloc[0],
                "Ciudad": dir_group["Ciudad"].iloc[0],
                "Pais": dir_group["Pais"].iloc[0],
                "CuentaBancaria": []
            }

            # Agregar cuentas bancarias si existen datos válidos
            cuentas = dir_group[["NumeroCuenta", "NombreBanco",
                                 "TipoCuenta",
                                 "ConceptoPago"]].dropna(
                how='all').to_dict(orient="records")
            if cuentas:
                direccion["CuentaBancaria"] = cuentas

            documento["Direcciones"].append(direccion)

        resultado["DATA"].append(documento)

    return resultado


def enviar_lote(envio=1, lista=None):
    """Envía un lote de registros no enviados al servicio."""
    global df_tercerosma

    if "Enviado" not in df_tercerosma.columns:
        df_tercerosma["Enviado"] = False

    if envio == 2:
        df_lote = df_tercerosma[df_tercerosma['NumeroDocumento'].isin(lista)]
    else:
        # Filtrar registros no enviados
        df_lote = df_tercerosma[df_tercerosma['Enviado']
                                == False].head(TAMANO_LOTE)

    df_cuentase = buscarcuentaterceros(df_lote, df_cuentas)

    df_terceroscb = df_lote.merge(df_cuentase,
                                  on=['NumeroDocumento',
                                      'UnidadNegocio'], how='left')

    if df_lote.empty:
        print("✅ No hay registros pendientes de envío.")
        return

    # Convertir a JSON en el formato esperado
    data_json = construir_json(df=df_terceroscb)

    try:
        nombre_archivo = f"datos_terceros_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(data_json, f, indent=4, ensure_ascii=False)
        # Enviar al servicio
        # envio_integracion(dev=2, json_resultado=data_json)
        # Marcar registros como enviados
        df_tercerosma.loc[df_lote.index, 'Enviado'] = True
        revisionenvio = df_tercerosma['Enviado'].value_counts()
        print(revisionenvio)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error en la conexión: {e}")


if __name__ == "__main__":
    columnas_terceros = ['Nombre', 'TipoDocumento', 'NumeroDocumento',
                         'Email', 'Naturaleza', 'TipoProveedor',
                         'PrimerNombre', 'SegundoNombre',
                         'PrimerApellido', 'SegundoApellido',
                         'Actividad Economica', 'TipoContribuyente',
                         'UnidadNegocio', 'Direccion',
                         'Departamento', 'Ciudad', 'Pais']

    df_tercerosma = df_terceros[columnas_terceros].copy()

    lista_numeros = ['830006777', '830037248']
    enviar_lote(envio=1, lista=lista_numeros)
