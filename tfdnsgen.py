#!/usr/bin/env python3

import argparse
import csv
import json

parser = argparse.ArgumentParser(description='Terraform Code Generator')
parser.add_argument('--rg', action="store", dest='rg', required=True, help='resource group name')
parser.add_argument('--zone', action="store", dest='zone', required=True, help='name of the DNS zone')
parser.add_argument('--tffile', action="store", dest='tffile', required=True, help='output file to write the generated code')
parser.add_argument('--csvfile', action="store", dest='csvfile', required=True, help='input file to read from')

args = parser.parse_args()

def csv_file_to_tf_code(file, zone, rg):
    json_string = csv_file_to_json(file)
    records = json.loads(json_string)
    tf_code = ""

    for record in records:
        if record["Type"] == "CNAME":
            tf_code += parse_cname(record, zone, rg) + '\n'
        elif record["Type"] == "A":
            tf_code += parse_arecord(record, zone, rg) + '\n'

    return tf_code

def csv_file_to_json(file, pretty = False):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])

    return json.dumps(csv_rows, sort_keys=False, indent=4, separators=(',', ': ')) if pretty else json.dumps(csv_rows)

def write_json_file(data, json_file, pretty = True):
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')) if pretty else json.dumps(data))

def write_file(data, file):
    with open(file, "w") as f:
        f.write(data)

def generate_terraform_name(zone, name):
    return name.replace(".", "_").replace("-", "_") + "_" + zone.replace(".", "_")

def parse_cname(record, zone, rg):
    r = 'resource "azurerm_dns_cname_record" "%s" {\n' % generate_terraform_name(zone, record['Name'])
    r += ' zone_name = "%s"\n' % zone
    r += ' resource_group_name = "%s"\n' % rg
    r += ' ttl = "%s"\n' % record['TTL']
    r += ' record = "%s"\n' % record['Value']
    r += ' provider = azurerm.prod\n'
    r += '}\n'

    return r

def parse_arecord(record, zone, rg):
    r = 'resource "azurerm_dns_a_record" "%s" {\n' % generate_terraform_name(zone, record['Name'])
    r += ' zone_name = "%s"\n' % zone
    r += ' resource_group_name = "%s"\n' % rg
    r += ' ttl = "%s"\n' % record['TTL']
    r += ' records = ["%s"]\n' % record['Value']
    r += ' provider = azurerm.prod\n'
    r += '}\n'

    return r

def main():
    csv_file = args.csvfile
    tf_file = args.tffile
    zone = args.zone
    rg = args.rg

    tf_code = csv_file_to_tf_code(csv_file, zone, rg)
    print(csv_file_to_json(csv_file, True))
    print(tf_code)
    write_file(tf_code, tf_file)

if __name__ == "__main__":
    main()
