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
    LogTrain, LogCorel
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib.auth import *
from django.core.paginator import Paginator
from django.template import loader
from django.contrib.sitemaps import Sitemap
from django.utils import  simplejson
from markpic.mark import  word2another

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
            ownpic["src"]="http://justpic.b0.upaiyun.com/"+str(pic.picpath)[18:]+"!v1"
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
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    c = {'form': form}
    return render_to_response("registration/register1.html", c, context_instance=RequestContext(request))


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        studentid = request.POST['studentid']
        password = request.POST['password']
        user = authenticate(username=studentid, password=password)
        if user is not None:
            login(request, user)
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
        print 'response here'
        print picids
        print wordid
        print studentid
        print pictureindex
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
    print response
    return HttpResponse(simplejson.dumps(response))
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
    return render_to_response("future.html",context_instance=RequestContext(request))

def game(request):
    return render_to_response("future.html",context_instance=RequestContext(request))

def api(request):
    return render_to_response("future.html",context_instance=RequestContext(request))
