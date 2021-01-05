from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from mainfile import gcode1
from flask import send_file

app = Flask(__name__)
name='gcode.txt'

@app.route('/',methods=['GET'])
def upload():
   return render_template('login.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload1_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      code=gcode1(f.filename)
      file = open(name,"w")
      file.write(code )
      file.close()
      return send_file(name, as_attachment=True)
  


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
