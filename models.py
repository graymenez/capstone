from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__="users"

    def __repr__(self):
        return f"User {self.id}: {self.first_name} {self.last_name}"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.Text,nullable=False)
    last_name = db.Column(db.Text,nullable=False)
    title = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False)


    @classmethod
    def register(cls,first_name,last_name,title,email,pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_pwd = hashed.decode('utf8')

        return cls(first_name=first_name,last_name=last_name,title=title,email=email,password=hashed_pwd)
    
    @classmethod
    def auth(cls,email,pwd):
        user = cls.query.filter_by(email = email).first()
        if user and bcrypt.check_password_hash(user.password,pwd):
            return user
        else:
            return False

class MedicalCenter(db.Model):
    """Create Hospital From Mapbox Api"""
    __tablename__="medical_centers"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    place_address = db.Column(db.Text,nullable=False,unique=True)

    facility_name = db.Column(db.Text,nullable=False)
    
    category = db.Column(db.Text,nullable=False)
    coordinates = db.Column(db.Text,nullable=False)



class UserMedicalCenter(db.Model):
    """Creates a Model for User and MedcialCenter Relationship"""

    __tablename__='user_medical_centers'


    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),primary_key=True)
    medical_center_id = db.Column(db.Integer,db.ForeignKey("medical_centers.id"),primary_key=True)

    user = db.relationship('User',backref='user_medical_center',cascade='delete',passive_deletes=True)

    medical_centers = db.relationship('MedicalCenter',backref='medical_centers',cascade='delete',passive_deletes=True)
    



