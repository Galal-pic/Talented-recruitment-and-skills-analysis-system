from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,SelectField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,URL,ValidationError
from resume.models import seekr,recruiter
import pycountry


class UploadForm(FlaskForm):
    cv = FileField('Upload PDF File')
    submit = SubmitField('Upload')


class RegistrationSeeker(FlaskForm):
    cv = FileField('Upload cv File', validators=[FileAllowed(['pdf'], 'Only PDF files are allowed!')])
    fname = StringField("First Name",validators=[DataRequired(),Length(min=2,max=25)])
    lname = StringField("Last Name",validators=[DataRequired(),Length(min=2,max=25)])
    username = StringField("User Name",validators=[DataRequired(),Length(min=2,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    country = SelectField('Country', choices=[(country.alpha_2, country.name) for country in pycountry.countries], validators=[DataRequired()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    linkedin = StringField('Linkedin Link',validators=[DataRequired(),URL()])
    seniority_level = SelectField('Seniority Level', choices=[('Junior', 'Junior'), ('Senior', 'Senior'), ('Mid-level', 'Mid-level')], validators=[DataRequired()])
    current_position = StringField('Current Position',validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Regexp(
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$")])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self,username):
        uname = seekr.query.filter_by(username = username.data).first()
        if uname:
            raise ValidationError ('Username already exists! please chosse a different one')

    def validate_email(self,email):
        uemail = seekr.query.filter_by(email = email.data).first()
        if uemail:
            raise ValidationError ('Email already exists! please chosse a different one')

    def validate_linkedin(self,linkedin):
        ulinked = seekr.query.filter_by(linkedin = linkedin.data).first()
        if ulinked:
            raise ValidationError ('URL already exists! please chosse a different one')



class RegistrationRecruiter(FlaskForm):
    fname = StringField("First Name",validators=[DataRequired(),Length(min=2,max=25)])
    lname = StringField("Last Name",validators=[DataRequired(),Length(min=2,max=25)])
    username = StringField("User Name",validators=[DataRequired(),Length(min=2,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    linkedin = StringField('Linkedin Link',validators=[DataRequired(),URL()])
    company= StringField("Company Name",validators=[DataRequired()])
    industry = StringField('Industry',validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Regexp(
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),],)
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self,username):
        rname = recruiter.query.filter_by(username = username.data).first()
        if rname:
            raise ValidationError ('Username already exists! please chosse a different one')

    def validate_email(self,email):
        rmail = recruiter.query.filter_by(email = email.data).first()
        if rmail:
            raise ValidationError ('Email already exists! please chosse a different one')

    def validate_linkedin(self,linkedin):
        rlinked = recruiter.query.filter_by(linkedin = linkedin.data).first()
        if rlinked:
            raise ValidationError ('URL already exists! please chosse a different one')



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")
