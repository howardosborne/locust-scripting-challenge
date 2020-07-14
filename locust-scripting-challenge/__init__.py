import os
from flask import Flask, flash, render_template, abort, redirect, url_for, request, make_response, jsonify, session
from werkzeug.utils import secure_filename
import random, string

app = Flask(__name__)
app.secret_key = b'sdvsdkdsfdaw4ttgsdvzdgwtasq242'

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
        return f'<p>Well done {session["username"]}.</p><p> When you have written your script, submit it <a href="/submit_script">here</a> and if it passes, you\'ll appear on the <a href="/challenge_met">Challenge Met</a> board.</p>'
    else:
        abort(400) 

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'py'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/submit_script', methods=['GET', 'POST'])
def submit_script():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_folder = 'test_script_' + ''.join(random.choices(string.ascii_lowercase, k=5))
            appended_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder)
            os.mkdir(appended_path)
            full_pathname = os.path.join(app.config['UPLOAD_FOLDER'], new_folder, filename)
            status_filename = os.path.join(app.config['UPLOAD_FOLDER'], new_folder, "status.json")
            file.save(full_pathname)
            username = request.form['username']
            status_output = f'{{status:"uploaded",id:"{new_folder}",username:{username}}}'
            status_file = open(status_filename,"w")
            status_file.write(status_output)
            return f'Thanks'
    return '''
    <div class="form-group">
        <form method=post enctype=multipart/form-data action="/submit_script">
            <label for="file">script</label>
            <input class="form-control" type=file name="file">
            <label for="username">Name (publicly visible)</label>
            <input class="form-control" id="username" name="username">
            <input type=submit value=Upload>
        </form>
    </div>
    '''
@app.route('/challenge_met')
def submit_script():
    return "challenge_met!"
