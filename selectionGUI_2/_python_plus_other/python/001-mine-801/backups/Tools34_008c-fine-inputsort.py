import marianodoc as rd
import pandas as pd

# modified 2022, Dec 2, 21:44
# Dec 7, 16:16
# Dec 22,10:10
# Jan06, forgot
# Jan12, 1412 , changed sort to min, line 30, at the time 
# Jan14, 1353



#ztools
def cleancode(c):
    i=c.find("-")
    if i<0:
        return c
    return str(c[0:i])



def getsort(sort):
    if sort=='mean' or sort=='min' or sort=='count':
        return sort
    return 'mean'

def get_filtered(df_use,minhr1,minhr2,minHPC,minCh,mincount,minavg,sort):
    df_copy=df_use.copy()
    
    filt01=(df_copy['HR1']>=minhr1)&(df_copy['HR2']>=minhr2)&\
    (df_copy['HPC']>=minHPC)&(df_copy['Change']>=minCh)
    
    df_filtered=df_copy.loc[filt01]
    sort=getsort(sort)
    
    df_result=df_filtered.groupby(['CC'])[['SR']]\
    .agg(['count','mean','median','min'])\
    .sort_values( [('SR',   sort )],ascending=False  )   # Jan 14, changed to variable
    #.sort_values( [('SR',   'min' )],ascending=False  )  # Jan 12, changed to min
    
    
    colcount=('SR',   'count')
    colmean=('SR',   'mean')
    
    print("minavg=",minavg)
    
    filt02=(df_result[colcount]>=mincount) & (df_result[colmean]>=minavg)  
    df_result=df_result.loc[filt02].round(2)
    df_result['clean']=df_result.index
    df_result['clean']=df_result['clean'].apply(cleancode)
    #df_result['focus']=focus
    df_result['min_hr1']=minhr1
    df_result['min_hr2']=minhr2
    df_result['min_count']=mincount
    
    
    return df_result

def get_items(df, minHR1,minhr2,minHPC,minCh):
    cleancodes=df.clean
    strvals=""
    count=0
    extension=", >>  HR1 >= "+str(minHR1)+" HR2 >="+str(minhr2)
    extension+=" minHPC="+str(minHPC)+" minCh="+str(minCh)
    for c in cleancodes:
        strvals+=c+","
        count+=1
        if count==8:
            #strvals+= extension+",\n"
            strvals+= ",\n"
            
            count=0
            pass
        pass
    
    # show no extension, maybe revert back
    extension=""
    return strvals+extension

def width(val,size,char="_"):
    if type(val)==float:
        result=f2(val)
    
    result=str(val)
    short=size-len(result)
    for i in range(0,short):
        result+=char
        pass
    return result

def f2(float):
    return "{:.2f}".format(float)


def getinput(desc,default,t=str):
    result=default
    res=input(desc+" default="+str(default)+" >>  " )
    res=res.strip().upper()
    if len(res)>=1:
        result=res
        pass
    else:
        return default
    
    
    if t==bool :
        result=(res=="YES" or res=="Y" or res=='1' or res=="T" or res=="TRUE")
        pass
    elif t==int or t==float:
        try:
            result=t(result)
        except:
            result=default
            pass
        
        
    return result

def getstr(desc,default):
    return getinput(desc,default,t=str)

def getnumber(desc,default):
    return getinput(desc,default,t=float)

def getint(desc,default):
    return getinput(desc,default,t=int)

def getyesno(desc,default):
    return getinput(desc,default,t=bool)


# moved July 24, 2022

#focus,minhr,mincount='5-H',106,4



def program34(minhr1,minhr2,minHPC,minCh,mincount,raindoc,listlimit,createfiles,minavg,sort='mean'):
    
    raindoc.insert_line("")
    title="minhr1="+str(minhr1)+" minhr2="+str(minhr2)
    title+=" minhpc="+str(minHPC)+" minCh="+str(minCh)
    raindoc.insert_line(title, font_bold=True)
    raindoc.insert_line("")
    #doc.insert_line("")
    
    
    selected=["SNDX","VIRT","PHR","ATGE","TREX","TNDM"]

    directory=""
    


    directory="C:\\Users\\USER\\Desktop\\StratsEzy\\export\\"
    filename="export001.csv"
    full_filename=directory+filename


    df_main= pd.read_csv(full_filename)
    df_main['CC']=df_main['Code'].apply(cleancode)
    dictMT=get_MTdict(df_main['CC'],df_main['Code'])
    
    
    
    
    fileout=filename[0:len(filename)-4]




    df_out1=get_filtered( df_main,minhr1,minhr2,minHPC,minCh,mincount,minavg,sort )
    items=get_items(df_out1,minhr1,minhr2,minHPC,minCh)

    raindoc.insert_line("step 1 done, ** length=",len(df_main))
    
    #raindoc.insert_line("target:",focus, minhr, "mincount=",mincount)
    #print("fileout will be,",fileout)

    print()


    raindoc.insert_line("items")
    raindoc.insert_line(items,font_size=rd.FontSize.TINY)

    codes=df_out1.index
    clean=df_out1.clean
    counts=df_out1[('SR',  'count')]
    means=df_out1[('SR',  'mean')]
    meds=df_out1[('SR',  'median')]
    mins=df_out1[('SR',  'min')]
    

    #means=np.round_(means, decimals = 3)
    raindoc.linebreak()
    raindoc.insert_line("start")

    tab="\t"
    for i in range(0,len(codes)):
        ast=""
        if clean[i] in selected:
            ast="  *"

        strv=width(codes[i]+"-",7,char="_")+"\t ->"+\
             width(counts[i],3)+"\t"+\
             f2(means[i])+"\t"+f2(meds[i])+"\t"+f2(mins[i])+ast +"\t hereJan14"+\
             "\t"+dictMT.get(clean[i], "???->"+clean[i]) 

        raindoc.insert_line(strv,font_size=rd.FontSize.TINY,print_console=True)

        if i>=(listlimit-1):
            break
            pass
        pass
    



    if createfiles: 
        raindoc.createPDFFile("docs\\pdf-"+fileout+".pdf" )
        raindoc.createTextFile("docs\\txt-"+fileout+".txt" )
        raindoc.createWordFile("docs\\doc-"+fileout+".docx" )
        raindoc.pagebreak()




    #print(items)
    #df_out1.head(80)
    return 1

# Jan 06, 2023
def get_MTdict(cc,full):
    result={}
    length=len(cc)
    for i in range(length):
        a=cc[i]
        b=full[i]
        result[a]=b+"$"
        print("dictionary add",a,b)
    
    return result








print("ready to run JupyterLoop below")





