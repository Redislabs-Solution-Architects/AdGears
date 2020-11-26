def runIt(x):
    execute('TS.INCRBY', "ADVIEW:%s" %(x['value']['ad'].replace(" ", '')), 1, 'TIMESTAMP', int(int(x['id'].split('-')[0])/1000))
    execute('TS.INCRBY', 'TOTALREVENUE', x['value']['score'], 'TIMESTAMP', int(int(x['id'].split('-')[0])/1000))
    j = execute('DECR', "counter:%s" %(x['value']['ad'].replace(" ", '')))
    if j == 0 :
        execute('ZREM', x['value']["campaign"], x['value']['ad'])
        execute('UNLINK', "counter:%s" %(x['value']['ad'].replace(" ", ''))) 
gb =  GearsBuilder(
        reader = 'StreamReader',
        desc   = "Process Adserv impressions")

gb.map(runIt)
gb.register('ADDSTATS')

