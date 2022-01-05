from flask import Flask,session,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db,connect_db,User,MedicalCenter,UserMedicalCenter
from forms import RegisterUserForm,LoginUserForm,EditEmail,EditTitle,EditPassword,DeleteAccountForm
from flask_bcrypt import Bcrypt
from datetime import date
from sqlalchemy.exc import IntegrityError
import geocoder
from geopy.geocoders import Nominatim
import requests
import os


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ='postgresql:///ems_gps_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SQLALCHEMY_ECHO"]=True
app.config['SECRET_KEY']='854f46078d77cb798c4615f5d1bfc1302a28844340fda940b3120671b2c3f26364dd0275e362a9bb952083387599420d6ec9d60fea4791'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]=False

debug = DebugToolbarExtension(app)


connect_db(app)

bcrypt = Bcrypt()

today_date = date.today()
g = geocoder.ip('me')
string_loc = str(f"{g.latlng[1]},{g.latlng[0]}")
# string_loc = "-104.81614200518457, 39.58123985953683"
# string_loc = "-95.36450545466745, 29.763025340291243"

url_news = "https://bing-news-search1.p.rapidapi.com/news"

querystring = {"safeSearch":"Off","textFormat":"Raw"}

headers = {
    'x-bingapis-sdk': "true",
    'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
    'x-rapidapi-key': "d679a166f2msh7b54a2db9eea6c3p124dc4jsna3a4150de9b1"
    }

response = requests.request("GET", url_news, headers=headers, params=querystring)

url_geo = f"https://api.mapbox.com/geocoding/v5/mapbox.places/hospital.json?proximity={string_loc}&limit=10&access_token=pk.eyJ1IjoiZ3JleW1lbmV6IiwiYSI6ImNrdTN4N2thZjFzdnMyb283bDZiOHkzNW0ifQ.QJmv9m2vcBuuVQ7N0FZZ3A"
# url_geo = f"https://api.mapbox.com/geocoding/v5/mapbox.places/hospital.json?type=poi&proximity={string_loc}&access_token=pk.eyJ1IjoiZ3JleW1lbmV6IiwiYSI6ImNrdm0xaXkyNDNhcjUydXFpazZoN3dzejEifQ.3UPkaylDPQMh9yeUMxiLUw"

hospitals_located = []

def locate_hospitals():
    
    res = requests.get(url_geo)
    data = res.json()
    for d in data['features']:
        if d not in hospitals_located:
            hospitals_located.append(d)
        else:
            None
    return hospitals_located

def get_medical_center_data():
    res = requests.get(url_geo)
    data = res.json()
    place_address_list = []
    facility_name_list = []
    category_list = []
    coordinates_list = []
    for d in data['features']:
        place_address = d['place_name']
        facility_name = d['text']
        category = d['properties']['category']
        coordinates = d['geometry']['coordinates']

        place_address_list.append(place_address)
        facility_name_list.append(facility_name)
        category_list.append(category)
        coordinates_list.append(coordinates)
    med_centers = [MedicalCenter(place_address=p,facility_name=f,category=ca,coordinates=co) for p,f,ca,co in zip(place_address_list,facility_name_list,category_list,coordinates_list)] 
    return db.session.add_all(med_centers)


