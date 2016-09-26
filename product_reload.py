from sqla import get_all_cert_xml, add_records, check_product, remove_records
from xml_file_parse import get_ecert_elements
from mappings import Product


def repopulate_product():
    remove_records(Product)
    all_cert = get_all_cert_xml()
    products = {}
    add_rows = []

    for row in all_cert:
        products[row[0]] = get_ecert_elements(row[1])['lots']

    for cert, lots in products.iteritems():
        for lot in lots:
            if not check_product(cert, lot.get('lot')):
                add_rows.append(lot)

    add_records(add_rows, Product)


if __name__ == '__main__':
    repopulate_product()
