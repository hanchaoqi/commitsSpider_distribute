import ConfigParser

class PrivateData(object):
    cf = ConfigParser.ConfigParser()
    cf.read("private_data")
    host = cf.get("db","db_host")
    port = cf.getint("db","db_port")

