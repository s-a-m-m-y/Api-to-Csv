import time, thread
import csv
import sys
import urllib, json

def parse_csv( field_name, geometry_type, input_geoIds_file, output_csv_file ):
    with open( input_geoIds_file ) as geoIds_file:
        with open( output_csv_file, 'wb' ) as out_csv_file:
            reader = csv.DictReader(geoIds_file)
            writer = None
            for row in reader:
                # row['_bad_request'] = ''
                results = query_api( row[field_name] )
                if results is not None:
                    for result in results:
                        this_result = row.copy()
                        this_result.update(result)
                        this_result['geographyName'] = this_result['geographyName'].encode('utf-8')
                        if writer is None:
                              writer = csv.DictWriter(out_csv_file, fieldnames=this_result.keys())
                              writer.writeheader()
                        writer.writerow(this_result)
                # else:
                #     row['_bad_request'] = 'bad request'
                #     if writer is None:
                #         writer = csv.DictWriter(out_csv_file, fieldnames=row.keys())
                #         writer.writeheader()
                #     writer.writerow(this_result)

def parse_api_results ( data ):
    return data['Results']

def query_api( geo_id ):
    if len(geo_id) < 5:
        print "zfill " + geo_id + " to " + str(geo_id).zfill(5)
    url = 'https://www.broadbandmap.gov/broadbandmap/speedtest/county/ids/' + str(geo_id).zfill(5) + '?format=json'
    print url
    try:
        response = urllib.urlopen( url )
        data = json.loads( response.read() )
        new_field_value = parse_api_results( data )
        return new_field_value
    except:
        return None

if __name__ == "__main__":
    field_name = sys.argv[1]
    geometry_type = sys.argv[2]
    input_geoIds_file = sys.argv[3]
    output_csv_file = sys.argv[4]

    parse_csv( field_name, geometry_type, input_geoIds_file, output_csv_file )
