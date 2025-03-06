import csv
import json

# Read the CSV file
csvfile = 'URA_21022025_TER_30.csv'
data = []
with open(csvfile, mode='r', encoding='latin-1') as file:
    csvreader = csv.DictReader(file, delimiter=';')
    for row in csvreader:
        # Crear el vector CuentaBancaria solo si tiene valores
        if row["NumeroCuenta"] or row["NombreBanco"] or row["TipoCuenta"] or row["ConceptoPago"]:
            cuenta_bancaria = [{
                "NumeroCuenta": row["NumeroCuenta"],
                "NombreBanco": row["NombreBanco"],
                "TipoCuenta": row["TipoCuenta"],
                "ConceptoPago": row["ConceptoPago"]
            }]
        else:
            cuenta_bancaria = None

        # Crear el diccionario dentro de la lista Direcciones
        direcciones = {
            "UnidadNegocio": row["UnidadNegocio"],
            "Direccion": row["Direccion"],
            "Departamento": row["Departamento"],
            "Ciudad": row["Ciudad"],
            "Pais": row["Pais"]
        }

        # Agregar CuentaBancaria si no es None
        if cuenta_bancaria:
            direcciones["CuentaBancaria"] = cuenta_bancaria

        # Agregar la lista al diccionario de la fila
        row["Direcciones"] = [direcciones]

        # Eliminar las variables originales del diccionario de la fila
        del row["UnidadNegocio"]
        del row["Direccion"]
        del row["Departamento"]
        del row["Ciudad"]
        del row["Pais"]
        del row["NumeroCuenta"]
        del row["NombreBanco"]
        del row["TipoCuenta"]
        del row["ConceptoPago"]
        data.append(row)

# Convert to JSON
jsondata = json.dumps(data, indent=4, ensure_ascii=False)

# Save JSON to a file
jsonfile = 'URA_21022025_TER_30.json'
with open(jsonfile, 'w', encoding='utf-8') as file:
    file.write(jsondata)
print(
    f"CSV data has been successfully converted to JSON and saved to {jsonfile}.")
