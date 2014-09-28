# -*- coding=UTF-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
import os
from annotation import settings
import StringIO
import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from markpic.models import Picture5K, KeyWord5K, KeyWordCorel, Student, Log5k, PictureTest, PictureTrain, LogTest, \
    LogTrain, LogCorel,PrivatePicture
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib.auth import *
from django.core.paginator import Paginator
from django.template import loader
from django.contrib.sitemaps import Sitemap
from markpic.mark import  word2another

import upyun
up=upyun.UpYun('justpic','justpic','woshi007',timeout=30,endpoint=upyun.ED_AUTO)

def genePicName():
    #picindex=random.randint(0,1)
    picindex = 0
    piclist = []
    if picindex == 0:
        picid = random.randint(0, 4999)
        piclist = KeyWord5K.objects.filter(pictures=picid)
    elif picindex == 1:
        picid = random.randint(0, 30000)
        piclist = KeyWordCorel.objects.filter(pictures=picid)
    if len(piclist) == 0:
        return None
    elif piclist:
        pic = random.choice(piclist)
        return pic.keyname
    else:
        return genePicName()

def querykeyid(keyname=None,picindex=0):
    if picindex == 0:
        keylist = KeyWord5K.objects.filter(keyname=keyname)
    elif picindex == 1:
        keylist = KeyWordCorel.objects.filter(keyname=keyname)
    if keylist:
        key = keylist[0]
        return key.keyid
    else:
        return -1

def querypic(word):
    piclist = []
    picindex = 0
    if picindex == 0:
        keylist = KeyWord5K.objects.filter(keyname=word)
    elif picindex == 1:
        keylist = KeyWordCorel.objects.filter(keyname=word)
    if keylist:
        key = keylist[0]
        piclist = []
        picturelist = []
        picturelist.extend(random.sample(key.pictures.all(), min(len(key.pictures.all()), 5)))
        indexlist = word2another(key,picindex)
        for index in indexlist:
            id = index + 1
            if picindex == 0:
                key = KeyWord5K.objects.get(keyid=id)
            elif picindex == 1:
                key = KeyWordCorel.objects.get(keyid=id)
            picturelist.extend(random.sample(key.pictures.all(), min(len(key.pictures.all()), 5)))
        for pic in picturelist:
            ownpic = dict()
            ownpic["id"] = pic.picid
            ownpic["name"] = pic.picname

            # request_url="/apps/justpic"+str(pic.picpath)[18:]
            # response = pcs.thumbnail(request_url, 512, 512)
            # #'/apps/justpic/5K/118000/118097.jpeg'
            # ownpic.src = response.url
            # print str(pic.picpath)[18:]
            # pic.path local path
            print pic.picpath
            ownpic["src"]="http://justpic.b0.upaiyun.com/"+str(pic.picpath)+"!v1"
            piclist.append(ownpic)
        return piclist
    else:
        return []


class Log5KSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.4
    def items(self):
        return Log5k.objects.all()

    def annotationid(self, obj):
        return obj.annotationid

    def picid(self, obj):
        return obj.picid

