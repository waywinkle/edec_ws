from sqlalchemy import create_engine, exists, literal
from sqlalchemy.orm import sessionmaker
from properties import get_property
import urllib
from mappings import Ecert, Product
from datetime import datetime
from xml_file_parse import get_xml_root_from_file

CON_STRING = urllib.quote_plus(get_property('properties.json', 'connection_string'))
XML_FILE = 'test_xml\data_raw_material.xml'
TEST_RECORDS = [{
    'certificate_id': 'ASDF1234',
    'update_date': datetime(year=2016, month=2, day=5),
    'xml_data': get_xml_root_from_file(XML_FILE),
    'status': 'approved',
    'departure_date': datetime(year=2016, month=2, day=5),
    'consignor_id': 'asdfee',
    'consignee_id': 'EEIRIRI'
},
{
    'certificate_id': 'ASDF2234',
    'update_date': datetime(year=2016, month=2, day=5),
    'xml_data': get_xml_root_from_file(XML_FILE),
    'status': 'approved',
    'departure_date': datetime(year=2016, month=2, day=5),
    'consignor_id': 'asdfee',
    'consignee_id': 'EEIRIRI'
}
]


def get_engine():
    return create_engine('mssql+pyodbc:///?odbc_connect=%s' % CON_STRING)


def check_cert(cert_id):
    Session = sessionmaker(bind=get_engine())
    session = Session()
    q = session.query(Ecert).filter(Ecert.certificate_id == cert_id)
    return session.query(literal(True)).filter(q.exists()).scalar()


def add_records(rows_list, table_map):
    adds = []
    for row in rows_list:
        adds.append(table_map(**row))

    Session = sessionmaker(bind=get_engine())
    session = Session()

    session.add_all(adds)
    session.commit()


def create_structure():
    engine = get_engine()
    Ecert.metadata.create_all(engine)
    Product.metadata.create_all(engine)


if __name__ == '__main__':
    # add_records(TEST_RECORDS, Ecert)
    result = check_cert('ASDF2234')
    print(result)

