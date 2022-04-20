from tkinter import *
from tkinter.ttk import *
from ruqoyat import *
from tkvideo import tkvideo
from tooltip import CreateToolTip
import time
import shutil
from urllib3 import exceptions
import sys
import subprocess

SRC_DIR="C:/Users/Public/Documents/ruqoyat/"
BASE_DIR="C:/Users/personal/Documents/Python Scripts/Creo"
IMG_DIR="C:/Users/personal/Documents/Python Scripts/Creo/img"
os.chdir(BASE_DIR)

def vp_start_gui():
    global window
    window=Tk()
    window.title('Ruqoyat')
    window.geometry('600x650')
    window.minsize(600,650)
    window.maxsize(600,650)

    connect_creo_btn=Button(window, text='Connect Creo Software',command=launch_creo,).pack(pady=10)
    connect_creoson_btn=Button(window, text='Connect Creoson Server',command=launch_creoson,).pack(pady=(0,30))
    restart_btn=Button(window, text='Restart',command=refresh).place(x=40,y=40)
    def screen_func(Msg):
        screen=Text(window, height = 1, width=70)
        screen.place(x=20,y=80)
        screen.tag_configure('center', justify='center')
        screen.insert(END, Msg)
        screen.tag_add('center', '1.0', 'end')
        window.after(5000, lambda: screen.destroy())
        return

    tabControl = Notebook(window)

    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
    #tab3 = Frame(tabControl)

    tabControl.add(tab1, text ='Lathe')
    tabControl.add(tab2, text ='Drilling')
    #tabControl.add(tab3, text ='Milling')
    tabControl.pack(expand = 1, fill ="both")

    #Label(tab3,text ="Lets dive into ").grid(column = 0, row = 0,  padx = 30, pady = 30)

    def callback(input):
        if input.isdigit():
            return True
        elif input is "":
            return True
        else:
            return False

    #TAB 1
    #workpiece frame
    workpiece_frame = LabelFrame(tab1, text='Cylindrical Workpiece', width=500, height=90).grid(column = 0, row = 0,  padx = 10, pady = (10,0))
    diameter_var=StringVar()
    length_var=StringVar()
    diameter_label = Label(tab1, text = 'Diameter:').place(x=40,y=30)
    diameter_entry = Entry(tab1,textvariable = diameter_var)
    diameter_entry.place(x=130,y=30)
    reg=window.register(callback)
    diameter_entry.config(validate='key',validatecommand=(reg, '%P'))
    length_label = Label(tab1, text = 'Length:').place(x=40,y=70)
    length_entry=Entry(tab1, textvariable = length_var)
    length_entry.place(x=130,y=70)
    length_entry.config(validate='key',validatecommand=(reg, '%P'))

    def generate_workpiece():
        try:
            c=connect_creoson()
            c.file_open('plain.prt')
            c.view_activate("RUQOYAT")
            workpiece_length=length_var.get()
            workpiece_diameter=diameter_var.get()
            c.dimension_set('workpiece_length',workpiece_length)
            c.dimension_set('workpiece_diameter',workpiece_diameter)
            c.dimension_set('spindle_distance',workpiece_length)
            c.dimension_set('height2',0.1)
            c.file_regenerate()
            c.interface_export_image(filename="workpiece.jpg", file_type="JPEG")
            if 'workpiece.jpg' in os.listdir():
                os.remove('workpiece.jpg')
            filename='workpiece.jpg'
            src=SRC_DIR
            dest=BASE_DIR
            shutil.move(os.path.join(src,filename), os.path.join(dest,filename))
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        return

    def default():
        c=connect_creoson()
        c.file_open('plain.prt')
        c.view_activate("RUQOYAT")
        c.dimension_set('height2',0.1)
        c.dimension_set('spindle_distance',47)
        c.dimension_set('workpiece_length',50)
        c.dimension_set('workpiece_diameter',50)
        c.dimension_set('circle_diameter',40)
        # c.dimension_set('horizontal_difference',0.1)
        # c.dimension_set('vertical_difference',0.1)
        c.file_regenerate()
        return

    generate_workpiece_btn=Button(tab1,text = 'Generate', command = generate_workpiece ,width=20).place(x=300,y=30)
    default_btn=Button(tab1,text = 'Default', command = default ,width=20).place(x=300,y=70)
    def mymedia_workpiece():
        if 'workpiece.jpg' in os.listdir():
            os.startfile(BASE_DIR+"/workpiece.jpg")
        return
    workpiece_simulation_btn=Button(tab1,text = 'VIEW', command = mymedia_workpiece ,width=5, height=3)
    workpiece_simulation_btn.place(x=470,y=30)

    #plain turning frame
    def plain_turning():
        try:
            start=time.time()
            workpiece_length=int(length_var.get())
            workpiece_diameter=int(diameter_var.get())
            depth=int(plain_depth_var.get())
            turning_length=int(plain_length_var.get())
            c=connect_creoson()
            c.file_open('plain.prt')
            c.view_activate("RUQOYAT")
            increment=workpiece_length//50
            if depth>=workpiece_diameter:
                screen_func('Depth of cut cannot be greater than or equal to workpiece diameter')
            elif turning_length>=workpiece_length:
                screen_func('Length of cut cannot be greater than or equal to workpiece length')
            else:
                c.dimension_set('workpiece_length',workpiece_length)
                c.dimension_set('workpiece_diameter',workpiece_diameter)
                circle_diameter=workpiece_diameter-depth
                c.dimension_set('circle_diameter',circle_diameter)
                height2=0.1
                c.dimension_set('spindle_length',workpiece_diameter)
                i=0
                while height2<turning_length:
                    c.dimension_set('height2',height2)
                    c.dimension_set('spindle_distance',workpiece_length)
                    workpiece_length-=increment
                    height2+=increment
                    c.file_regenerate()
                    i+=1
                    c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                    copy_file(i)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)

        video('plain_turning.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        plain_time_var.set(str(machining_time)[:6]+" (secs)")

        # root=Toplevel()
        # root.title('Simulation')
        # video_label=Label(root)
        # video_label.pack()
        # player=tkvideo('plain_turning.avi',video_label,loop=0,size=(600,650))
        # player.play()
        return

    plain_depth_var=StringVar()
    plain_length_var=StringVar()
    plain_time_var=StringVar()
    plain_frame = LabelFrame(tab1, text='Plain Turning', width=500, height=90).grid(column = 0, row = 1,  padx = 30, pady = (10,0))
    plain_depth_label = Label(tab1, text = 'Depth of Cut:').place(x=40,y=130)
    plain_depth_entry = Entry(tab1,textvariable = plain_depth_var)
    plain_depth_entry.place(x=130,y=130)
    plain_depth_entry.config(validate='key',validatecommand=(reg, '%P'))
    plain_length_label = Label(tab1, text = 'Length of cut:').place(x=40,y=170)
    plain_length_entry=Entry(tab1, textvariable = plain_length_var)
    plain_length_entry.place(x=130,y=170)
    plain_length_entry.config(validate='key',validatecommand=(reg, '%P'))

    plain_btn=Button(tab1,text = 'Run', command = plain_turning,width=20)
    plain_btn.place(x=300,y=130)
    plain_time=Entry(tab1, textvariable = plain_time_var, width=25)
    plain_time.place(x=300,y=170)
    def mymedia():
        if 'plain_turning.avi' in os.listdir():
            os.startfile(BASE_DIR+"/plain_turning.avi")
        return
    plain_simulation_btn=Button(tab1,text = 'PLAY', command = mymedia ,width=5, height=3)
    plain_simulation_btn.place(x=470,y=130)

    def taper_turning():
        try:
            start=time.time()
            workpiece_length=int(length_var.get())
            workpiece_diameter=int(diameter_var.get())
            taper_depth=int(taper_depth_var.get())
            taper_angle=int(taper_angle_var.get())
            taper_turning_length=int(taper_length_var.get())
            c=connect_creoson()
            c.file_open('taper.prt')
            c.view_activate("RUQOYAT")
            increment=workpiece_length//50
            if taper_depth>=workpiece_diameter:
                screen_func('Depth of cut cannot be greater than or equal to workpiece diameter')
            elif taper_turning_length>=workpiece_length:
                screen_func('Length of cut cannot be greater than or equal to workpiece length')
            else:
                c.dimension_set('workpiece_length',workpiece_length)
                c.dimension_set('workpiece_diameter',workpiece_diameter)
                c.dimension_set('taper_angle',taper_angle)
                taper_diameter=workpiece_diameter-taper_depth
                c.dimension_set('taper_diameter',taper_diameter)
                taper_height=0.1
                c.dimension_set('spindle_length',workpiece_diameter)
                i=0
                while taper_height<taper_turning_length:
                    c.dimension_set('taper_height',taper_height)
                    c.dimension_set('spindle_distance',workpiece_length)
                    workpiece_length-=increment
                    taper_height+=increment
                    c.file_regenerate()
                    i+=1
                    c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                    copy_file(i)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        video('taper_turning.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        taper_time_var.set(str(machining_time)[:6]+" (secs)")
        return

    #taper turning frame
    taper_depth_var=StringVar()
    taper_angle_var=StringVar()
    taper_length_var=StringVar()
    taper_time_var=StringVar()
    taper_frame = LabelFrame(tab1, text='Taper Turning', width=500, height=90).grid(column = 0, row = 2,  padx = 30, pady = (10,0))
    taper_depth_label = Label(tab1, text = 'Taper Depth:').place(x=40,y=230)
    taper_depth_entry = Entry(tab1,textvariable = taper_depth_var)
    taper_depth_entry.place(x=130,y=230)
    taper_depth_entry.config(validate='key',validatecommand=(reg, '%P'))
    taper_angle_label = Label(tab1, text = 'Angle:').place(x=40,y=270)
    taper_angle_entry=Entry(tab1, textvariable = taper_angle_var)
    taper_angle_entry.place(x=80,y=270,width=60)
    taper_angle_entry.config(validate='key',validatecommand=(reg, '%P'))
    taper_length_label = Label(tab1, text = 'Length:').place(x=150,y=270)
    taper_length_entry=Entry(tab1, textvariable = taper_length_var)
    taper_length_entry.place(x=200,y=270,width=60)
    taper_length_entry.config(validate='key',validatecommand=(reg, '%P'))

    taper_btn=Button(tab1,text = 'Run', command = taper_turning,width=20)
    taper_btn.place(x=300,y=230)
    taper_time=Entry(tab1, textvariable = taper_time_var, width=25)
    taper_time.place(x=300,y=270)
    def mymedia_taper():
        if 'taper_turning.avi' in os.listdir():
            os.startfile(BASE_DIR+"/taper_turning.avi")
        return
    taper_simulation_btn=Button(tab1,text = 'PLAY', command = mymedia_taper ,width=5, height=3)
    taper_simulation_btn.place(x=470,y=230)

    #shoulder turning frame
    def shoulder_turning():
        try:
            start=time.time()
            workpiece_length=int(length_var.get())
            workpiece_diameter=int(diameter_var.get())
            number_of_shoulders=int(num_shoulders_var.get())
            c=connect_creoson()
            c.file_open('shoulder.prt')
            c.view_activate("RUQOYAT")
            if number_of_shoulders==1:
                d1=int(sd1_var.get())
                l1=int(sl1_var.get())
                d2,d3,l2,l3=(0.1,0.1,0.1,0.1)
            elif number_of_shoulders==2:
                d1=int(sd1_var.get())
                l1=int(sl1_var.get())
                d2=int(sd2_var.get())
                l2=int(sl2_var.get())
                d3,l3=(0.1,0.1)
            elif number_of_shoulders==3:
                d1=int(sd1_var.get())
                l1=int(sl1_var.get())
                d2=int(sd2_var.get())
                l2=int(sl2_var.get())
                d3=int(sd3_var.get())
                l3=int(sl3_var.get())
            elif number_of_shoulders>3 or number_of_shoulders<1:
                screen_func('Number of shoulders must be at least 1 and maximum 3')
            depth=[d1,d2,d3]
            depth.sort(reverse=True)
            turning_length=[l1,l2,l3]
            turning_length.sort()
            increment=workpiece_length//50
            if max(depth)>=workpiece_diameter:
                screen_func('Depth of cut cannot be greater than or equal to workpiece diameter')
            elif max(turning_length)>=workpiece_length:
                screen_func('Length of cut cannot be greater than or equal to workpiece length')
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
                i=0
                while height_2<turning_length[2]:
                    if l1>=height_2:
                        c.dimension_set('height_0',height_2)
                        c.dimension_set('height_1',height_2)
                        c.dimension_set('height_2',height_2)
                        c.dimension_set('spindle_distance',workpiece_length)
                        workpiece_length-=increment
                        height_2+=increment
                        c.file_regenerate()
                        i+=1
                        c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                        copy_file(i)
                    elif l2>=height_2:
                        c.dimension_set('height_1',height_2)
                        c.dimension_set('height_2',height_2)
                        c.dimension_set('spindle_distance',workpiece_length)
                        workpiece_length-=increment
                        height_2+=increment
                        c.file_regenerate()
                        i+=1
                        c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                        copy_file(i)
                    else:
                        c.dimension_set('height_2',height_2)
                        c.dimension_set('spindle_distance',workpiece_length)
                        workpiece_length-=increment
                        height_2+=increment
                        c.file_regenerate()
                        i+=1
                        c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                        copy_file(i)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        video('shoulder_turning.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        shoulder_time_var.set(str(machining_time)[:6]+" (secs)")
        return

    num_shoulders_var=StringVar()
    sd1_var=StringVar()
    sl1_var=StringVar()
    sd2_var=StringVar()
    sl2_var=StringVar()
    sd3_var=StringVar()
    sl3_var=StringVar()
    shoulder_time_var=StringVar()
    shoulder_frame = LabelFrame(tab1, text='Shoulder Turning', width=500, height=90).grid(column = 0, row = 3,  padx = 30, pady = (10,0))
    num_shoulders_label = Label(tab1, text = 'Number of Shoulders:').place(x=40,y=330)
    num_shoulders_var.set(1)
    num_shoulders_entry = OptionMenu(tab1,num_shoulders_var,1,2,3)
    num_shoulders_entry.place(x=180,y=330,width=80)
    sd1_label = Label(tab1, text = 'D1: ').place(x=40,y=370)
    sd1_entry=Entry(tab1, textvariable = sd1_var)
    sd1_entry.place(x=60,y=370,width=40)
    sd1_entry.config(validate='key',validatecommand=(reg, '%P'))
    sl1_label = Label(tab1, text = 'L1:').place(x=90,y=370)
    sl1_entry=Entry(tab1, textvariable = sl1_var)
    sl1_entry.place(x=110,y=370,width=40)
    sl1_entry.config(validate='key',validatecommand=(reg, '%P'))

    sd2_label = Label(tab1, text = 'D2:').place(x=130,y=370)
    sd2_entry=Entry(tab1, textvariable = sd2_var)
    sd2_entry.place(x=150,y=370,width=40)
    sd2_entry.config(validate='key',validatecommand=(reg, '%P'))
    sl2_label = Label(tab1, text = 'L2:').place(x=180,y=370)
    sl2_entry=Entry(tab1, textvariable = sl2_var)
    sl2_entry.place(x=200,y=370,width=40)
    sl2_entry.config(validate='key',validatecommand=(reg, '%P'))

    sd3_label = Label(tab1, text = 'D3:').place(x=220,y=370)
    sd3_entry=Entry(tab1, textvariable = sd3_var)
    sd3_entry.place(x=240,y=370,width=40)
    sd3_entry.config(validate='key',validatecommand=(reg, '%P'))
    sl3_label = Label(tab1, text = 'L3:').place(x=270,y=370)
    sl3_entry=Entry(tab1, textvariable = sl3_var)
    sl3_entry.place(x=290,y=370,width=30)
    sl3_entry.config(validate='key',validatecommand=(reg, '%P'))

    shoulder_btn=Button(tab1,text = 'Run', command = shoulder_turning,width=20)
    shoulder_btn.place(x=300,y=330)
    shoulder_time=Entry(tab1, textvariable = shoulder_time_var, width=16)
    shoulder_time.place(x=350,y=370)
    def mymedia_shoulder():
        if 'shoulder_turning.avi' in os.listdir():
            os.startfile(BASE_DIR+"/shoulder_turning.avi")
        return
    shoulder_simulation_btn=Button(tab1,text = 'PLAY', command = mymedia_shoulder ,width=5, height=3)
    shoulder_simulation_btn.place(x=470,y=330)

    #chamfer frame
    def chamfering():
        try:
            start=time.time()
            workpiece_length=int(length_var.get())
            workpiece_diameter=int(diameter_var.get())
            horizontal_difference=int(chamfer_hor_var.get())
            vertical_difference=int(chamfer_ver_var.get())
            c=connect_creoson()
            c.file_open('chamfer.prt')
            c.view_activate("RUQOYAT")
            increment=workpiece_length//50
            if horizontal_difference>=workpiece_diameter//2:
                screen_func('Horizontal difference cannot be greater than or equal to half the workpiece diameter')
            elif vertical_difference>=workpiece_length:
                prinscreen_funct('Vertical differece cannot be greater than or equal to workpiece length')
            else:
                c.dimension_set('workpiece_length',workpiece_length)
                c.dimension_set('workpiece_diameter',workpiece_diameter)
                c.dimension_set('horizontal_difference',horizontal_difference)
                vertical_height=0.1
                c.dimension_set('spindle_length',workpiece_diameter)
                i=0
                while vertical_height<vertical_difference:
                    c.dimension_set('vertical_difference',vertical_height)
                    c.dimension_set('spindle_distance',workpiece_length)
                    workpiece_length-=increment
                    vertical_height+=increment
                    c.file_regenerate()
                    i+=1
                    c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                    copy_file(i)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)

        video('chamfering.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        chamfer_time_var.set(str(machining_time)[:6]+" (secs)")
        return

    chamfer_hor_var=StringVar()
    chamfer_ver_var=StringVar()
    chamfer_time_var=StringVar()
    chamfer_frame = LabelFrame(tab1, text='Chamfering', width=500, height=90).grid(column = 0, row = 4,  padx = 30, pady = (10,0))
    chamfer_hor_label = Label(tab1, text = 'Horizontal Dist:').place(x=40,y=430)
    chamfer_hor_entry = Entry(tab1,textvariable = chamfer_hor_var)
    chamfer_hor_entry.place(x=130,y=430)
    chamfer_hor_entry.config(validate='key',validatecommand=(reg, '%P'))
    chamfer_ver_label = Label(tab1, text = 'Vertical Dist:').place(x=40,y=470)
    chamfer_ver_entry=Entry(tab1, textvariable = chamfer_ver_var)
    chamfer_ver_entry.place(x=130,y=470)
    chamfer_ver_entry.config(validate='key',validatecommand=(reg, '%P'))

    chamfer_btn=Button(tab1,text = 'Run', command = chamfering,width=20)
    chamfer_btn.place(x=300,y=430)
    chamfer_time=Entry(tab1, textvariable = chamfer_time_var, width=25)
    chamfer_time.place(x=300,y=470)
    def mymedia_chamfer():
        if 'chamfering.avi' in os.listdir():
            os.startfile(BASE_DIR+"/chamfering.avi")
        return
    chamfer_simulation_btn=Button(tab1,text = 'PLAY', command = mymedia_chamfer ,width=5, height=3)
    chamfer_simulation_btn.place(x=470,y=430)

    #TAB 2 Workpiece
    def generate_rect_workpiece():
        try:
            c=connect_creoson()
            c.file_open('drill.prt')
            c.view_activate("RUQOYAT")
            workpiece_length=rect_length_var.get()
            workpiece_width=rect_width_var.get()
            workpiece_height=rect_height_var.get()
            c.dimension_set('length',workpiece_length)
            c.dimension_set('width',workpiece_width)
            c.dimension_set('height',workpiece_height)
            c.dimension_set('d_1',0.1)
            c.dimension_set('d_2',0.1)
            c.dimension_set('d_3',0.1)
            c.file_regenerate()
            c.interface_export_image(filename="rect_workpiece.jpg", file_type="JPEG")
            if 'rect_workpiece.jpg' in os.listdir():
                os.remove('rect_workpiece.jpg')
            filename='rect_workpiece.jpg'
            src=SRC_DIR
            dest=BASE_DIR
            shutil.move(os.path.join(src,filename), os.path.join(dest,filename))
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        return

    rect_length_var=StringVar()
    rect_width_var=StringVar()
    rect_height_var=StringVar()
    workpiece_frame2 = LabelFrame(tab2, text='Rectangular Workpiece', width=500, height=90).grid(column = 0, row = 0,  padx = 30, pady = (10,0))
    rect_length_label = Label(tab2, text = 'Length:').place(x=40,y=30)
    rect_length_entry=Entry(tab2, textvariable = rect_length_var)
    rect_length_entry.place(x=130,y=30)
    rect_length_entry.config(validate='key',validatecommand=(reg, '%P'))
    rect_width_label = Label(tab2, text = 'Width:').place(x=40,y=70)
    rect_width_entry = Entry(tab2,textvariable = rect_width_var)
    rect_width_entry.place(x=130,y=70)
    rect_width_entry.config(validate='key',validatecommand=(reg, '%P'))
    rect_height_label = Label(tab2, text = 'Height:').place(x=300,y=70)
    rect_height_entry = Entry(tab2,textvariable = rect_height_var)
    rect_height_entry.place(x=350,y=70,width=100)
    rect_height_entry.config(validate='key',validatecommand=(reg, '%P'))

    generate_workpiece_btn=Button(tab2,text = 'Generate', command = generate_rect_workpiece ,width=20).place(x=300,y=30)
    def mymedia_rect_workpiece():
        if 'rect_workpiece.jpg' in os.listdir():
            os.startfile(BASE_DIR+"/rect_workpiece.jpg")
        return
    rect_workpiece_simulation_btn=Button(tab2,text = 'VIEW', command = mymedia_rect_workpiece ,width=5, height=3)
    rect_workpiece_simulation_btn.place(x=470,y=30)

    #Drilling frame
    def drilling():
        try:
            start=time.time()
            workpiece_length=int(rect_length_var.get())
            workpiece_width=int(rect_width_var.get())
            workpiece_height=int(rect_height_var.get())
            num_of_holes=int(drill_num_holes_var.get())
            c=connect_creoson()
            c.file_open('drill.prt')
            c.view_activate("RUQOYAT")
            increment=2
            c.dimension_set('length',workpiece_length)
            c.dimension_set('width',workpiece_width)
            c.dimension_set('height',workpiece_height)
            c.dimension_set('d_1',0.1)
            c.dimension_set('d_2',0.1)
            c.dimension_set('d_3',0.1)
            if num_of_holes==1:
                d_1=int(drill_d1_var.get())
                h1=int(drill_h1_var.get())
                x1=int(drill_x1_var.get())
                y1=int(drill_y1_var.get())
                d_2,d_3,h2,h3,x2,x3,y2,y3=(0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1)
            elif num_of_holes==2:
                d_1=int(drill_d1_var.get())
                h1=int(drill_h1_var.get())
                x1=int(drill_x1_var.get())
                y1=int(drill_y1_var.get())
                d_2=int(drill_d2_var.get())
                h2=int(drill_h2_var.get())
                x2=int(drill_x2_var.get())
                y2=int(drill_y2_var.get())
                d_3,h3,x3,y3=(0.1,0.1,0.1,0.1)
            elif num_of_holes==3:
                d_1=int(drill_d1_var.get())
                h1=int(drill_h1_var.get())
                x1=int(drill_x1_var.get())
                y1=int(drill_y1_var.get())
                d_2=int(drill_d2_var.get())
                h2=int(drill_h2_var.get())
                x2=int(drill_x2_var.get())
                y2=int(drill_y2_var.get())
                d_3=int(drill_d3_var.get())
                h3=int(drill_h3_var.get())
                x3=int(drill_x3_var.get())
                y3=int(drill_y3_var.get())
            elif num_of_holes<1 or num_of_holes>3:
                screen_func('Number of holes must be a minimum or 1 and maximum 3')
            d=[d_1,d_2,d_3]
            h=[h1,h2,h3]
            x=[x1,x2,x3]
            y=[y1,y2,y3]
            ds=['d_1','d_2','d_3']
            xs=['x1','x2','x3']
            ys=['y1','y2','y3']
            tool_length=['tool_length1','tool_length2','tool_length3']
            hole=['hole1', 'hole2', 'hole3']
            j=0
            for i in range(0,num_of_holes):
                if y[i]>workpiece_length or x[i]>workpiece_width:
                    screen_func('Make sure the X and Y coordinates are within the workpiece dimension')
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
                    j+=1
                    c.interface_export_image(filename=f"{j}"+".jpeg", file_type="JPEG")
                    copy_file(j)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)

        video('drilling.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        drill_time_var.set(str(machining_time)[:6]+" (secs)")
        return

    drill_num_holes_var=StringVar()
    drill_d1_var=StringVar()
    drill_h1_var=StringVar()
    drill_x1_var=StringVar()
    drill_y1_var=StringVar()
    drill_d2_var=StringVar()
    drill_h2_var=StringVar()
    drill_x2_var=StringVar()
    drill_y2_var=StringVar()
    drill_d3_var=StringVar()
    drill_h3_var=StringVar()
    drill_x3_var=StringVar()
    drill_y3_var=StringVar()
    drill_time_var=StringVar()
    drilling_frame = LabelFrame(tab2, text='Drilling', width=500, height=90).grid(column = 0, row = 1,  padx = 30, pady = (10,0))
    drill_num_holes_label = Label(tab2, text = 'Holes:').place(x=40,y=130)
    drill_num_holes_var.set(1)
    drill_num_holes_entry = OptionMenu(tab2,drill_num_holes_var, 1, 2, 3)
    drill_num_holes_entry.place(x=80,y=130, width=40)
    #drill_num_holes_entry.config(validate='key',validatecommand=(reg, '%P'))

    drill_d1_label = Label(tab2, text = 'D1:').place(x=130,y=130)
    drill_d1_entry=Entry(tab2, textvariable = drill_d1_var)
    drill_d1_entry.place(x=150,y=130,width=30)
    drill_d1_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_h1_label = Label(tab2, text = 'H1:').place(x=180,y=130)
    drill_h1_entry=Entry(tab2, textvariable = drill_h1_var)
    drill_h1_entry.place(x=200,y=130, width=30)
    drill_h1_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_x1_label = Label(tab2, text = 'X1:').place(x=230,y=130)
    drill_x1_entry=Entry(tab2, textvariable = drill_x1_var)
    drill_x1_entry.place(x=250,y=130, width=30)
    drill_x1_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_y1_label = Label(tab2, text = 'Y1:').place(x=280,y=130)
    drill_y1_entry=Entry(tab2, textvariable = drill_y1_var)
    drill_y1_entry.place(x=300,y=130, width=30)
    drill_y1_entry.config(validate='key',validatecommand=(reg, '%P'))

    drill_d2_label = Label(tab2, text = 'D2:').place(x=40,y=170)
    drill_d2_entry=Entry(tab2, textvariable = drill_d2_var)
    drill_d2_entry.place(x=60,y=170,width=25)
    drill_d2_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_h2_label = Label(tab2, text = 'H2:').place(x=80,y=170)
    drill_h2_entry=Entry(tab2, textvariable = drill_h2_var)
    drill_h2_entry.place(x=100,y=170,width=25)
    drill_h2_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_x2_label = Label(tab2, text = 'X2:').place(x=120,y=170)
    drill_x2_entry=Entry(tab2, textvariable = drill_x2_var)
    drill_x2_entry.place(x=140,y=170,width=25)
    drill_x2_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_y2_label = Label(tab2, text = 'Y2:').place(x=160,y=170)
    drill_y2_entry=Entry(tab2, textvariable = drill_y2_var)
    drill_y2_entry.place(x=180,y=170,width=25)
    drill_y2_entry.config(validate='key',validatecommand=(reg, '%P'))

    drill_d3_label = Label(tab2, text = 'D3:').place(x=200,y=170)
    drill_d3_entry=Entry(tab2, textvariable = drill_d3_var)
    drill_d3_entry.place(x=220,y=170,width=25)
    drill_d3_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_h3_label = Label(tab2, text = 'H3:').place(x=240,y=170)
    drill_h3_entry=Entry(tab2, textvariable = drill_h3_var)
    drill_h3_entry.place(x=260,y=170,width=25)
    drill_h3_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_x3_label = Label(tab2, text = 'X3:').place(x=280,y=170)
    drill_x3_entry=Entry(tab2, textvariable = drill_x3_var)
    drill_x3_entry.place(x=300,y=170,width=25)
    drill_x3_entry.config(validate='key',validatecommand=(reg, '%P'))
    drill_y3_label = Label(tab2, text = 'Y3:').place(x=320,y=170)
    drill_y3_entry=Entry(tab2, textvariable = drill_y3_var)
    drill_y3_entry.place(x=340,y=170,width=25)
    drill_y3_entry.config(validate='key',validatecommand=(reg, '%P'))

    drill_btn=Button(tab2,text = 'Run', command = drilling,width=12)
    drill_btn.place(x=350,y=130)
    drill_time=Entry(tab2, textvariable = drill_time_var, width=8)
    drill_time.place(x=390,y=170)
    def mymedia_drill():
        if 'drilling.avi' in os.listdir():
            os.startfile(BASE_DIR+"/drilling.avi")
        return
    drill_simulation_btn=Button(tab2,text = 'PLAY', command = mymedia_drill ,width=5, height=3)
    drill_simulation_btn.place(x=470,y=130)


    #Reaming//Boring frame
    def reaming_boring():
        try:
            start=time.time()
            workpiece_length=int(rect_length_var.get())
            workpiece_width=int(rect_width_var.get())
            workpiece_height=int(rect_height_var.get())
            d_1=int(bore_d1_var.get())
            h_1=int(bore_h1_var.get())
            x1=int(bore_x1_var.get())
            y1=int(bore_y1_var.get())
            c=connect_creoson()
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
            c.file_regenerate()
            c.interface_export_image(filename=f"{1}"+".jpeg", file_type="JPEG")
            copy_file(1)
            time.sleep(2)
            c.dimension_set('hole1',0.1)
            c.dimension_set('tool_length1',workpiece_height)
            org_depth=workpiece_height+h_1
            vertical_height=0.1
            i=1
            while vertical_height<org_depth:
                c.dimension_set('hole1',vertical_height)
                vertical_height+=increment
                c.file_regenerate()
                i+=1
                c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                copy_file(i)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        video('reaming_boring.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        bore_time_var.set(str(machining_time)[:6]+" (secs)")
        return

    bore_d1_var=StringVar()
    bore_h1_var=StringVar()
    bore_x1_var=StringVar()
    bore_y1_var=StringVar()
    bore_time_var=StringVar()
    reaming_boring_frame = LabelFrame(tab2, text='Reaming/Boring', width=500, height=90).grid(column = 0, row = 2,  padx = 30, pady = (10,0))
    bore_d1_label = Label(tab2, text = 'Hole Diameter:').place(x=40,y=230)
    bore_d1_entry = Entry(tab2,textvariable = bore_d1_var)
    bore_d1_entry.place(x=130,y=230)
    bore_d1_entry.config(validate='key',validatecommand=(reg, '%P'))
    bore_h1_label = Label(tab2, text = 'Depth:').place(x=40,y=270)
    bore_h1_entry=Entry(tab2, textvariable = bore_h1_var)
    bore_h1_entry.place(x=80,y=270,width=60)
    bore_h1_entry.config(validate='key',validatecommand=(reg, '%P'))
    bore_x1_label = Label(tab2, text = 'X:').place(x=150,y=270)
    bore_x1_entry=Entry(tab2, textvariable = bore_x1_var)
    bore_x1_entry.place(x=170,y=270,width=40)
    bore_x1_entry.config(validate='key',validatecommand=(reg, '%P'))
    bore_y1_label = Label(tab2, text = 'Y:').place(x=200,y=270)
    bore_y1_entry=Entry(tab2, textvariable = bore_y1_var)
    bore_y1_entry.place(x=220,y=270,width=30)
    bore_y1_entry.config(validate='key',validatecommand=(reg, '%P'))

    bore_btn=Button(tab2,text = 'Run', command = reaming_boring,width=20)
    bore_btn.place(x=300,y=230)
    bore_time=Entry(tab2, textvariable = bore_time_var, width=25)
    bore_time.place(x=300,y=270)
    def mymedia_bore():
        if 'reaming_boring.avi' in os.listdir():
            os.startfile(BASE_DIR+"/reaming_boring.avi")
        return
    bore_simulation_btn=Button(tab2,text = 'PLAY', command = mymedia_bore ,width=5, height=3)
    bore_simulation_btn.place(x=470,y=230)


    #Taper Boring frame
    def taper_drill():
        try:
            start=time.time()
            workpiece_length=int(rect_length_var.get())
            workpiece_width=int(rect_width_var.get())
            workpiece_height=int(rect_height_var.get())
            diameter=int(taper_drill_diameter_var.get())
            depth=int(taper_drill_depth_var.get())
            x1=int(taper_drill_X_var.get())
            y1=int(taper_drill_Y_var.get())
            angle=int(taper_drill_angle_var.get())
            c=connect_creoson()
            c.file_open('taper_drill.prt')
            c.view_activate("RUQOYAT")
            c.creo_set_config('display','wireframe')
            if depth>workpiece_height:
                screen_func('Depth of hole cannot be greater than workpiece height')
            else:
                increment=1
                c.dimension_set('length',workpiece_length)
                c.dimension_set('width',workpiece_width)
                c.dimension_set('height',workpiece_height)
                c.dimension_set('diameter',diameter)
                c.dimension_set('x1',x1)
                c.dimension_set('y1',y1)
                c.dimension_set('angle',angle)
                height2=0.1
                i=0
                while height2<depth:
                    c.dimension_set('depth',height2)
                    height2+=increment
                    c.file_regenerate()
                    i+=1
                    c.interface_export_image(filename=f"{i}"+".jpeg", file_type="JPEG")
                    copy_file(i)
        except RuntimeError:
            screen_func('Error! Please try using only values between 50 to 100')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        except (ConnectionError, ConnectionRefusedError, exceptions.NewConnectionError, exceptions.MaxRetryError, ValueError, IndexError, FileNotFoundError):
            screen_func('Error! Please click the restart button and reconnect Creoson Server')
            shutil.rmtree(IMG_DIR)
            os.makedirs(IMG_DIR)
        video('taper_drill.avi')
        shutil.rmtree(IMG_DIR)
        os.makedirs(IMG_DIR)
        end=time.time()
        machining_time=end-start
        taper_drill_time_var.set(str(machining_time)[:6]+" (secs)")
        return

    taper_drill_angle_var=StringVar()
    taper_drill_diameter_var=StringVar()
    taper_drill_depth_var=StringVar()
    taper_drill_X_var=StringVar()
    taper_drill_Y_var=StringVar()
    taper_drill_time_var=StringVar()
    taper_boring_frame = LabelFrame(tab2, text='Taper Boring', width=500, height=90).grid(column = 0, row = 3,  padx = 30, pady = (10,0))
    taper_drill_diameter_label = Label(tab2, text = 'Diameter:').place(x=40,y=330)
    taper_drill_diameter_entry = Entry(tab2, textvariable=taper_drill_diameter_var)
    taper_drill_diameter_entry.place(x=100,y=330,width=50)
    taper_drill_diameter_entry.config(validate='key',validatecommand=(reg, '%P'))
    taper_drill_angle_label = Label(tab2, text = 'Angle:').place(x=160,y=330)
    taper_drill_angle_entry=Entry(tab2, textvariable = taper_drill_angle_var)
    taper_drill_angle_entry.place(x=200,y=330,width=40)
    taper_drill_angle_entry.config(validate='key',validatecommand=(reg, '%P'))

    taper_drill_depth_label = Label(tab2, text = 'Depth: ').place(x=40,y=370)
    taper_drill_depth_entry=Entry(tab2, textvariable = taper_drill_depth_var)
    taper_drill_depth_entry.place(x=85,y=370,width=40)
    taper_drill_depth_entry.config(validate='key',validatecommand=(reg, '%P'))
    taper_drill_X_label = Label(tab2, text = 'X:').place(x=130,y=370)
    taper_drill_X_entry=Entry(tab2, textvariable = taper_drill_X_var)
    taper_drill_X_entry.place(x=150,y=370,width=40)
    taper_drill_X_entry.config(validate='key',validatecommand=(reg, '%P'))
    taper_drill_Y_label = Label(tab2, text = 'Y:').place(x=180,y=370)
    taper_drill_Y_entry=Entry(tab2, textvariable = taper_drill_Y_var)
    taper_drill_Y_entry.place(x=200,y=370,width=40)
    taper_drill_Y_entry.config(validate='key',validatecommand=(reg, '%P'))

    taper_drill_btn=Button(tab2,text = 'Run', command = taper_drill,width=20)
    taper_drill_btn.place(x=300,y=330)
    taper_drill_time=Entry(tab2, textvariable = taper_drill_time_var, width=24)
    taper_drill_time.place(x=300,y=370)
    def mymedia_taper_drill():
        if 'taper_drill.avi' in os.listdir():
            os.startfile(BASE_DIR+"/taper_drill.avi")
        return
    taper_drill_simulation_btn=Button(tab2,text = 'PLAY', command = mymedia_taper_drill ,width=5, height=3)
    taper_drill_simulation_btn.place(x=470,y=330)





    #HOVER
    CreateToolTip(diameter_entry, 'Enter the diameter of the cylindrical workpiece, values between 50 to 100 preferably')
    CreateToolTip(length_entry, 'Enter the length of the cylindrical workpiece, values between 50 to 100 preferably')
    CreateToolTip(plain_depth_entry, 'The depth of cut must be less than workpiece diameter')
    CreateToolTip(plain_length_entry, 'The length of cut must be less than workpiece length')
    CreateToolTip(plain_time, 'Displays the machining time')
    CreateToolTip(taper_time, 'Displays the machining time')
    CreateToolTip(shoulder_time, 'Displays the machining time')
    CreateToolTip(chamfer_time, 'Displays the machining time')
    CreateToolTip(taper_depth_entry, 'The depth of taper must be less than workpiece diameter')
    CreateToolTip(taper_angle_entry, 'Specify the angle at which to cut the taper')
    CreateToolTip(taper_length_entry, 'The length of taper must be less than workpiece length')
    CreateToolTip(num_shoulders_entry, 'Specify the number of shoulders, minimum = 1 and maximum = 3')
    CreateToolTip(sd1_entry, 'Specify the diameter of first shoulder')
    CreateToolTip(sd2_entry, 'Specify the diameter of second shoulder (ignore if n/a)')
    CreateToolTip(sd3_entry, 'Specify the diameter of third shoulder (ignore if n/a)')
    CreateToolTip(sl1_entry, 'Specify the length of first shoulder')
    CreateToolTip(sl2_entry, 'Specify the length of second shoulder (ignore if n/a)')
    CreateToolTip(sl3_entry, 'Specify the length of third shoulder (ignore if n/a)')
    CreateToolTip(chamfer_hor_entry, 'The value must be less than half the workpiece diameter')
    CreateToolTip(chamfer_ver_entry, 'The value must be less than the workpiece length')
    CreateToolTip(rect_length_entry, 'Enter the Length of the rectangular workpiece, values between 50 to 100 preferably')
    CreateToolTip(rect_width_entry, 'Enter the Width of the rectangular workpiece, values between 50 to 100 preferably')
    CreateToolTip(rect_height_entry, 'Enter the Height of the rectangular workpiece')
    CreateToolTip(drill_num_holes_entry, 'Enter the number of holes to drill, minimum=1 and maximum=3')
    CreateToolTip(drill_d1_entry, 'Specify the diameter of the first hole')
    CreateToolTip(drill_h1_entry, 'Specify the depth of the first hole')
    CreateToolTip(drill_x1_entry, 'Specify the X coordinate of the first hole relative to workpiece width')
    CreateToolTip(drill_y1_entry, 'Specify the Y coordinate of the first hole relative to workpiece length')
    CreateToolTip(drill_d2_entry, 'Specify the diameter of the second hole (ignore if n/a)')
    CreateToolTip(drill_h2_entry, 'Specify the depth of the second hole (ignore if n/a)')
    CreateToolTip(drill_x2_entry, 'Specify the X coordinate of the second hole (ignore if n/a)')
    CreateToolTip(drill_y2_entry, 'Specify the Y coordinate of the second hole (ignore if n/a)')
    CreateToolTip(drill_d3_entry, 'Specify the diameter of the third hole (ignore if n/a)')
    CreateToolTip(drill_h3_entry, 'Specify the depth of the third hole (ignore if n/a)')
    CreateToolTip(drill_x3_entry, 'Specify the X coordinate of the third hole (ignore if n/a)')
    CreateToolTip(drill_y3_entry, 'Specify the Y coordinate of the third hole (ignore if n/a)')
    CreateToolTip(bore_d1_entry, 'Specify the diameter of the exiting hole to bore')
    CreateToolTip(bore_h1_entry, 'Specify the depth of the existing hole to bore')
    CreateToolTip(bore_x1_entry, 'Specify the X coordinate of the hole relative to workpiece width')
    CreateToolTip(bore_y1_entry, 'Specify the X coordinate of the hole relative to workpiece length')
    CreateToolTip(taper_drill_diameter_entry, 'Specify the diameter of the hole')
    CreateToolTip(taper_drill_depth_entry, 'Depth of hole cannot be moore than workpiece height')
    CreateToolTip(taper_drill_angle_entry, 'Specify the taper angle')
    CreateToolTip(taper_drill_X_entry, 'Specify the X coordinate of the hole')
    CreateToolTip(taper_drill_Y_entry, 'Specify the Y coordinate of the hole')







    window.mainloop()

if __name__=='__main__':
    def refresh():
        window.destroy()
        os.system('gui.py')
        sys.exit()
        vp_start_gui()
    
    vp_start_gui()