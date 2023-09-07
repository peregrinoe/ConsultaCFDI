import requests
from bs4 import BeautifulSoup
from xml.dom import minidom
import csv

archivos_csv = [input("Ingresar el nombre del archivo a revisar: ")]  # Lista de nombres de archivos CSV

# Nombre del archivo de salida CSV
archivo_salida_csv = "resultados.csv"

# Encabezados del archivo CSV
encabezados_csv = ["Folio Fiscal", "Estado", "Es Cancelable", "Código de Estatus"]

with open(archivo_salida_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(encabezados_csv)  # Escribir los encabezados en el archivo CSV

    for archivo in archivos_csv:
        with open(archivo, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                folio_fiscal = row[3]
                rfc_emisor = row[4]
                rfc_receptor = row[6]
                total_cfdi = row[5]

                url = "https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc"
                headers = {
                    'Accept': 'text/xml',
                    'Content-Type': 'text/xml;charset="utf-8"',
                    'SOAPAction': 'http://tempuri.org/IConsultaCFDIService/Consulta'}
                xml = f"""<soapenv:Envelope
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:tem="http://tempuri.org/">
                        <soapenv:Header/>
                        <soapenv:Body>
                                <tem:Consulta>
                                        <tem:expresionImpresa>
                                                <![CDATA[?re={rfc_emisor.title()}&rr={rfc_receptor.title()}&tt={total_cfdi.title()}&id={folio_fiscal.title()}&fe=uDu8/g==]]>
                                        </tem:expresionImpresa>
                                </tem:Consulta>
                        </soapenv:Body>
                </soapenv:Envelope>"""

                r = requests.post(url, data=xml, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')

                # Obtener los valores de los resultados
                estado = soup.find_all('a:estado')[0].get_text()
                es_cancelable = soup.find_all('a:escancelable')[0].get_text()
                codigo_estatus = soup.find_all('a:codigoestatus')[0].get_text()

                # Escribir los resultados en la terminal
                print(folio_fiscal, " |", estado, " |", es_cancelable, " |", codigo_estatus)

                # Escribir los resultados en el archivo CSV
                writer.writerow([folio_fiscal, estado, es_cancelable, codigo_estatus])

            
