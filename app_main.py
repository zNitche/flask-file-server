from flask import Flask, render_template, send_file, request, redirect
import os
from werkzeug import secure_filename
import subprocess
import glob
import shutil

app = Flask(__name__)

max_upload_size = 90 #max uploaded file size in MB

app.config['MAX_CONTENT_LENGTH'] = max_upload_size * 1024 * 1024

upload_location = "/home/zodi/Documents/Python/venvs/flask1/webapp/upload/" #upload location
tmp_location = "/home/zodi/Documents/Python/venvs/flask1/webapp/tmp/" #temp location
max_size = "400000000" #size in Bytes


@app.route('/', methods=['GET', 'POST'])
def index():
    loc = os.listdir(upload_location)
    size = 0
    try:
        inf = (os.popen("lsb_release -a").read()).split("\n")
        for files in glob.glob(f"{upload_location}*"):
            size = size + os.path.getsize(files)
    except Exception as e:
        inf = e
        size = e

    dic = {}
    for file in loc:
        if os.path.isdir(f"{upload_location}{file}"):
            pass
        else:
            dic[file] = (os.path.getsize(f"{upload_location}{file}"))/1000

    current_size = (str(size / 1024)).split(".")[0]
    return render_template('index.html', dict=dic, inf=inf, current_size=current_size, max_size=int(max_size)/1000, max_upload_size=max_upload_size)


@app.route('/file/')
def file_operation():
    if request.args.get('file'):
        file = request.args.get('file')
        if file.split(".")[-1] == "jpg" or file.split(".")[-1] == "png" or file.split(".")[-1] == "txt" or file.split(".")[-1] == "pdf":
            return send_file(f'{upload_location}{file}')
        else:
            return send_file(f'{upload_location}{file}', as_attachment=True, attachment_filename=f'{file}')
    elif request.args.get('delete'):
        file = request.args.get('delete')

        x = os.listdir(upload_location)
        t = []

        for elem in x:
            if os.path.isdir(f"{upload_location}{elem}"):
                pass
            else:
                t.append(elem)

        if file in t:
            os.remove(f"{upload_location}{file}")
        else:
            pass

        return redirect('/')
    else:
        pass


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():

    f = request.files['file']
    filename = f.filename

    if filename == "":
        return redirect('/')
    else:
        f.save(f"{tmp_location}/temp_file")
        size = os.stat(f"{tmp_location}/temp_file").st_size

        file_size = 0
        for files in glob.glob(f"{upload_location}*"):
            file_size = file_size + os.path.getsize(files)

        current_size = (str(file_size)).split(".")[0]

        if (size + int(current_size)) > int(max_size):
            try:
                os.remove(f"{tmp_location}/temp_file")
                return redirect('/')
            except:
                return redirect('/')
        else:
            destination = f"{upload_location}{filename}"

            if os.path.isfile(f"{tmp_location}/temp_file"):
                shutil.move(f"{tmp_location}/temp_file", destination)
                return redirect('/')
            else:
                return redirect('/')

@app.route('/zodiacc/')
def about():
    return redirect("https://github.com/TheZodiaCC")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)