@app.route('/')
def main():
    if 'user_id' in session:
        curr_user = User.query.get_or_404(session['user_id'])
        return redirect('/profile')
    return render_template('main.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        title = form.title.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(first_name,last_name,title,email,password)
        db.session.add(new_user)
        try:
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect('/profile')
        except IntegrityError:
            form.email.errors.append('Email already exists.')
            return render_template('register.html',form=form)

    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_user():
    form = LoginUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        auth_user = User.auth(email,password)
        if auth_user:
            session['user_id'] = auth_user.id
            return redirect('/profile')
        else:
            form.email.errors = ['Invalid Email/Password']
    return render_template('loginForm.html',form=form)

@app.route('/profile')
def profile_main():
    if 'user_id' in session:
        images = []
        results = response.json()['value']
        def get_images():
            for data in results:
                images.append(data['image'])
                return images
        get_images()
        curr_user = User.query.get_or_404(session['user_id'])
        return render_template('/users/profile_main.html',curr_user=curr_user,results=results,images=images,today_date=today_date)
    else:
        return redirect('/')

@app.route('/logout')
def user_logout():
    if 'user_id' in session:
        session.pop('user_id')
        return(redirect('/'))
    else:
        return(redirect('/'))
@app.route('/map',methods=['GET','POST'])
def map():
    if 'user_id' in session:
        curr_user = User.query.get_or_404(session['user_id'])
        destination = request.form.get('searchBar')
        print(destination)
        return render_template('/users/maps.html',curr_user=curr_user)
    else:
        return redirect('/')

@app.route("/emerg-doc")
def search_results():
    if 'user_id' in session:
        curr_user = User.query.get_or_404(session['user_id'])
        curr_loc = g.latlng
        user_centers = curr_user.user_medical_center
        saved_data = len(user_centers)
        return render_template('/users/emerg_doc.html',curr_loc=curr_loc,curr_user=curr_user,user_centers=user_centers,saved_data=saved_data)
    else:
        return redirect('/')

@app.route('/emerg-doc/results')
def test():
    if 'user_id' in session:
        curr_user = User.query.get_or_404(session['user_id'])
        curr_loc = g.latlng
        user_centers = curr_user.user_medical_center
        saved_data = len(user_centers)
        locate_hospitals()
        get_medical_center_data()
        try:
            db.session.commit()
            
        except IntegrityError:
            db.session.rollback()
            return render_template('/users/emerg_doc_results.html',curr_loc=curr_loc,hospitals_located=hospitals_located,curr_user=curr_user,user_centers=user_centers,saved_data=saved_data)
        return render_template('/users/emerg_doc_results.html',curr_loc=curr_loc,hospitals_located=hospitals_located,curr_user=curr_user,user_centers=user_centers)
    else:
        return redirect('/')

@app.route('/testing-map/<hospital_name>',methods=["GET","POST"])
def test_post(hospital_name):
    if 'user_id' in session:
        curr_loc = g.latlng
        directions = request.form['hospital_address']
        return render_template('/users/testmap.html',curr_loc=curr_loc,directions=directions)
    else:
        return redirect("/")
    
@app.route('/testing-map')
def test_map():
    if 'user_id' in session:
        curr_loc = g.latlng
        return render_template('/users/testmap.html',curr_loc=curr_loc)
    else:
        return redirect('/')

@app.route('/save/<place_name>',methods=['POST'])
def save(place_name):
    if 'user_id' in session:
        try:
            medical_center_to_save = MedicalCenter.query.filter(MedicalCenter.place_address == place_name).first()
            saved_center = UserMedicalCenter(user_id=session['user_id'],medical_center_id=medical_center_to_save.id)

            db.session.add(saved_center)
            db.session.commit()
            flash('Saved!','success')
            return redirect('/emerg-doc/results')
        except IntegrityError:
            flash("Already saved!",'warning')
            return redirect('/emerg-doc/results')
    else:
        return redirect('/')

@app.route('/delete/<facility_id>',methods=['POST'])
def delete_facility(facility_id):
    if 'user_id' in session:
        facility = UserMedicalCenter.query.filter(UserMedicalCenter.medical_center_id == facility_id).first()
        db.session.delete(facility)
        db.session.commit()
        return redirect('/emerg-doc')
    else:
        return redirect('/')

@app.route('/settings')
def settings():
    curr_user = User.query.get_or_404(session['user_id'])
    return render_template('/users/account_settings.html',curr_user=curr_user)


@app.route('/settings/edit-email',methods=['GET','POST'])
def edit_email():
    curr_user = User.query.get_or_404(session['user_id'])
    form = EditEmail()
    if 'user_id' in session:
        if form.validate_on_submit():
            new_email = form.new_email.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            if password == password_confirm:
                auth_user = curr_user.auth(curr_user.email,password_confirm)
                if auth_user:
                    auth_user.email = new_email
                    db.session.commit()
                    flash("Email changed!","success")
                    return redirect('/settings/edit-email')
                else:
                    form.password_confirm.errors = ['Invalid Password']
            else:
                form.password_confirm.errors = ['Passwords Do Not Match']
        return render_template('/users/edit_email.html',curr_user=curr_user,form=form)
    return redirect('/')

@app.route('/settings/edit-title',methods=['GET','POST'])
def edit_title():
    curr_user = User.query.get_or_404(session['user_id'])
    form = EditTitle()
    if 'user_id' in session:
        if form.validate_on_submit():
            new_title = form.new_title.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            if password == password_confirm:
                auth_user = curr_user.auth(curr_user.email,password_confirm)
                if auth_user:
                    auth_user.title = new_title
                    db.session.commit()
                    flash("Title changed!","success")
                    return redirect('/settings/edit-title')
                else:
                    form.password_confirm.errors = ['Invalid Password']
            else:
                form.password_confirm.errors = ['Passwords Do Not Match']
        return render_template('/users/edit_title.html',curr_user=curr_user,form=form)
    return redirect('/')

@app.route('/settings/password-change',methods=['GET','POST'])
def edit_password():
    curr_user = User.query.get_or_404(session['user_id'])
    form = EditPassword()
    if 'user_id' in session:
        if form.validate_on_submit():
            curr_password = form.curr_password.data
            new_password = form.new_password.data
            new_password_confirm = form.new_password_confirm.data
            if new_password == new_password_confirm:
                if bcrypt.check_password_hash(curr_user.password,curr_password):
                
                    auth_user = curr_user.auth(curr_user.email,curr_password)
                    if auth_user:
                            
                        hashed = bcrypt.generate_password_hash(new_password)
                        hashed_pwd = hashed.decode('utf8')
                        auth_user.password = hashed_pwd
                        db.session.commit()
                        flash("Password changed!","success")
                        return redirect('/settings/password-change')
                else:
                    form.curr_password.errors = ["Invalid Password"]        
            else:
                form.new_password_confirm.errors = ['Passwords Do Not Match']
        return render_template('/users/edit_password.html',curr_user=curr_user,form=form)
    return redirect('/')


@app.route('/settings/delete',methods=['GET','POST'])
def delete_account():
    curr_user = User.query.get_or_404(session['user_id'])
    form = DeleteAccountForm()
    if 'user_id' in session:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            if password == password_confirm:
                auth_user = curr_user.auth(curr_user.email,password_confirm)
                if auth_user and email == curr_user.email:
                    session.pop('user_id')
                    db.session.delete(auth_user)
                    db.session.commit()
                    return redirect('/')
                elif not auth_user:
                    form.password_confirm.errors = ['Invalid Password']
                elif email != curr_user.email:
                    form.email.errors = ['Invalid email']
        return render_template('/users/delete_account.html',curr_user=curr_user,form=form)
    return redirect('/')




    
