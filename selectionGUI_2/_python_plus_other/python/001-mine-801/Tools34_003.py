import helloworldbasic5message as rd
import pandas as pd


#ztools
def cleancode(c):
    i=c.find("-")
    return str(c[0:i])


def get_filtered(df_use,focus, minhr,minHPC,minCh,mincount):
    df_copy=df_use.copy()
    
    filt01=(df_copy[focus]>=minhr)&(df_copy['HPC']>=minHPC)&(df_copy['Change']>=minCh)
    
    df_filtered=df_copy.loc[filt01]
    
    df_result=df_filtered.groupby(['Code'])[['SR']].agg(['count','mean','median']).\
            sort_values( [('SR',   'mean')],ascending=False  )
    
    colcount=('SR',   'count')
    colmean=('SR',   'mean')
    
    filt02=(df_result[colcount]>=mincount) & (df_result[colmean]>=102.0)  
    df_result=df_result.loc[filt02].round(2)
    df_result['clean']=df_result.index
    df_result['clean']=df_result['clean'].apply(cleancode)
    df_result['focus']=focus
    df_result['min_hr']=minhr
    df_result['min_count']=mincount
    
    
    return df_result

def get_items(df, focus, minHR,minHPC,minCh):
    cleancodes=df.clean
    strvals=""
    count=0
    extension=", >>  "+focus+" >= "+str(minHR)+" minHPC="+str(minHPC)
    extension+=" minCh="+str(minCh)
    for c in cleancodes:
        strvals+=c+","
        count+=1
        if count==8:
            #strvals+= extension+",\n"
            strvals+= ",\n"
            
            count=0
            pass
        pass
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



def program34(focus,minhr,minHPC,minCh,mincount,raindoc,listlimit):
    
    raindoc.insert_line("")
    title="focus="+focus+" minhr="+str(minhr)+" minhpc="+str(minHPC)
    raindoc.insert_line(title, font_bold=True)
    raindoc.insert_line("")
    #doc.insert_line("")
    
    
    selected=["SNDX","VIRT","PHR","ATGE","TREX","TNDM"]

    directory=""
    


    directory="C:\\Users\\USER\\Desktop\\StratsEzy\\export\\"
    filename="export001.csv"
    full_filename=directory+filename


    df_main= pd.read_csv(full_filename)
    fileout=filename[0:len(filename)-4]




    df_out1=get_filtered( df_main,focus,minhr,minHPC,minCh,mincount )
    items=get_items(df_out1,focus,minhr,minHPC,minCh)

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

    #means=np.round_(means, decimals = 3)
    raindoc.linebreak()
    raindoc.insert_line("start")

    tab="\t"
    for i in range(0,len(codes)):
        ast=""
        if clean[i] in selected:
            ast="  *"

        strv=width(codes[i],9,char="_")+"\t ->"+\
             width(counts[i],3)+"\t"+\
             f2(means[i])+"\t"+f2(meds[i])+ast 

        raindoc.insert_line(strv,font_size=rd.FontSize.TINY,print_console=True)

        if i>=(listlimit-1):
            break
            pass
        pass
    



     
    raindoc.createPDFFile("docs\\pdf-"+fileout+".pdf" )
    raindoc.createTextFile("docs\\txt-"+fileout+".txt" )
    raindoc.createWordFile("docs\\doc-"+fileout+".docx" )
    raindoc.pagebreak()




    #print(items)
    df_out1.head(80)
    return 1







print("ready to run JupyterLoop below")





