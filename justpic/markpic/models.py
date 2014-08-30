from django.db import models
#from django.contrib.localflavor.us.models import USStateField
import os
import hashlib
# Create your models here.

class PictureCache(models.Model):
    picid=models.AutoField(primary_key=True)
    picname=models.CharField(max_length=30)
    picurl=models.CharField(max_length=500)

class PictureTrain(models.Model):
    picid=models.AutoField(primary_key=True)
    picname=models.CharField(max_length=30)
    picpath=models.ImageField(upload_to=r'pictures\train')

class KeyWordTrain(models.Model):
    keyid=models.AutoField(primary_key=True)
    keyname=models.CharField(max_length=30)
    pictures=models.ManyToManyField(PictureTrain)

class PictureTest(models.Model):
    picid=models.AutoField(primary_key=True)
    picname=models.CharField(max_length=30)
    picpath=models.ImageField(upload_to='pictures\test')

class KeyWordTest(models.Model):
    keyid=models.AutoField(primary_key=True)
    keyname=models.CharField(max_length=30)
    pictures=models.ManyToManyField(PictureTest)

class PictureCustom(models.Model):
    picid=models.AutoField(primary_key=True)
    picname=models.CharField(max_length=30)
    picpath=models.ImageField(upload_to='pictures\custom')

class Picture5K(models.Model):
    picid=models.AutoField(primary_key=True)
    picname=models.CharField(max_length=30)
    picpath=models.ImageField(upload_to='pictures\5K')

class KeyWord5K(models.Model):
	keyid=models.AutoField(primary_key=True)
	keyname=models.CharField(max_length=30)
	pictures=models.ManyToManyField(Picture5K)

class PictureCorel(models.Model):
    picid=models.AutoField(primary_key=True)
    picname=models.CharField(max_length=30)
    picpath=models.ImageField(upload_to='pictures\corel30k')

class KeyWordCorel(models.Model):
    keyid=models.AutoField(primary_key=True)
    keyname=models.CharField(max_length=30)
    pictures=models.ManyToManyField(PictureCorel)

class Student(models.Model):
    studentid=models.CharField(max_length=12,primary_key=True)
    password=models.CharField(max_length=12)
    name=models.CharField(max_length=30)
    score=models.CharField(max_length=50)
    is_active=models.BooleanField()
    def is_authenticated(self):
        return True

    def hashed_password(self,password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()
        
    def check_password(self,password):
        if self.hashed_password(password)==self.password:
            return True
        return False

class LogTrain(models.Model):
    annotationid=models.AutoField(primary_key=True)
    picid=models.CharField(max_length=30)
    keyid=models.CharField(max_length=30)
    studentid=models.CharField(max_length=12)

class LogTest(models.Model):
    annotationid=models.AutoField(primary_key=True)
    picid=models.CharField(max_length=30)
    keyid=models.CharField(max_length=30)
    studentid=models.CharField(max_length=12)

class LogCorel(models.Model):
    annotationid=models.AutoField(primary_key=True)
    picid=models.CharField(max_length=30)
    keyid=models.CharField(max_length=30)
    studentid=models.CharField(max_length=12)
    
class Log5k(models.Model):
    annotationid=models.AutoField(primary_key=True)
    picid=models.CharField(max_length=30)
    keyid=models.CharField(max_length=30)
    studentid=models.CharField(max_length=12)    
    
class PictureToken(models.Model):
    tokenid=models.AutoField(primary_key=True)
    access_token=models.CharField(max_length=200)
    refresh_token=models.CharField(max_length=200)



    picname=models.CharField(max_length=30)
    picpath=models.ImageField(upload_to=r'pictures\train')

from django.contrib.auth.models import User
class UserInfo(models.Model):
    user=models.OneToOneField(User)
    score=models.CharField(max_length=50)


class pic:
    def __init__(self):
        self.name=''
        self.path=''
        
def search(folder,filter,piclist):
    folders=os.listdir(folder)
    for name in folders:
        curname=os.path.join(folder,name)
        isfile=os.path.isfile(curname)
        if isfile:
            ext=os.path.splitext(curname)[1]
            count=filter.count(ext)
            if count>0:
                cur=pic()
                cur.name=name
                cur.path=curname[25:]
                piclist.append(cur)
        else:
            search(curname,filter,piclist)
    return piclist

def insertpic():
    filter=[".jpg",".png",".jpeg"]
    piclist=[]
    path="/home/matrix56/annotation/media/pictures/5K"
    search(path,filter,piclist)
    print piclist[0].path
    for pic in piclist:
        p=Picture5K(picname=pic.name,picpath=pic.path)
        p.save()