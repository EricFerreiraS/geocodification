import sys
import csv
import json
import requests

filename = sys.argv[1]
api = 'https://maps.googleapis.com/maps/api/geocode/json?address='

f = open(filename, 'rb')
#g = open(filename+'_changed', 'wb')
try:
    reader = csv.reader(f, delimiter= ';')
    #writer = csv.writer(g, delimiter= ';')
    for row in reader:
        endereco = str(row[2]).replace(' ', '+')+ ',+' +str(row[3]).replace(' ', '+') + ',+' + str(row[4]).replace(' ', '+') + ',+'+ str(row[5]).replace(' ', '+')
        resp = requests.get(api+endereco)
        if resp.status_code == 200:
    		value = json.loads(resp.content)
    		if value['status'] != 'ZERO_RESULTS':
                    lat = value['results'][0]['geometry']['location']['lat']
                    lng = value['results'][0]['geometry']['location']['lng']
                    #writer.writerow(row,)
except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
finally:
    f.close()
