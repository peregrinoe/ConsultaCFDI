# SAT CFDI Verifier 🧾

Herramienta en **Python** para consultar el **estado de facturas electrónicas (CFDI)** directamente desde el **Web Service oficial del SAT (México)**, utilizando un archivo CSV como entrada.

Ideal para **validaciones masivas de CFDIs** de forma rápida y automatizada.

---

## 🚀 ¿Qué hace este script?

Para cada CFDI contenido en el archivo CSV, el script consulta al SAT y obtiene:

- **Estado del CFDI** (Vigente, Cancelado, No Encontrado, etc.)
- **Es Cancelable**
- **Código de Estatus**
- **Estatus de Cancelación**

Los resultados se guardan automáticamente en un **archivo CSV de salida**.

---

## 📂 Flujo de funcionamiento

1. El usuario ingresa el nombre del archivo CSV a revisar.
2. El script envía consultas paralelas al SAT usando múltiples hilos.
3. Se procesa la respuesta XML del servicio SOAP.
4. Se genera un archivo `resultado_<archivo>.csv` con los resultados.

---

## 📄 Formato del archivo CSV

El script asume que el archivo de entrada contiene, al menos, las siguientes columnas:

| Índice | Campo |
|------:|------|
| 3 | Folio Fiscal (UUID) |
| 4 | RFC Emisor |
| 5 | Total del CFDI |
| 6 | RFC Receptor |

⚠️ **Importante:**  
El orden de las columnas debe coincidir con el formato esperado en el código.  
Si tu CSV tiene otro formato, ajusta los índices dentro de la función `consultar_estado`.

### 📌 Ejemplo de CSV

```csv
col1,col2,col3,folio_fiscal,rfc_emisor,total,rfc_receptor
x,x,x,550E8400-E29B-41D4-A716-446655440000,AAA010101AAA,1234.56,BBC020202BBB
```

## ⚙️ Requisitos

Python 3.6 o superior

Paquetes:
- requests
- beautifulsoup4
- urllib3
- lxml

📦 Instalación de dependencias

```
pip install -r requirements.txt
```

## ▶️ Uso

Coloca el archivo CSV en la misma carpeta del script.

Ejecuta:

```
python consulta_cfdi.py
```

Ingresa el nombre del archivo CSV cuando se solicite.
Revisa el archivo generado:

```
resultado_<archivo>.csv
```

## 🧵 Concurrencia

El script utiliza múltiples hilos para acelerar las consultas al SAT:

```
NUM_THREADS = 10
```
Puedes ajustar este valor según tus pruebas y conexión a internet.

## ⚠️ Notas importantes

- El valor `fe` utilizado en la consulta es fijo, ya que el SAT no lo valida estrictamente.
- El script implementa reintentos automáticos ante errores temporales (HTTP 429, errores 5xx).
- El uso intensivo puede provocar bloqueos temporales del servicio del SAT.
- Esta herramienta es solo de consulta; no modifica ni cancela CFDIs.

--- 
## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## 📌 Disclaimer

Este proyecto no es oficial y no tiene afiliación con el SAT.
Úsalo bajo tu propia responsabilidad y conforme a la normatividad vigente.





