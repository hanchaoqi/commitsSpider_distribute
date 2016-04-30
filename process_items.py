import redis
import json
from commitsSpider.private import PrivateData

def main():
    pool = redis.ConnectionPool(host = PrivateData.host,port = PrivateData.port,db=0)
    r = redis.Redis(connection_pool=pool)
    while True:
        source,data = r.blpop(["githubSpider:items"])
        item = json.loads(data)
        try:
            print u"Processing:%(url)s<%(cve)s>" % item
        except KeyError:
            print u"Error processng:%r" % item

if __name__=='__main__':
    main()
