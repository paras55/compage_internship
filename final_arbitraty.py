#XEND[i]= current value of x
#YEND[I]= current value of y 
# dictionary with integer keys
import numpy as np
tool_table = {350: 'T-1', 400: 'T-1',450: 'T-1',40: 'T1',30: 'T2',86: 'T3',86: 'T4'}
import math

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def gcode1(name):
        OPENFILEPATH=name
        track=0
        h={}
        SKIMHEIGHT  = "3"
        STARTHEIGHT = "1"
        CUTDEPTH    = "-0.15"
        FEEDRATE    = "200"
        DRILLDEPTH  = "-1.8"
        DRILLRATE   = "30"
        FINISHPOS    = "G0 X-100"
        R           = 2      # Round off to decimal places
        drill_radius    = 0.51     # Maximum circle RADIUS[i] to drill
        safe=10
        check_arc=None  #flag for checking arc
        # Varibles used by program. Do not alter !
        TEXT         = ""
        ERROR        = ""
        i= 0
        HOLECOUNT    = 1
        BIGCOUNT    = 0
        COUNT        = 0
        FEEDFLAG    = 0
        XMAX = 0
        XMIN = 0
        tool=None
        YMAX = 0
        YMIN = 0
        QTY=15
        XSTART = [0 for i in range(QTY)]
        RADIUS = [0 for i in range(QTY)]
        YSTART = [0 for i in range(QTY)]
        XEND   = [0 for i in range(QTY)]
        YEND   = [0 for i in range(QTY)]
        XHOLE  = [0 for i in range(QTY)]
        YHOLE  = [0 for i in range(QTY)]
        #i=0
       # DXFPATH, DXFNAME = os.path.split(OPENFILEPATH)
        gcode=''
        #RADIUS[i]=None
        
        #### Read DXF file ############################################
        
        file = open(OPENFILEPATH,"r") 
        
        while True: #### Main DXF read loop ####
            TEXT = file.readline()
            TEXT = TEXT.strip() # Remove spaces
            if (TEXT == "AcDbLine"):
                print( str(i) +' in line')
                while True:
                    #print(TEXT)
                    TEXT = file.readline() # Read identifier
                    TEXT = TEXT.strip()
                    #print(TEXT)
                    if (TEXT == "10"): 
                        #print('i am here')
                        TEXT = file.readline() # Read X start poosition
                        TEXT = TEXT.strip()
                        XSTART[i]= float(TEXT)
                        #TEXT="NOTHING"
                        #break
                    
                    #print(TEXT)
                    if (TEXT == "20"): 
                        #print(TEXT)
                        #print('hi')
                        TEXT = file.readline() # Read Y start poosition
                        #print(TEXT)
                        TEXT = TEXT.strip()
                        YSTART[i]= float(TEXT)
                        TEXT = "NOTHING"
                        
                    
                    if (TEXT == "11"): 
                        TEXT = file.readline() # Read X end poosition
                        TEXT = TEXT.strip()
                        XEND[i]= float(TEXT)
                        TEXT = "NOTHING"
                    
                    if (TEXT == "21"): 
                        TEXT = file.readline() # Read Y end poosition
                        TEXT = TEXT.strip()
                        YEND[i]= float(TEXT)
                        TEXT = "NOTHING"
                        
                    if (TEXT == "0"):
                        gcode=gcode+'G00 Z'+str(safe)+'\n'
                        #h[XSTART[i]]='G01 X'+str(XEND[i])+' Y'+str(YEND[i])+'\n'
                        gcode=gcode+'G00 X'+str(XSTART[i])+' Y'+str(YSTART[i])+'\n'
                        gcode=gcode+'G01 X'+str(XEND[i])+' Y'+str(YEND[i])+'\n'
                        h[str([XSTART[i],YSTART[i],'line',i])]=[[XEND[i],YEND[i]],i]
                        i=i+1
                        break
                    
            if TEXT=='EOF':
                    l=[gcode,h]
                    return l
                    break   
                        
            if (TEXT == "AcDbCircle"): # Found circle
                print(str(i)+' in circle')
                while True:
                    TEXT = file.readline() # Read identifier
                    TEXT = TEXT.strip()
                    #print(TEXT)
                    if (TEXT == "10"): 
                        TEXT = file.readline() # Read X centre poosition
                        TEXT = TEXT.strip()
                        #print(i)
                        XHOLE[i]= float(TEXT)
                        TEXT = "NOTHING"
                        
                    
                    if (TEXT == "20"): 
                        TEXT = file.readline() # Read Y centre poosition
                        TEXT = TEXT.strip()
                        YHOLE[i]= float(TEXT)
                        TEXT = "NOTHING"
                    
                    if (TEXT == "40"): 
                        TEXT = file.readline() # Read RADIUS[i]
                        TEXT = TEXT.strip()
                        #global RADIUS[i]
                        RADIUS[i]=TEXT
                        #print( RADIUS[i])
                        #RADIUS[i]= float(TEXT)
                        if RADIUS[i] in tool_table:
                            tool=tool_table[RADIUS[i]]
                            
                    if (TEXT == "50"): 
                        TEXT = file.readline() 
                        TEXT = TEXT.strip()
                        startingangle=TEXT
                        #print('HELLO')
                       # print(np.cos(np.array((TEXT)) * np.pi / 180))
                        #print(np.sin(np.array((0., 30., 45., 60., 90.)) * np.pi / 180.))
                        XEND1=float(np.cos(np.array(float(TEXT)) * np.pi / 180.))*float(RADIUS[i])+ float(XHOLE[i]) #starting X point of arc 
                        YEND1=float(np.sin(np.array(float(TEXT)) * np.pi / 180.))*float(RADIUS[i])+ float(YHOLE[i])  #ending Y point of arc
                        
                        gcode=gcode+'G00 X'+str(XEND1)+' Y'+str(YEND1)+'\n'
                        check_arc=True
                            
                    if (TEXT == "51"): 
                        TEXT = file.readline() 
                        TEXT = TEXT.strip()
                        endingangle=TEXT
                        #print(TEXT)
                       # print(np.cos(np.array((TEXT)) * np.pi / 180))
                        #print(np.sin(np.array((0., 30., 45., 60., 90.)) * np.pi / 180.))
                        XEND[i]=float(np.cos(np.array(float(TEXT)) * np.pi / 180.))*float(RADIUS[i])+ float(XHOLE[i])
                        YEND[i]=float(np.sin(np.array(float(TEXT)) * np.pi / 180.))*float(RADIUS[i])+ float(YHOLE[i])
                        #check_arc=True
                    #print(check_arc)
                    if (TEXT == "0"):
                        gcode=gcode+'G00 Z'+str(safe)+'\n'
                        
                        if tool!=None:
                          gcode=gcode+'N10 '+tool 
                          
                        '''if check_arc==True:
                            #gcode=gcode+'G00 X'+str(XEND[i])+' Y'+str(YEND[i])+'\n'
                           #if XEND[i-1]==XHOLE[i]: #horizontal line and circle  
                            if YEND[i-1]>YHOLE[i]: #clockwise circle downwards right corner
                                   gcode=gcode+'G02 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                               
                            elif YEND[i-1]<YHOLE[i]: #anticlockwise circle upwards
                                    gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                    
                           #elif YEND[i-1]==YHOLE[HOLECOUNT]:  # vertical line and circle
                            elif XEND[i-1]>XHOLE[i]: #centre of circle on left
                                   gcode=gcode+'G02 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                               
                            elif XEND[i-1]<XHOLE[i]:  #centre of circle on right
                                   gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                   
                            check_arc=None
                            i=i+1'''
                        
                        if check_arc==True:
                            '''if str([XEND1,YEND1]) in h :
                                h[str([XEND1,YEND1,'new'])]=[XEND[i],YEND[i]]
                            else:
                                h[str([XEND1,YEND1])]=[XEND[i],YEND[i]]'''
                            rad='R'+str(RADIUS[i])
                            h[str([XEND1,YEND1,'arc',rad,startingangle,endingangle,i])]=[[XEND[i],YEND[i]],i]
                           
                            #gcode=gcode+'G00 X'+str(XEND[i])+' Y'+str(YEND[i])+'\n'
                           #if XEND[i-1]==XHOLE[i]: #horizontal line and circle  
                            if XEND1>XEND[i] and YEND1>YEND[i]: #clockwise circle downwards right corner
                                   #h[XEND1]='G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                   gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                               
                            elif XEND1>XEND[i] and YEND1<YEND[i]: #anticlockwise circle upwards
                                    #h[XEND1]='G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                    gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                    
                           #elif YEND[i-1]==YHOLE[HOLECOUNT]:  # vertical line and circle
                            elif XEND1<XEND[i] and YEND1>YEND[i]: #centre of circle on left
                                   #h[XEND1]='G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                   gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                               
                            elif XEND1<XEND[i] and YEND1<YEND[i]: #centre of circle on right
                                   #h[XEND1]='G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                   gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                   
                            check_arc=None
                            i=i+1
                            
                            
                        
                        elif check_arc==None:# and RADIUS[i] > drill_RADIUS[i]:
                            RADIUS[i]=float(RADIUS[i])
                            x_point=XHOLE[i]+float(RADIUS[i])
                            gcode=gcode+'G00 Z'+str(safe)+'\n'
                            gcode=gcode+'G00 X'+str(XHOLE[i]-RADIUS[i])+' Y'+str(YHOLE[i])+'\n'
                            radi='R'+str(RADIUS[i])
                            iden='full'
                            h[str([XHOLE[i]-RADIUS[i],YHOLE[i],iden,radi,i])]=[[x_point,YHOLE[i]],i]
                            print('helllllloooo')
                            gcode=gcode+'G02 X'+str(x_point)+' Y'+str(YHOLE[i]) + ' R'+str(RADIUS[i])+'\n'
                            gcode=gcode+'G02 X'+str(XHOLE[i]-RADIUS[i])+' Y'+str(YHOLE[i]) + ' R'+str(RADIUS[i])+'\n'
                            i=i+1
                            
                        break
                    
               # print(XSTART)
                #print(h)
        #return h
               # break
