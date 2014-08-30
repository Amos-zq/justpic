import os
import MySQLdb
import sys
sys.path.insert(0,'../')
from markpic.models import *
class pic:
    def __init__(self):
        self.name = ''
        self.path = ''

folder = "pictures"
filter = ".jpg|.jpeg"
piclist = []

def search(folder, filter, piclist):
    folders = os.listdir(folder)
    global id
    for name in folders:
        curname = os.path.join(folder, name)
        #print curname
        isfile = os.path.isfile(curname)
        if isfile:
            ext = os.path.splitext(curname)[1]
            count = filter.count(ext)
            if count > 0:
                cur = pic()
                cur.name = name
                cur.path = os.path.normcase(curname)
                piclist.append(cur)
        else:
            search(curname, filter, piclist)
#    return piclist

#database process
class BlobDataTestor:
    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123654', db='pr_site')

    def __del__(self):
        try:
            self.conn.close()
        except Exception,e:
            pass


    def closedb(self):
        self.conn.close()


    def setup(self):
        #cursor = self.conn.cursor()
        #cursor.execute("""CREATE TABLE IF NOT EXISTS `5k` (
      	#	                   `picid` int(11) NOT NULL AUTO_INCREMENT,
      	#	                   `picname` varchar(30) NOT NULL,
      	#	                   `picpath` varchar(100) NOT NULL,
    	#	                   PRIMARY KEY (`picid`)
    	#		               ) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8""")
        pass

    def teardown(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("Drop Table Picture")
        except:
            pass


    def testRWBlobData(self):
        filter = [".jpg", ".png", ".jpeg"]
        pic5klist = []
        path5k = r"../media/imagepool/5K"
        search(path5k, filter, pic5klist)
        #corel 30k is not included
        # pic30klist = []
        # path30k = r"pictures/corel30k"
        # search(path30k,filter,pic30klist)
        #print pic5klist[0].name
        #insert pic info into the mysql
        #print pic30klist[0].path

        for pic in pic5klist:
            p=Picture5K(picname=pic.name,picpath=pic.path)
            p.save()

#        for pic in pic30klist:
#            p=PictureCorel(picname=pic.name,picpath=pic.path)
#            p.save()

def main():
    test = BlobDataTestor()
    test.setup()
    test.testRWBlobData()
    test.closedb()
if __name__ == "__main__":
    test = BlobDataTestor()
    test.setup()
    test.testRWBlobData()
    test.closedb()

