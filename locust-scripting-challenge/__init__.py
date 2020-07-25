import os, subprocess, glob
from flask import Flask, flash, render_template, abort, redirect, url_for, request, make_response, jsonify, session
import requests
from werkzeug.utils import secure_filename
import random, string

app = Flask(__name__)
app.secret_key = b'sdvsdkdsfdaw4ttgsdvzdgwtasq242'

if os.name == 'nt':
    UPLOAD_FOLDER = "./uploads"
else:
    UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'py'}
#if the upload folder doesn't exist, add it
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def test(token=None):
    session['one_time_tokens'] = ""
    session['username'] = ""
    session['list_of_items'] = ""
    session['list_of_cookies'] = ""
    session['list_of_headers'] = ""
    token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    session['one_time_tokens'] = token
    return render_template('test.html', token=token)

@app.route('/challenge_board')
def challenge_board():
    import json
    response = requests.get('https://adhoc-results-server.herokuapp.com/results/get/4')
    completed = "<ul>"
    json_response = json.loads(response.text)
    for item in json_response:
        completed += "<li>" + item['name'] + "</li>"
    completed += "</ul>"
    return render_template('challenge_board.html', completed=completed)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/submit_script', methods=['POST'])
def submit_script():
    if 'file' not in request.files:
        flash('No file part')
        return render_template('upload.html')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return render_template('upload.html')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        username = request.form['username']
        meta_data = {"username": username}
        url = "https://adhoc-file-server.herokuapp.com/scripting-challenge/submit_script"
        files = {'file': (file.filename, file.read())}
        requests.post(url, data=meta_data, files=files)
        return render_template('challenge_board.html')
    else:
        return render_template('upload.html')

#test_steps

@app.route('/api/verify_correlation')
def verify_correlation():
    #verify that the values passed through were correct
    #if so, return an item_id in json format
    token = request.args.get('token', '')
    username = request.args.get('username', '')
    print(session['one_time_tokens'])
    if token == session['one_time_tokens']:
        session['username'] = username
        response_text = '{"status":"OK", "item_id":"' + ''.join(random.choices(string.digits, k=10)) + '"}'
        resp = make_response(response_text)
        resp.set_cookie('token', token)
        return resp
    else:
        abort(400)

@app.route('/api/parse_json', methods=['POST'])
def parse_json():
    #just going to parse it - not verify it...
    item_id = request.get_json()['item_id']
    return 'So long, and thanks for all the fish!'

@app.route('/api/urlencoded/<message>')
def urlencoded(message=None):
    #just capture - not verify it...
    item_list = []
    for i in range(5):
        item_list.append(''.join(random.choices(string.digits, k=7)))
    html_list = '</li><li>'.join(item_list)
    lowest_item = sorted(item_list)[0]
    session['list_of_items'] = lowest_item
    return '<ul><li>' + html_list + '</li></ul>'

@app.route('/api/html_extract/<lowest_item>')
def html_extract(lowest_item=None):
    print(session['list_of_items'])
    if session['list_of_items'] == lowest_item:
        cookie = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        session['list_of_cookies'] = cookie
        return 'custom_cookie=' + cookie + ''
    else:
        abort(400)

@app.route('/api/cookie')
def parse_cookie():
    #look for cookie
    cookie = request.cookies.get('custom_cookie')
    if session['list_of_cookies'] == cookie:
        header = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        session['list_of_headers'] = header
        return header 
    else:
        abort(400) 

@app.route('/api/header')
def parse_header():
    #look for cookie
    header = request.headers.get('custom_header')
    if session['list_of_headers'] == header:
        #return f'<p>Well done {session["username"]}. When you have written your script, upload it <a href="/upload">here</a>.'
        return f'<p>Well done {session["username"]}.'
    else:
        abort(400) 

#for getting files that have been uploaded

@app.route('/api/uploads')
def uploads():
    glob_pattern = os.path.join(app.config['UPLOAD_FOLDER'],"*","*.py")
    return jsonify(glob.glob(glob_pattern))

@app.route('/api/uploaded_script/<test_folder>/<filename>')
def uploaded_script(test_folder=None,filename=None):
    #think about removing anything potentially malicious
    file_contents = open(os.path.join(app.config['UPLOAD_FOLDER'], test_folder, filename)).read()
    return file_contents
