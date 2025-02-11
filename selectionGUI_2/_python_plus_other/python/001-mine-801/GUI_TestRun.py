
#import rainbowdoc


import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
from tkinter import messagebox

import clipboard
#import zTools as zt
#import zTools003 as zt
import Tools34_003 as zt

#import rainbowdoc as rd
#import numpy as np
import localmarianodoc001 as rd




def clrTXT():
    textarea.delete("1.0",END)
    pass

def Clear():
    scroll.delete("1.0", END)
    pass


def listclean(lns):
    start=False;
    for tup in lns:
        txt=tup[0]
        if start==False:
            start= (txt=="start")
            #scroll_line("not started="+txt)
        else:
            hypen_index=txt.find("-")
            if hypen_index>0:
                scroll_line( txt[0:hypen_index] )


    pass

def Go():

    if clear_go.get():
        Clear()
        pass


    raindoc = rd.MarianoDocument()


    focus=eFocus.get()
    minHR=float(eMinHR.get())
    minhpc=float( eMinHPC.get() )

    mincount=int(eMinCount.get())
    listlimit=int(eListLimit.get())


    minCh=0
    zt.program34(focus, minHR,minhpc,minCh, mincount, raindoc, listlimit)

    lns=raindoc.get_lines()
    lncount,itemsindex=0,400
    startitems=False

    for l in lns:
        line=l[0]

        # this if-else is for attaching clean code at end of line
        if startitems==False:
            startitems= line=="start"
        else :
            hyphen_index=line.find("-")
            if hyphen_index>1:
                line += ",\t"+line[:hyphen_index]


        if line=="linebreak":
            line="\n"
        elif line=="pagebreak":
            line="-----"

        #scroll_line(str(lncount)+"->" +line)  # works fine
        scroll_line(line)  # works fine
        if (line=="items"):
            itemsindex=lncount+1
            pass


        # scroll.insert(INSERT, line + "\n"), for some reason won't work, may repaint
        if (lncount==itemsindex):
            clipboard.copy(line)

        lncount+=1
        pass

    if check_attach.get():
        listclean(lns)
    return 1














    #zt.JupyterLoop(scroll)
    #zt.testrun()
    pass

def scroll_line(ln):
    scroll.insert(INSERT, ln+"\n")


def testFunct():
    #clipboard.copy("abc")
    #v=messagebox.askyesno("Test 123")
    #messagebox.showinfo("","you answered="+str(v))
    if check_attach.get():
        messagebox.showinfo("", "selected")
    else:
        messagebox.showinfo("", " NOT selected")



def getButton(text,runfunct, ypos):
    btnResult = tk.Button(frame, text=text, command=runfunct, font=("Comic Sans", 20), fg="green", bg="orange", height=20)
    btnResult.place(x=30, y=ypos, w=160, h=40)
    return btnResult

def getEntry(lbldesc,text,ypos):
    result = tk.Entry(frame, font=("Arial", 10), )
    result.insert(0,text)
    lbl = tk.Label(frame, text=lbldesc, font=("Arial", 10))

    result.place(x=110, y=ypos, w=80, h=30)
    lbl.place(x=10, y=ypos, w=90, h=30)
    return result

def exit():
    "dummy function"
    pass


window =tk.Tk()
window.geometry("900x600")

window.protocol("WM_DELETE_WINDOW", exit)


frame=tk.Frame()
frame.place(x=0,y=0, w=200, h=600)

btnGo=getButton("Go",Go,20)
btnClear=getButton("Clear",Clear,70)
btnTest=getButton("Test",testFunct,120)



eFocus=getEntry( "Focus", "5-H",  200)
eMinHR=getEntry( "MIN HR", "106.0", 250)
eMinHPC=getEntry( "MIN HPC", "101.0", 300)
eMinCount=getEntry( "MIN Count", "4", 350)
eListLimit=getEntry( "List Limit", "20", 400)



check_attach = tk.IntVar()
clear_go = tk.IntVar()


cbAttach=tk.Checkbutton(master=frame,text="Attach clean codes",variable =check_attach)
cbAttach.place(x=50,y=450)

cbClearGo=tk.Checkbutton(master=frame,text="Clear on Go",variable =clear_go)
cbClearGo.place(x=50,y=480)





scroll=tk.scrolledtext.ScrolledText(window)
scroll.place(x=220,y=0,w=600,h=400)
scroll.insert(INSERT,"Ready to start\n")

textarea=tk.Text(master=window, background="#F5F5DC")
textarea.place(x=220,y=410,w=600,h=100)
textarea.insert(INSERT,"Notes area\n")
buttonCLR=tk.Button(master=window, command=clrTXT, text="CLR")
buttonCLR.place(x=785,y=412,w=30,h=20)

btn_quit = Button( text="Quit", command=window.destroy )
btn_quit.pack()





# alternatives
#btnClear.pack(side=tk.BOTTOM)
#btnClear.pack(anchor=tk.E, expand=False)
#scroll.pack(expand=True)
#scroll.grid(column=0,row=0)


#btnGo=tk.Button(frame,text="Go",command=Go,font=("Comic Sans",30),fg="green",bg="orange",height=20)
#btnGo.place(x=0,y=0,w=100,h=40)

#btnClear=tk.Button(frame,text="Clear",command=Clear,font=("Comic Sans",30),fg="green",bg="orange",height=20)
#btnClear.place(x=0,y=50,w=100,h=40)

def get_csvitems(entrybox):
    text=entrybox.get()
    result=text.split(',')
    return result

def get_iscsvitems(s,csv_items):
    return s in csv_items





window.mainloop()
