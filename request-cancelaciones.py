import requests
from bs4 import BeautifulSoup
from xml.dom import minidom

# archivo=input("Ingresar nombre del archivo: ")
# doc = minidom.parse("/mnt/c/Users/EduardoMitzaelRodríg/Downloads/"+archivo)

folio_fiscal = input("UUID: ")
rfc_emisor = input("RFC Emisor: ")
rfc_receptor = input("RFC Receptor: ")
total_cfdi = input("Total CFDI: ")
# archivo=input("Ingresar nombre del archivo: ")

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

print(folio_fiscal," |", soup.find_all('a:estado')[0].get_text()," |", soup.find_all('a:escancelable')[0].get_text()," |", soup.find_all('a:codigoestatus')[0].get_text())