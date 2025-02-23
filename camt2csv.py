import csv
import glob
import os
import xml.etree.ElementTree as ET


def parse_camt_file(camt_file):
    tree = ET.parse(camt_file)
    root = tree.getroot()
    namespaces = {'ns': root.tag.split('}')[0].strip('{')}
    transactions = []
    
    # Assuming CAMT file structure, extract necessary data
    for entry in root.findall('.//ns:Ntry', namespaces):
        print("Found entry")
        for tx in entry.findall('.//ns:NtryDtls/ns:TxDtls', namespaces):
            print("Found transaction details")
            transaction = {
                'date': entry.find('ns:BookgDt/ns:Dt', namespaces).text.encode("utf-8") if entry.find('ns:BookgDt/ns:Dt', namespaces) is not None else 'N/A',
                'amount': tx.find('ns:Amt', namespaces).text.encode("utf-8") if tx.find('ns:Amt', namespaces) is not None else 'N/A',
                'currency': tx.find('ns:Amt', namespaces).attrib['Ccy'] if tx.find('ns:Amt', namespaces) is not None else 'N/A',
                'debtor': tx.find('ns:RltdPties/ns:Dbtr/ns:Nm', namespaces).text.encode("utf-8") if tx.find('ns:RltdPties/ns:Dbtr/ns:Nm', namespaces) is not None else 'N/A',
                'creditor': tx.find('ns:RltdPties/ns:Cdtr/ns:Nm', namespaces).text.encode("utf-8") if tx.find('ns:RltdPties/ns:Cdtr/ns:Nm', namespaces) is not None else 'N/A',
                'remittance_info': tx.find('ns:RmtInf/ns:Ustrd', namespaces).text.encode("utf-8") if tx.find('ns:RmtInf/ns:Ustrd', namespaces) is not None else 'N/A',
                'book_info': entry.find('ns:AddtlNtryInf', namespaces).text.encode("utf-8") if entry.find('ns:AddtlNtryInf', namespaces) is not None else 'N/A',
                'deb_account': 'Bank (Kontokorrent)',
                'crd_account': 'Imbalance (Kontokorrent)'
            }
            print("Transaction: {}".format(transaction))
            transactions.append(transaction)
    
    print("Parsed {} transactions".format(len(transactions)))
    return transactions

def write_csv(transactions, csv_file):
    with open(csv_file, mode='w') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'amount', 'currency', 'debtor', 'creditor', 'remittance_info','book_info','deb_account','crd_account'])
        writer.writeheader()
        for transaction in transactions:
            print("Writing transaction: {}".format(transaction))
            writer.writerow(transaction)
    print("CSV file written to {}".format(csv_file))

def camt_to_csv(camt_file, csv_file):
    transactions = parse_camt_file(camt_file)
    write_csv(transactions, csv_file)
    print("Wrote {} transactions".format(len(transactions)))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert CAMT file to CSV.')
    parser.add_argument('xml_dir', help='The source directory where CAMT files are.')
    
    args = parser.parse_args()

    directory = args.xml_dir
    files = glob.glob(os.path.join(directory, "*"))  # List all files
    
    for camt_file in files:
        camt_to_csv(camt_file, os.path.splitext(camt_file)[0] + '.csv')
    print("Conversion complete")

