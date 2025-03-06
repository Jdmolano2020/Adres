import csv
import json

# Leer el archivo CSV
csvfile = 'calculo_impuestos.csv'
data = []

with open(csvfile, mode='r', encoding='utf-8-sig') as file:
    csvreader = csv.DictReader(file, delimiter=';')
    for row in csvreader:
        data.append(row)

# Convertir a JSON
jsondata = json.dumps(data, indent=4, ensure_ascii=False)

# Guardar JSON en un archivo
jsonfile = 'calculo_impuestos.json'
with open(jsonfile, 'w', encoding='utf-8') as file:
    file.write(jsondata)

print(
    f"Los datos del CSV se han convertido exitosamente a JSON y se han guardado en {jsonfile}.")
