import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import Label, PhotoImage, Text, Toplevel, messagebox
import tkcalendar as cal
import pickle
import time
import datetime
import webbrowser

#global variable
newWindow=1
text_box=1

# style
g="#282a2b"
lg="#949494"
w="#ffffff"
r="#bf4040"

# window setup
root = tk.Tk()
root.iconbitmap("navi.ico")
root.geometry("600x550")
root.title("Layer 0")
root.configure(bg=g)
root.resizable(False, False)


# calendar
today = datetime.date.today()

CALENDAR = cal.Calendar(root,disabledforeground='red',selectmode="day",showweeknumbers=0,showothermonthdays=0,
                        normalbackground=g,headersbackground=g,foreground=w,normalforeground=w,weekendbackground=g,
                        weekendforeground=w,background=g,bordercolor=g,headersforeground=w,selectbackground=lg)
CALENDAR.pack(fill="both", expand=True)

# dates
event_date=[]
try:
    event_date = pickle.load(open("dates.dat","rb"))
except EOFError:
    pass

#date_events
date_event_dict={}
try:
    date_event_dict = pickle.load(open("save.dat","rb"))
except EOFError:
    pass

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
            ev_date = open("dates.dat","wb")
            pickle.dump(event_date,ev_date)
            ev_date.close()
            date_event_dict.update({date_gotten:t})
            to_save = open('save.dat','wb')
            pickle.dump(date_event_dict,to_save)
            to_save.close()
        newWindow.destroy()

# delete date
def delete_event():
    global date_event_dict
    date_gotten = CALENDAR.selection_get()
    #checking if event exists
    if date_gotten not in event_date:
        messagebox.showerror("Layer 0","Event does not exist")
    else:
        messagebox.showinfo("Layer 0","Event Deleted")
        CALENDAR.tag_config(str(date_gotten),background=g, foreground=w)
        text_box.delete("0.0","end")
        date_event_dict.pop(date_gotten)
        event_date.remove(date_gotten)
        #saving
        to_save = open('save.dat','wb')
        pickle.dump(date_event_dict,to_save)
        to_save.close()
        ev_date = open("dates.dat","wb")
        pickle.dump(event_date,ev_date)
        ev_date.close()
        newWindow.destroy()

# new window
def NewWindow():
    global newWindow
    global text_box
    newWindow = Toplevel() 
    newWindow.geometry("500x190")
    newWindow.resizable(False, False)
    newWindow.iconbitmap("navi.ico")
    date_gotten = CALENDAR.selection_get()
    Label(newWindow,text =date_gotten).grid(row=0,column=1)
    text_box = st.ScrolledText(newWindow,width=60,height=9,wrap='word')
    text_box.grid(row=1,column=0,columnspan=3)
    interval.pop(0)

    #existing event
    for e in date_event_dict:
        if e == date_gotten: 
            t=date_event_dict[e]
            text_box.insert(0.0,t)


    #buttons
    confirm = tk.Button(newWindow,text='Confirm', command=set_event)
    confirm.grid(row=2,column=0)
    delete = tk.Button(newWindow,text='Delete Event',command=delete_event)
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
    if len(interval)!=2:
        pass
    elif len(interval)==2:
        if interval[1]-interval[0]<0.2:
            NewWindow()
        try:
            interval.pop(0)
        except IndexError:
            pass

CALENDAR.bind("<<CalendarSelected>>", doubleclick)

def about():
    about = Toplevel() 
    about.geometry("500x190")
    about.resizable(False, False)
    about.iconbitmap("navi.ico")
    about.configure(bg=g)
    Label(about,text ="About",bg=g,fg=w,font=20).grid(row=0,column=1,columnspan=3)
    Label(about,text="Version 2.7",bg=g,fg=w).grid(row=1,column=2)
    Label(about,text="\nMade by GrimWatch \nPossible New updates at GitHUB              \nlink to GitHUb page",bg=g,fg=w,anchor="w",justify="left").grid(row=2,column=0)
    link1=Label(about,text="https://github.com/GrimWatch/Layer-0",bg=g,justify="left",fg="#add8e6",cursor="hand2")
    def openlink(event):
        webbrowser.open_new("https://github.com/GrimWatch/Layer-0")
    link1.bind("<Button-1>",openlink)
    link1.grid(row=3,column=0)

    about.transient(root)
    about.grab_set()
    root.wait_window(about)

    about.mainloop

#buttons
photo=PhotoImage(file=r"lain.png").subsample(4,4)
lain = tk.Button(root,image=photo,bg=g,activebackground=g,command=about).pack(side='right')


root.mainloop()
