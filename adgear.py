def findAd(name):
    demo = getDemo(name)
    c = "campaign:%s" %(demo)
    ads = execute("zrevrange", c, 0, 100)
    for ad in ads:
        j = execute("BF.ADD", ad, name)
        if j > 0:
            return(ad)
    return("FallBackAd")

def getDemo(name):
    u = "user:%s" %(name.replace(" ", ''))
    d = execute("HMGET",  u, "Sex", "IncomeDemo", "AgeDemo")
    return(":".join(d))

def runIt(x):
    id=x[1]
    return(findAd(id))

bg = GB('CommandReader', desc="Maximize My Ads")
bg.map(runIt)
bg.register(trigger='adserv')
