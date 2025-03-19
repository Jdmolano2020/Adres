Objetivo:

Buscar si un tercero con un concepto de pago existe en alguno de los ambientes de prueba (dev1, dev2); si no existe actualizarlo o crearlo.



Leer Archivos Replicas de información descargadas de los ambientes
	• ADR_RP (Oracle), Archivos Descargada (DINAMICS), OCI_TERCEROS (Construcción a 31 de enero-"alterno")
Leer Archivo con los números de identificación y concepto de los terceros a Buscar
	1. Encontrar aquellos terceros que existen en la base de Oracle creados (numerodocumento ->esta) 
	2. Si esta verificar si el concepto a buscar se encuentran 
	3. Encontrar los terceros que existe y que en el concepto a buscar no se encuentra
		a. Con los terceros existentes que no contienen el concepto es necesario Consultar las cuentas 
		b. Construir la data con las reglas de estructura establecida para la carga de información
			i. La dirección a priorizar es la del ambiente 
			ii. Los demás campos los trae de dynamics.
			iii. La actualización de tercero y concepto para el ambiente es singular
		c. Construir Archivo de salida (Json) y ejecutarlo en el servicio
	4. Los terceros inexistentes en el ambiente será necesario cruzar con la data de dynamis para cargar toda la información
		a. Carga la información de cuentas con el concepto a buscar
		b. Construir Archivos de salida (Json) y ejecutarlo en el servicio
		c. Si tiene 2 concepto la creación y la actualización de tercero y concepto para el ambiente es singular
		d. Construir Archivo de salida (Json) y ejecutarlo en el servicio
	5. Los terceros inexistentes en el ambiente y en el historial de información (dymaniscs) son Aquellos a Armar lo que implica una intervención manual
	
	

![image](https://github.com/user-attachments/assets/c16e81d5-56ae-4bb8-a663-304267f4a83f)
