import json
import sys
import string
import time
import requests

'''
terminal command: python matchDetails.py user

user: the specified user name which is used to gather both api key and matchId files.
'''

user = sys.argv[1]
k = 'UserData/'+user+'/userData.txt'
k = open(k)
api = k.readline()
api = string.replace(api,'\n','')
k.close()

'''
This code assumes the following (assuming user phreak):
- The file containing the matchIds to query with are stored in phreakData/midNoDup.txt
- matchId are being separated by \n within minNoDup.txt
- Match details (more specifically, team compositions and the winner) are stored as a json string format in phreakData/matchDetails.txt, each match separated by the '\n' character
- If the program recieves the KeyboardInterrupt (typically ctrl-c), it will write all match details currently in matches variable into matchDetails.txt before closing.
'''

path = user+'Data/midNoDup.txt'
mids = open(path)

matches = {}

try:    
    for match in mids:
        match = string.replace(match,'\n','')
        l = time.time()        
        success = 0
        print(str(match))
        
        while success == 0:            
            try:
                r = requests.get('https://na.api.pvp.net/api/lol/na/v2.2/match/'+match+'?api_key='+api)
            except requests.exceptions.RequestException as e:
                print(e);
            if r.status_code is 200:
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
                
            elif (r.status_code == 429) or (r.status_code == 500) or (r.status_code == 503):
                print(str(r.status_code)+' error, trying again')
            else:
                success = 1
                print(str(r.status_code)+' error, moving on')
            
            while (time.time() - l < 1.2):
                '''
                1.2 is the interval in seconds determined by the 500 calls:10 minutes ratio.
                Change according to slowest api rate limit for whichever key you're using.
                '''
                pass

except KeyboardInterrupt:
    print('Keyboard Interrupt, closing')

path = user+'Data/matchDetails.txt'
mDeets = open(path, 'w')    
for match in matches:
    mDeets.write(str(match)+'\n')
print('done')
    
