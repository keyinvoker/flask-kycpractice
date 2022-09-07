from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, fields
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/kycapp'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    ktp = db.Column(db.String(16), nullable=False)
    npwp = db.Column(db.String(20), nullable=False)
    last_verified = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        salary = request.form['salary']
        ktp = request.form['ktp']
        npwp = request.form['npwp']

        last_verified = date.today()

        new_user = Users(
            name=name,
            email=email,
            phone=phone,
            address=address,
            salary=salary,
            ktp=ktp,
            npwp=npwp,
            # password = password,
            last_verified = last_verified,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed adding user!'
    else:
        return render_template('register.html')

@app.route('/verify/<int:id>', methods=['POST', 'GET'])
def verify(id):
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']
        user.salary = request.form['salary']
        user.ktp = request.form['ktp']
        user.npwp = request.form['npwp']
        user.last_verified = date.today()
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed updating user!'
    else:
        return render_template('verify.html', user=user)
