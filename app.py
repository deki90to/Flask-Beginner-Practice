from flask import Flask, render_template, request, redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
db = SQLAlchemy(app)

class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return (f'Name: {self.id}')



@app.route('/')
def index():
	name = 'Dejan Jovanovic'
	return render_template('index.html', name=name)


@app.route('/about')
def about():
	names = ['Rachel', 'Monica', 'Phoebe', 'Joey', 'Chandler', 'Ross']
	return render_template('about.html', names=names)


@app.route('/subscribe')
def subscribe():
	title = 'Subscribe To My Channel'
	return render_template('subscribe.html', title=title)


@app.route('/form', methods=['POST'])
def form():
	first_name = request.form.get('first_name') 
	last_name = request.form.get('last_name')
	e_mail = request.form.get('e_mail')


	message = 'You have beed subscribed to my channel'
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login('deki90to@gmail.com', '> enterUserPassword <')
	server.sendmail('deki90to@gmail.com', e_mail, message)

	if not first_name or not last_name or not e_mail:
		error = 'All Fields Required'
		return render_template('subscribe.html', error=error, first_name=first_name, last_name=last_name, e_mail=e_mail)

	title = 'Thanks for subscribe'
	return render_template('form.html', title=title, first_name=first_name, last_name=last_name, e_mail=e_mail)


@app.route('/friends', methods=['POST', 'GET'])
def friends():
	title = 'My Friends List'

	if request.method == 'POST':
		friend_name = request.form['name']
		new_friend = Friends(name=friend_name)

		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/friends')

		except:
			return 'There was an error adding'
	else:
		friends = Friends.query.order_by(Friends.date)
		return render_template('friends.html', title=title, friends=friends)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	update_friend = Friends.query.get_or_404(id)

	if request.method == 'POST':
		update_friend.name = request.form['name']

		try:
			db.session.commit()
			return redirect('/friends')
		except:
			return 'There was a problem with updating name'
	else:
		return render_template('update.html', update_friend=update_friend)


@app.route('/delete/<int:id>')
def delete(id):
	delete_friend = Friends.query.get_or_404(id)

	try:
		db.session.delete(delete_friend)
		db.session.commit()
		return redirect('/friends')
	except:
		return 'Problem with deleting'