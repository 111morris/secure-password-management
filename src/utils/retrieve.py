from utils.dbconfig import dbconfig

def retrieveEntries(mp, ds, search, decyptPassword = False):
 db = dbconfig()
 cursor = db.cursor()


 query = ""