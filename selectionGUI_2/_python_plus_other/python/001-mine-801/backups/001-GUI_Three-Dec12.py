
#import rainbowdoc


import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
from tkinter import messagebox

import clipboard
#import zTools as zt
#import zTools003 as zt
#import Tools34_002 as zt


edition_use=5
if edition_use==3:
    import Tools34_003 as zt
elif edition_use==4:
    import Tools34_004 as zt
else:
    import Tools34_005 as zt



#import rainbowdoc as rd
#import numpy as np

try:
    print("impprting local md")
    import localmarianodoc001 as rd
except:
    mes="Error loading mariano doc"
    messagebox.showinfo(message=mes)
    print(mes)
    input("press any key , continue")


def closeapp():
    if messagebox.askyesno("Close app ?"):
        window.destroy()
    pass



window =tk.Tk()
window.geometry("1050x600")
window.protocol("WM_DELETE_WINDOW", closeapp)

frameLeft=tk.Frame()
frameLeft.place(x=0,y=0, w=200, h=600)

frameRight=tk.Frame()
frameRight.place(x=820,y=0, w=200, h=600)







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

    if check_cleargo.get():
        Clear()
        pass


    raindoc = rd.MarianoDocument()


    focus=eFocus.get()
    minHR1=float(eMinHR1.get())
    minHR2=float(eMinHR2.get())

    minHPC=float( eMinHPC.get() )
    minCh=float( eMinCh.get() )


    mincount=int(eMinCount.get())
    listlimit=int(eListLimit.get())
    createfiles = check_createfiles.get()

    if edition_use==3:
        zt.program34(focus, minHR1,minHPC,minCh, mincount, raindoc, listlimit)
    elif edition_use==4:
        zt.program34(focus, minHR1,minHR2,minHPC,minCh, mincount, raindoc, listlimit, createfiles )
    else:
        zt.program34(minHR1, minHR2, minHPC, minCh, mincount, raindoc, listlimit, createfiles)



    lns=raindoc.get_lines()
    lncount,itemsindex=0,400
    startitems=False
    specialitems=get_csvitems(especialitems)
    specialQ=""

    for l in lns:
        line=l[0]

        # this if-else is for attaching clean code at end of line
        if startitems==False:
            startitems= line=="start"
        else :
            hyphen_index=line.find("-")
            if hyphen_index>1:
                cleancode=line[:hyphen_index]
                market=line[hyphen_index: hyphen_index+4]
                is_midcap= (market=="-400" or market=="-500")


                if is_midcap and check_midcap.get() :
                    line += ",\t" + cleancode + ", ****"
                    specialQ+=cleancode+","
                elif cleancode in specialitems:
                    line += ",\t" + cleancode+", ****"
                    specialQ += cleancode + ","

                elif check_specialonly.get()==False:
                    line += ",\t"+cleancode+","
                else:
                    line=""


        if line=="linebreak":
            line="\n"
        elif line=="pagebreak":
            line="-----"

        if line=="":
            continue


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
    setText(especialQ,specialQ)

    if check_attach.get():
        listclean(lns)
    return 1














    #zt.JupyterLoop(scroll)
    #zt.testrun()
    pass

def scroll_line(ln):
    scroll.insert(INSERT, ln+"\n")

def setText(ebox, text):
    ebox.delete('0',END)
    ebox.insert(INSERT,text)


def resetFunct():
    setText(eMinHR1,'90')
    setText(eMinHPC,'90')
    setText(eMinCh,'90')
    setText(eMinHR2,'90')

    pass


def testFunct():
    #clipboard.copy("abc")
    #v=messagebox.askyesno("Test 123")
    #messagebox.showinfo("","you answered="+str(v))
    if check_attach.get():
        messagebox.showinfo("", "selected")
    else:
        messagebox.showinfo("", " NOT selected")



def getButton(master,text,runfunct, ypos):
    btnResult = tk.Button(master=master, text=text, command=runfunct, font=("Comic Sans", 20), fg="green", bg="orange", height=20)
    btnResult.place(x=30, y=ypos, w=160, h=40)
    return btnResult

