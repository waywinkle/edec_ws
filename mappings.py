from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, Sequence, types, ForeignKey
from sqlalchemy.orm import relationship
import xml.etree.ElementTree as etree

Base = declarative_base()


class XMLType(types.TypeDecorator):

    impl = types.UnicodeText
    type = etree.Element

    def get_col_spec(self):
        return 'xml'

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return etree.tostring(value)
            else:
                return None
        return process

    def process_result_value(self, value, dialect):
        if value is not None:
            value = etree.fromstring(value.encode('utf-8'))
        return value


class Ecert(Base):
    __tablename__ = 'Ecert'

    # id = Column(Integer, Sequence('ecert_id_seq') , primary_key=True)
    certificate_id = Column(String(60), primary_key=True)
    status = Column(String(15))
    departure_date = Column(DATETIME)
    update_date = Column(DATETIME)
    consignor_id = Column(String(15))
    consignee_id = Column(String(15))
    xml_data = Column(XMLType)

    # product = relationship('Product', back_populates='certificate_id')

    def __repr__(self):
        return "<Ecert(certificate_id='%s', departure_date='%s')>" % (
            self.certificate_id, self.departure_date
        )


class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    certificate_id = Column(String(60), ForeignKey('Ecert.certificate_id'))
    lot = Column(String(25))
    product_item = Column(Integer)

    # ecert = relationship('certificate_id', back_populates='product')

    def __repr__(self):
        return "<Product(lot='%s')>" % (
            self.lot
        )



