import random
from datetime import datetime

publishers = [ 'micha', 'mark', 'melanie', 'logan'] 
sources = ['yahoo', 'google']

print('date,pub_name,source,clicks,revenue')

for i in range(1,32):
    d = datetime(2019,10,i).date()
    for pub in publishers:
        source = sources[random.randint(0,1)]
        clicks = random.randint(20,500)
        revenue = '{:0.2f}'.format(clicks*(random.randint(0,150)/150) )
        print('{},{},{},{},{}'.format(d, pub, source, clicks, revenue))