def getEntry(frame,lbldesc,text,xpos=10,ypos=10, width=80, height=30, fontsize=10):
    result = tk.Entry(frame, font=("Arial", fontsize), )
    result.insert(0,text)
    lbl = tk.Label(frame, text=lbldesc, font=("Arial", 10))

    result.place(x=xpos+100, y=ypos, w=width, h=height)
    lbl.place(x=xpos, y=ypos, w=90, h=30)
    return result


def get_csvitems(entrybox):
    text=entrybox.get().upper()
    result=text.split(',')
    for i in range(0,len(result) ):
        result[i]=result[i].strip()
    return result

def get_iscsvitems(s,csv_items):
    return s in csv_items





check_attach,check_cleargo,check_specialonly,check_midcap = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
check_createfiles=tk.IntVar()


def getcheckbox(master, text,variable,x,y,set):
    result = tk.Checkbutton(master=master, text=text, variable=variable)
    result.place(x=x, y=y)
    variable.set(set)
    return result
    pass





btnGo=getButton(frameLeft, "Go",Go,20)
btnClear=getButton(frameLeft,"Clear",Clear,70)
btnMins90=getButton(frameLeft,"Mins=90",resetFunct,120)


leftStart=200
eFocus=getEntry(frameLeft, "Focus", "NA v-5+",  xpos=10,ypos=leftStart+0)
eMinHR1=getEntry( frameLeft,"MIN HR 1", "106.0", xpos=10,ypos=leftStart+50)
eMinHR2=getEntry( frameLeft,"MIN HR 2", "90.0", xpos=10,ypos=leftStart+100)

eMinHPC=getEntry( frameLeft,"MIN HPC", "101.0", xpos=10,ypos=leftStart+200)
eMinCh=getEntry( frameLeft,"MIN Change", "90.0", xpos=10,ypos=leftStart+250)




rightStart=120
btnTest=getButton(frameRight,"Test",testFunct,20)

eMinCount=getEntry( frameRight,"MIN Count", "4", xpos=2,ypos=rightStart, width=40)
eListLimit=getEntry( frameRight,"List Limit", "9000", xpos=2,ypos=rightStart+50, width=40)

cbAttach=getcheckbox(frameRight,"Attach clean codes",check_attach,10,rightStart+100,0)
cbClearGo=getcheckbox(frameRight,"ClearGo",check_cleargo,10,rightStart+130,1)
cbSpecialOnly=getcheckbox(frameRight,"SpecialOnly",check_specialonly,10,rightStart+160,0)
cbMidCapSpecial=getcheckbox(frameRight,"MidCap Special",check_midcap,10,rightStart+190,1)
cbCreatewordfiles=getcheckbox(frameRight,"Create Files",check_createfiles,10,rightStart+220,0)






scroll=tk.scrolledtext.ScrolledText(window)
scroll.place(x=220,y=0,w=600,h=400)
scroll.insert(INSERT,"Ready to start\n")

textarea=tk.Text(master=window, background="#F5F5DC")
textarea.place(x=220,y=410,w=600,h=100)
textarea.insert(INSERT,"Notes area\n")
buttonCLR=tk.Button(master=window, command=clrTXT, text="CLR")
buttonCLR.place(x=785,y=412,w=30,h=20)

especialitems=getEntry(window,"special-items","AAPL,MSFT",xpos=220,ypos=520, width=500, fontsize=6)
especialQ=getEntry(window,"special-Q","",xpos=220,ypos=560, width=500,fontsize=6)








# alternatives
#btnClear.pack(side=tk.BOTTOM)
#btnClear.pack(anchor=tk.E, expand=False)
#scroll.pack(expand=True)
#scroll.grid(column=0,row=0)


#btnGo=tk.Button(frame,text="Go",command=Go,font=("Comic Sans",30),fg="green",bg="orange",height=20)
#btnGo.place(x=0,y=0,w=100,h=40)

#btnClear=tk.Button(frame,text="Clear",command=Clear,font=("Comic Sans",30),fg="green",bg="orange",height=20)
#btnClear.place(x=0,y=50,w=100,h=40)




window.mainloop()
