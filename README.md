SAT CFDI Verifi#er

Herramienta en Python para consultar el estado de facturas electrónicas (CFDI) directamente desde el Web Service oficial del SAT (México), utilizando un archivo CSV como entrada.

Ideal para validaciones masivas de CFDIs de forma rápida y automatizada.

🚀 ¿Qué hace este script?

Para cada CFDI contenido en el archivo CSV, el script consulta al SAT y obtiene:

Estado del CFDI (Vigente, Cancelado, No Encontrado, etc.)

Es Cancelable

Código de Estatus

Estatus de Cancelación

Los resultados se guardan automáticamente en un archivo CSV de salida.

---

📂 Flujo de funcionamiento

El usuario ingresa el nombre del archivo CSV a revisar.

El script envía consultas paralelas al SAT usando múltiples hilos.

Se procesa la respuesta XML del servicio SOAP.

Se genera un archivo resultado_<nombre_archivo>.csv con los resultados.

---

El script asume que el archivo de entrada contiene, al menos, las siguientes columnas (por índice):

Índice	Campo
3	Folio Fiscal (UUID)
4	RFC Emisor
5	Total del CFDI
6	RFC Receptor

⚠️ Importante:
El orden de las columnas debe coincidir con el formato esperado en el código.
Si tu CSV tiene otro formato, ajusta los índices dentro de la función consultar_estado.

---

⚠️ Notas importantes

El valor fe utilizado en la consulta es fijo, ya que el SAT no lo valida estrictamente en este servicio.

El script implementa reintentos automáticos ante errores temporales (HTTP 429, 5xx).

El uso intensivo puede provocar bloqueos temporales del servicio del SAT.

Esta herramienta es solo para consulta, no modifica ni cancela CFDIs.

---

📌 Disclaimer

Este proyecto no es oficial y no tiene afiliación con el SAT.
Úsalo bajo tu propia responsabilidad y conforme a la normatividad vigente.

## ⚙️ Requisitos

- Python 3.6 o superior
- Paquetes:
  - `requests`
  - `beautifulsoup4`
  - `urllib3`
  - `lxml`

Instalación rápida de dependencias:

```bash
pip install -r requirements.txt
 - `requests`


