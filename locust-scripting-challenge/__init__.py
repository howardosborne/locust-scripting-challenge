import os
from flask import Flask, render_template, abort, redirect, url_for, request, make_response, jsonify, session
import random, string

app = Flask(__name__)

#might want to think about how to stop these lists from getting very large...
session['one_time_tokens'] = []
session['tokens'] = {}
session['list_of_items'] = []
session['list_of_cookies'] = []
session['list_of_headers'] = []

@app.route('/')
def test(token=None):
    token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    session['one_time_tokens'].append(token)
    return render_template('test.html', token=token)

@app.route('/api/verify_correlation')
def verify_correlation():
    #verify that the values passed through were correct
    #if so, return an item_id in json format
    token = request.args.get('token', '')
    username = request.args.get('username', '')
    print(session['one_time_tokens'])
    if token in session['one_time_tokens']:
        session['one_time_tokens'].remove(token)
        session['tokens'][token] = username
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
    return 'So long and thanks for all the fish'

@app.route('/api/urlencoded/<message>')
def urlencoded(message=None):
    #just capture - not verify it...
    item_list = []
    for i in range(5):
        item_list.append(''.join(random.choices(string.digits, k=7)))
    html_list = '</li><li>'.join(item_list)
    lowest_item = sorted(item_list)[0]
    session['list_of_items'].append(lowest_item)
    return '<ul><li>' + html_list + '</li></ul>'

@app.route('/api/html_extract/<lowest_item>')
def html_extract(lowest_item=None):
    print(session['list_of_items'])
    if lowest_item in session['list_of_items']:
        session['list_of_items'].remove(lowest_item)
        cookie = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        session['list_of_cookies'].append(cookie)
        return 'custom_cookie=' + cookie + ''
    else:
        abort(400)

@app.route('/api/cookie')
def parse_cookie():
    #look for cookie
    cookie = request.cookies.get('custom_cookie')
    if cookie in session['list_of_cookies']:
        session['list_of_cookies'].remove(cookie)
        header = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        session['list_of_headers'].append(header)
        return header 
    else:
        abort(400) 

@app.route('/api/header')
def parse_header():
    #look for cookie
    header = request.headers.get('custom_header')
    username = session['tokens'][request.cookies.get("token")]
    if header in session['list_of_headers']:
        session['list_of_headers'].remove(header)
        del session['tokens'][request.cookies.get("token")]
        return f'Well done {username}'
    else:
        abort(400) 
