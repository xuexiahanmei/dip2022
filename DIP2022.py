# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 10:30:53 2018
 
形態學操作就是改變物體的形狀，如腐蝕使物體"變瘦"，膨脹使物體"變胖"
先腐蝕後膨脹會分離物體，所以叫開運算，常用來去除小區域物體
先膨脹後腐蝕會消除物體內的小洞，所以叫閉運算
img_path = asksaveasfilename(initialdir = file_path, 
              filetypes=[("jpg格式","jpg"), ("png格式","png"), ("bmp格式","bmp")],
              parent = self.root,
              title = '儲存影像')
"""
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
import imutils
from collections import deque
from skimage import morphology
import scipy.special as special
import matplotlib.pyplot as plt
from skimage import util
import keyboard
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename  
import cv2
import numpy as np
import datetime
file_path = os.path.dirname(__file__)
test_file_path = 'D:/images/lena_std_512.jpg'
WIN_WIDTH = 1224
WIN_HEIGHT = 672
class Image_sys():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1224x672+80+80')
        self.root.title('數位影像處理-2022')#設置視窗標題
       # self.root.iconbitmap('./icon.ico')# 設置視窗圖示
        #scnWidth, scnHeight = self.root.maxsize()
        # 螢幕中心居中
        #center = '%dx%d %d %d' % (WIN_WIDTH, WIN_HEIGHT, (scnWidth - WIN_WIDTH) / 2, (scnHeight - WIN_HEIGHT) / 2)
        #print(center)
        # 設置視窗的大小寬x高 偏移量
        #self.root.geometry(center)
        # 調用方法會禁止根表單改變大小
        self.root.resizable(False, False)
                 
        menubar = tk.Menu(self.root)# 創建功能表列 (Menu)
        self.root.config(menu = menubar)
         
        # 創建文件下拉式功能表
        # 檔菜單下 tearoff=0 表示有沒有分隔符號，默認為有分隔符號
        file_menu = tk.Menu(menubar, tearoff = 0)
        #為頂級功能表實例添加功能表，並級聯相應的子功能表實例
        menubar.add_cascade(label = "影像", menu = file_menu)
        file_menu.add_command(label = "打開測試影像", command = self.open_test_file)
        file_menu.add_command(label = "打開自訂影像", command = self.open_file)
        file_menu.add_command(label = "儲存目標影像", command = self.save_file)
        file_menu.add_command(label = "復原", command = self.recover)
        file_menu.add_command(label = "清除", command = self.clear)
        file_menu.add_command(label = "退出", command = self.exit_sys)
         
        # 創建文件下拉式功能表
        video_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "視訊", menu = video_menu)
        video_menu.add_command(label = "視訊檔播放", command = self.video_player)
        video_menu.add_command(label = "Cam 攝影", command = self.cam_record)
        video_menu.add_command(label = "Cam 照相", command = self.cam_snapshot)
        
        # 強化
        turn_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "強化", menu = turn_menu)
        turn_menu.add_command(label = "影像負片", command = self.image_negative)
        turn_menu.add_command(label = "灰階直方圖", command = self.gray_histogram)
        turn_menu.add_command(label = "色平面直方圖", command = self.color_histogram)
        turn_menu.add_command(label = "曝光&對比強化:直方圖等化", command =self.histogram_equalization)
        turn_menu.add_command(label = "曝光加強:對數(gamma02)轉換", command =self.log_transformation)
        turn_menu.add_command(label = "曝光加強:gamma01 轉換", command =self.gamma01_transformation)
        turn_menu.add_command(label = "曝光加強:gamma05 轉換", command =self.gamma05_transformation)
        turn_menu.add_command(label = "曝光減弱:gamma12 轉換", command =self.gamma12_transformation)
        turn_menu.add_command(label = "曝光減弱:gamma22 轉換", command =self.gamma22_transformation)
        turn_menu.add_command(label = "對比柔化:beta0505 轉換", command =self.beta0505_transformation)
        turn_menu.add_command(label = "對比銳化:beta2020 轉換", command =self.beta2020_transformation)
        
        # 創建翻轉下拉式功能表
        turn_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "翻轉", menu = turn_menu)
        turn_menu.add_command(label = "水平", command = self.flip_horizontal)
        turn_menu.add_command(label = "垂直", command = self.flip_vertical)
        turn_menu.add_command(label = "水平&垂直", command = self.flip_hor_ver)
 
        # 形態學
        morph_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "形態學", menu = morph_menu)
        morph_menu.add_command(label = "腐蝕", command = self.mor_corrosion)
        morph_menu.add_command(label = "膨脹", command = self.mor_expand)
        morph_menu.add_command(label = "開運算", command = self.mor_open_operation)
        morph_menu.add_command(label = "閉運算", command = self.mor_close_operation)
        morph_menu.add_command(label = "型態梯度", command = self.mor_gradient)
        morph_menu.add_command(label = "頂帽", command = self.mor_top_hat)
        morph_menu.add_command(label = "黑帽", command = self.mor_black_hat)
        morph_menu.add_command(label = "取骨架_白底", command = self.mor_whiteskelton)
        morph_menu.add_command(label = "取骨架_黑底", command = self.mor_blackskelton)
        morph_menu.add_command(label = "細線化_白底", command = self.mor_whitethinning)
        morph_menu.add_command(label = "細線化_黑底", command = self.mor_blackthinning)
        
        
        # 雜訊
        noise_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "雜訊", menu = noise_menu)
        noise_menu.add_command(label = "高斯雜訊", command = lambda: self.noise_pic(1))
        noise_menu.add_command(label = "區域異變數雜訊", command = lambda: self.noise_pic(2))
        noise_menu.add_command(label = "波義森雜訊", command = lambda: self.noise_pic(3))
        noise_menu.add_command(label = "鹽雜訊", command = lambda: self.noise_pic(4))
        noise_menu.add_command(label = "胡椒雜訊", command = lambda: self.noise_pic(5))
        noise_menu.add_command(label = "胡椒鹽雜訊", command = lambda: self.noise_pic(6))
        noise_menu.add_command(label = "史培克雜訊", command = lambda: self.noise_pic(7))
        
        
 
        # 濾波-平滑模糊
        blur_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "濾波-平滑模糊", menu = blur_menu)
        blur_menu.add_command(label = "均值 3x3", command = self.filter_mean3)
        blur_menu.add_command(label = "均值 5x5", command = self.filter_mean5)
        blur_menu.add_command(label = "均值 7x7", command = self.filter_mean7)
        blur_menu.add_command(label = "均值 9x9", command = self.filter_mean9)
        blur_menu.add_command(label = "均值 11x11", command = self.filter_mean11)
        blur_menu.add_command(label = "均值 15x15", command = self.filter_mean15)
        blur_menu.add_command(label = "均值 21x21", command = self.filter_mean21)
        blur_menu.add_command(label = "方框 3x3nf", command = self.filter_box3nf)
        blur_menu.add_command(label = "方框 3x3nt", command = self.filter_box3nt)
        blur_menu.add_command(label = "高斯 3x3", command = self.filter_gauss3)
        blur_menu.add_command(label = "高斯 5x5", command = self.filter_gauss5)
        blur_menu.add_command(label = "高斯 7x7", command = self.filter_gauss7)
        blur_menu.add_command(label = "高斯 9x9", command = self.filter_gauss9)
        blur_menu.add_command(label = "高斯 11x11", command = self.filter_gauss11)
        blur_menu.add_command(label = "高斯 15x15", command = self.filter_gauss15)
        blur_menu.add_command(label = "高斯 21x21", command = self.filter_gauss21)
        blur_menu.add_command(label = "中值 3", command = self.filter_mid3)
        blur_menu.add_command(label = "中值 5", command = self.filter_mid5)
        blur_menu.add_command(label = "中值 7", command = self.filter_mid7)
        blur_menu.add_command(label = "中值 9", command = self.filter_mid9)
        blur_menu.add_command(label = "中值 11", command = self.filter_mid11)
        blur_menu.add_command(label = "中值 15", command = self.filter_mid15)
        blur_menu.add_command(label = "中值 21", command = self.filter_mid21)
        blur_menu.add_command(label = "雙邊 37575", command = self.filter_bilateral37575)
        blur_menu.add_command(label = "雙邊 57575", command = self.filter_bilateral57575)
        blur_menu.add_command(label = "雙邊 77575", command = self.filter_bilateral77575)
        blur_menu.add_command(label = "雙邊 97575", command = self.filter_bilateral97575)
        blur_menu.add_command(label = "雙邊 117575", command = self.filter_bilateral117575)
        blur_menu.add_command(label = "雙邊 157575", command = self.filter_bilateral157575)
        blur_menu.add_command(label = "雙邊 217575", command = self.filter_bilateral217575)
        
        # 濾波-梯度邊緣銳化
        sharp_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "濾波-梯度邊緣銳化", menu = sharp_menu)
        sharp_menu.add_command(label = "SobelGx", command = self.filter_sobelGx)
        sharp_menu.add_command(label = "SobelGy", command = self.filter_sobelGy)
        sharp_menu.add_command(label = "PrewittGx", command = self.filter_prewittGx)
        sharp_menu.add_command(label = "PrewittGy", command = self.filter_prewittGy)
        sharp_menu.add_command(label = "FreiChenGx", command = self.filter_freichenGx)
        sharp_menu.add_command(label = "FreiChenGy", command = self.filter_freichenGy)        
        sharp_menu.add_command(label = "ScharrGx", command = self.filter_scharrGx)
        sharp_menu.add_command(label = "ScharrGy", command = self.filter_scharrGy)
        sharp_menu.add_command(label = "Laplacian3x3-01", command = self.filter_laplacian3301)
        sharp_menu.add_command(label = "Laplacian3x3-02", command = self.filter_laplacian3302)
        sharp_menu.add_command(label = "Laplacian3x3-03", command = self.filter_laplacian3303)
        sharp_menu.add_command(label = "Laplacian5x5", command = self.filter_laplacian55)
        sharp_menu.add_command(label = "Laplacian7x7", command = self.filter_laplacian77)
        sharp_menu.add_command(label = "Laplacian9x9", command = self.filter_laplacian99)
        sharp_menu.add_command(label = "Canny", command = self.filter_canny)
        sharp_menu.add_command(label = "EdgeSharp3x3-01", command = self.filter_edgesharp3301)
        sharp_menu.add_command(label = "EdgeSharp3x3-02", command = self.filter_edgesharp3302)
        sharp_menu.add_command(label = "EdgeSharp3x3-03", command = self.filter_edgesharp3303)
        sharp_menu.add_command(label = "EdgeSharp5x5", command = self.filter_edgesharp55)
        sharp_menu.add_command(label = "EdgeSharp7x7", command = self.filter_edgesharp77)
        
        # 縮放
        scale_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "縮放", menu = scale_menu)
        scale_menu.add_command(label = "放大PyrUp", command = self.scale_pyrup)
        scale_menu.add_command(label = "縮小PyrDown", command = self.scale_pyrdown)
        scale_menu.add_command(label = "放大Resize", command = self.scale_zoom_in)
        scale_menu.add_command(label = "縮小Resize", command = self.scale_zoom_out)
 
        # 旋轉
        rotate_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "旋轉", menu = rotate_menu)
        rotate_menu.add_command(label = "平移", command = self.rotate_offset)
        rotate_menu.add_command(label = "仿射", command = self.rotate_affine)
        rotate_menu.add_command(label = "透射", command = self.rotate_transmission)
        rotate_menu.add_command(label = "順時針-無縮放", command = self.rotate_clockwise)
        rotate_menu.add_command(label = "順時針-縮放", command = self.rotate_clockwise_zoom)
        rotate_menu.add_command(label = "逆時針-縮放", command = self.rotate_anti_zoom)
        rotate_menu.add_command(label = "零旋轉-縮放", command = self.rotate_zero_zoom)
        
        # 色彩檢測
        color_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "色彩檢測", menu = color_menu)
        color_menu.add_command(label = "五行色彩檢測", command = self.color_5)
        color_menu.add_command(label = "紅球追蹤", command = self.redball_tracking)
        
        
        # 即時影像處理
        video_real_time_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Video 即時影像處理", menu = video_real_time_menu)
        video_real_time_menu.add_command(label = "Video_SobelX", command = lambda: self.video_real_time_fun(1))
        video_real_time_menu.add_command(label = "Video_SobelY ", command = lambda: self.video_real_time_fun(2))
        video_real_time_menu.add_command(label = "Video_Laplacian", command = lambda: self.video_real_time_fun(3))
        video_real_time_menu.add_command(label = "Video_Canny", command = lambda: self.video_real_time_fun(4))

        
        # CAM 即時影像處理
        cam_real_time_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "CAM 即時影像處理", menu = cam_real_time_menu)
        cam_real_time_menu.add_command(label = "CAM_SobelX", command = lambda: self.cam_real_time_fun(1))
        cam_real_time_menu.add_command(label = "CAM_SobelY ", command = lambda: self.cam_real_time_fun(2))
        cam_real_time_menu.add_command(label = "CAM_Laplacian", command = lambda: self.cam_real_time_fun(3))
        cam_real_time_menu.add_command(label = "CAM_Canny", command = lambda: self.cam_real_time_fun(4))
        
        
        # 人臉檢測
        face_detection_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "人臉檢測", menu = face_detection_menu)
        face_detection_menu.add_command(label = "影像人臉檢測", command = self.picture_face)
        face_detection_menu.add_command(label = "視訊檔人臉檢測 ", command = self.video_face)
        face_detection_menu.add_command(label = "攝影機人臉檢測", command = self.cam_face)
        
        
 
        # 幫助
        help_menu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "幫助", menu = help_menu)
        help_menu.add_command(label = "版權", command = self.help_copyright)
        help_menu.add_command(label = "關於", command = self.help_about)                
         
  
        # 創建一個容器,其父容器為self.root
        self.frame_scr = ttk.LabelFrame(self.root, text="Source image") 
        # padx  pady   該容器週邊需要留出的空餘空間
        self.frame_scr.place(x = 80, y = 50, width = 512, height  = 512) 
       
        # 創建一個容器,其父容器為self.root
        self.frame_des = ttk.LabelFrame(self.root, text="Destination image") 
        # padx  pady   該容器週邊需要留出的空餘空間
        self.frame_des.place(x = 632, y = 50, width = 512, height  = 512)    
 
 
        # 創建兩個label
        label_scr = ttk.Label(self.root, text = '來源影像', font = 25, foreground = 'blue', anchor = 'center')
        label_scr.place(x = 80, y = 562, width = 100, height  = 50)
        
        label_des = ttk.Label(self.root, text = '目標影像', font = 25, foreground = 'blue', anchor = 'center')
        label_des.place(x = 632, y = 562, width = 100, height  = 50)
         
         
        self.label_scr_image = None
        self.label_des_image = None          
        self.path = ''           
        self.root.mainloop()    
    
        
        
    def des1(self):
        image_pil = Image.fromarray(self.image)
        tk_image = ImageTk.PhotoImage(image_pil)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
             
    def open_test_file(self):
        self.path = test_file_path
        image = Image.open(self.path)
        test_image = ImageTk.PhotoImage(image)
        if(self.label_des_image != None):
            self.label_des_image.pack_forget()# 隱藏控制項
            self.label_des_image = None
        if(self.label_scr_image == None):
            self.label_scr_image = tk.Label(self.frame_scr,image = test_image)
        self.label_scr_image.configure(image=test_image)
        self.label_scr_image.pack()
        self.root.mainloop()
   
    def open_file(self):
        # 打開文件對話方塊
        open_img_path =askopenfilename(initialdir = file_path, 
               filetypes=[("jpg格式","jpg"), ("png格式","png"), ("bmp格式","bmp")],
               parent = self.root,
               title = '打開自訂影像')
        if (open_img_path == ''):
            return
        else:                
            if(self.label_des_image != None):
                self.label_des_image.pack_forget()# 隱藏控制項
                self.label_des_image = None
            self.path =  open_img_path
            image = Image.open(self.path)
            tk_image = ImageTk.PhotoImage(image)
            if(self.label_scr_image == None):
                self.label_scr_image = tk.Label(self.frame_scr,image = tk_image)
            self.label_scr_image.configure(image = tk_image)
            self.label_scr_image.pack() # 顯示控制項
            self.root.mainloop()
    
    def save_file(self):
        # 開啟存檔黨對話方塊
        save_img_path = asksaveasfilename(initialdir = file_path, 
              filetypes=[("jpg格式","jpg"), ("png格式","png"), ("bmp格式","bmp")],
              parent = self.root,
              title = '儲存目標影像')  
        if (save_img_path == ''):
            return
        else:                
            if(self.label_des_image == None):
                return
            image = self.image
            img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename=save_img_path, img=img)
            self.root.mainloop()

    def recover(self):
        if(self.path == ''):
            return       
        image = Image.open(self.path)
        tk_image = ImageTk.PhotoImage(image)
        if(self.label_des_image == None):
            return
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def clear(self):
        if(self.label_scr_image != None):
            self.label_scr_image.pack_forget()# 隱藏控制項
            self.label_scr_image = None
            self.path = ''
        if(self.label_des_image != None):
            self.label_des_image.pack_forget()# 隱藏控制項
            self.label_des_image = None
            self.path = ''
        try: 
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.destroy()
        except AttributeError: 
            pass 
        
            
    def exit_sys(self):
        quit_root = messagebox.askokcancel('提示', '確定要退出嗎?')
        if (quit_root == True):
            self.root.destroy()
            return
    
    
    def video_player(self):
        # 開啟開檔對話方塊
        open_video_path = askopenfilename(initialdir = file_path,
                                         filetypes=[('AVI', '*.avi'), ('MP4', '*.mp4'), ('MKV', '*.mkv'), ('All Files','*')],
                                         parent = self.root,
                                         title = '開啟視訊檔')
        if (open_video_path == ''):
            print("Can not open video file!")
            return
        else:
            self.i = 0
            self.path = open_video_path
            # Create a VideoCapture object and read from input file
            self.cap = cv2.VideoCapture(self.path)
            # 創建一個按鈕,，按下按鈕 , 會將當下的畫面存檔
            self.btn = ttk.Button(self.root, text="拍照-Snapshot",command=self.take_snapshot)
            self.btn.place(x = 512, y = 620, width = 200, height = 30)
            self.snap = 0 
            self.rw = 0
            self.video_loop()
            self.root.mainloop()

    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, self.frame = self.cap.read() # read frame from video stream
        self.frame = cv2.flip(self.frame, 1)
        if keyboard.is_pressed("q"):
            """if not os.path.isfile(format(self.path)) and self.snap == 0:
                print("Can not save video file!")"""
            self.btn.destroy()
            self.clear()
            ok = 0
            if self.rw == 1 :
                self.cap.release()
                if self.snap == 0:
                    self.out.release()
            self.root.mainloop()
        if keyboard.is_pressed("s"):
            if self.rw == 0:
                self.take_snapshot()
                cv2.waitKey(180)
            else:
                print("Can not take snapshot!")
        if ok: # frame captured without any errors
            if self.rw == 1:
                self.out.write(self.frame)
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA) # convert colorsfrom BGR to RGBA
            self.current_image = Image.fromarray(cv2image) # convert image for PIL
            tk_image = ImageTk.PhotoImage(image=self.current_image) # convert image for tkinter
            if(self.label_scr_image == None):
                self.label_scr_image = tk.Label(self.frame_scr,image = tk_image) #initialize image panel
            self.label_scr_image.tk_image = tk_image # anchor tk_image so it does not be deleted by garbage-collector
            self.label_scr_image.configure(image = tk_image) # show the image
            self.label_scr_image.pack() # 顯示控制項
            self.root.after(10, self.video_loop) # call the same function after 10 milliseconds
        else:
            pass
            
    def cam_record(self):
        self.output_path = "D:\images\cam-record"
        """ Take datetime to make the output file name """
        ts = datetime.datetime.now() # grab the current timestamp
        filename = "{}.mp4".format(ts.strftime("%Y-%m-%d_%H-%M-%S")) # construct filename
        self.output_path = os.path.join(self.output_path, filename) # construct output path
        if(self.output_path == ''):
            print("[INFO] {} can not be saved.".format(filename))
            return
        else:
            # 創建一個按鈕,，按下按鈕 , 會將當下的畫面存檔
            self.btn = ttk.Button(self.root, text="拍照-Snapshot",command=self.take_snapshot)
            self.btn.place(x = 512, y = 620, width = 200, height = 30)
            self.path = self.output_path
            # capture video frames, 0 is your default video camera
            self.cap = cv2.VideoCapture(0)
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(self.path,fourcc, 15.0, (640,480))
            self.i = 0
            self.snap = 0
            self.rw = 1
            # 將照片持續寫入影音檔
            print("[INFO] {} is saving ...".format(self.path))
            self.video_loop()
            # Release everything if job is finished
            self.root.mainloop()
        self.cap.release()
        self.out.release()

    def video_capture(self):
        self.cap = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        self.rw = 0
        self.video_loop()
        self.root.mainloop()

    def cam_snapshot(self):
        # 創建一個按鈕,，按下按鈕 , 會將當下的畫面存檔
        self.btn = ttk.Button(self.root, text="拍照-Snapshot", command=self.take_snapshot)
        self.btn.place(x = 512, y = 620, width = 200, height = 30)
        self.i = 0
        self.rw = 0
        self.snap = 1 #snap模式
        self.video_capture()
        # btn.pack_forget() # 按鈕先隱藏，必要時才顯現

    def take_snapshot(self):
        self.output_path = "D:\images\cam-snapshot"
        """ Take snapshot and save it to the file """
        #ts = datetime.datetime.now() # grab the current timestamp
        self.i=self.i+1
        filename = "{}.jpg".format(self.i) # construct filename
        p = os.path.join(self.output_path, filename) # construct output path
        image = self.current_image
        img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
        cv2.imwrite(p, img=img)
        print("[INFO] saved {}".format(p))
        tk_image = ImageTk.PhotoImage(image=self.current_image) # convert image for tkinter
        if(self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image) #initialize image panel
        self.label_des_image.tk_image = tk_image # anchor tk_image so it does not be deleted by garbage-collector
        self.label_des_image.configure(image = tk_image) # show the image
        self.label_des_image.pack() # 顯示控制項
        if not os.path.isfile(format(p)):
            print("Can not save picture frame!")
    
    def image_negative(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        if(self.label_des_image != None):
            self.label_des_image.pack_forget()# 隱藏控制項
            self.label_des_image = None
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        rows = image.shape[0]
        cols = image.shape[1]
        for r in range(rows):
            for c in range(cols):
                image[r, c, 0] = 255-image[r, c, 0]
                image[r, c, 1] = 255-image[r, c, 1]
                image[r, c, 2] = 255-image[r, c, 2]
        self.image = image
        self.des1()
               
    def gray_histogram(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        if(self.label_des_image != None):
            self.label_des_image.pack_forget()# 隱藏控制項
            self.label_des_image = None
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# 轉為灰階圖片
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.hist(gray.ravel(), 256, [0, 256])
        a.set_title ("gray histogram", fontsize=16)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_des)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_des)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        
        
    def color_histogram(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        color = ('b','g','r')
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        for i, col in enumerate(color):
            histr = cv2.calcHist([image],[i],None,[256],[0, 256])
            a.plot(histr, color = col)
            #a.xlim([0, 256])
        a.set_title ("Histogram", fontsize=16)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_des)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_des)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        
    def histogram_equalization(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        # 對每一個通道均衡化
        bH = cv2.equalizeHist(b)
        gH = cv2.equalizeHist(g)
        rH = cv2.equalizeHist(r)
        image = cv2.merge([rH,gH,bH])# 三通道合併
        self.image = image
        self.des1()
        
    def log_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        invgamma = 1/5
        brighter_image = np.array(np.power((image/225),invgamma)*225,dtype=np.uint8)
        self.image = brighter_image
        self.des1()
        
    def gamma01_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        invgamma = 0.1
        brighter_image = np.array(np.power((image/225),invgamma)*225,dtype=np.uint8)
        self.image = brighter_image
        self.des1()
        
    def gamma05_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        invgamma = 0.5
        brighter_image = np.array(np.power((image/225),invgamma)*225,dtype=np.uint8)
        self.image = brighter_image
        self.des1()
        
    def gamma12_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        brighter_image = np.power(image/float(np.max(image)),1.2)
        self.image = (brighter_image * 255).astype('uint8') 
        self.des1()
        
    def gamma22_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        brighter_image = np.power(image/float(np.max(image)),2.2)
        self.image = (brighter_image * 255).astype('uint8') 
        self.des1()
        
    def beta0505_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        a = b = 0.5
        g = image.copy( )
        nr, nc = image.shape[:2]
        x = np.linspace( 0, 1, 256 )
        table = np.round( special.betainc( a, b, x ) * 255, 0 )
        if image.ndim != 3:
            for x in range(nr):
                for y in range(nc):
                    g[x,y] = table[image[x,y]]
        else:
            for x in range( nr ):
                for y in range( nc ):
                     for k in range( 3 ):
                         g[x,y,k] = table[image[x,y,k]]
        self.image = g
        self.des1()
        
    def beta2020_transformation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        a = b = 2.0
        g = image.copy( )
        nr, nc = image.shape[:2]
        x = np.linspace( 0, 1, 256 )
        table = np.round( special.betainc( a, b, x ) * 255, 0 )
        if image.ndim != 3:
            for x in range(nr):
                for y in range(nc):
                    g[x,y] = table[image[x,y]]
        else:
            for x in range( nr ):
                for y in range( nc ):
                     for k in range( 3 ):
                         g[x,y,k] = table[image[x,y,k]]
        self.image = g
        self.des1()
    
    
 
    def flip_horizontal(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return       
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        # Flipped Horizontally 水準翻轉
        image_hflip = cv2.flip(image, 1)
        image_pil_hflip = Image.fromarray(image_hflip)
        tk_image = ImageTk.PhotoImage(image_pil_hflip)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = image_hflip
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def flip_vertical(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return       
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        # Flipped Horizontally 水準翻轉
        image_hflip = cv2.flip(image, 0)# 垂直翻轉
        image_pil_hflip = Image.fromarray(image_hflip)
        tk_image = ImageTk.PhotoImage(image_pil_hflip)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = image_hflip
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop() 
     
    def flip_hor_ver(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return       
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        # Flipped Horizontally 水準翻轉
        image_hflip = cv2.flip(image, -1)# 水準垂直翻轉
        image_pil_hflip = Image.fromarray(image_hflip)
        tk_image = ImageTk.PhotoImage(image_pil_hflip)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = image_hflip
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
     # 腐蝕
    def mor_corrosion(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #kernel = np.ones((5, 5), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_erosion = cv2.erode(image, kernel)  # 腐蝕
        image_pil_erosion = Image.fromarray(img_erosion)
        tk_image = ImageTk.PhotoImage(image_pil_erosion)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_erosion
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()                
    # 膨脹    
    def mor_expand(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #kernel = np.ones((5, 5), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_dilation = cv2.dilate(image, kernel) # 膨脹
        image_pil_dilation = Image.fromarray(img_dilation)
        tk_image = ImageTk.PhotoImage(image_pil_dilation)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_dilation
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop() 
    # 開運算    
    def mor_open_operation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #kernel = np.ones((5, 5), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_open_operation = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)  # 開運算
        image_pil_open = Image.fromarray(img_open_operation)
        tk_image = ImageTk.PhotoImage(image_pil_open)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_open_operation
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop() 
    # 閉運算    
    def mor_close_operation(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #kernel = np.ones((5, 5), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_close_operation = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)# 閉運算
        image_pil_close = Image.fromarray(img_close_operation)
        tk_image = ImageTk.PhotoImage(image_pil_close)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_close_operation
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
    # 形態學梯度：膨脹圖減去腐蝕圖，dilation - erosion，這樣會得到物體的輪廓：
    def mor_gradient(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #kernel = np.ones((5, 5), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel) # 形態學梯度
        image_pil_gradient = Image.fromarray(img_gradient)
        tk_image = ImageTk.PhotoImage(image_pil_gradient)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gradient
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
    # 頂帽    
    def mor_top_hat(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        kernel = np.ones((7, 7), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_top_hat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel) # 頂帽
        image_pil_top_hat = Image.fromarray(img_top_hat)
        tk_image = ImageTk.PhotoImage(image_pil_top_hat)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_top_hat
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
    # 黑帽    
    def mor_black_hat(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        kernel = np.ones((7, 7), np.uint8)# 指定核大小
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 橢圓結構
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形結構
        img_black_hat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel) # 黑帽
        image_pil_black_hat = Image.fromarray(img_black_hat)
        tk_image = ImageTk.PhotoImage(image_pil_black_hat)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_black_hat
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
              
    # 取骨架白底 
    def mor_whiteskelton(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        img = cv2.imread(self.path, 0)   # 讀取圖片
        img = cv2.medianBlur(img,11)   # 將圖片做模糊化，可以取除雜訊
        binary2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,171,2)
        binary2[binary2==255] = 1
        skeleton02 = morphology.skeletonize(binary2)   # 骨架提取
        skeleton2 = skeleton02.astype(np.uint8)*255
        self.image = skeleton2
        self.des1()
        
    # 取骨架黑底
    def mor_blackskelton(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        img = cv2.imread(self.path, 0)   # 讀取圖片
        img = cv2.medianBlur(img,11)   # 將圖片做模糊化，可以取除雜訊
        binary2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,171,2)
        binary2[binary2==255] = 1
        skeleton02 = morphology.skeletonize(binary2)   # 骨架提取
        skeleton2 = skeleton02.astype(np.uint8)*255
        self.image = skeleton2
        self.des1()      
        
    # 細線化白底
    def mor_whitethinning(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        img = cv2.imread(self.path, 0)   # 讀取圖片
        img = cv2.medianBlur(img,11)   # 將圖片做模糊化，可以取除雜訊
        binary2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,171,2)
        binary2[binary2==255] = 1
        thin02 = morphology.thin(binary2)              # 細線化
        thin2 = thin02.astype(np.uint8)*255
        self.image = thin2
        self.des1()
        
    # 細線化黑底
    def mor_blackthinning(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        img = cv2.imread(self.path, 0)   # 讀取圖片
        img = cv2.medianBlur(img,11)   # 將圖片做模糊化，可以取除雜訊
        binary2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,171,2)
        binary2[binary2==255] = 1
        thin02 = morphology.thin(binary2)              # 細線化
        thin2 = thin02.astype(np.uint8)*255
        self.image = thin2
        self.des1()   
      
    """-------------------------------------------------------------------------"""
        
        
    def noise_pic(self,a):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img = np.asarray(image)
        if a == 1:
            #加上高斯雜訊
            noise_gs_img = util.random_noise(img,mode='gaussian')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        elif a == 2 :
            #加上區域異變數雜訊
            noise_gs_img = util.random_noise(img,mode='localvar')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        elif a == 3 :
            #加上波義森雜訊
            noise_gs_img = util.random_noise(img,mode='poisson')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        elif a == 4 :
            #加上鹽雜訊
            noise_gs_img = util.random_noise(img,mode='salt')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        elif a == 5 :
            #加上胡椒雜訊
            noise_gs_img = util.random_noise(img,mode='pepper')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        elif a == 6 :
            #加上鹽胡椒雜訊
            noise_gs_img = util.random_noise(img,mode='s&p')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        elif a == 7 :
            #加上史培克雜訊
            noise_gs_img = util.random_noise(img,mode='speckle')
            image_noise = (255*noise_gs_img).astype(np.uint8)
        else:
            pass
        self.image = image_noise
        image_pil_noise = Image.fromarray(image_noise)
        tk_image = ImageTk.PhotoImage(image_pil_noise)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()  
    
    
    """-------------------------------------------------------------------------"""
    '''
    常見雜訊有椒鹽雜訊和高斯雜訊，椒鹽雜訊可以理解為斑點，
    隨機出現在圖像中的黑點或白點；
    高斯雜訊可以理解為拍攝圖片時由於光照等原因造成的雜訊；
    這樣解釋並不準確，只要能簡單分辨即可。
    '''
    # 均值濾波3
    def filter_mean3(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (3, 3)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       
    # 均值濾波5
    def filter_mean5(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (5, 5)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       
    # 均值濾波7
    def filter_mean7(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (7, 7)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       
    # 均值濾波9
    def filter_mean9(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (9, 9)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       
    # 均值濾波11
    def filter_mean11(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (11, 11)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       
    # 均值濾波15
    def filter_mean15(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (15, 15)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       
    # 均值濾波21
    def filter_mean21(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mean = cv2.blur(image, (21, 21)) # 均值濾波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mean
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
       

    # 方框濾波方框濾波跟均值濾波很像，當可選參數normalize為True的時候，
    # 方框濾波就是均值濾波，
    # 如3×3的核，a就等於1/9；
    # normalize為False的時候，a=1，相當於求區域內的圖元和。
    #參數 normalize 的值設置為 0，卷積核大小設置成 2×2
    def filter_box3nf(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_box = cv2.boxFilter(image, -1, (3, 3), normalize = False) # 方框濾波
        image_pil_box = Image.fromarray(img_box)
        tk_image = ImageTk.PhotoImage(image_pil_box)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_box
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()


    #參數 normalize 的值設置為 1，卷積核大小設置成 2×2
    def filter_box3nt(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_box = cv2.boxFilter(image, -1, (3, 3), normalize = 1) # 方框濾波
        image_pil_box = Image.fromarray(img_box)
        tk_image = ImageTk.PhotoImage(image_pil_box)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_box
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
     
    #高斯濾波與兩種濾波方式，卷積核內的每個值都一樣，
    #相當於圖像區域中每個圖元的權重也就一樣。
    #高斯濾波的卷積核權重並不相同，中間圖元點權重最高，
    #越遠離中心的圖元權重越小。
    #高斯濾波相比均值濾波效率要慢，但可以有效消除高斯雜訊，
    #能保留更多的圖像細節，所以經常被稱為最有用的濾波器。
    #3×3 大小的卷積核，權重的標準差為默認值
    def filter_gauss3(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (3, 3), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    #5×5 大小的卷積核，權重的標準差為1
    def filter_gauss5(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (5, 5), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    #7×7 大小的卷積核，權重的標準差為1
    def filter_gauss7(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (7, 7), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    #9×9 大小的卷積核，權重的標準差為1
    def filter_gauss9(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (9, 9), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    #11×11 大小的卷積核，權重的標準差為1
    def filter_gauss11(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (11, 11), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    #15×15 大小的卷積核，權重的標準差為1
    def filter_gauss15(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (15, 15), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    #21×21 大小的卷積核，權重的標準差為1
    def filter_gauss21(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_gauss = cv2.GaussianBlur(image, (21, 21), 0,0) # 高斯濾波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_gauss
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        

    #中值濾波，中值又叫中位數，是所有值排序後取中間的值。
    #中值濾波就是用區域內的中值來代替本圖元值，所以那種孤立的斑點，
    #如0或255很容易消除掉，適用於去除椒鹽雜訊和斑點雜訊。
    #中值是一種非線性操作，效率相比前面幾種線性濾波要慢。
    #斑點雜訊圖，用中值濾波顯然更好：
    #濾波核大小設置為 3，表示寬度和高度均為 3
    def filter_mid3(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 3) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    #濾波核大小設置為 5，表示寬度和高度均為 5
    def filter_mid5(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 5) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    #濾波核大小設置為 7，表示寬度和高度均為 7
    def filter_mid7(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 7) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    #濾波核大小設置為 9，表示寬度和高度均為 9
    def filter_mid9(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 9) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    #濾波核大小設置為 11，表示寬度和高度均為 11
    def filter_mid11(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 11) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    #濾波核大小設置為 15，表示寬度和高度均為 15
    def filter_mid15(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 15) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    #濾波核大小設置為 21，表示寬度和高度均為 21
    def filter_mid21(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_mid_value = cv2.medianBlur(image, 21) # 中值濾波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_mid_value
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()


    #雙邊濾波，模糊操作基本都會損失掉圖像細節資訊，
    #尤其前面介紹的線性濾波器，圖像的邊緣資訊很難保留下來。
    #然而，邊緣edge資訊是圖像中很重要的一個特徵，所以這才有了雙邊濾波。
    def filter_bilateral37575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 3, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def filter_bilateral57575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 5, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def filter_bilateral77575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 7, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def filter_bilateral97575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 9, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def filter_bilateral117575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 11, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def filter_bilateral157575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 15, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    def filter_bilateral217575(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_bilateral = cv2.bilateralFilter(image, 21, 75, 75) # 雙邊濾波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_bilateral
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
    """-------------------------------------------------------------------------"""
    
    
    def filter_sobelGx(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #Sobel 算子
        x = cv2.Sobel(image, cv2.CV_16S, 1, 0) #对 x 求一阶导
        y = cv2.Sobel(image, cv2.CV_16S, 0, 1) #对 y 求一阶导
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        Sobel = cv2.addWeighted(absX, 1, absY, 0, 0)
        self.image = Sobel
        self.des1()
        
    def filter_sobelGy(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #Sobel 算子
        x = cv2.Sobel(image, cv2.CV_16S, 1, 0) #对 x 求一阶导
        y = cv2.Sobel(image, cv2.CV_16S, 0, 1) #对 y 求一阶导
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        Sobel = cv2.addWeighted(absX, 0, absY, 1, 0)
        self.image = Sobel
        self.des1()
       
    def filter_prewittGx(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #Prewitt 算子
        kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]], dtype=int)
        kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=int)
        x = cv2.filter2D(image, cv2.CV_16S, kernelx)
        y = cv2.filter2D(image, cv2.CV_16S, kernely)
        #转 uint8
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        prewitt = cv2.addWeighted(absX,0,absY,1/3,0)
        self.image = prewitt
        self.des1()
       
    def filter_prewittGy(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #Prewitt 算子
        kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]], dtype=int)
        kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=int)
        x = cv2.filter2D(image, cv2.CV_16S, kernelx)
        y = cv2.filter2D(image, cv2.CV_16S, kernely)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        prewitt = cv2.addWeighted(absX,1/3,absY,0,0)
        self.image = prewitt
        self.des1()
        
        
    def filter_freichenGx(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #Prewitt 算子
        kernelx = np.array([[1,pow(2, .5),1],[0,0,0],[-1,-pow(2, .5),-1]], dtype=int)
        kernely = np.array([[-1,0,1],[-pow(2, .5),0,pow(2, .5)],[-1,0,1]], dtype=int)
        x = cv2.filter2D(image, cv2.CV_16S, kernelx)
        y = cv2.filter2D(image, cv2.CV_16S, kernely)
        #转 uint8
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        prewitt = cv2.addWeighted(absX,0,absY,1/(2+pow(2, .5)),0)
        
        self.image = prewitt
        self.des1()
        
    def filter_freichenGy(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #Prewitt 算子
        kernelx = np.array([[1,pow(2, .5),1],[0,0,0],[-1,-pow(2, .5),-1]], dtype=int)
        kernely = np.array([[-1,0,1],[-pow(2, .5),0,pow(2, .5)],[-1,0,1]], dtype=int)
        x = cv2.filter2D(image, cv2.CV_16S, kernelx)
        y = cv2.filter2D(image, cv2.CV_16S, kernely)
        #转 uint8
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        prewitt = cv2.addWeighted(absX,1/(2+pow(2, .5)),absY,0,0)
        self.image = prewitt
        self.des1()
                
    def filter_scharrGx(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        # Scharr算子
        x = cv2.Scharr(image, cv2.CV_32F, 1, 0) #X方向
        y = cv2.Scharr(image, cv2.CV_32F, 0, 1) #Y方向
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        Scharr = cv2.addWeighted(absX, 1, absY, 0.5, 0)
        self.image = Scharr
        self.des1()
                
    def filter_scharrGy(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Scharr算子
        x = cv2.Scharr(grayImage, cv2.CV_32F, 1, 0) #X方向
        y = cv2.Scharr(grayImage, cv2.CV_32F, 0, 1) #Y方向
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        Scharr = cv2.addWeighted(absX, 0.5, absY, 1, 0)
        self.image = Scharr
        self.des1()
                              
    def filter_laplacian3301(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #laplacian矩陣
        laplacian = np.array([[0,1,0],[1,-4,1],[0,1,0]],dtype=int)
        image = cv2.filter2D(image, -1, laplacian)
        #Laplacian = cv2.Laplacian(image, cv2.CV_16S, ksize = 3)
        #image = cv2.convertScaleAbs(Laplacian)
        self.image = image
        self.des1()
                              
    def filter_laplacian3302(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #laplacian矩陣
        laplacian = np.array([[1,1,1],[1,-8,1],[1,1,1]],dtype=int)
        image = cv2.filter2D(image, -1, laplacian)
        self.image = image
        self.des1()
                              
    def filter_laplacian3303(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #laplacian矩陣
        laplacian = np.array([[-1,2,-1],[2,-4,2],[-1,2,-1]],dtype=int)
        image = cv2.filter2D(image, -1, laplacian)
        self.image = image
        self.des1()
                              
    def filter_laplacian55(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #laplacian矩陣
        laplacian = np.array([[0,0,-1,0,0],[0,-1,-2,-1,0],
                              [-1,-2,16,-2,-1],[0,-1,-2,-1,0],[0,0,-1,0,0]],dtype=int)
        image = cv2.filter2D(image, -1, laplacian)
        self.image = image
        self.des1()
                              
    def filter_laplacian77(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #laplacian矩陣
        laplacian = np.array([[0,0,-1,-1,-1,0,0],[0,-1,-3,-3,-3,-1,0],[-1,-3,0,7,0,-3,-1],[-1,-3,7,24,7,-3,-1],
                              [-1,-3,0,7,0,-3,-1],[0,-1,-3,-3,-3,-1,0],[0,0,-1,-1,-1,0,0],],dtype=int)
        image = cv2.filter2D(image, -1, laplacian)
        self.image = image
        self.des1()
                                
    def filter_laplacian99(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #laplacian矩陣
        laplacian = np.array([[0,1,1,2,2,2,1,1,0],[1,2,4,5,5,5,4,2,1],[1,4,5,3,0,3,5,4,1],
                              [2,5,3,-12,-24,-12,3,5,2],[2,5,0,-24,-40,-24,0,5,2],[2,5,3,-12,-24,-12,3,5,2],
                              [1,4,5,3,0,3,5,4,1],[1,2,4,5,5,5,4,2,1],[0,1,1,2,2,2,1,1,0]],dtype=int)
        image = cv2.filter2D(image, -1, laplacian)
        self.image = image
        self.des1()
        
    def filter_canny(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #高斯滤波降噪
        gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
        #Canny算子
        Canny = cv2.Canny(gaussian, 50, 150)
        self.image = Canny
        self.des1()
        
    def filter_edgesharp3301(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #高斯滤波降噪
        gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
        #laplacian矩陣
        laplacian = np.array([[0,1,0],[1,-4,1],[0,1,0]],dtype=int)
        img = cv2.filter2D(gaussian, -1, laplacian)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        image = cv2.addWeighted(image, 1, img, 0.5, 0)
        self.image = image
        self.des1()
              
    def filter_edgesharp3302(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #高斯滤波降噪
        gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
        #laplacian矩陣
        laplacian = np.array([[1,1,1],[1,-8,1],[1,1,1]],dtype=int)
        img = cv2.filter2D(gaussian, -1, laplacian)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        image = cv2.addWeighted(image, 1, img, 0.5, 0)
        self.image = image
        self.des1()
              
    def filter_edgesharp3303(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #高斯滤波降噪
        gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
        #laplacian矩陣
        laplacian = np.array([[-1,2,-1],[2,-4,2],[-1,2,-1]],dtype=int)
        img = cv2.filter2D(gaussian, -1, laplacian)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        image = cv2.addWeighted(image, 1, img, 0.5, 0)
        self.image = image
        self.des1()
              
    def filter_edgesharp55(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #高斯滤波降噪
        gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
        #laplacian矩陣
        laplacian = np.array([[0,0,-1,0,0],[0,-1,-2,-1,0],
                              [-1,-2,16,-2,-1],[0,-1,-2,-1,0],[0,0,-1,0,0]],dtype=int)
        img = cv2.filter2D(gaussian, -1, laplacian)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        image = cv2.addWeighted(image, 1, img, 0.5, 0)
        self.image = image
        self.des1()
              
    def filter_edgesharp77(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #灰度化处理图像
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #高斯滤波降噪
        gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
        #laplacian矩陣
        laplacian = np.array([[0,0,-1,-1,-1,0,0],[0,-1,-3,-3,-3,-1,0],[-1,-3,0,7,0,-3,-1],[-1,-3,7,24,7,-3,-1],
                              [-1,-3,0,7,0,-3,-1],[0,-1,-3,-3,-3,-1,0],[0,0,-1,-1,-1,0,0],],dtype=int)
        img = cv2.filter2D(gaussian, -1, laplacian)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        image = cv2.addWeighted(image, 1, img, 0.5, 0)
        self.image = image
        self.des1()
        
        
        
    # 圖像金字塔操作的將是圖像的圖元問題（圖像變清晰了還是模糊了）
    # 圖像金字塔主要有兩類：高斯金字塔和拉普拉斯金字塔。
    def scale_pyrup(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_pyrup = cv2.pyrUp(image) # 高斯金字塔
        image_pil_pyrup = Image.fromarray(img_pyrup)
        tk_image = ImageTk.PhotoImage(image_pil_pyrup)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_pyrup
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()        
         
    def scale_pyrdown(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        img_pyrdown = cv2.pyrDown(image) # 高斯金字塔
        image_pil_pyrdown = Image.fromarray(img_pyrdown)
        tk_image = ImageTk.PhotoImage(image_pil_pyrdown)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_pyrdown
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(relx=0,rely=0)# 放置元件的不同方式
        self.label_des_image.pack()
        self.root.mainloop() 
    # 放大
    def scale_zoom_in(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        size = (2*image.shape[1], 2*image.shape[0])
        img_zoom_in = cv2.resize(image, size) # 放大
        image_pil_zoom_in = Image.fromarray(img_zoom_in)
        tk_image = ImageTk.PhotoImage(image_pil_zoom_in)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_zoom_in
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.place(x=0, y=0)
        # 放置元件的不同方式與金字塔放大相比對齊方式不同顯示不同
        # self.label_des_image.pack()
        self.root.mainloop()
    # 縮小
    def scale_zoom_out(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        size = (int(0.3*image.shape[1]), int(0.3*image.shape[0]))
        img_zoom_out = cv2.resize(image, size) # 放大
        image_pil_zoom_out = Image.fromarray(img_zoom_out)
        tk_image = ImageTk.PhotoImage(image_pil_zoom_out)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_zoom_out
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
    # 平移
    def rotate_offset(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        width, height = image.shape[1], image.shape[0]
        direction = np.float32([[1,0,50],[0,1,50]])# 沿x軸移動50，沿y軸移動50
        img_offset = cv2.warpAffine(image, direction, (width, height))
        image_pil_offset = Image.fromarray(img_offset)
        tk_image = ImageTk.PhotoImage(image_pil_offset)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_offset
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
    # 仿射-需要三個點座標
    def rotate_affine(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        width, height = image.shape[1], image.shape[0]
        pts1 = np.float32([[50,50],[200,50],[50,200]])
        pts2 = np.float32([[10,100],[200,50],[100,250]])
        rot_mat = cv2.getAffineTransform(pts1,pts2)# 沿x軸移動50，沿y軸移動50
        img_affine = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_affine = Image.fromarray(img_affine)
        tk_image = ImageTk.PhotoImage(image_pil_affine)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_affine
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
   # 透射 -需要四個點的座標
    def rotate_transmission(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        #width, height = image.shape[1], image.shape[0]
        pts1 = np.float32([[56,65],[238,52],[28,237],[239,240]])
        pts2 = np.float32([[0,0],[250,0],[0,250],[250,250]])
        rot_mat = cv2.getPerspectiveTransform(pts1,pts2)
        img_transmission = cv2.warpPerspective(image, rot_mat, (250, 250))
        # 透射與仿射的函數不一樣
        image_pil_transmission = Image.fromarray(img_transmission)
        tk_image = ImageTk.PhotoImage(image_pil_transmission)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_transmission
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
    # 順時針無縮放   
    def rotate_clockwise(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width//2, height//2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle = -45, scale = 1) 
        # 旋轉中心rotate_center，角度degree， 縮放scale
        img_clockwise = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_clockwise = Image.fromarray(img_clockwise)
        tk_image = ImageTk.PhotoImage(image_pil_clockwise)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = image_pil_clockwise
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
    # 順時針-縮放
    def rotate_clockwise_zoom(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width//2, height//2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle = -45, scale = 0.6)
        # 旋轉中心rotate_center，角度degree， 縮放scale
        img_clockwise_zoom = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_clockwise_zoom = Image.fromarray(img_clockwise_zoom)
        tk_image = ImageTk.PhotoImage(image_pil_clockwise_zoom)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_clockwise_zoom
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
    # 逆時針-縮放
    def rotate_anti_zoom(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width//2, height//2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle = 45, scale = 0.6) 
        # 旋轉中心rotate_center，角度degree， 縮放scale
        img_anti_zoom = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_anti_zoom = Image.fromarray(img_anti_zoom)
        tk_image = ImageTk.PhotoImage(image_pil_anti_zoom)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = image_pil_anti_zoom
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
    # 零旋轉-縮放
    def rotate_zero_zoom(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width//2, height//2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle = 0, scale = 0.6) 
        # 旋轉中心rotate_center，角度degree， 縮放scale
        img_zero_zoom = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_zero_zoom = Image.fromarray(img_zero_zoom)
        tk_image = ImageTk.PhotoImage(image_pil_zero_zoom)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.image = img_zero_zoom
        self.label_des_image.configure(image = tk_image)
        #self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.root.mainloop()
        
        
    # 五行色彩檢測  
    def color_5(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        yellow= cv2.inRange(hsv, (25,50,50), (32,255,255))
        yellow02 = cv2.inRange(hsv,  (52,47,48), (60,100,97))
        img_yellow = yellow + yellow02
        
        red= cv2.inRange(hsv, (0,175,20), (10,255,255))
        red02 = cv2.inRange(hsv,  (170,175,20), (180,255,255))
        img_red = red + red02

        img_purple = cv2.inRange(hsv,(100,45,45),(155,255,255))
        img_white = cv2.inRange(hsv,(0,0,220),(180,30,255))
        img_green = cv2.inRange(hsv,(35,45,45),(75,255,255))
        
        yellow = cv2.bitwise_and(image,image,mask = img_yellow)
        red = cv2.bitwise_and(image,image,mask = img_red)
        purple = cv2.bitwise_and(image,image,mask = img_purple)
        white = cv2.bitwise_and(image,image,mask = img_white)
        green = cv2.bitwise_and(image,image,mask = img_green)
        cv2.imshow('yellow',yellow)
        cv2.imshow('red',red)
        cv2.imshow('purple',purple)
        cv2.imshow('white',white)
        cv2.imshow('green',green)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
        
    # video_loop2
    def video_loop2(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, self.frame = self.cap.read() # read frame from video stream
        
        if keyboard.is_pressed("q") or not ok :
            """if not os.path.isfile(format(self.path)) and self.snap == 0:
                print("Can not save video file!")"""
            self.clear()
            ok = 0
            self.cap.release()
            if self.rw > 0:
                self.out.release()
            self.rw = -1
        else:
            self.frame = cv2.flip(self.frame, 1)
            desframe = self.frame
            
        
        if ok: # frame captured without any errors
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA) # convert colorsfrom BGR to RGBA
            self.current_image = Image.fromarray(cv2image) # convert image for PIL
            tk_image = ImageTk.PhotoImage(image=self.current_image) # convert image for tkinter
            if(self.label_scr_image == None):
                self.label_scr_image = tk.Label(self.frame_scr,image = tk_image) #initialize image panel
            self.label_scr_image.tk_image = tk_image # anchor tk_image so it does not be deleted by garbage-collector
            self.label_scr_image.configure(image = tk_image) # show the image
            self.label_scr_image.pack() # 顯示控制項
            
        if self.rw == 0:
            blurred = cv2.GaussianBlur(desframe, (9, 9), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # define range of color in HSV
            # change it according to your need !
            
            lower_color = np.array([0,175,20],np.uint8)
            upper_color = np.array([10,255,255],np.uint8)
            lower_color02 = np.array([170,175,20],np.uint8)
            upper_color02 = np.array([180,255,255],np.uint8)
        
            # Threshold the HSV image to get the selected color
            mask = cv2.inRange(hsv, lower_color, upper_color)
            mask02 = cv2.inRange(hsv, lower_color02, upper_color02)
            mask = mask + mask02
            
            #Morphological transformation, Dilation
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
           
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
            # only proceed if at least one contour was found
            if len(cnts) > 1:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # only proceed if the radius meets a minimum size
                if radius > 30:
                    # draw the circle and centroid on the desframe,
                    # then update the list of tracked points
                    cv2.circle(desframe, (int(x), int(y)), int(radius),
                               (0, 255, 255), 2)
                    cv2.circle(desframe, center, 5, (0, 0, 255), -1)
            # update the points queue
            self.pts.appendleft(center)
            # loop over the set of tracked points
            for i in range(1, len(self.pts)):
                # if either of the tracked points are None, ignore them
                if self.pts[i - 1] is None or self.pts[i] is None:
                    continue
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
                cv2.line(desframe, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)
                
        elif self.rw == 1:
            #灰度化处理图像
            grayImage = cv2.cvtColor(desframe, cv2.COLOR_BGR2GRAY)
            #Sobel 算子
            x = cv2.Sobel(grayImage, cv2.CV_16S, 1, 0) #对 x 求一阶导
            desframe = cv2.convertScaleAbs(x)
            desframe = cv2.cvtColor(desframe, cv2.COLOR_GRAY2BGR)
            desframe = cv2.resize(desframe, (640,480 ))  # 將大小修改成480*640
            self.out.write(desframe)
            
        elif self.rw == 2:
            #灰度化处理图像
            grayImage = cv2.cvtColor(desframe, cv2.COLOR_BGR2GRAY)
            #Sobel 算子
            y = cv2.Sobel(grayImage, cv2.CV_16S, 0, 1) #对 y 求一阶导
            desframe = cv2.convertScaleAbs(y)
            desframe = cv2.cvtColor(desframe, cv2.COLOR_GRAY2BGR)
            desframe = cv2.resize(desframe, (640,480 ))  # 將大小修改成480*640
            self.out.write(desframe)
            
        elif self.rw == 3:
            #laplacian矩陣
            laplacian = np.array([[0,0,-1,-1,-1,0,0],[0,-1,-3,-3,-3,-1,0],[-1,-3,0,7,0,-3,-1],[-1,-3,7,24,7,-3,-1],
                                  [-1,-3,0,7,0,-3,-1],[0,-1,-3,-3,-3,-1,0],[0,0,-1,-1,-1,0,0],],dtype=int)
            desframe = cv2.filter2D(desframe, -1, laplacian)
            desframe = cv2.resize(desframe, (640,480 ))  # 將大小修改成480*640
            self.out.write(desframe)
            
        elif self.rw == 4:
            #灰度化处理图像
            grayImage = cv2.cvtColor(desframe, cv2.COLOR_BGR2GRAY)
            #高斯滤波降噪
            gaussian = cv2.GaussianBlur(grayImage, (3,3), 0)
            #Canny算子
            desframe = cv2.Canny(gaussian, 50, 150)
            desframe = cv2.cvtColor(desframe, cv2.COLOR_GRAY2BGR)
            desframe = cv2.resize(desframe, (640,480 ))  # 將大小修改成480*640
            self.out.write(desframe)
            
        elif self.rw == 5:
            #灰度化处理图像
            gray = cv2.cvtColor(desframe, cv2.COLOR_BGR2GRAY)
            
            # 偵測臉部
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.08,
                minNeighbors=5,
                minSize=(32, 32))
            # 繪製人臉部份的方框
            for (x, y, w, h) in faces:
                cv2.rectangle(desframe, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #(0, 255, 0)欄位可以變更方框顏色(Blue,Green,Red)
            desframe = cv2.resize(desframe, (640,480 ))  # 將大小修改成480*640
            self.out.write(desframe)
            
        else:
            pass
            

            
        if ok: # frame captured without any errors
            
            cv2image = cv2.cvtColor(desframe, cv2.COLOR_BGR2RGBA) # convert colorsfrom BGR to RGBA
            self.current_image = Image.fromarray(cv2image) # convert image for PIL
            tk_image = ImageTk.PhotoImage(image=self.current_image) # convert image for tkinter
            if(self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des,image = tk_image) #initialize image panel
            self.label_des_image.tk_image = tk_image # anchor tk_image so it does not be deleted by garbage-collector
            self.label_des_image.configure(image = tk_image) # show the image
            self.label_des_image.pack() # 顯示控制項
            self.root.after(10, self.video_loop2) # call the same function after 10 milliseconds
        else:
            pass
    
    
    def savevideo(self):
        self.output_path = "D:\images\cam-record"
        ts = datetime.datetime.now() # grab the current timestamp
        filename = "{}.mp4".format(ts.strftime("%Y-%m-%d_%H-%M-%S")) # construct filename
        self.output_path = os.path.join(self.output_path, filename) # construct output path
        # 將照片持續寫入影音檔
        print("[INFO] {} is saving ...".format(self.output_path))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.output_path,fourcc, 15.0, (640,480))
        
        
    # 紅球追蹤
    def redball_tracking(self):
        self.rw = 0
        self.cap = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        self.pts = deque(maxlen=32)
        self.video_loop2()
        self.root.mainloop()
        
        
    # video 即時影像處理
    def video_real_time_fun(self,a):
        open_video_path = askopenfilename(initialdir = file_path,
                                         filetypes=[('AVI', '*.avi'), ('MP4', '*.mp4'), ('MKV', '*.mkv'), ('All Files','*')],
                                         parent = self.root,
                                         title = '開啟視訊檔')
        if (open_video_path == ''):
            print("Can not open video file!")
            return
        else:
            self.rw = a
            self.savevideo()
            self.path = open_video_path
            self.cap = cv2.VideoCapture(self.path) # capture video frames, 0 is your default video camera
            self.video_loop2()
            self.root.mainloop()
            self.out.release()
            
            
    #cam 即時影像處理    
    def cam_real_time_fun(self,a = -1):
        self.rw = a
        self.savevideo()
        self.cap = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        self.video_loop2()
        self.root.mainloop()
        self.cap.release()
        self.out.release()
        
    # 人臉檢測
    def picture_face(self):
        if(self.path == ''):
            return
        if(self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)# 讀取圖片
        b, g, r = cv2.split(image)# 三通道分離
        image = cv2.merge([r,g,b])# 三通道合併
        # 載入分類器
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        # 轉成灰階圖片
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 偵測臉部
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.08,
            minNeighbors=7,
            minSize=(43, 43))
        # 繪製人臉部份的方框
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #(0, 255, 0)欄位可以變更方框顏色(Blue,Green,Red)
        self.image = image
        image_pil = Image.fromarray(self.image)
        tk_image = ImageTk.PhotoImage(image_pil)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des,image = tk_image)
        self.label_des_image.configure(image = tk_image)
        self.label_des_image.pack()
        self.root.mainloop()
        
        
    def video_face(self):
        # 載入分類器
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.video_real_time_fun(5)
        
    def cam_face(self):
        # 載入分類器
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.cam_real_time_fun(5)


         
    def help_copyright(self):
        tk.messagebox.showinfo(title='版權', message='實習成果展示使用')
    def help_about(self):
        tk.messagebox.showinfo(title='關於', message='數位影像處理-2022')
         
if __name__ == '__main__':        
    Image_sys()
     
'''
tkinter.messagebox中有如下函數：
askokcancel(title=None, message=None, **options)
Ask if operation should proceed; return true if the answer is ok
askquestion(title=None, message=None, **options)
Ask a question
askretrycancel(title=None, message=None, **options)
Ask if operation should be retried; return true if the answer is yes
askyesno(title=None, message=None, **options)
Ask a question; return true if the answer is yes
askyesnocancel(title=None, message=None, **options)
Ask a question; return true if the answer is yes, None if cancelled.
showerror(title=None, message=None, **options)
Show an error message
showinfo(title=None, message=None, **options)
Show an info message
showwarning(title=None, message=None, **options)
Show a warning message
'''   