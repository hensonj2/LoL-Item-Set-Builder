import requests
import json
import time
import string
import sys

i = sys.argv[1]
k = 'UserData/'+i+'/userData.txt'
k = open(k)
api = k.readline()
api = string.replace(api,'\n','')
k.close()
try:
    for j in ['CHALLENGER','MASTER','GOLD','PLATINUM','DIAMOND']:
        path = i+'Data/'+j+'/'+j+'master.txt'
        ids = open(path)
        path = i+'Data/'+j+'/mid.txt'
        mid = open(path, 'w')
        
        matchids = []
        
        for summonerid in ids:
            summonerid = string.replace(summonerid,'\n','')
            summonerid = summonerid.split(',')[0]
            l = time.time()
            success = 0
        
            while success is 0:
                try:
                    r = requests.get('https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/'+summonerid+'?seasons=SEASON2016&api_key='+api)
                except requests.exceptions.RequestException as e:
                    print('RequestException');
                
                if r.status_code is 200:
                    success = 1
                    b = r.json()
                    z = 0;
                    if 'matches' in b:
                        for m in b['matches']:
                            if (str(m['season']) == 'PRESEASON2017') and (m['matchId'] not in matchids):
                                t = str(m['matchId'])+'\n'
                                mid.write(t);
                                matchids.append(m['matchId'])
                                z = 1;
                    if z is 1:
                        print('Valid matches found')
                    
                elif r.status_code not in [429, 503, 500]:
                    success = 1
                    print(str(r.status_code)+' error, moving on.')       

                else:
                    print(str(r.status_code)+' error, trying again');
            
                while(time.time() - l < 1.2):
                    pass    
    ids.close()
    mid.close()
    print('Done')
except KeyboardInterrupt:
    ids.close()
    mid.close()
    print('Program Complete on Keyboard Interruption')
    
                     
