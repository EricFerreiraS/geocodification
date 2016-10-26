import sys
import csv
import json
import requests
import datetime
import time

filename = sys.argv[1]
api = 'https://maps.googleapis.com/maps/api/geocode/json?address='
key = ['','AIzaSyCJK4dg7NabAMFIwxPKyE2EICiPARah6lw', 'AIzaSyCcaNivsVgF1iSDF5zSwZ3sKJ3JLP7jQVk','AIzaSyAwdsKp74cwS5RJ73HS38oHDtVKw8ZAKgA','AIzaSyAhADEiuwuhs92u1pjC8n1ZTYB5b56yF7c']

f = open(filename, 'rb')
g = open(filename+'_changed', 'wb')
try:
	reader = csv.reader(f, delimiter= ';')
	writer = csv.writer(g, delimiter= ';')
	i = 1
	j = 0
	for row in reader:
		endereco = str(row[2]).replace(' ', '+')+ ',+' +str(row[3]).replace(' ', '+') + ',+' + str(row[4]).replace(' ', '+') + ',+'+ str(row[5]).replace(' ', '+')
		resp = requests.get(api+endereco+'&key='+key[j])
		if resp.status_code == 200:
			value = json.loads(resp.content)
			if value['status'] != 'ZERO_RESULTS' and value['status'] != 'OVER_QUERY_LIMIT':
				lat = value['results'][0]['geometry']['location']['lat']
				lng = value['results'][0]['geometry']['location']['lng']
				row.append(lat)
				row.append(lng)
				writer.writerow(row)
			elif value['status'] == 'OVER_QUERY_LIMIT':
				#time.sleep(300)
				j = j+1
				print ('Trocando Chave {0}').format(key[j])
				endereco = str(row[2]).replace(' ', '+')+ ',+' +str(row[3]).replace(' ', '+') + ',+' + str(row[4]).replace(' ', '+') + ',+'+ str(row[5]).replace(' ', '+')
				resp = requests.get(api+endereco+'&key='+key[j])
				value = json.loads(resp.content)
				lat = value['results'][0]['geometry']['location']['lat']
				lng = value['results'][0]['geometry']['location']['lng']
				row.append(lat)
				row.append(lng)
				writer.writerow(row)
			else:
				writer.writerow(row)
		print ('Linha {0} processada - {1}').format(i,datetime.datetime.now())
		i = i+1
except csv.Error as e:
	sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
finally:
	f.close()
	g.close()
