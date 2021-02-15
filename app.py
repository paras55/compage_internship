from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from mainfile import gcode1
from flask import send_file
import math

app = Flask(__name__)
name='gcode.txt'

@app.route('/')
def upload():
   return render_template('login.html')
	

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n



def final(p,f,sh,ss,rg5,d,w):
        #parameters
        safe_height=sh
        spindle_speed=ss
        spindle_waiting_time=w
        radius_for_g5=rg5
        depth_of_z=str('-')+str(d)
        pappu=''
        p2=0      
        feed_rate=f
        
        
        
        
        #headers                  #newgcode
        pappu=pappu+'g54'+'\r\n'+'T1'+'\r\n'
        pappu=pappu+'G0'+' Z'+str(safe_height)+'\r\n'
        pappu=pappu+'G0 X0.000 Y0.000 A90C0'+'\r\n'
        pappu=pappu+'S'+str(spindle_speed)+'M3'+'\r\n'
        pappu=pappu+'G4 K'+str(spindle_waiting_time)+'\r\n'
        pappu=pappu+'g5 r'+str(radius_for_g5)+'\r\n'
        pappu=pappu+'p1='+str(depth_of_z)+'\r\n'
        pappu=pappu+'p2=0 \r\n'
        pappu=pappu+'g40'+'\r\n'
        pappu=pappu+'n100'+'\r\n'
        pappu=pappu+'G1 Z '+str(p2)+' F'+str(feed_rate)+'\r\n'
        
        
        dic=p[1]
        dicto=dic
        res = list(dic.keys())[0]       #first element (key) in form of string to get value
        res1 = res.strip('][').split(', ') 
        
        cordinates=[res1[0],res1[1]]
        
        pappu=pappu+'G0'+' X'+res1[0]+' Y'+res1[1]+'\r\n'
        valuedic=dic[res]
        valuewhat=res1[2].replace("'", "")    #circle/line/arc
        if valuewhat=='line':
            print('hi')
            pappu=pappu+'G01'+' X'+str(valuedic[0][0])+' Y'+str(valuedic[0][1])+'\r\n'
            
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
                        pappu=pappu+'G01'+' X'+str(valuedic1[0][0])+' Y'+str(valuedic1[0][1])+'\r\n'
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
                            pappu=pappu+'G03'+' X'+str(valuedic1[0][0])+' Y'+str(valuedic[0][1])+' R'+str( radius1[2:len(radius1)-1])+'\r\n'
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
                                pappu=pappu+'G01'+' X'+str(res_new2[0])+' Y'+str(res_new2[1])+'\r\n'
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
                                    pappu=pappu+'G02'+' X'+str(res_new2[0])+' Y'+str(res_new2[1])+' R'+str( radius2[2:len(radius2)-1])+'\r\n'
                                    last_cordinate_track=[float(res_new2[0]),float(res_new2[1])]
                                    print(last_cordinate_track)
                                    del dic[k]
                                    break
                            
                            
        
                            
        
        
                    
        for r in dic:
                #res = list(dic.keys())[0]       #first element (key) in form of string to get value
                u = r.strip('][').split(', ') 
                pappu=pappu+'G00 '+'X'+str(u[0])+' Y'+str(u[1])+'\r\n'
                key=dic[r]
                radiu=u[3]
                pappu=pappu+'G02 '+'X'+str(key[0][0])+' Y'+str(key[0][1])+' R'+str( radiu[2:len(radiu)-1])+'\r\n'
                pappu=pappu+'G02 '+'X'+str(u[0])+' Y'+str(u[1])+' R'+str( radiu[2:len(radiu)-1])+'\r\n'
                    
                    
        pappu=pappu+'p2=p2-2'+'\r\n'
        pappu=pappu+'IF(p2>p1) 100'+'\r\n'
        pappu=pappu+'G0Z15.000'+'\r\n'
        pappu=pappu+'G0Y0.000'+'\r \n'
        pappu=pappu+'G0X0'+' \r\n'
        pappu=pappu+'M30'
        return pappu
    
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload1_file():
   if request.method == 'POST':
      f = request.files['file']
      feed_rate = request.form['feed']
      safe_height=request.form['safe']
      spindle_speed=request.form['s_speed']
      radius_for_g5=request.form['radiusg5']
      depth_of_cut=request.form['depth']
      spindle_waiting_time=request.form['wait']
      print(feed_rate,safe_height)
      f.save(secure_filename(f.filename))
      code=gcode1(f.filename)
      gcode=final(code,feed_rate,safe_height,spindle_speed,radius_for_g5,depth_of_cut,spindle_waiting_time)
      file = open(name,"w")
      file.write(gcode )
      file.close()
      return send_file(name, as_attachment=True)
  
    
@app.route('/signin')
def signin():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    if username == 'client1' and password == 'compage':
        return render_template('upload.html')
    
    elif username == 'client2' and password == 'compage':
       return render_template('upload.html')

    else :
        return render_template('login.html', warning='Please enter correct username and password')
      #return code
		
if __name__ == '__main__':
   app.run()
