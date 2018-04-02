# Author: Aditya Subramanian Muralidaran
'''
1. Enter the actual apiKey.

'''

import urllib.request
import urllib.response
import json
import time

file1 = open("Zipcodes.txt", "r")
zipList = file1.read().split(',')
print("total zipcodes: ",len(zipList))
apiKey = 'xxxxxxxxxxxxxxxxx'

writeFile = open("WeartherData_Final", "a", encoding='utf-8')
j = 0
for i in range(len(zipList)):
  try:
    print(i)
    #------------------20180318------------------
    url = 'http://api.wunderground.com/api/'+str(apiKey)+'/almanac/geolookup/history_20180318/q/' \
          + str(zipList[i]).strip() + '/test.json'
    #request = urllib.request.Request(url)
    response = urllib.request.urlopen(url)
    if(response.getcode() == 200):
      data = json.load(response)
      if ('location' in data and 'history' in data and 'almanac' in data):
        if ('date' in data['history'] and len(data['history']['dailysummary']) > 0 and len(data['history']['observations']) > 16):
          writeFile.write(json.dumps(data, ensure_ascii=False))
          writeFile.write(",")
    else:
      print("stopped at i = ",i,zipList[i])
      break

    #------------------20180319------------------
    url = 'http://api.wunderground.com/api/'+str(apiKey)+'/almanac/geolookup/history_20180319/q/' \
          + str(zipList[i]).strip() + '/test.json'
    response = urllib.request.urlopen(url)
    if (response.getcode() == 200):
      data = json.load(response)
      if ('location' in data and 'history' in data and 'almanac' in data):
        if ('date' in data['history'] and len(data['history']['dailysummary']) > 0 and len(data['history']['observations']) > 16):
          writeFile.write(json.dumps(data, ensure_ascii=False))
          writeFile.write(",")
    else:
      print("stopped at i = ", i, zipList[i])
      break

    #------------------20180320------------------
    url = 'http://api.wunderground.com/api/'+str(apiKey)+'/almanac/geolookup/history_20180320/q/' \
          + str(zipList[i]).strip() + '/test.json'
    response = urllib.request.urlopen(url)
    if (response.getcode() == 200):
      data = json.load(response)
      if ('location' in data and 'history' in data and 'almanac' in data):
        if ('date' in data['history'] and len(data['history']['dailysummary']) > 0 and len(data['history']['observations']) > 16):
          writeFile.write(json.dumps(data, ensure_ascii=False))
          writeFile.write(",")
    else:
      print("stopped at i = ", i, zipList[i])
      break
    #time.sleep(1)

    j += 1
    if(j == 3):
      j = 0
      time.sleep(60)

  except:
    print("stopped at exception")
    break

writeFile.close()
