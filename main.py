from datetime import datetime, timedelta
import time
from properties import get_all_properties
from ecert import call_ecert
from sqla import check_cert, add_records
from mappings import Ecert, Product
import logging

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


def retrieve_range(date_range):
    from_date, to_date = date_range

    log_file = 'logs\\log_' + time.strftime("%Y%m%d") + '.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')
    log = logging.getLogger('ex')

    while from_date <= to_date:
        extract_range = {'first': from_date, 'last': from_date + timedelta(days=1)}
        try:
            retrieve_ecerts(extract_range, PROPERTIES)
            logging.info('Processed dates %s to %s' % (extract_range['first'], extract_range['last']))
        except:
            log.exception('Error processing dates %s to %s' % (extract_range['first'], extract_range['last']))

        from_date = from_date + timedelta(days=2)


if __name__ == "__main__":
    # result = retrieve_ecerts({'first': datetime(2016, 8, 06), 'last': datetime(2016, 8, 31)}, PROPERTIES)
    result = retrieve_range((datetime(2015, 1, 1), datetime(2015, 12, 31)))
