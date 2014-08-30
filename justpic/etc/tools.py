#notice 12100 has 99 pictures in 5k
import sys
sys.path.insert(0,'../')
sys.path.insert(0,'./')
from markpic.models import KeyWord5K,Picture5K
words_list=[]
for line in open("../markpic/words"):
    line=line[:-1]
    words_list.append(line)

imagename_list=[]
for line in open("./image_nums"):
    line=line[:-1]
    line=line+".jpeg"
    imagename_list.append(line)

wordsrelation_list=[]
wordsrelation=[]
for line in open("document_words"):
    line=line[:line.find("-99")]
    wordsrelation=line.split()
    wordsrelation_list.append(wordsrelation)

#print wordsrelation
print len(wordsrelation)
#from markpic.models import PictureCorel,KeyWordCorel
for word in words_list:
    worddata=KeyWord5K(keyname=word)
    worddata.save()
#print imagename_list

for imagename in imagename_list:
#    print imagename
    pic=Picture5K.objects.get(picname=imagename)
    if pic.picid>=len(wordsrelation_list):
        continue
    for word in wordsrelation_list[pic.picid]:
        keyword=KeyWord5K.objects.get(keyid=word)
        picture=Picture5K.objects.get(picname=imagename)
        keyword.pictures.add(picture)
      #  keyword=KeyWordCorel(keyname=word,picture=pic.picid)


