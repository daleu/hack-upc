#all the imports
import sqlite3
import os
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
from contextlib import closing
from sqlalchemy import text
from werkzeug import secure_filename
from instagram.client import InstagramAPI

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = '/home/quim/html/flaskr/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
access_token = "243316452.1677ed0.aaf45b2c124449a3a53fc51ae5e0a214"

# application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def show_entries():
    return render_template('layout.html')

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	sql = g.db.execute('select username from users')
	boolean = None
	username = None
	for row in sql:
	    if request.form['username'] == row[0]:
		 boolean = True
	         username = row[0]
	if boolean:
            sql = g.db.execute('select pass from users where username="' + username + '"')
            names = []
	    password = None
            for row in sql:
	        password = row[0]
	    if request.form['password'] == password:
		session['logged_in'] = True
		flash('You were logged in')
		return redirect(url_for('show_entries'))
	    else:
		error = 'Invalid password'
		return render_template('login.html', error=error)
	else:
	    error = 'Invalid user'
	    return render_template('login.html', error=error)
    return render_template('login.html', error=error)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/submit_image', methods=['POST'])
def submit_image():
    file = request.files['image']
    if file and allowed_file(file.filename):
	    filename = secure_filename(file.filename)
	    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	    url = 'https://www.wolframcloud.com/objects/0200604e-85e2-4f0a-9a58-8cfc6d34788d?url='
	    path = 'http://46.101.213.69/uploads/' + filename
	    req = requests.get(url + path)
	    array = req.text.split('"')
	    #names -> object with the generated tags
	    names = []
	    for i in range(0,len(array)-1):
	    	if (i%2 == 1):
	    		names.append(array[i])

	    api = InstagramAPI(
	    	access_token=access_token,
	    	client_ips="8ab1830bac414c72b81daa905f890a3e",
	    	client_secret="b8608ed65a644382a82312113ac39af2")

	    media_with_location=[]
	    all_media_ids = []
	    media_ids,next = api.tag_recent_media(tag_name='france', count=1000)
	    position_tuple = ()
	    for media_id in media_ids:
	    	all_media_ids.append(media_id.id)
	    	#some media_ids don't have location assoicated with them... this maybe a hacky way of doing it, but it works
	    	if "location" in dir(media_id):
	    		#you can do it this way if that is the way you want your information, I did it using Tuples to have your data more organized and easir to access once its VERY large.
	    		#position = str(media_id.id) + "," + str(media_id.location.point.latitude) + ',' + str(media_id.location.point.longitude) + ';' + str(media_id.get_standard_resolution_url())
	    		# i found that some of the data doesn't have a full location ... so this just to check for that case.
	    		if ("point" in dir(media_id.location)) and ("latitude" in dir(media_id.location.point)) and ("longitude" in dir(media_id.location.point)):
	    			position_tuple=(str(media_id.id),str(media_id.location.point.latitude),str(media_id.location.point.longitude),str(media_id.get_standard_resolution_url()))
	    			media_with_location.append(position_tuple)
		#print media_with_location
	    media_with_location2=[]
	    all_media_ids2 = []
	    media_ids2,next = api.tag_recent_media(tag_name='trip', count=1000)
	    position_tuple2 = ()
	    for media_id in media_ids2:
	    	all_media_ids2.append(media_id.id)
	    	#some media_ids don't have location assoicated with them... this maybe a hacky way of doing it, but it works
	    	if "location" in dir(media_id):
	    		#you can do it this way if that is the way you want your information, I did it using Tuples to have your data more organized and easir to access once its VERY large.
	    		#position = str(media_id.id) + "," + str(media_id.location.point.latitude) + ',' + str(media_id.location.point.longitude) + ';' + str(media_id.get_standard_resolution_url())
	    		# i found that some of the data doesn't have a full location ... so this just to check for that case.
	    		if ("point" in dir(media_id.location)) and ("latitude" in dir(media_id.location.point)) and ("longitude" in dir(media_id.location.point)):
	    			position_tuple2=(str(media_id.id),str(media_id.location.point.latitude),str(media_id.location.point.longitude),str(media_id.get_standard_resolution_url()))
	    			media_with_location2.append(position_tuple)

	    #print media_with_location2

	    trobat = None
	    location = ''

	    for i in media_with_location:
	    	for j in media_with_location2:
	    		if (i==j and trobat==None):
	    			location = i[1] + "," + i[2]
	    			trobat = True

	    if (trobat == None):
	    	location = i[1] + "," + i[2]
	    return render_template('list_items.html', word=names)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'GET':
	    return render_template('register.html', error=error)
    else:
	    sql = g.db.execute('select username from users')
	    names = []
	    for row in sql:
		names.append(row[0])
	    boolean = None
	    for name in names:
		if request.form['username'] == name:
		     boolean = True
	    if boolean:
    	        error = 'User already exists'
		return render_template('register.html', error= error)
	    else:
		g.db.execute('insert into users (username, pass) values (?, ?)', [request.form['username'], request.form['password']])
		g.db.commit()
		print "user registered"
	        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
