import os
from PIL import Image

def ensure_dir(f):
    d=os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def main():
    #set max image dimensions
    max_width=640
    max_height=400

    #set the thumbnail size
    thumb_size=(65,65)

    #optional-set the folder name if  different names needed
    photo_source_folder="photos"
    output_big_folder="pics"
    output_thumb_folder="thumbs"

    #do not edit below this line
    htmlsource=""
    thumb_box=(0,0)

    source_folder=os.getcwd()+"/"+photo_source_folder+"/"
    current_folder=os.getcwd()+"/"
    ensure_dir(current_folder+output_big_folder+"/")
    ensure_dir(current_folder+output_thumb_folder+"/")

    dirList=[fname for fname in os.listdir(source_folder) if fname.lower().endswith(".png") or fname.lower().endswith(".jpg")]

    for fname in dirList:
        print "Resizing %s" %fname
        htmlsource+=""
















