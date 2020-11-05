from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from check import gcode
from flask import send_file

app = Flask(__name__)
name='gcode.txt'
@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload1_file():
   if request.method == 'POST':
      f = request.files['file']
      #f.save(secure_filename(f.filename))
      code=gcode(f.filename)
      file = open(name,"w")
      file.write(code )
      file.close()
      return send_file(name, as_attachment=True)
      #return code
		
if __name__ == '__main__':
   app.run()
