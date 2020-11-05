import os
import time
import datetime


def gcode(name):
        OPENFILEPATH=name
        
        SAFEHEIGHT 	= "10"
        SKIMHEIGHT  = "3"
        STARTHEIGHT = "1"
        CUTDEPTH    = "-0.15"
        FEEDRATE    = "200"
        DRILLDEPTH  = "-1.8"
        DRILLRATE   = "30"
        FINISHPOS	= "G0 X-100"
        QTY         = 100	 # Quantity of memory to be used
        R           = 2 	 # Round off to decimal places
        CIRCLERAD	= 0.51	 # Maximum circle radius to drill
        
        
        # Varibles used by program. Do not alter !
        TEXT 		= ""
        ERROR		= ""
        LINECOUNT	= 1
        HOLECOUNT	= 1
        BIGCOUNT	= 0
        COUNT		= 0
        FEEDFLAG	= 0
        XMAX = 0
        XMIN = 0
        YMAX = 0
        YMIN = 0
        XSTART = [0 for i in range(QTY)]
        YSTART = [0 for i in range(QTY)]
        XEND   = [0 for i in range(QTY)]
        YEND   = [0 for i in range(QTY)]
        XHOLE  = [0 for i in range(QTY)]
        YHOLE  = [0 for i in range(QTY)]
        RADIUS = [0 for i in range(QTY)]
        DXFPATH, DXFNAME = os.path.split(OPENFILEPATH)
        
        
        
        #### Read DXF file ############################################
        
        file = open(OPENFILEPATH,"r") 
        
        while True: #### Main DXF read loop ####
        	TEXT = file.readline()
        	
        	TEXT = TEXT.strip() # Remove spaces
        	#print TEXT # Used to de-bug
        	
        	if (TEXT == "AcDbLine"): # Found line
        		while True:
        			TEXT = file.readline() # Read identifier
        			TEXT = TEXT.strip()
        			
        			if (TEXT == "10"): 
        				TEXT = file.readline() # Read X start poosition
        				TEXT = TEXT.strip()
        				XSTART[LINECOUNT]= float(TEXT)
        				TEXT="NOTHING"
        			
        			if (TEXT == "20"): 
        				TEXT = file.readline() # Read Y start poosition
        				TEXT = TEXT.strip()
        				YSTART[LINECOUNT]= float(TEXT)
        				TEXT = "NOTHING"
        				
        			
        			if (TEXT == "11"): 
        				TEXT = file.readline() # Read X end poosition
        				TEXT = TEXT.strip()
        				XEND[LINECOUNT]= float(TEXT)
        				TEXT = "NOTHING"
        			
        			if (TEXT == "21"): 
        				TEXT = file.readline() # Read Y end poosition
        				TEXT = TEXT.strip()
        				YEND[LINECOUNT]= float(TEXT)
        				TEXT = "NOTHING"
        			
        			if (TEXT == "0"): # No more data
        				if (YSTART[LINECOUNT] > YMAX): YMAX = YSTART[LINECOUNT]
        				if (YSTART[LINECOUNT] < YMIN): YMIN = YSTART[LINECOUNT]
        				if (YEND[LINECOUNT] > YMAX): YMAX = YEND[LINECOUNT]
        				if (YEND[LINECOUNT] < YMIN): YMIN = YEND[LINECOUNT]
        				if (XSTART[LINECOUNT] > XMAX): XMAX = XSTART[LINECOUNT]
        				if (XSTART[LINECOUNT] < XMIN): XMIN = XSTART[LINECOUNT]
        				if (XEND[LINECOUNT] > XMAX): XMAX = XEND[LINECOUNT]
        				if (XEND[LINECOUNT] < XMIN): XMIN = XEND[LINECOUNT]
        				LINECOUNT = LINECOUNT + 1
        				break
        	
        	if (TEXT == "AcDbCircle"): # Found circle
        		while True:
        			TEXT = file.readline() # Read identifier
        			TEXT = TEXT.strip()
        			
        			if (TEXT == "10"): 
        				TEXT = file.readline() # Read X centre poosition
        				TEXT = TEXT.strip()
        				XHOLE[HOLECOUNT]= float(TEXT)
        				TEXT = "NOTHING"
        			
        			if (TEXT == "20"): 
        				TEXT = file.readline() # Read Y centre poosition
        				TEXT = TEXT.strip()
        				YHOLE[HOLECOUNT]= float(TEXT)
        				TEXT = "NOTHING"
        			
        			if (TEXT == "40"): 
        				TEXT = file.readline() # Read radius
        				TEXT = TEXT.strip()
        				RADIUS[HOLECOUNT]= float(TEXT)
        				if RADIUS[HOLECOUNT] > CIRCLERAD : BIGCOUNT = BIGCOUNT + 1
        				TEXT = "NOTHING"
        			
        			if (TEXT == "0"): # No more data
        				if XHOLE[HOLECOUNT] > XMAX : XMAX = XHOLE[HOLECOUNT]
        				if XHOLE[HOLECOUNT] < XMIN : XMIN = XHOLE[HOLECOUNT]
        				if YHOLE[HOLECOUNT] > YMAX : YMAX = YHOLE[HOLECOUNT]
        				if YHOLE[HOLECOUNT] < YMIN : YMIN = YHOLE[HOLECOUNT]
        				HOLECOUNT = HOLECOUNT + 1
        				break
        			
        	if (LINECOUNT >= QTY):
        		ERROR = ERROR + "ERROR - Ran out of dimentioned line arrey. Increase QTY value.\n"
        		TEXT = "EOF"
        		break
        	
        	if (HOLECOUNT >= QTY):
        		ERROR = ERROR + "ERROR - Ran out of dimentioned circle arrey. Increase QTY value.\n"
        		TEXT = "EOF"
        		break
        		
        	if (TEXT =="EOF"):break
        
        file.close	
        	
        
        
        
        #### Create G-Code ############################################
        
        GCODE = "(" + DXFNAME + ")\n"
        GCODE = GCODE + "(" + str(datetime.datetime.now()) + ")\n"
        GCODE = GCODE + "G90 G17 G21\n"  # Absolute, XY plane, MM
        GCODE = GCODE + "G0 Z" + SAFEHEIGHT + "\n"
        
        GCODE = GCODE + "(OUTSIDE TEST)\n"
        GCODE = GCODE + "G0 X" + str(round(XMIN,R)) + " Y" + str(round(YMIN,R)) + "\n"
        GCODE = GCODE + "G0 Y" + str(round(YMAX,R)) + "\n"
        GCODE = GCODE + "G0 X" + str(round(XMAX,R)) + "\n"
        GCODE = GCODE + "G0 Y" + str(round(YMIN,R)) + "\n"
        GCODE = GCODE + "G0 X" + str(round(XMIN,R)) + "\n"
        
        GCODE = GCODE + "M3 S1000\n" # Spindle motor on
        GCODE = GCODE + "(MACHINE LINES)\n" # Remark
        
        for i in range(1,LINECOUNT):
        	print ("Line X start" , XSTART[i] , " Y start" , YSTART[i] , "  X end", XEND[i] , " Y end" , YEND[i])
        	if(XSTART[i] != XEND[i-1] or YSTART[i] != YEND[i-1]):
        		GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
        		GCODE = GCODE + "(LINE " + str(i) + ")\n"
        		GCODE = GCODE + "G0 X" + str(round(XSTART[i],R)) + " Y" + str(round(YSTART[i],R)) + "\n"
        		GCODE = GCODE + "G0 Z" + STARTHEIGHT + "\n"
        		GCODE = GCODE + "G1 Z" + CUTDEPTH + " F" + DRILLRATE + "\n"
        		FEEDFLAG = 0
        		# End if
        	
        	GCODE = GCODE + "G1 X" + str(round(XEND[i],R)) + " Y" + str(round(YEND[i],R)) 
        	if (FEEDFLAG == 0 ):
        		GCODE = GCODE + " F" + FEEDRATE
        		FEEDFLAG = 1
        		# End if
        	GCODE = GCODE +  "\n"
        	# NEXT i
        	
        GCODE = GCODE + "G0 Z" + SAFEHEIGHT + "\n" # Rapid up to safe height
        
        GCODE = GCODE + "(DRILL HOLES)\n" # Remark
        
        for i in range(1,HOLECOUNT):
        	print ("Circle X centre", XHOLE[i], " Y centre", YHOLE[i] , " Radius" , RADIUS[i])
        	if RADIUS[i] < CIRCLERAD :
        		COUNT = COUNT + 1
        		GCODE = GCODE + "(HOLE " + str(COUNT) + ")\n"
        		GCODE = GCODE + "G0 X" + str(round(XHOLE[i],R)) + " Y" + str(round(YHOLE[i],R)) + "\n"
        		GCODE = GCODE + "G0 Z" + STARTHEIGHT + "\n"
        		GCODE = GCODE + "G1 Z" + DRILLDEPTH + " F" + DRILLRATE + "\n"
        		GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
        	# NEXT i
        	
        GCODE = GCODE + "G0 Z" + SAFEHEIGHT + "\n" # Rapid up to safe height
        GCODE = GCODE + "M5\n" # Spindle motor off
        GCODE = GCODE + "G0 X0 Y0\n" # Go home rapid
        GCODE = GCODE + FINISHPOS
        
        #### Display findings and G-Code ###############################
        
        
        #### Save to text file #########################################
        
        
        return GCODE
        

#print ("G-Code written to file > ", SAVEFILE)
