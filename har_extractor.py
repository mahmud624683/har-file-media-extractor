import os 
import shutil 
from tkinter import filedialog
from tkinter import *
import pathlib
import cv2
import glob
import sys

    

root = Tk()
root.withdraw()
harfile = filedialog.askopenfilename(filetypes = (("harfiles", "*.har"), ("all files", "*.har")))
print("Input File Location : ",harfile)
destination = os.path.basename(harfile)
try: 
    destination = destination.split(".")[0]
    destination = destination.split("_")[0]
except:
    pass
zip_des = harfile.replace(destination,"zip_des")
if not os.path.isdir(zip_des):
    os.mkdir(zip_des)
command = f"har-extractor -o {zip_des} -nv -i {harfile}"
os.system(command)

destination = os.path.join(os.path.dirname(harfile),destination)
print("Output Location : ",destination)
vid_des = os.path.join(destination,"videos")
photo_des = os.path.join(destination,"photos")
if not os.path.isdir(destination):
    os.mkdir(destination)
    os.mkdir(vid_des)
    os.mkdir(photo_des)

photo_ext=[".jpg",".jpeg",".png",".webp"]
video_ext=[".mp4",".gif"]
bar = ["-","\\","|","/"]
i=0
for root, dirs, files in os.walk(zip_des):
    for filename in files:

        ext = pathlib.Path(filename).suffix
        basename = filename.replace(ext, "")
        filename = os.path.join(root, filename)
        try:
            file_size = os.path.getsize(filename)
        except:
            file_size = 0

        if file_size>20480:
            if ext in photo_ext:
                im = cv2.imread(filename)
                h, w, _ = im.shape

                if (h>600) & (w>600):

                    filename_new = filename.replace(basename, basename.split(".")[0])
                    basename = basename.split(".")[0]+ext

                    if ext ==".webp":
                        filename_new = filename_new.replace(".webp", ".jpg")

                    if filename_new!=filename:
                        os.rename(filename,filename_new)
                        filename = filename_new

                    des_file = os.path.join(photo_des,basename)
                    file_list = glob.glob(des_file)

                    if len(file_list)<1:
                        try:
                            shutil.move(filename, photo_des) 
                        except:
                            pass
                    else:
                        im = cv2.imread(des_file)
                        h2, w2, _ = im.shape
                        if (h2*w2)>(h*w):
                            os.remove(des_file)
                            shutil.move(filename, photo_des)

            elif ext in video_ext:
                try:
                    shutil.move(filename, vid_des)
                except:
                    pass
        i+=1
        sys.stdout.write("\rWork in progress: [{0}]".format(bar[i%4]))
        sys.stdout.flush()

try:
    shutil.rmtree(zip_des)
except:
    print("can't remove the temp unzipped folder")