{"expires_in":2592000,"refresh_token":"22.ca7aeff542c491ee0c9de8a3010a9de4.315360000.1724417263.3875775130-1056026","access_token":"21.8bdf77c07a392aea779d571a24903d45.2592000.1411649263.3875775130-1056026","session_secret":"8ddef6d7ab2a0b36034c53a46bcbb6c0","session_key":"9mnRfHBbgiKJcCaPaY1v1Qjo2\/VryC6ZM+X+sorRrQ6C8hWQeryRbEXcZmR2RyHGaDPD8yD8\/LGm+jHuvnVhx6fV0IO5EEJGmQ==","scope":"basic netdisk"}

# "refresh_token":"22.ca7aeff542c491ee0c9de8a3010a9de4.315360000.1724417263.3875775130-1056026"
# "access_token":"21.8bdf77c07a392aea779d571a24903d45.2592000.1411649263.3875775130-1056026"

client_id='oA8jMPTjA8yrtaGsc2i5HHdx'
client_secret='kas6A0XFr7uArRnXL4Da0GCvyxRqRiWw'

#get the foever token ?
import MySQLdb
db = MySQLdb.connect("localhost","david","david","picturetoken")
cursor=db.cursor()

cursor.execute("select * from picturetoken")
rs=cursor.fetchone()
# cursor.close
print rs
print rs[2]
refresh_token=rs[2]

from baidupcs.tools import get_new_access_token
response=get_new_access_token(refresh_token,client_id,client_secret)
access_token=response.json()['access_token']
refresh_token=response.json()['refresh_token']
print access_token
print refresh_token
print type(access_token)
# cursor=db.cursor()
# print
# add_salary = """insert into picturetoken(access_token, refresh_token) values(%s,%s)""" ,(access_token,refresh_token)
# print add_salary
cursor.execute("delete from picturetoken")
cursor.execute( """insert into picturetoken(access_token, refresh_token) values(%s,%s)""" ,(str(access_token),str(refresh_token)))
cursor.close()
db.commit()
db.close()

