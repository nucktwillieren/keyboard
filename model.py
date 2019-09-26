from tkinter import *
import tkinter.filedialog as filedialog
import os,time,threading,msvcrt,json,configparser
from os.path import basename
from pygame import *
import pygame   

class key_def:
    def play(self,key):
        try:
            dest = self.key_dict[key]
            if dest.track != '':
                if not self.repeat:
                    if not dest.status:
                        dest.track.play()
                        print('start',id(dest.track))
                    else:
                        dest.track.stop()
                        print('stop',id(dest.track))
                    dest.status = not dest.status
                else:
                    dest.track.play()
                    print('start',id(dest.track))
        except KeyError:
            pass

    def bind_play(self,event):
        key = event.char       
        try:
            dest = self.key_dict[key]
            if dest.track != '':
                if not dest.status:
                    dest.track.play()
                    print('start',id(dest.track))
                else:
                    dest.track.stop()
                    print('stop',id(dest.track))
                dest.status = not dest.status
        except KeyError:
            pass
    
    def listen(self):
        while 1:
            try:
                self.keyin1 = msvcrt.getch()
                self.keyin2 = msvcrt.getch()
                self.keyin_value = self.keyin1.decode('utf-8')
                self.play(self.keyin_value)
            except KeyboardInterrupt:
                break

    def modify(self,key,filename=None):
        if filename == None:
            filename = filedialog.askopenfilename()
        else:
            filename = filename
        self.key_dict[key].filename = filename
        self.key_dict[key] = button_onboard(key,filename)
        if filename != '':
            self.key_dict[key].track = mixer.Sound(self.key_dict[key].track)

    def repeater(self):
        self.repeat = not self.repeat

    def __init__(self, *args, **kwargs):
        self.key_dict = {chr(k):button_onboard(chr(k),'') for k in range(97,123)}
        for i in range(10):
            self.key_dict[str(i)] = button_onboard(str(i),'')

        self.repeat = False
            
        #th = threading.Thread(target=self.listen)
        #th.start()

class config:
    def save_config(self,key_dict):
        filename = filedialog.asksaveasfile()
        for k in key_dict:
            self.config['keyboard'][k] = key_dict[k].filename
            print(self.config['keyboard'][k],k)
        self.config.write(filename+'.ini')

    def __init__(self, *args, **kwargs):
        filename = filedialog.askopenfile()
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) 
        if filename == '':
            self.config_path = os.path.join(self.base_dir,'default_keyboard.ini')
        else:
            self.config_path = filename
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.config.sections()   

class button_onboard:
    def __init__(self, keyword, track, *args, **kwargs):
        mixer.init()
        self.status = False           
        self.keyword = keyword  
        self.track = track  
        self.filename = ''
        self.basefilename = ''

class main_keyboard:
    def create_modify_button(self,master,key):
        button = Button(master=master,
                        text=key,
                        command=lambda: self.key_onkeyboard.modify(key),
                        width=10,height=10)
        self.button_list.append(button)
        button.pack()

    def create_listbox(self,master,data,title,x,y):   
        t = StringVar()         
        t.set(data)
        cust_list = Listbox(master,listvariable=t,height=50)
        cust_list.place(x=x,y=y)

    def import_audio(self):        
        key_list = self.key_list.copy()
        self.filenames = list(filedialog.askopenfilenames())
        if len(self.filenames) < 36:
            for i in range(36-len(self.filenames)):
                self.filenames.append('')
        for filename,key in zip(self.filenames,key_list):
            self.key_onkeyboard.modify(key=key,filename=filename)
        self.status_list = []
        for k in key_list:
            self.status_list.append(self.key_onkeyboard.key_dict[k].status)

        base_filenames = [basename(f) for f in self.filenames]
        self.key_mapping = []
        for k,f in zip(key_list,base_filenames):
            self.key_mapping.append(k+"__"+f)
        audios = self.create_listbox(self.window,self.key_mapping,'files',200,10)
        self.status_list = []
        for k in self.key_list:
            self.status_list.append(self.key_onkeyboard.key_dict[k].status)
        status = self.create_listbox(self.window,self.status_list,'files',600,10)  

    def button_change_color(self,event):
        if self.key_onkeyboard.repeat == False:
            self.repeat_button.configure(bg='white')
        else:
            self.repeat_button.configure(bg='green')

    def __init__(self, *args, **kwargs):        
        self.window = Tk()
        self.window.title('Keyboard GUI')
        self.window.geometry('1440x900')

        #self.config = config()
        self.key_onkeyboard = key_def()
        self.button_list = []

        self.window.bind('<Key>',self.key_onkeyboard.bind_play)
        self.filenames = []

        num_key_list = [str(i) for i in range(10)]
        letter_key_list = ['q','w','e','r','t','y','u','i','o','p','a','s','d',
        'f','g','h','j','k','l','z','x','c','v','b','n','m']
        self.key_list = num_key_list + letter_key_list

        #for k in range(97,123):
        #    self.create_modify_button(self.window,chr(k))

        self.save_button = Button(master=self.window,
                        text='Save',
                        command=lambda: self.config.save_config(self.key_onkeyboard.key_dict),
                        width=10,height=10)
        self.save_button.place(x=20,y=20)
        self.import_button = Button(master=self.window,
                        text='Import',
                        command=lambda: self.import_audio(),
                        width=10,height=10)
        self.import_button.place(x=20,y=120)
        self.repeat_button = Button(master=self.window,
                        text='Repeat',
                        command=lambda: self.key_onkeyboard.repeater(),
                        width=10,height=10)
        self.repeat_button.bind('<Button-1>',self.button_change_color)
        self.repeat_button.place(x=20,y=220)

        self.window.mainloop()

if __name__ == '__main__':
    main_keyboard()