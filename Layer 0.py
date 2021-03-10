import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import Canvas, Label, PhotoImage, Text, Toplevel, messagebox
from PIL import Image
import tkcalendar as cal
import pickle
import time
import webbrowser

#global variable
newWindow=None
text_box=None
anim = []

# style
g="#282a2b"
lg="#949494"
w="#ffffff"
r="#bf4040"

# window setup
root = tk.Tk()
root.iconbitmap(r"Materials\navi.ico")
root.geometry("600x550")
root.title("Layer 0")
root.configure(bg=g)
root.resizable(False, False)

# calendar
CALENDAR = cal.Calendar(root,disabledforeground='red',selectmode="day",showweeknumbers=0,showothermonthdays=0,
                        normalbackground=g,headersbackground=g,foreground=w,normalforeground=w,weekendbackground=g,
                        weekendforeground=w,background=g,bordercolor=g,headersforeground=w,selectbackground=lg)
CALENDAR.pack(fill="both", expand=True)

# dates
event_date=[]
try:
    event_date = pickle.load(open("Data\dates.dat","rb"))
except EOFError:
    pass

#date_events
date_event_dict={}
try:
    date_event_dict = pickle.load(open("Data\save.dat","rb"))
except EOFError:
    pass

#saving
def saving():
    to_save = open('Data\save.dat','wb')
    pickle.dump(date_event_dict,to_save)
    to_save.close()
    ev_date = open("Data\dates.dat","wb")
    pickle.dump(event_date,ev_date)
    ev_date.close()

#deleting past events
date_gotten = CALENDAR.selection_get()
for ii in event_date:
    if date_gotten > ii:
        anim.append(ii)
for jj in anim:
    date_event_dict.pop(jj)
    event_date.remove(jj)
    #saving
    saving()

# load text
for j in event_date:
    CALENDAR.calevent_create(j,'reminder2',str(j))
    CALENDAR.tag_config(str(j),background=r, foreground=w)

# add date and set event
def set_event():
    global date_event_dict
    #checking textbot
    t = text_box.get('1.0','end-1c')
    if t == "":
            messagebox.showerror("Layer 0","No Event to be added")
    else:
        date_gotten = CALENDAR.selection_get()
        #new event
        if str(date_gotten) not in event_date :
            CALENDAR.calevent_create(date_gotten,'reminder2',str(date_gotten))
            CALENDAR.tag_config(str(date_gotten),background=r, foreground=w)
            event_date.append(date_gotten)
            messagebox.showinfo("Layer 0","Event added successfully")
            #saving
            date_event_dict.update({date_gotten:t})
            saving()


        newWindow.destroy()

# delete date
def delete_event():
    global date_event_dict
    date_gotten = CALENDAR.selection_get()
    #checking if event exists
    if date_gotten not in event_date:
        messagebox.showerror("Layer 0","Event does not exist")
    else:
        CALENDAR.tag_config(str(date_gotten),background=g, foreground=w)
        text_box.delete("0.0","end")
        date_event_dict.pop(date_gotten)
        event_date.remove(date_gotten)
        #saving
        saving()
        messagebox.showinfo("Layer 0","Event Deleted")
        newWindow.destroy()

# new window
def NewWindow():
    global newWindow
    global text_box
    newWindow = Toplevel() 
    newWindow.geometry("500x190")
    newWindow.configure(bg=g)
    newWindow.resizable(False, False)
    newWindow.iconbitmap(r"Materials\navi.ico")
    date_gotten = CALENDAR.selection_get()
    Label(newWindow,text =date_gotten,bg=g,fg=w).grid(row=0,column=1)
    text_box = st.ScrolledText(newWindow,width=60,height=9,wrap='word',bg=g,fg=w,insertbackground=w)
    text_box.grid(row=1,column=0,columnspan=3)
    interval.pop(0)
    #existing event
    for e in date_event_dict:
        if e == date_gotten: 
            t=date_event_dict[e]
            text_box.insert(0.0,t)
    #closing window
    def on_closing():
        if messagebox.askokcancel("Quit", "         Do you want to quit?\nall unsaved changes will be lost"):
            newWindow.destroy()
  
    newWindow.protocol("WM_DELETE_WINDOW", on_closing)
    #buttons
    confirm = tk.Button(newWindow,text='Confirm',bg=g,fg=w, command=set_event)
    confirm.grid(row=2,column=0)
    delete = tk.Button(newWindow,text='Delete Event',bg=g,fg=w,command=delete_event)
    delete.grid(row=2,column=2)

    newWindow.transient(root)
    newWindow.grab_set()
    root.wait_window(newWindow)

    newWindow.mainloop()

#double click
interval=[]
def doubleclick(event):
    global interval
    time_interval=time.perf_counter()
    interval.append(time_interval)
    if len(interval)==2:
        if interval[1]-interval[0]<0.2:
            NewWindow()
        try:
            interval.pop(0)
        except IndexError:
            pass

CALENDAR.bind("<<CalendarSelected>>", doubleclick)

def about():
    about = Toplevel() 
    about.geometry("500x230")
    about.resizable(False, False)
    about.iconbitmap(r"Materials\navi.ico")
    about.configure(bg=g)
    Label(about,text ="About",bg=g,fg=w,font=20).grid(row=0,column=2)
    Label(about,text="Version 2.8",bg=g,fg=w).grid(row=1,column=2)
    Label(about,text="\n\n\nMade by GrimWatch \nPossible New updates at GitHUB              \nlink to GitHUb page",bg=g,fg=w,anchor="w",justify="left").grid(row=2,column=0)
    link1=Label(about,text="https://github.com/GrimWatch/Layer-0",bg=g,justify="left",fg="#add8e6",cursor="hand2")
    #link
    def openlink(event):
        webbrowser.open_new("https://github.com/GrimWatch/Layer-0")
    link1.bind("<Button-1>",openlink)
    link1.grid(row=3,column=0)
    #images
    image=PhotoImage(file="Materials\github.png").subsample(3,3)
    Label(about, image=image,bg=g).grid(row=4,column=0)
    file="Materials\wired.gif"
    info = Image.open(file)
    frames = info.n_frames  # gives total number of frames that gif contains
    # creating list of PhotoImage objects for each frames
    im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]
    count = 0
    def animation(count):
        global anim
        im2 = im[count]
        gif_label.configure(image=im2,bg=g)
        count += 1
        if count == frames:
            count = 0
        anim = root.after(50,lambda :animation(count))

    gif_label = tk.Label(about,image="")
    gif_label.grid(row=2,column=3,rowspan=3)
    animation(count)

    about.transient(root)
    about.grab_set()
    root.wait_window(about)

    about.mainloop

#buttons
photo=PhotoImage(file=r"Materials\lain.png").subsample(4,4)
lain = tk.Button(root,image=photo,bg=g,activebackground=g,command=about).pack(side='right')

root.mainloop()
