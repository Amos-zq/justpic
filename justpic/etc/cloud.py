import MySQLdb
db = MySQLdb.connect("localhost","david","david","picturetoken")
cursor=db.cursor()

cursor.execute("select * from picturetoken")
rs=cursor.fetchone()
# cursor.close
print rs
print rs[2]
access_token=rs[1]
refresh_token=rs[2]
from baidupcs import PCS
# access_token = '21.9403b998cd9b271fa44a54199aad2949.2592000.1401980588.3875775130-1056026'
pcs = PCS(access_token)

def create_cache():
    pass

def test_thumbnail():
    response = pcs.thumbnail('/apps/justpic/5K/118000/118097.jpeg', 400, 400)
    print response.url
    # im = Image.open(StringIO(response.content))
    # im.show()
    print response.ok
    assert response.ok

test_thumbnail()