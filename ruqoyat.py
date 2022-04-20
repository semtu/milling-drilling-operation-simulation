import creopyson
import shutil
import os
import time
from tkinter import *
import cv2
import os

SRC_DIR="C:/Users/Public/Documents/ruqoyat/"
BASE_DIR="C:/Users/personal/Documents/Python Scripts/Creo"
BASE_DIR1='C:/Users/personal/Documents/Python Scripts/Creo/'
IMG_DIR="C:/Users/personal/Documents/Python Scripts/Creo/img"
CREO_DIR=r"C:\Program Files\PTC\Creo 5.0.0.0\Parametric\bin\parametric.exe"
CREOSON_DIR=r"C:\Users\personal\Downloads\CreosonServerWithSetup-2.8.0-win64"
CREOSON_BAT_DIR=r"C:\Users\personal\Downloads\CreosonServerWithSetup-2.8.0-win64\creoson_run.bat"

def launch_creo():
    os.startfile(CREO_DIR)
    time.sleep(10)
    return

def launch_creoson():
    os.chdir(CREOSON_DIR)
    os.startfile(CREOSON_BAT_DIR)
    time.sleep(2)
    os.chdir(BASE_DIR)
    return

def connect_creoson():
    c = creopyson.Client()
    c.connect()
    c.server
    c.sessionId
    c.creo_cd(SRC_DIR)
    c.creo_set_config('display','shadewithedges')
    c.creo_set_config('display_planes','no')
    # c.creo_set_config('display_planes_tags','no')
    c.creo_set_config('display_axes','no')
    # c.creo_set_config('display_axes_tags','no')
    c.creo_set_config('datum_point_display','no')
    # c.creo_set_config('display_point_tags','no')
    c.creo_set_config('display_coord_sys','no')
    # c.creo_set_config('display_coord_sys_tags','no')
    # c.creo_set_config('display_images','no')
    return c

def copy_file(i):
    if "img/"+f"{i}"+".jpg" in os.listdir():
        os.remove("img/"+f"{i}"+".jpg")
    filename=f"{i}"+".jpg"
    src=SRC_DIR
    dest=IMG_DIR
    #shutil.move(SRC_DIR+f"{i}"+".jpg",IMG_DIR)
    shutil.move(os.path.join(src,filename), os.path.join(dest,filename))
    return

def video(video_name):
    image_folder=IMG_DIR

    images=[img for img in os.listdir(image_folder) if img.endswith('.jpg')]
    frame=cv2.imread(os.path.join(image_folder,images[0]))
    height, width, layers=frame.shape

    video=cv2.VideoWriter(BASE_DIR1+video_name,0,2,(width,height))

    short_images=[int(img[:-4]) for img in os.listdir(image_folder) if img.endswith('.jpg')]
    for image in sorted(short_images):
        video.write(cv2.imread(os.path.join(image_folder, str(image)+'.jpg')))

    cv2.destroyAllWindows()
    video.release()
    return

def get_machining_time():
    start=time.time()
    #function
    end=time.time()
    machining_time=end-start
    return machining_time

def default():
    #c.dimension_set('height2',0.1)
    #c.dimension_set('spindle_distance',47)
    #c.dimension_set('workpiece_length',50)
    #c.dimension_set('circle_diameter',40)
    # c.dimension_set('taper_height',0.1)
    # c.dimension_set('taper_diameter',40)
    c.dimension_set('circle0_diameter',40)
    c.dimension_set('height_0',0.1)
    c.dimension_set('circle1_diameter',40)
    c.dimension_set('height_1',0.1)
    c.dimension_set('circle2_diameter',40)
    c.dimension_set('height_2',0.1)
    # c.dimension_set('horizontal_difference',0.1)
    # c.dimension_set('vertical_difference',0.1)
    c.file_regenerate()
    return

def plain_turning(workpiece_length=100, workpiece_diameter=50, depth=10, turning_length=90):
    c.file_open('plain.prt')
    c.view_activate("RUQOYAT")
    try:
        increment=workpiece_length//50
        if depth>=workpiece_diameter:
            print('Depth of cut cannot be greater than or equal to workpiece diameter')
        elif turning_length>=workpiece_length:
            print('Length of cut cannot be greater than or equal to workpiece length')
        else:
            c.dimension_set('workpiece_length',workpiece_length)
            c.dimension_set('workpiece_diameter',workpiece_diameter)
            circle_diameter=workpiece_diameter-depth
            c.dimension_set('circle_diameter',circle_diameter)
            #height2=c.dimension_list('height2')[0].get('value')
            height2=0.1
            # spindle_distance=50
            # i=0
            c.dimension_set('spindle_length',workpiece_diameter)
            while height2<turning_length:
                # i+=1
                c.dimension_set('height2',height2)
                # if i>3:
                c.dimension_set('spindle_distance',workpiece_length)
                workpiece_length-=increment
                # else:
                #     c.dimension_set('spindle_distance',50)
                height2+=increment
                c.file_regenerate()
            #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
            #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return

