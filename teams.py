'''
teams.py

Sorts the data from details_master.txt into separate files.
The two files, teams_wins.tab and teams_losses.tab, respectively, contain the winning or losing team (each champion shown in respect to their id number) of a match on each line.

e.g.:
1 2 3 4 5
1 2 3 4 6

For the purposes of this example, these files can be uploaded into R in order to generate a set of association rules, determined by setting a minimum support and confidence percentages.
'''
import json
import string
o = open('details_master.txt')

path = 'teams_wins.tab'
teams_wins = open(path, 'w')
path = 'teams_losses.tab'
teams_losses = open(path, 'w')
i = 0

for match in o:
    match = string.replace(match,'\n','')
    match = eval(match)
    key = match.keys()
    match = match[key[0]]
    winner = match['winner']

    if len(match['blue']) == 5:
        for key in match.keys():
            if key == 'blue':
                l = 1
                st = ""            
                for ch in match['blue']:
                    if l:
                        st = '{0}'.format(str(ch))
                        l = 0
                    else:
                        st = '{0} {1}'.format(st, str(ch))
                st = st + '\n'
                if winner is 0:
                    teams_wins.write(st)
                else:
                    teams_losses.write(st)
            elif key =='red':
                l = 1
                st = ""
                for ch in match['red']:
                    if l:
                        st = '{0}'.format(str(ch))
                        l = 0
                    else:
                        st = '{0} {1}'.format(st, str(ch))
                st = st + '\n'
                if winner is 1:
                    teams_wins.write(st)
                else:
                    teams_losses.write(st)
        i = i+1

teams_wins.close()
teams_losses.close()
o.close()        
