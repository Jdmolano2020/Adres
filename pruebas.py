import pandas as pd
import json
import requests

# Función para construir el JSON


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

        # Agrupar dentro del documento por UnidadNegocio, Direccion, Departamento, Ciudad, Pais
        for _, dir_group in doc_group.groupby(["UnidadNegocio", "Direccion", "Departamento", "Ciudad", "Pais"], dropna=False):
            direccion = {
                "UnidadNegocio": dir_group["UnidadNegocio"].iloc[0],
                "Direccion": dir_group["Direccion"].iloc[0],
                "Departamento": dir_group["Departamento"].iloc[0],
                "Ciudad": dir_group["Ciudad"].iloc[0],
                "Pais": dir_group["Pais"].iloc[0],
                "CuentaBancaria": []
            }

            # Agregar cuentas bancarias si existen datos válidos
            cuentas = dir_group[["NumeroCuenta", "NombreBanco", "TipoCuenta", "ConceptoPago"]].dropna(
                how='all').to_dict(orient="records")
            if cuentas:
                direccion["CuentaBancaria"] = cuentas

            documento["Direcciones"].append(direccion)

        resultado["DATA"].append(documento)

    return resultado


# Generar el JSON con la función

columnas_terceros = ['Nombre', 'TipoDocumento', 'NumeroDocumento',
                     'Email', 'Naturaleza', 'TipoProveedor',
                     'PrimerNombre', 'SegundoNombre',
                     'PrimerApellido', 'SegundoApellido',
                     'Actividad Economica', 'TipoContribuyente',
                     'UnidadNegocio', 'Direccion',
                     'Departamento', 'Ciudad', 'Pais']
df_tercerosmae = df_duplicados[columnas_terceros].copy()

df_tercerosmaecb = df_tercerosmae.merge(df_cuentas,
                                        on=['NumeroDocumento',
                                            'UnidadNegocio'], how='left')
df_tercerosmaecb.drop(columns=['NombreBanco'], inplace=True)
df_tercerosmaecb.rename(columns={'CodigoBanco': 'NombreBanco'}, inplace=True)


# Generar el JSON con la función
json_resultado = construir_json(df_tercerosmaecb)

# Guardar en un archivo
with open("datos_terceros.json", "w", encoding="utf-8") as f:
    json.dump(json_resultado, f, indent=4, ensure_ascii=False)

def Envio_integracion(dev=2, json_resultado={"DATA": []}):
    # URL del servicio
    url = "https://desarrrollo-adr-axstgrwlxen2-px.integration.us-phoenix-1.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/ADR_CREARACTUA_TERCERO/1.0/data"

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

