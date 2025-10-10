# SAT CFDI Verifier 🇲🇽

Este script en Python permite consultar el estado de **facturas electrónicas (CFDIs)** directamente al web service del SAT (Servicio de Administración Tributaria de México) a partir de un archivo CSV.

## 🔍 ¿Qué hace?

Para cada CFDI en el archivo de entrada, el script consulta:

- **Estado** (Vigente, Cancelado, No Encontrado, etc.)
- **Es Cancelable**
- **Código de Estatus**
- **Estatus de Cancelación**

Todo se guarda en un archivo de salida con los resultados.

---

## ⚙️ Requisitos

- Python 3.6 o superior
- Paquetes:
  - `requests`
  - `beautifulsoup4`
  - `urllib3`

Instalación rápida de dependencias:

```bash
pip install -r requirements.txt
