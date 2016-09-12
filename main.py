from datetime import datetime
from properties import get_all_properties
from ecert import call_ecert
from sqla import check_cert, add_records
from mappings import Ecert, Product

PROPERTIES = get_all_properties('properties.json')


def retrieve_ecerts(date_range, properties):
    ecerts = call_ecert(properties['wsdl'],
                        properties['username'],
                        properties['password'],
                        date_range
                        )
    ecert_add = []
    lot_add = []

    for cert in ecerts:
        if not check_cert(cert['certificate_id']):
            ecert_add.append(cert['header'])
            lot_add = lot_add + cert['lots']

    add_records(ecert_add, Ecert)
    add_records(lot_add, Product)

    return None


if __name__ == "__main__":
    result = retrieve_ecerts({'first': datetime(2016, 8, 06), 'last': datetime(2016, 8, 31)}, PROPERTIES)
