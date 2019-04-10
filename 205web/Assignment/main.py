from flask import Flask, render_template, request, session, url_for, redirect
from hihihi import *
import os
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

UPLOAD_FOLDER = os.getcwd() + '/static' + '/upload'
UPLOAD_FOLDER2 = os.getcwd() + '/static' + '/upload' + '/icon'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

engine = create_engine('sqlite:///DataBase.db', echo=True)
app = Flask(__name__)
mail = Mail(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '2019205project@gmail.com'
app.config['MAIL_PASSWORD'] = '2019205CDE'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###################################################################################################

#Home Page

###################################################################################################

@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('Home.html', username = 'Guest')
	else:
		return render_template('Home.html', username = session['username'])

###################################################################################################

#About

###################################################################################################
@app.route('/About')
def About():
	bg = "background-image: url("+url_for('static', filename='zz3.jpg')+")"
	if not session.get('logged_in'):
		return render_template('About.html', username = 'Guest', bg = bg)
	else:
		return render_template('About.html', username = session['username'], bg = bg)

###################################################################################################

#Course Detail

###################################################################################################
@app.route('/Detail')
def Detail():
	bg = "background-image: url("+url_for('static', filename='freedom2.jpg')+")"
	if not session.get('logged_in'):
		return render_template('Detail.html', username = 'Guest', bg = bg)
	else:
		return render_template('Detail.html', username = session['username'], bg = bg)

###################################################################################################

#Gallery

###################################################################################################
@app.route('/gallery')
def gallery():
	Session = sessionmaker(bind=engine)
	S = Session()

	line = S.query(Image).all()
	List=[]
	for i in line:
		image=0
		try:
			f = open('static/upload/' + str(i.ImageName) + '.' + 'png')
			f.close()
			image=1
		except Exception:
			try:
				f = open('static/upload/' + str(i.ImageName) + '.' + 'jpg')
				f.close()
				image=2
			except Exception:
				try:
					f = open('static/upload/' + str(i.ImageName) + '.' + 'jpeg')
					f.close()
					image=3
				except Exception:
					break
		if image == 1:
			List.append('png')
		elif image == 2:
			List.append('jpg')
		elif image == 3:
			List.append('jpeg')
		elif image == 0:
			if not session.get('logged_in'):
				return render_template('Gallery.html', username = 'Guest')
			else:
				return render_template('Gallery.html', username = session['username'])
	if not session.get('logged_in'):
		return render_template('Gallery.html', username = 'Guest', line=line, List=List)
	else:
		return render_template('Gallery.html', username = session['username'], line=line, List=List)

###################################################################################################

#Upload Image

###################################################################################################

@app.route('/uploadi', methods=['GET', 'POST'])
def uploadi():
    if request.method == 'POST':
    	file = request.files['uploadimage']
    	name = request.form['newname']
    	if Path(os.getcwd() + '/static/upload' + str(name) + '.png').exists():
    		return render_template('Error3.html')
    	elif Path(os.getcwd() + '/static/upload' + str(name) + '.jpg').exists():
    		return render_template('Error4.html')
    	elif Path(os.getcwd() + '/static/upload' + str(name) + '.jpeg').exists():
    		return render_template('Error5.html')
    	else:
	        if 'uploadimage' not in request.files:
	            return render_template('Error.html')
	        file = request.files['uploadimage']
	        if file.filename == "":
	            return ImageError()
	        if name == "":
	        	return ImageError()
	        if file and allowed_file(file.filename):
	        	Session = sessionmaker(bind=engine)

	        	S = Session()
	        	S.add(Image(ImageName=name))
	        	S.commit()


		        filename = str(name) + '.' + secure_filename(file.filename).split('.')[-1]
		        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		        return AdminPage()
###################################################################################################

#Course

###################################################################################################

@app.route('/junior')
def junior():
	bg = "background-image: url("+url_for('static', filename='wing2.jpg')+")"
	if session.get('logged_in'):
		return render_template('JuniorCourse.html',bg=bg, username = session['username'])

@app.route('/juniorform', methods = ['POST', 'GET'])
def juniorform():
	bg = "background-image: url("+url_for('static', filename='wing2.jpg')+")"
	if request.method == 'POST':
		name = request.form['username']
		part = request.form['part']
		phone = request.form['phoneno']
		email = request.form['Email']
		date = request.form['Date']
		option = request.form['Option']
		pay = request.form['Payment']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(JuniorForm).filter(JuniorForm.Name.in_([name]))
		line2 = S.query(JuniorForm).filter(JuniorForm.Phone.in_([phone]))
		line3 = S.query(JuniorForm).filter(JuniorForm.Email.in_([email]))
		line4 = S.query(JuniorForm).filter(JuniorForm.Time.in_([date]))
		line5 = S.query(JuniorForm).filter(JuniorForm.Option.in_([option]))
		line6 = S.query(JuniorForm).filter(JuniorForm.Payment.in_([pay]))
		line7 = S.query(JuniorForm).filter(JuniorForm.Part.in_([part]))
		record = line.first()
		record2 = line2.first()
		record3 = line3.first()
		record4 = line4.first()
		record5 = line5.first()
		record6 = line6.first()
		record7 = line7.first()

		if name == "" or part == "" or email == "" or phone == "" or date == "" or pay == "":
			return Error9()
		else:
			S.add(JuniorForm(Name=name, Part=part, Phone=phone, Email=email, Time=date, Option=option, Payment=pay))

			S.commit()
			return render_template("JuniorCourse.html",bg=bg, username = session['username'])

@app.route('/senior')
def senior():
	bg = "background-image: url("+url_for('static', filename='baba2.jpg')+")"
	if session.get('logged_in'):
		return render_template('SeniorCourse.html',bg=bg, username = session['username'])

@app.route('/seniorform', methods = ['POST', 'GET'])
def seniorform():
	bg = "background-image: url("+url_for('static', filename='baba2.jpg')+")"
	if request.method == 'POST':
		name = request.form['username']
		part = request.form['part']
		phone = request.form['phoneno']
		email = request.form['Email']
		date = request.form['Date']
		option = request.form['Option']
		pay = request.form['Payment']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(SeniorForm).filter(SeniorForm.Name.in_([name]))
		line2 = S.query(SeniorForm).filter(SeniorForm.Phone.in_([phone]))
		line3 = S.query(SeniorForm).filter(SeniorForm.Email.in_([email]))
		line4 = S.query(SeniorForm).filter(SeniorForm.Time.in_([date]))
		line5 = S.query(SeniorForm).filter(SeniorForm.Option.in_([option]))
		line6 = S.query(SeniorForm).filter(SeniorForm.Payment.in_([pay]))
		line7 = S.query(SeniorForm).filter(SeniorForm.Part.in_([part]))
		record = line.first()
		record2 = line2.first()
		record3 = line3.first()
		record4 = line4.first()
		record5 = line5.first()
		record6 = line6.first()
		record7 = line7.first()

		if name == "" or part == "" or email == "" or phone == "" or date == "" or pay == "":
			return Error10()
		else:
			S.add(SeniorForm(Name=name, Part=part, Phone=phone, Email=email, Time=date, Option=option, Payment=pay))

			S.commit()
			return render_template("SeniorCourse.html",bg=bg, username = session['username'])

###################################################################################################

#OEM

###################################################################################################

@app.route('/oem')
def oem():
	bg = "background-image: url("+url_for('static', filename='zz4.jpg')+")"
	if not session.get('logged_in'):
		return render_template('OEM.html', bg=bg, username = 'Guest')
	else:
		return render_template('OEM.html', bg=bg, username = session['username'])

@app.route('/OEMF', methods = ['POST', 'GET'])
def OEMF():
	bg = "background-image: url("+url_for('static', filename='zz4.jpg')+")"
	if request.method == 'POST':
		name = request.form['name']
		phone = request.form['phoneno']
		email = request.form['Email']
		option = request.form['Option']
		pname = request.form['Pname']
		price = request.form['Price']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(OEM).filter(OEM.Name.in_([name]))
		line2 = S.query(OEM).filter(OEM.Phone.in_([phone]))
		line3 = S.query(OEM).filter(OEM.Email.in_([email]))
		line4 = S.query(OEM).filter(OEM.Option.in_([option]))
		line5 = S.query(OEM).filter(OEM.Pname.in_([pname]))
		line6 = S.query(OEM).filter(OEM.Price.in_([price]))
		record = line.first()
		record2 = line2.first()
		record3 = line3.first()
		record4 = line4.first()
		record5 = line5.first()
		record6 = line6.first()

		if name == "" or phone == "" or email == "" or pname == "" or price == "":
			return Error7()
		else:
			S.add(OEM(Name=name, Phone=phone, Email=email, Pname=pname, Price=price, Option=option))

			S.commit()
			return render_template("OEM.html",bg=bg, username = session['username'])

@app.route('/Del', methods = ['POST', 'GET'])
def Del():
	if request.method == 'POST':
		Session = sessionmaker(bind=engine)

		S = Session()
		line1 = S.query(OEM).filter(OEM.Name.in_([session['username']])).all()
		line2 = S.query(Admin).first().AdminName
		for i in line1:
			try:
				ID = request.form[str(i.id)]
				S.query(OEM).filter(OEM.id.in_([i.id])).first().Name = line2
				S.commit()
				return Personal()
			except Exception:
				pass
	else:
		return Personal()


###################################################################################################

#Register

###################################################################################################

@app.route('/register')
def register():
	return render_template('Register.html', username = 'Guest')

@app.route('/Register', methods = ['POST', 'GET'])
def Register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['Email']
		phone = request.form['phoneno']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(User).filter(User.Username.in_([username]))
		line2 = S.query(User).filter(User.Password.in_([password]))
		line3 = S.query(User).filter(User.PhoneNO.in_([phone]))
		line4 = S.query(User).filter(User.Email.in_([email]))
		line5 = S.query(Admin).filter(Admin.AdminName.in_([username]))
		line6 = S.query(Admin).filter(Admin.AdminPassword.in_([password]))
		record = line.first()
		record2 = line2.first()
		record3 = line3.first()
		record4 = line4.first()
		record5 = line5.first()
		record6 = line6.first()

		if record:
			return Error()
		elif record2:
			return Error2()
		elif record3:
			return Error3()
		elif record4:
			return Error4()
		elif record5:
			return index()
		elif record6:
			return index()
		elif username == "" or password == "" or email == "" or phone == "":
			return Error5()
		elif len(str(phone)) <= 15 and len(str(username)) <= 15 and len(str(password)) <= 10: 
			S.add(User(Username=username, Password=password, PhoneNO=phone, Email=email))

			S.commit()
			return render_template("Home.html", username = 'Guest')
		else:
			return redirect(url_for("RegError"))
###################################################################################################

#Login

###################################################################################################

@app.route('/login')
def login():
	return render_template('Login.html', username = 'Guest')

@app.route('/Login', methods = ['POST', 'GET'])
def Login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(User).filter(User.Username.in_([username]), User.Password.in_([password]))
		line5 = S.query(Admin).filter(Admin.AdminName.in_([username]), Admin.AdminPassword.in_([password]))
		record = line.first()
		record5 = line5.first()

		if record:
			session['logged_in'] = True
			session['username'] = username
			return index()
		elif record5:
			session['logged_in'] = True
			session['username'] = username
			session['admin'] = username
			return AdminPage()
		elif username == "" or password == "":
			return Error8()
		else:
			return LoginError()

###################################################################################################

#Email

###################################################################################################

@app.route('/Forget', methods=['POST', 'GET'])
def Forget():
	if request.method == 'POST':
		username = request.form['name']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(User).filter(User.Username.in_([username]))
		record = str(line.first().Password)
		record2 = str(line.first().Email)
		msg = Message('Hello User', sender = '2019205project@gmail.com', recipients = [record2])
		msg.body = "This is your user password:" + "" + record
		mail.send(msg)
		return index()

###################################################################################################

#Icon

###################################################################################################

@app.route('/uploadicon', methods=['GET', 'POST'])
def uploadicon():
    if request.method == 'POST':
    	file = request.files['uploadicon']
    	if 'uploadicon' in request.files:
    		file = request.files['uploadicon']
    		if file.filename == '':
    			return render_template('UserPage.html')
    		elif file and allowed_file(file.filename):
    			filename = str(session['username']) + '.' + secure_filename(file.filename).split('.')[-1]
    			file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
    			return redirect(url_for('Personal'))
    		else:
    			return render_template('UserPage.html', username = session['username'])
###################################################################################################

#Logout

###################################################################################################

@app.route('/Logout')
def Logout():
	session['logged_in'] = False
	session.clear()

	return index()
###################################################################################################

#Personal Page

###################################################################################################

@app.route('/Personal')
def Personal():
	Session = sessionmaker(bind=engine)

	S = Session()
	line = S.query(OEM).filter(OEM.Name.in_([session['username']])).all()
	line2 = S.query(JuniorForm).filter(JuniorForm.Name.in_([session['username']])).all()
	line3 = S.query(SeniorForm).filter(SeniorForm.Name.in_([session['username']])).all()
	if Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.png').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.png'
	elif Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.jpg').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.jpg'
	elif Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.jpeg').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.jpeg'
	else:
		icon = '/static/upload/icon/' + 'Defaulticon.png'

	return render_template('UserPage.html', line=line, line2=line2, line3=line3, username = session['username'], icon = icon)

###################################################################################################

#Edit Pwd

###################################################################################################
@app.route('/Change', methods = ['POST', 'GET'])
def Change():
	if request.method == 'POST':
		password = request.form['password']
		npassword= request.form['new']
		change = session['username']

		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(User).filter(User.Password.in_([password]))
		line2 = S.query(User).filter(User.Password.in_([npassword]))
		record = line.first()
		record2 = line2.first()

		if record:
			if not record2:
				if npassword != "":
					if password != "":
						if npassword == password:
					 		return Repeat()
						else:
							S.query(User).filter(User.Username.in_([change])).first().Password = npassword

							S.commit()
							return index()
					else:
						return ChangeError()
				else:
					return ChangeError()
			else:
				return ChangeError()
		else:
			return ChangeError()
###################################################################################################

#Admin

###################################################################################################

@app.route('/AdminPage')
def AdminPage():
		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(JuniorForm).all()
		line2 = S.query(SeniorForm).all()
		line3 = S.query(OEM).all()


		return render_template('Admin.html',line=line,line2=line2,line3=line3, username = session['username'])

###################################################################################################

#Error

###################################################################################################

@app.route('/Error')
def Error():
	if not session.get('logged_in'):
		return render_template('Error.html', username = 'Guest')
	else:
		return render_template('Error.html', username = session['username'])

@app.route('/Error2')
def Error2():
	if not session.get('logged_in'):
		return render_template('Error2.html', username = 'Guest')
	else:
		return render_template('Error2.html', username = session['username'])

@app.route('/Error3')
def Error3():
	if not session.get('logged_in'):
		return render_template('Error3.html', username = 'Guest')
	else:
		return render_template('Error3.html', username = session['username'])

@app.route('/Error4')
def Error4():
	if not session.get('logged_in'):
		return render_template('Error4.html', username = 'Guest')
	else:
		return render_template('Error4.html', username = session['username'])

@app.route('/Error5')
def Error5():
	if not session.get('logged_in'):
		return render_template('Error5.html', username = 'Guest')
	else:
		return render_template('Error5.html', username = session['username'])

@app.route('/RegError')
def RegError():
	return register()

@app.route('/Error7')
def Error7():
	bg = "background-image: url("+url_for('static', filename='zz4.jpg')+")"
	if not session.get('logged_in'):
		return render_template('Error7.html', username = 'Guest', bg=bg)
	else:
		return render_template('Error7.html', username = session['username'], bg=bg)

@app.route('/Error8')
def Error8():
	if not session.get('logged_in'):
		return render_template('Error8.html', username = 'Guest')
	else:
		return render_template('Error8.html', username = session['username'])

@app.route('/Error9')
def Error9():
	bg = "background-image: url("+url_for('static', filename='wing2.jpg')+")"
	if not session.get('logged_in'):
		return render_template('Error9.html', username = 'Guest', bg=bg)
	else:
		return render_template('Error9.html', username = session['username'], bg=bg)

@app.route('/Error10')
def Error10():
	bg = "background-image: url("+url_for('static', filename='baba2.jpg')+")"
	if not session.get('logged_in'):
		return render_template('Error10.html', username = 'Guest', bg=bg)
	else:
		return render_template('Error10.html', username = session['username'], bg=bg)

@app.route('/LoginError')
def LoginError():
	if not session.get('logged_in'):
		return render_template('LoginError.html', username = 'Guest')
	else:
		return render_template('LoginError.html', username = session['username'])

@app.route('/ChangeError')
def ChangeError():
	Session = sessionmaker(bind=engine)

	S = Session()
	line = S.query(OEM).filter(OEM.Name.in_([session['username']])).all()
	line2 = S.query(JuniorForm).filter(JuniorForm.Name.in_([session['username']])).all()
	line3 = S.query(SeniorForm).filter(SeniorForm.Name.in_([session['username']])).all()
	if Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.png').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.png'
	elif Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.jpg').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.jpg'
	elif Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.jpeg').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.jpeg'
	else:
		icon = '/static/upload/icon/' + 'Defaulticon.png'
	if not session.get('logged_in'):
		return render_template('ChangeError.html', username = 'Guest')
	else:
		return render_template('ChangeError.html', line=line, line2=line2, line3=line3, username = session['username'], icon = icon)

@app.route('/Repeat')
def Repeat():
	Session = sessionmaker(bind=engine)

	S = Session()
	line = S.query(OEM).filter(OEM.Name.in_([session['username']])).all()
	line2 = S.query(JuniorForm).filter(JuniorForm.Name.in_([session['username']])).all()
	line3 = S.query(SeniorForm).filter(SeniorForm.Name.in_([session['username']])).all()
	if Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.png').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.png'
	elif Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.jpg').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.jpg'
	elif Path(os.getcwd() + '/static/upload/icon/' + str(session['username']) + '.jpeg').exists():
		icon = '/static/upload/icon/' + str(session['username']) + '.jpeg'
	else:
		icon = '/static/upload/icon/' + 'Defaulticon.png'
	if not session.get('logged_in'):
		return render_template('Repeat.html', username = 'Guest')
	else:
		return render_template('Repeat.html', line=line, line2=line2, line3=line3, username = session['username'], icon = icon)

@app.route('/ImageError')
def ImageError():
		Session = sessionmaker(bind=engine)

		S = Session()
		line = S.query(JuniorForm).all()
		line2 = S.query(SeniorForm).all()
		line3 = S.query(OEM).all()

		if not session.get('logged_in'):
			return render_template('ImageError.html', username = 'Guest')
		else:
			return render_template('ImageError.html',line=line,line2=line2,line3=line3, username = session['username'])

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True)