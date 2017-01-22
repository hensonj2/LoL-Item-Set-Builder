import json
import mongo
import sys
import string
import time
import requests

user = sys.argv[1]
k = 'UserData/'+user+'/userData.txt'
api = k.readLine()
api = string.replace(api,'\n','')
k.close()

path = user+'Data/midNoDup.txt'
mids = open(path)

matches = {}

for match in mids:
    match = string.replace(match,'\n','')
    l = time.time()

    success = 0

    while success = 0:
        try:
            r = requests.get('https://na.api.pvp.net/api/lol/na/v2.2/match/'+match+'?api_key='+api)
        except requests.exceptions.RequestException as e:
            print(e);

        if r.status_code is 200:
            #Collect all data, or relevent data?
            success = 1
            m = r.json()
            red = []
            blue = []
            winner = -1
                
            for p in m["participants"]:
                if p["teamId"] is 100:
                    blue.append(p["championId"])
                    if winner == "" and p["stats"]["winner"] == true:
                        winner = 0
                    else:
                    red.append(p['championId'])
                    if winner == "" and p["stats"]["winner"] == true:
                        winner = 1
            matches.update({match:{'red':red, 'blue':blue, 'winner':winner}})
        elif r.status_code not in [429,500,503]:
            print(str(r.status_code)+' error, trying again')
        else:
            print(str(r.status_code)+' error, moving on')
            while (time.time() - l < 1.2):
                pass
path = user+'Data/mDetails.txt'
mDeets = open(path, 'w')
for match in matches:
    mDeets.write(str(match)+'\n')
print('done')
            
