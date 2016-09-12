from suds.client import Client
from properties import get_all_properties, get_file_location
import base64
from xml_file_parse import get_ecert_elements, get_xml_root_from_string
from datetime import datetime
from calendar import monthrange
import pprint

TEST_FILE = get_file_location('data_export.xml')
PROPERTIES = get_all_properties('properties.json')


def connect(wsdl, username, password):
    return Client(wsdl, username=username, password=password)


def month_range_from_date(month_datetime):
    month_range = monthrange(month_datetime.year, month_datetime.month)
    return {'first': datetime(month_datetime.year, month_datetime.month, 1),
            'last': datetime(month_datetime.year, month_datetime.month, month_range[1])}


def call_ecert(wsdl, username, password, date_range):
    client = Client(wsdl, username=username, password=password)
    end = False
    page = 0
    certs = []

    while not end:
        cert_for_day = client.service.find_eligibility_documents_by_update_date(page=page,
                                                                                from_date=date_range['first'],
                                                                                to_date=date_range['last'])

        for item in cert_for_day:
            for cert in item[1]:
                if cert == 'END':
                    end = True
                else:
                    cert_dict = dict()
                    cert_dict['certificate_id'] = cert
                    xml_root = get_xml_root_from_string(get_cert_details(client, cert))
                    cert_dict.update(get_ecert_elements(xml_root))
                    cert_dict['header']['xml_data'] = xml_root
                    certs.append(cert_dict)

        page += 1

    return certs


def get_cert_details(client, cert_id):
    encoded = client.service.get_eligibility_document_xml(certificate_id=cert_id)
    xml_data = base64.b64decode(encoded)
    return xml_data


if __name__ == '__main__':
    result = call_ecert(PROPERTIES['wsdl'],
                        PROPERTIES['username'],
                        PROPERTIES['password'],
                        {'first': datetime(2016, 8, 01), 'last': datetime(2016, 8, 02)})
    # result = get_cert_details(connect(PROPERTIES['wsdl'],
    #                                   PROPERTIES['username'],
    #                                   PROPERTIES['password']),
    #                                   'NZL2016/540/140162T')
    # result = range_from_date(datetime(2016, 8, 01))
    # print result
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)
