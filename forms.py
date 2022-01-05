from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, Email,Length
import email_validator

class RegisterUserForm(FlaskForm):
    """Creates a user"""

    first_name=StringField("First Name",validators=[DataRequired()],render_kw={"placeholder":"John"})

    last_name=StringField("Last Name",validators=[DataRequired()],render_kw={"placeholder":"Doe"})

    title = StringField("Title",validators=[DataRequired()],render_kw={"placeholder":"Firefighter/Paramedic ect.."})

    email = StringField("Email",validators=[DataRequired()],render_kw={"placeholder":"Email"})
    
    password = PasswordField('Password',validators=[Length(min=8)],render_kw={"placeholder":"Password"})

class LoginUserForm(FlaskForm):
    """User Login Form"""

    email = StringField("Email",validators=[DataRequired()],render_kw={"placeholder":"Email"})
    
    password = PasswordField('Password',validators=[Length(min=8)],render_kw={"placeholder":"Password"})

class EditEmail(FlaskForm):
    """Edit email form"""
    new_email = StringField("New Email",validators=[DataRequired()],render_kw={"placeholder":"Email"})
    password = PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})
    password_confirm = PasswordField("Confirm Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})

class EditTitle(FlaskForm):
    """Edit title form"""
    new_title = StringField("New Title",validators=[DataRequired()],render_kw={"placeholder":"Title"})
    password = PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})
    password_confirm = PasswordField("Confirm Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})

class EditPassword(FlaskForm):
    """Edit title form"""
    curr_password = PasswordField("Current Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})
    new_password = PasswordField("New Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})
    new_password_confirm = PasswordField("Confirm New Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})


class DeleteAccountForm(FlaskForm):
    """Edit title form"""
    email = StringField("Email",validators=[DataRequired()],render_kw={"placeholder":"Email"})
    password = PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})
    password_confirm = PasswordField("Confirm Password",validators=[DataRequired()],render_kw={"placeholder":"Password"})