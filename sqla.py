from sqlalchemy import create_engine, literal, select
from sqlalchemy.orm import sessionmaker
from properties import get_property
from urllib import quote_plus
from mappings import Ecert, Product
from datetime import datetime
from xml_file_parse import get_xml_root_from_file
from sqlalchemy.dialects import mssql

CON_STRING = quote_plus(get_property('properties.json', 'connection_string'))
XML_FILE = 'test_xml\data_raw_material.xml'
TEST_RECORDS = [{
    'certificate_id': 'NZL2015/S3002/10027T',
    'lot': 'asdfasdf'
}
]


def get_engine():
    return create_engine('mssql+pyodbc:///?odbc_connect=%s' % CON_STRING)


def check_cert(cert_id):
    Session = sessionmaker(bind=get_engine())
    session = Session()
    q = session.query(Ecert).filter(Ecert.certificate_id == cert_id)
    if session.query(literal(True)).filter(q.exists()).scalar():
        return True
    else:
        return False


def check_product(cert_id, lot):
    Session = sessionmaker(bind=get_engine())
    session = Session()
    q = session.query(Product).filter(Product.certificate_id == cert_id, Product.lot == lot)
    if session.query(literal(True)).filter(q.exists()).scalar():
        return True
    else:
        return False


def get_all_cert_xml():
    Session = sessionmaker(bind=get_engine())
    session = Session()
    s = select([Ecert.certificate_id, Ecert.xml_data])

    return session.execute(s)


def remove_records(table):
    Session = sessionmaker(bind=get_engine())
    session = Session()
    session.query(table).delete()
    session.commit()


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
    add_records(TEST_RECORDS, Product)
    result = check_cert('ASDF2234')
    print(result)