#gcode1('latest.DXF')
p=gcode1('latest.DXF')

dic=p[1]
dicto=dic
res = list(dic.keys())[0]       #first element (key) in form of string to get value
res1 = res.strip('][').split(', ') 

cordinates=[res1[0],res1[1]]
pappu=''                        #newgcode
pappu=pappu+'G0'+' X'+res1[0]+' Y'+res1[1]+'\n'
valuedic=dic[res]
valuewhat=res1[2].replace("'", "")    #circle/line/arc
if valuewhat=='line':
    print('hi')
    pappu=pappu+'G01'+' X'+str(valuedic[0][0])+' Y'+str(valuedic[0][1])+'\n'
    
del dic[res]
last_cordinate_track=valuedic[0]
print(last_cordinate_track)
#print(dic)
#print(last_cordinate_track,'op')
for h in range(13):
# first searching in keys

    dic_keys=list(dic.keys())           #list of keysof dictionary
    
    #print(type(valuedic[0]))
    for i in dic_keys: #for searching in keys
        #print('in keys')
        res_new = i.strip('][').split(', ') #mking it a list from str
        ok=[float(res_new[0]),float(res_new[1])] #making pair of key to check with value
        #print(ok)
        ok[0]=truncate(ok[0],2)
        last_cordinate_track[0]=truncate(last_cordinate_track[0],2)
        ok[1]=truncate(ok[1],2)
        last_cordinate_track[1]=truncate(last_cordinate_track[1],2)
        print(ok,last_cordinate_track)
        if ok==last_cordinate_track:
            valuewhat1=res_new[2].replace("'", "")    #circle/line/arc
            #print(valuewhat1)
            if valuewhat1=='line':
                #print('i am inside line')
                print(h,' I am in line of keys')
                valuedic1=dic[i]
                pappu=pappu+'G01'+' X'+str(valuedic1[0][0])+' Y'+str(valuedic1[0][1])+'\n'
                last_cordinate_track=valuedic1[0]
                print(last_cordinate_track)
                del dic[i]
                break
            elif valuewhat1=='arc':
                #print('i am inside arc')
                print(h,' I am in arc of keys')
                valuedic1=dic[i]
                radius1=res_new[3]
                sangle=res_new[4] #starting angle of arc
                eangle=res_new[5] #ending angle of arc
                if sangle<eangle or sangle>eangle :
                    pappu=pappu+'G03'+' X'+str(valuedic1[0][0])+' Y'+str(valuedic[0][1])+str( radius1)+'\n'
                    last_cordinate_track=valuedic1[0]
                    del dic[i]
                    break
        
     
    #second searchin in values
    
    valuesofdic=list(dic.values())
    
    for j in valuesofdic:
        #print('yar')
        #print(len(last_cordinate_track))
        res_new1=j[0]
        #print(res_new1,last_cordinate_track)
        #last_cordinate_track=[float(last_cordinate_track[0]),float(last_cordinate_track[1])]
        #print(res_new1)
        #res_new56 = list(k.strip('][').split(', '))
        res_new1[0]=truncate(res_new1[0],2)
        last_cordinate_track[0]=truncate(last_cordinate_track[0],2)
        res_new1[1]=truncate(res_new1[1],2)
        last_cordinate_track[1]=truncate(last_cordinate_track[1],2)
        if res_new1==last_cordinate_track:
            print(h, 'i am here for check')
            trackno=j[1]
            #print(trackno)
            for k in dic_keys:
                res_new2 = list(k.strip('][').split(', ')) #key found from value by using track no
                #print(res_new2)
                #print('start',k,res_new2[len(res_new2)-1],trackno)
                if int(res_new2[len(res_new2)-1])==trackno:                #searching by trackno
                    #print('hey')
                    valuewhat2=res_new2[2].replace("'", "")    #circle/line/arc
                    if valuewhat2=='line':
                        print('I am in line of values')
                        pappu=pappu+'G01'+' X'+str(res_new2[0])+' Y'+str(res_new2[1])+'\n'
                        last_cordinate_track=[float(res_new2[0]),float(res_new2[1])]
                        print(last_cordinate_track)
                        del dic[k]
                        break
                    elif valuewhat2=='arc':
                        print(h, 'I am in arc of values')
                        #valuedic2=j
                        radius2=res_new2[3]
                        sangle=res_new2[4] #starting angle of arc
                        eangle=res_new2[5] #ending angle of arc
                        if sangle<eangle or sangle>eangle :
                            pappu=pappu+'G02'+' X'+str(res_new2[0])+' Y'+str(res_new2[1])+str( radius2)+'\n'
                            last_cordinate_track=[float(res_new2[0]),float(res_new2[1])]
                            print(last_cordinate_track)
                            del dic[k]
                            break
                    
                    


            
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
