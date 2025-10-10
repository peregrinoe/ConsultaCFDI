import requests
from bs4 import BeautifulSoup
import csv
import os
import concurrent.futures
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# === CONFIGURACIÓN ===
NUM_THREADS = 10  # Número de consultas simultáneas (ajustar según prueba)
FE_DUMMY = "uDu8/g=="  # El 'fe' siempre es fijo en estas consultas
ARCHIVO_CSV = input("Ingresar el nombre del archivo a revisar: ")
ARCHIVO_SALIDA = f"resultado_{os.path.splitext(os.path.basename(ARCHIVO_CSV))[0]}.csv"

# === PREPARAR SESIÓN PERSISTENTE CON REINTENTOS ===
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"]
)
adapter = HTTPAdapter(max_retries=retries, pool_connections=NUM_THREADS, pool_maxsize=NUM_THREADS)
session.mount("https://", adapter)

# === FUNCIONES ===

def construir_xml(rfc_emisor, rfc_receptor, total_cfdi, folio_fiscal):
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                     xmlns:tem="http://tempuri.org/">
      <soapenv:Header/>
      <soapenv:Body>
         <tem:Consulta>
            <tem:expresionImpresa>
               <![CDATA[?re={rfc_emisor}&rr={rfc_receptor}&tt={total_cfdi}&id={folio_fiscal}&fe={FE_DUMMY}]]>
            </tem:expresionImpresa>
         </tem:Consulta>
      </soapenv:Body>
    </soapenv:Envelope>"""

def consultar_estado(row):
    folio_fiscal = row[3].strip()
    rfc_emisor = row[4].strip().upper()
    rfc_receptor = row[6].strip().upper()
    total_cfdi = row[5].strip()

    headers = {
        'Accept': 'text/xml',
        'Content-Type': 'text/xml;charset="utf-8"',
        'SOAPAction': 'http://tempuri.org/IConsultaCFDIService/Consulta'
    }

    xml = construir_xml(rfc_emisor, rfc_receptor, total_cfdi, folio_fiscal)

    try:
        r = session.post("https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc",
                         data=xml, headers=headers, timeout=(5, 20))
        soup = BeautifulSoup(r.text, 'xml')  # Usar 'xml' para evitar errores de parseo
        estado = soup.find('a:Estado').text if soup.find('a:Estado') else "Sin respuesta"
        es_cancelable = soup.find('a:EsCancelable').text if soup.find('a:EsCancelable') else "-"
        codigo_estatus = soup.find('a:CodigoEstatus').text if soup.find('a:CodigoEstatus') else "-"
        estatus_cancelacion = soup.find('a:EstatusCancelacion').text if soup.find('a:EstatusCancelacion') else "-"
        print(f"{folio_fiscal} | {estado} | {es_cancelable} | {codigo_estatus} | {estatus_cancelacion}")
        return [folio_fiscal, estado, es_cancelable, codigo_estatus, estatus_cancelacion]
    except Exception as e:
        print(f"⚠️ Error en folio {folio_fiscal}: {e}")
        return [folio_fiscal, "Error", "-", "-", str(e)]

# === EJECUCIÓN PRINCIPAL ===

def main():
    with open(ARCHIVO_CSV, 'r', newline='') as file_in, open(ARCHIVO_SALIDA, 'w', newline='') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        writer.writerow(["Folio Fiscal", "Estado", "Es Cancelable", "Código de Estatus", "Estatus Cancelación"])

        rows = list(reader)

        # Procesar en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            resultados = list(executor.map(consultar_estado, rows))

        # Escribir todos los resultados
        for resultado in resultados:
            writer.writerow(resultado)

        print(f"\n✅ Total de resultados procesados: {len(resultados)}")
        print(f"📄 Archivo generado: {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    main()
 
