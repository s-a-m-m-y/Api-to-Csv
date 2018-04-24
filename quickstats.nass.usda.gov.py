import time, thread
import csv
import sys
import urllib, json

def parse_csv( input_field_name, input_commodity_file, output_csv_file ):
    with open( input_commodity_file ) as geoIds_file:
        with open( output_csv_file, 'wb' ) as out_csv_file:
            reader = csv.DictReader(geoIds_file)
            writer = None
            for row in reader:
                this_result = row.copy()
                row['_bad_request'] = 'success'
                commodity_array = query_api( row[input_field_name] )
                if commodity_array is not None:
                    for commodity_row in commodity_array:
                        this_result = row.copy()
                        this_result.update(commodity_row)
                        if writer is None:
                              writer = csv.DictWriter(out_csv_file, fieldnames=this_result.keys())
                              writer.writeheader()
                        writer.writerow(this_result)
                else:
                    row['_bad_request'] = 'bad request'
                    if writer is None:
                        writer = csv.DictWriter(out_csv_file, fieldnames=row.keys())
                        writer.writeheader()
                    writer.writerow(this_result)

def parse_api_results ( data ):
    return data['data']

def query_api( commodity_desc ):
    key = 'use your request nass api key here' # NASS API Key
    year = '2012'
    domain_desc = 'TOTAL'
    source_desc = 'CENSUS'
    unit_desc ='$'
    url = 'https://quickstats.nass.usda.gov/api/api_GET/?' + \
            'key=' + key + \
            '&year__GE=' + year + \
            '&domain_desc='+ domain_desc + \
            '&source_desc=' + source_desc + \
            '&unit_desc=' + unit_desc + \
            '&commodity_desc=' + commodity_desc
    print url
    try:
        response = urllib.urlopen( url )
        data = json.loads( response.read() )
        commodity_array = parse_api_results( data )
        return commodity_array
    except:
        return None

if __name__ == "__main__":
    input_field_name = sys.argv[1]
    input_commodity_file = sys.argv[2]
    output_csv_file = sys.argv[3]

    parse_csv( input_field_name, input_commodity_file, output_csv_file )
