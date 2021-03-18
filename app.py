from flask import Flask, render_template, request
import smtplib



app = Flask(__name__)

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

	if not first_name or not last_name or not e_mail:
		error = 'All Fields Required'
		return render_template('subscribe.html', 
			error=error, first_name=first_name, 
			last_name=last_name, 
			e_mail=e_mail)

	title = 'Thanks for subscribe'
	return render_template('form.html', title=title, 
		first_name=first_name, 
		last_name=last_name, 
		e_mail=e_mail)