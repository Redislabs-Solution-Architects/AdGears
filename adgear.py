def findAd(name):
    demo = getDemo(name)
    c = "campaign:%s" %(demo)
    j = execute("zrevrange", c, 0, 100, "WITHSCORES")

    # 0::2 in a list gets all the even numbered elements
    ads    = j[0::2]
    scores = j[1::2]

    iters = 0
    while iters < len(ads):
        j = execute("BF.ADD", ads[iters], name.replace(" ", ''))
        if j > 0:
            execute("XADD", "ADDSTATS", '*', "ad", ads[iters], "score", scores[iters], "name", name, "campaign", c)
            return(ads[iters], scores[iters] )
        iters += 1
    execute("XADD", "ADDSTATS", '*', "ad", "FallBackAd", "score", 0, "name", name, "campaign", c)
    return("FallBackAd", 0)

def getDemo(name):
    u = "user:%s" %(name.replace(" ", ''))
    # Check to see if user has Intent to Buy
    i = execute("GET", "%s:intent" %(u))
    if i != None:
        return(i)
    d = execute("HMGET",  u, "Sex", "IncomeDemo", "AgeDemo")
    return(":".join(d))

def runIt(x):
    id=x[1]
    return(findAd(id))

bg = GB('CommandReader', desc="Maximize My Ads")
bg.map(runIt)
bg.register(trigger='adserv')
