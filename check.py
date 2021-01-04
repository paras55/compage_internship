import os
import time
import datetime
import numpy as np
tool_table = {350: 'T-1', 400: 'T-1',450: 'T-1',40: 'T1',30: 'T2',86: 'T3',86: 'T4'}


def gcode(name):
        OPENFILEPATH=name
        track=0
        
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
        QTY=1000
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
                        gcode=gcode+'G00 X'+str(XSTART[i])+' Y'+str(YSTART[i])+'\n'
                        gcode=gcode+'G01 X'+str(XEND[i])+' Y'+str(YEND[i])+'\n'
                        i=i+1
                        break
                    
            if TEXT=='EOF':
                    return gcode
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
                        print('HELLO')
                       # print(np.cos(np.array((TEXT)) * np.pi / 180))
                        #print(np.sin(np.array((0., 30., 45., 60., 90.)) * np.pi / 180.))
                        XEND1=float(np.cos(np.array(float(TEXT)) * np.pi / 180.))*float(RADIUS[i])+ float(XHOLE[i])
                        YEND1=float(np.sin(np.array(float(TEXT)) * np.pi / 180.))*float(RADIUS[i])+ float(YHOLE[i])
                        gcode=gcode+'G00 X'+str(XEND1)+' Y'+str(YEND1)+'\n'
                        check_arc=True
                            
                    if (TEXT == "51"): 
                        TEXT = file.readline() 
                        TEXT = TEXT.strip()
                        print(TEXT)
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
                            #gcode=gcode+'G00 X'+str(XEND[i])+' Y'+str(YEND[i])+'\n'
                           #if XEND[i-1]==XHOLE[i]: #horizontal line and circle  
                            if XEND1>XEND[i] and YEND1>YEND[i]: #clockwise circle downwards right corner
                                   gcode=gcode+'G02 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                               
                            elif XEND1>XEND[i] and YEND1<YEND[i]: #anticlockwise circle upwards
                                    gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                    
                           #elif YEND[i-1]==YHOLE[HOLECOUNT]:  # vertical line and circle
                            elif XEND1<XEND[i] and YEND1>YEND[i]: #centre of circle on left
                                   gcode=gcode+'G03 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                               
                            elif XEND1<XEND[i] and YEND1<YEND[i]: #centre of circle on right
                                   gcode=gcode+'G02 X'+str(XEND[i])+' Y'+str(YEND[i]) + ' R'+str(RADIUS[i])+'\n'
                                   
                            check_arc=None
                            i=i+1
                            
                            
                        
                        elif check_arc==None:# and RADIUS[i] > drill_RADIUS[i]:
                            RADIUS[i]=float(RADIUS[i])
                            x_point=XHOLE[i]+float(RADIUS[i])
                            gcode=gcode+'G00 Z'+str(safe)+'\n'
                            gcode=gcode+'G00 X'+str(XHOLE[i]-RADIUS[i])+' Y'+str(YHOLE[i])+'\n'
                            gcode=gcode+'G02 X'+str(x_point)+' Y'+str(YHOLE[i]) + ' R'+str(RADIUS[i])+'\n'
                            gcode=gcode+'G02 X'+str(XHOLE[i]-RADIUS[i])+' Y'+str(YHOLE[i]) + ' R'+str(RADIUS[i])+'\n'
                            i=i+1
                            
                        break
                    
                
            return gcode
        

#print ("G-Code written to file > ", SAVEFILE)