@login_required
def check(request):
    if request.user.is_superuser:
        res = up.getlist('upload')
        print res
        for item in res:
            file_path="%s/%s"%('upload',item['name'])
            up.delete(item['name'])
        #delete the links from private files
        PrivatePicture.objects.all().delete()
        return render_to_response("allpic.html",context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

@csrf_exempt
def home(request):
    if request.user.is_authenticated():
        return render_to_response('product.html', context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return render_to_response('login.html',context_instance=RequestContext(request))


@login_required
def loggedin(request):
    return render_to_response('select.html')


def processcorel30k(request):
    return render_to_response('base.html')

def genresult():
    picindex = 0
    keyname = genePicName()
    keyid = 0
    piclist = []
    while (keyname is  None):
        keyname=genePicName()

    keyid = querykeyid(keyname=keyname,picindex=picindex)
    piclist = querypic(keyname)
    random.shuffle(piclist)
    #convertpath(piclist)

    return {
        'picindex': picindex,
        'picture_list': piclist,
        'keyid': keyid,
        'keyword': keyname,
    }

def custom_proc(request):
    pre_result= genresult()
    pre_result['user']=request.user
    return pre_result

def getpics(request):
    piclist=PrivatePicture.objects.filter(user=request.user.get_profile())
    return {'piclist':piclist}

def search_proc(request):
    word=request.GET['word']
    piclist=[]
    return {
        'word':word,
        'picture_list':piclist
    }

def test(request):
    response = HttpResponse()
    response.content = "this is a test content"
    response.write("<p>Here's the write test")
    return response


@login_required
def processInit(request):
    c = RequestContext(request, processors=[custom_proc])
    return render_to_response('product.html', context_instance=RequestContext(request, processors=[custom_proc]))


def processLableMe(request):
    return render_to_response('LableMe.html')

def LableMeAnnotation(request):
    if request.is_ajax():
        message = "Hello Ajax"
        return HttpResponse(request.POST)
    return render_to_response('LableMe.html')


def search(request):
    print request.GET
    if 'word' in request.GET:
        keyid = querykeyid(request.GET['word'])
        piclist = querypic(request.GET['word'])
        if not piclist:
            return render_to_response('subsearch.html', context_instance=RequestContext(request,processors=[search_proc]))
        return render_to_response('subsearch.html', context_instance=RequestContext(request,processors=[search_proc]))
    else:
        message = 'You searched nothing'
    return render_to_response("search.html", context_instance=RequestContext(request))

#from django import oldforms as forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import UserProfile

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    # def save(self, commit=True):
    #     if not commit:
    #         raise NotImplementedError("Can't create User and UserProfile without database save")
    #     user = super(UserCreateForm, self).save(commit=True)
    #     user_profile = UserProfile(user=user,email=self.cleaned_data['email'])
    #     user_profile.save()
    #     return user, user_profile

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreateForm()
    c = {'form': form}
    return render_to_response("registration/register1.html", c, context_instance=RequestContext(request))

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        studentid = request.POST['studentid']
        password = request.POST['password']
        user = authenticate(username=studentid, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.is_active==False:
                return HttpResponseRedirect("/")

            return HttpResponseRedirect("/processinit")
        else:
            return HttpResponseRedirect("/account/invalid/")
    else:
        return HttpResponseRedirect("/")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
#    return render_to_response('login.html',context_instance=RequestContext(request))

@csrf_exempt
@login_required
def process(request):
    global picindex
    if request.is_ajax() and request.method == 'POST':
        print request.POST
        picids=request.POST.getlist('picids[]')
        wordid = request.POST.get('wordid')
        studentid = request.POST.get('studentid')
        pictureindex = request.POST.get('picindex')

        #store the log in to the mysql
        for picid in picids:
            if pictureindex == '0':
                log = Log5k(picid=picid, keyid=wordid, studentid=studentid)
                log.save()
            elif pictureindex == '1':
                log = LogCorel(picid=picid, keyid=wordid, studentid=studentid)
                log.save()
        # return HttpResponseRedirect("/processinit")
    response=genresult()
    return HttpResponse(json.dumps(response))
    # c = RequestContext(request, processors=[custom_proc])
    # return render_to_response('index.html', context_instance=RequestContext(request, processors=[custom_proc]))

def paginate(request):
    return render_to_response('pagination.html', context_instance=RequestContext(request, processors=[custom_proc]))

def recommend(request):
    return render_to_response("recommend.html", context_instance=RequestContext(request))

def analysis(request):
    return render_to_response("analysis.html",context_instance=RequestContext(request))

def project(request):
    return render_to_response("project.html",context_instance=RequestContext(request))

def profile(request):
    return render_to_response("profile.html",context_instance=RequestContext(request))

def instruction(request):
    return render_to_response("instruct.html",context_instance=RequestContext(request))

def recogn(request):
    return render_to_response("recogn.html",context_instance=RequestContext(request))

def private(request):
    return render_to_response('private.html', context_instance=RequestContext(request, processors=[getpics]))

    # return render_to_response("private.html",context_instance=RequestContext(request))

def game(request):
    return render_to_response("future.html",context_instance=RequestContext(request))

def api(request):
    return render_to_response("future.html",context_instance=RequestContext(request))

try:
    import Image
except:
    from PIL import Image
import time
def create_filename():
    seed=list("1234567890qwertyuiopasdfghjklzxcvbnm~-*")
    cpt = code = int(time.time()*1000)
    selected=[]
    cl=len(seed)
    while True:
        rest = cpt / cl
        mod = cpt % cl
        if rest <= cl:
            selected.append(rest)
            break
        else:
            selected.append(mod)
            cpt = rest
    return "".join([seed[n] for n in selected])

def load_data_access(holder_name):
    if holder_name:
        holder=__import__(holder_name.lower())
        return holder.read_file,holder.dump_file
    return read_file,dump_file

def success_rep(form,filename):
    success=form.get("on_success","")
    if success:
        success=success.replace("$status","true")
        success=success.replace("$filename",filename)
        return success
    return dict(status=True,filename=filename)

def error_rep(form,info):
    error=form.get("on_error","")
    if error:
        error=error.replace("$status","false")
        error=error.replace("$info",info)
        return error
    return dict(status=False,info=info)

SITE_ROOT=os.path.dirname(os.path.abspath(__file__))
UPFILE_ROOT=os.path.abspath(os.path.join(SITE_ROOT, 'upfile'))
def dump_file(filename,file_obj):
    file_path="%s/%s"%(UPFILE_ROOT,filename)
    filepath="%s/%s" % ('upload',filename)
    headers={'x-gmkerl-rotate':'180'}
    res=up.put(filepath,file_obj,checksum=True)
    print file_path
    print res
    with open(file_path,'wb') as f:
        f.write(file_obj)

def read_file(filename):
    file_path="%s"%(filename)
    return False,file_path

def get_ext_name(filename):
    return filename.split(".")[-1]

def change_size(ext,img_data,tar_w,tar_h):
    from StringIO import StringIO
    img=Image.open(StringIO(img_data))
    w,h=img.size
    resize=True
    if not tar_h and w<=tar_w:
        resize=False
    if not tar_w and h<=tar_w:
        resize=False
    if w<=tar_w and h<=tar_h:
        resize=False
    if not resize:
        return img_data
    if tar_w<w and tar_h==0:
        tar_h=int(w*1.0/tar_w*h)
    if tar_h<h and tar_w==0:
        tar_w=int(h*1.0/tar_h*w)
    img.thumbnail((tar_w,tar_w),Image.ANTIALIAS)
    tmpf=StringIO()
    img.save(tmpf,format=img.format)
    tmpf.seek(0)
    return tmpf.read()

@csrf_exempt
@login_required
def upload_file(request):
    file_object=request.FILES['thefile']
    sizes=file_object.size
    file_name=file_object.name
    ext_name=get_ext_name(file_name)
    if ext_name.lower() not in ['jpg','jpeg','gif','png']:
        return HttpResponse(json.dumps(**error_rep(request.FILES, "extention %s not allowed" % ext_name)))
    new_filename_prefix=create_filename()
    new_filename="%s.%s"%(new_filename_prefix,ext_name)
    image_data=file_object.read()
    try:
        dump_file(new_filename,image_data)
    except Exception,e:
        return HttpResponse(json.dumps(**error_rep(request.FILES, "please upload the file again due to the network")))
    file_path="%s/%s"%('upload',new_filename)
    picurl="http://justpic.b0.upaiyun.com/"+file_path
    p=PrivatePicture(picurl=picurl,picname=new_filename,user=request.user.get_profile())
    p.save()
    return HttpResponse(json.dumps(success_rep(request.FILES, new_filename)))