def taper_turning(workpiece_length=100, workpiece_diameter=50, taper_depth=20, taper_angle=20, taper_turning_length=40):
    c.file_open('taper.prt')
    c.view_activate("RUQOYAT")
    try:
        increment=workpiece_length//50
        if taper_depth>=workpiece_diameter:
            print('Depth of cut cannot be greater than or equal to workpiece diameter')
        elif taper_turning_length>=workpiece_length:
            print('Length of cut cannot be greater than or equal to workpiece length')
        else:
            c.dimension_set('workpiece_length',workpiece_length)
            c.dimension_set('workpiece_diameter',workpiece_diameter)
            c.dimension_set('taper_angle',taper_angle)
            taper_diameter=workpiece_diameter-taper_depth
            c.dimension_set('taper_diameter',taper_diameter)
            #height2=c.dimension_list('height2')[0].get('value')
            taper_height=0.1
            # spindle_distance=50
            # i=0
            c.dimension_set('spindle_length',workpiece_diameter)
            while taper_height<taper_turning_length:
                # i+=1
                c.dimension_set('taper_height',taper_height)
                # if i>3:
                c.dimension_set('spindle_distance',workpiece_length)
                workpiece_length-=increment
                # else:
                #     c.dimension_set('spindle_distance',50)
                taper_height+=increment
                c.file_regenerate()
            #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
            #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed. The server will be restarted automatically, please rerun your simulation')
    return

def shoulder_turning(workpiece_length=100, workpiece_diameter=50, number_of_shoulders=3, d1=10,d2=30,d3=20,l1=10,l2=20,l3=30):
    c.creo_cd(SRC_DIR)
    c.file_open('shoulder.prt')
    c.view_activate("RUQOYAT")
    try:
        if number_of_shoulders==0:
            print('Number of shoulders must be at least 1 and maximum 3')
        elif number_of_shoulders==1:
            d2,d3,l2,l3=(0.1,0.1,0.1,0.1)
        elif number_of_shoulders==2:
            d3,l3=(0.1,0.1)
        depth=[d1,d2,d3]
        depth.sort(reverse=True)
        turning_length=[l1,l2,l3]
        turning_length.sort()

        increment=workpiece_length//50
        if max(depth)>=workpiece_diameter:
            print('Depth of cut cannot be greater than or equal to workpiece diameter')
        elif max(turning_length)>=workpiece_length:
            print('Length of cut cannot be greater than or equal to workpiece length')
        else:
            c.dimension_set('workpiece_length',workpiece_length)
            c.dimension_set('workpiece_diameter',workpiece_diameter)
            circle0_diameter=workpiece_diameter-depth[0]
            c.dimension_set('circle0_diameter',circle0_diameter)
            circle1_diameter=workpiece_diameter-depth[1]
            c.dimension_set('circle1_diameter',circle1_diameter)
            circle2_diameter=workpiece_diameter-depth[2]
            c.dimension_set('circle2_diameter',circle2_diameter)
            height_2=0.1
            c.dimension_set('spindle_length',workpiece_diameter)
            while height_2<turning_length[2]:
                if l1>=height_2:
                    c.dimension_set('height_0',height_2)
                    c.dimension_set('height_1',height_2)
                    c.dimension_set('height_2',height_2)
                    c.dimension_set('spindle_distance',workpiece_length)
                    workpiece_length-=increment
                    height_2+=increment
                    c.file_regenerate()
                elif l2>=height_2:
                    c.dimension_set('height_1',height_2)
                    c.dimension_set('height_2',height_2)
                    c.dimension_set('spindle_distance',workpiece_length)
                    workpiece_length-=increment
                    height_2+=increment
                    c.file_regenerate()
                else:
                    c.dimension_set('height_2',height_2)
                    c.dimension_set('spindle_distance',workpiece_length)
                    workpiece_length-=increment
                    height_2+=increment
                    c.file_regenerate()
            #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
            #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return

def chamfering(workpiece_length=100, workpiece_diameter=50, horizontal_difference=20, vertical_difference=50):
    c.file_open('chamfer.prt')
    c.view_activate("RUQOYAT")
    try:
        increment=workpiece_length//50
        if horizontal_difference>=workpiece_diameter//2:
            print('Horizontal difference cannot be greater than or equal to half the workpiece diameter')
        elif vertical_difference>=workpiece_length:
            print('Vertical differece cannot be greater than or equal to workpiece length')
        else:
            c.dimension_set('workpiece_length',workpiece_length)
            c.dimension_set('workpiece_diameter',workpiece_diameter)
            c.dimension_set('horizontal_difference',horizontal_difference)
            vertical_height=0.1
            c.dimension_set('spindle_length',workpiece_diameter)
            while vertical_height<vertical_difference:
                c.dimension_set('vertical_difference',vertical_height)
                c.dimension_set('spindle_distance',workpiece_length)
                workpiece_length-=increment
                vertical_height+=increment
                c.file_regenerate()
            #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
            #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return

