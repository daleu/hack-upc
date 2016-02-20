#all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from sqlalchemy import text

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

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
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

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
