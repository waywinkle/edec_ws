try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from properties import get_file_location
from datetime import datetime

FILE_NAME = 'test_xml\\data_export.xml'
ECERT_NAMESPACE = {'n': 'http://sancrt.mpi.govt.nz/ecert/2013/ed-submission-schema.xsd'}


def get_xml_root_from_file(file_name):
    with open(get_file_location(file_name)) as xml_file:
        tree = ET.parse(xml_file)
        return tree.getroot()


def get_xml_root_from_string(xml_data):
    return ET.fromstring(xml_data)


def get_ecert_elements(root):
    ecert_header = dict()
    cert_id = root.find('./n:Identifiers/n:CertificateID', ECERT_NAMESPACE).text
    ecert_header['certificate_id'] = cert_id
    ecert_header['status'] = root.find('./n:Status', ECERT_NAMESPACE).text
    update_date = root.find('./n:LastUpdatedDate', ECERT_NAMESPACE).text
    ecert_header['update_date'] = datetime(year=int(update_date[0:4]),
                                           month=int(update_date[5:7]),
                                           day=int(update_date[8:10]))
    departure_date = root.find('./n:DepartureDate', ECERT_NAMESPACE).text
    ecert_header['departure_date'] = datetime(year=int(departure_date[0:4]),
                                              month=int(departure_date[5:7]),
                                              day=int(departure_date[8:10]))
    ecert_header['consignor_id'] = root.find('./n:Parties/n:ConsignorID', ECERT_NAMESPACE).text
    ecert_header['consignee_id'] = root.find('./n:Parties/n:ConsigneeID', ECERT_NAMESPACE).text

    lots = list()
    for product in root.findall('./n:Products/n:Product', ECERT_NAMESPACE):
        lot = dict()
        lot['certificate_id'] = cert_id
        if product.find('./n:ProductionBatch', ECERT_NAMESPACE) is not None:
            lot['lot'] = product.find('./n:ProductionBatch',
                                      ECERT_NAMESPACE).text
        elif product.find('./n:Packaging/n:Package/n:ShippingMarks/n:Name', ECERT_NAMESPACE) is not None:
            lot['lot'] = product.find('./n:Packaging/n:Package/n:ShippingMarks/n:Name',
                                      ECERT_NAMESPACE).text

        lots.append(lot)

    return {'header': ecert_header, 'lots': lots}


if __name__ == '__main__':
    result = get_ecert_elements(get_xml_root_from_file(FILE_NAME))

    for i, j in result.iteritems():
        print(i, j)