def default_rect_workpiece(workpiece_length=50, workpiece_width=50, workpiece_height=20):
    c.file_open('drill.prt')
    c.view_activate("RUQOYAT")
    try:
        increment=1
        c.dimension_set('length',workpiece_length)
        c.dimension_set('width',workpiece_width)
        c.dimension_set('height',workpiece_height)
        c.dimension_set('d_1',0.1)
        c.dimension_set('d_2',0.1)
        c.dimension_set('d_3',0.1)
        c.file_regenerate()
        #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
        #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return

def drilling(workpiece_length=50, workpiece_width=50, workpiece_height=20, num_of_holes=3, d_1=5,h1=20,x1=20,y1=20, d_2=10,h2=20,x2=40,y2=40, d_3=7,h3=40,x3=10,y3=30):
    try:
        c.file_open('drill.prt')
        c.view_activate("RUQOYAT")
        increment=1
        c.dimension_set('length',workpiece_length)
        c.dimension_set('width',workpiece_width)
        c.dimension_set('height',workpiece_height)
        c.dimension_set('d_1',0.1)
        c.dimension_set('d_2',0.1)
        c.dimension_set('d_3',0.1)
        if num_of_holes==1:
            d_2,d_3,h2,h3,x2,x3,y2,y3=(0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1)
        elif num_of_holes==2:
            d_3,h3,x3,y3=(0.1,0.1,0.1,0.1)
        elif num_of_holes<1 or num_of_holes>3:
            print('Number of holes must be a minimum or 1 and maximum 3')
        d=[d_1,d_2,d_3]
        h=[h1,h2,h3]
        x=[x1,x2,x3]
        y=[y1,y2,y3]
        ds=['d_1','d_2','d_3']
        xs=['x1','x2','x3']
        ys=['y1','y2','y3']
        tool_length=['tool_length1','tool_length2','tool_length3']
        hole=['hole1', 'hole2', 'hole3']
        for i in range(0,num_of_holes):
            if y[i]>workpiece_length or x[i]>workpiece_width:
                print('Make sure the X and Y coordinates are within the workpiece dimension')
            c.dimension_set(xs[i],x[i])
            c.dimension_set(ys[i],y[i])
            c.dimension_set(ds[i],d[i])
            c.dimension_set(tool_length[i],workpiece_height)
            org_depth=workpiece_height+h[i]
            vertical_height=0.1
            while vertical_height<org_depth:
                c.dimension_set(hole[i],vertical_height)
                vertical_height+=increment
                c.file_regenerate()
        #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
        #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return

def boring(workpiece_length=50, workpiece_width=50, workpiece_height=20, d_1=5, h_1=20, x1=20, y1=20):
    try:
        c.file_open('bore.prt')
        c.view_activate("RUQOYAT")
        increment=1
        c.dimension_set('length',workpiece_length)
        c.dimension_set('width',workpiece_width)
        c.dimension_set('height',workpiece_height)
        c.dimension_set('tool_length1',0.1)
        c.dimension_set('d_1',d_1)
        c.dimension_set('x1',x1)
        c.dimension_set('y1',y1)
        c.dimension_set('hole1',h_1)
        time.sleep(2)
        c.dimension_set('hole1',0.1)
        c.dimension_set('tool_length1',workpiece_height)
        org_depth=workpiece_height+h_1
        vertical_height=0.1
        while vertical_height<org_depth:
            c.dimension_set('hole1',vertical_height)
            vertical_height+=increment
            c.file_regenerate()
        #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
        #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return
    return

def taper_drill(workpiece_length=50, workpiece_width=50, workpiece_height=20, diameter=5, depth=20, x1=20, y1=20, angle=10):
    try:
        if depth>workpiece_height:
            print('Depth of hole cannot be greater than workpiece height')
        else:
            c.file_open('taper_drill.prt')
            c.view_activate("RUQOYAT")
            c.creo_set_config('display','wireframe')
            increment=1
            c.dimension_set('length',workpiece_length)
            c.dimension_set('width',workpiece_width)
            c.dimension_set('height',workpiece_height)
            c.dimension_set('diameter',diameter)
            c.dimension_set('x1',x1)
            c.dimension_set('y1',y1)
            height2=0.1
            i=0
            while height2<depth:
                c.dimension_set('depth',height2)
                height2+=increment
                c.file_regenerate()
            #c.interface_export_image(filename="ruqoyat.jpeg", file_type="JPEG")
            #copy_file()
    except RuntimeError:
        print('Use smaller values / Check your values for accuracy')
    except ConnectionError:
        print('Server has crashed, please restart the Creoson server')
    return


# launch_creo()
#launch_creoson()
#c=connect_creoson()
#drilling()
#default()
# plain_turning()
#taper_turning()
#shoulder_turning()
#chamfering()
# c.feature_user_select_csys()
#video()
#boring()
#taper_drill()