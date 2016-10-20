import sys
import csv
import json
import urllib2
import requests

filename = sys.argv[1]
api = 'https://maps.googleapis.com/maps/api/geocode/json?address='

f = open(filename, 'rb')
try:
    reader = csv.reader(f, delimiter= ';')
    for row in reader:
        endereco = str(row[2]).replace(' ', '+')+ ',+' +str(row[3]).replace(' ', '+') + ',+' + str(row[4]).replace(' ', '+') + ',+'+ str(row[5]).replace(' ', '+')
        resp = requests.get(api+endereco)
        result = resp.text
        jsonValue = json.loads(result)
        print jsonValue['results']
except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
finally:
    f.close()
