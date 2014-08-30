#-*-coding=utf-8-*-
from PIL import Image
import os
import fnmatch
import logging

class ThumbnailGenerator:
    #--*-- exts 为规定后的后缀名列表，空则获取所有类型文件 --*--
    def __getFileList(self,path,exts=None,subdir=True):
        if os.path.exists(path):
            dirlist=[]
            for name in os.listdir(path):
                fullname=os.path.join(path,name)
                if os.path.isdir(fullname):
                    dirlist+=self.getFileList(fullname,exts)
                else:
                    if exts and len(exts)>0:
                        for ext in exts:
                            if fnmatch.fnmatch(fullname,ext):
                                dirlist.append(fullname)
                                break
                    elif exts==None or len(exts)==0:
                        dirlist.append(fullname)
            return dirlist
        else:
            return []
    #--*-- sizes参数传递生成的尺寸，可以生成多种尺寸，每个size是一个二值元组
    def __make_thumb(self,source_file,dest_path,sizes):
        basename=os.path.basename(source_file)
        dest_path
        try:
            im=Image.open(source_file)
        except IOError,e:
            logging.error('Open %s error: '+str(e),source_file)
            return
        mode=im.mode
        if mode not in ('L','RGB'):
            if mode =='RGBA':
                #透明图片要加白色底
                alpha=im.split()[3]
                bgmask=alpha.point(lambda x:255-x)
                im=im.convert('RGB')
                #paste(color,box,mask)
                im.paste((255,255,255),None,bgmask)
            else:
                im=im.convert('RGB')
        width,height=im.size
        if width==height:
            region=im
        else:
            if width>height:
                delta=(width-height)/2
                box=(delta,0,delta+height,height)
            else:
                delta=(height-width)/2
                box=(0,delta,width,delta+width)
            region=im.crop(box)
        for size in sizes:
            filename=os.path.join(dest_path,basename)
            thumb=region.resize((size[0],size[1]),Image.ANTIALIAS)
            thumb.save(filename,quality=100) #默认JPEG保存质量是75，不太清楚，可选值(0~100)
    def thumb_generate(self,source_path,dest_path,sizes,subdir=True):
        exts=['*.jpg','*.png','*.bmp','*.jpeg','*.JPG','*.PNG','*.BMP','*.JPEG']
        file_list=self.__getFileList(source_path,exts,subdir)
        for file in file_list:
            try:
                self.__make_thumb(file,dest_path,sizes)
            except Exception,e:
                logging.error('Thumb %s error: '+str(e),file)

if __name__=="__main__":
    logging.basicConfig(filename='thumb.log',filemode='w',format='[%(asctime)s]-%(levelname)s:%(message)s',level=logging.DEBUG)
    sizes=[(180,180)]
    curpath=os.path.abspath(os.curdir)
    os.path.join(os.path.dirname("__file__"),os.path.pardir)
    cur_dir=os.path.abspath(os.curdir)
    parent_dir=os.path.dirname(cur_dir)
    root_dir=os.path.dirname(parent_dir)
    root_path=os.path.abspath(root_dir)

    source_path=os.path.join(root_path,'media/imagepool/5K/10000')
    # source_path='201206'
    # dest_path='s'
    dest_path=os.path.join(root_path,'media/imagepool/thumbnail/5K/10000')
    generator=ThumbnailGenerator()
    generator.thumb_generate(source_path,dest_path,sizes=sizes)
