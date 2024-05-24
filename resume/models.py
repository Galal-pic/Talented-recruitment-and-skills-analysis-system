from resume import db ,login_manager 
from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint


@login_manager.user_loader
def load_user(email):
    return seekr.query.filter_by(email=email).first() or recruiter.query.filter_by(email=email).first()

class seekr(db.Model,UserMixin):
    # id = db.Column(db.Integer,primary_key = True)
    def get_id(self):
        return self.email 
    email = db.Column(db.String(125),primary_key=True)
    fname = db.Column(db.String(25),nullable=False)
    lname = db.Column(db.String(25),nullable=False)
    username = db.Column(db.String(25),nullable=False,unique=True)
    linkedin = db.Column(db.String(125),nullable=False,unique=True)
    country = db.Column(db.String(25),nullable=False)
    phone = db.Column(db.String(25),nullable=False)
    seniority_level  = db.Column(db.String(25),nullable=False)
    current_position  = db.Column(db.String(25),nullable=False)
    password = db.Column(db.String(125),nullable=False)
    cv_name = db.Column(db.String(30),nullable=False,default='default.pdf')
    skills = db.Column(db.Text,nullable=False)
    embedding = db.Column(db.Text,nullable=False)
    jobs = db.Column(db.Text,nullable=False)
    def __repr__(self):
        return f"Seekr('{self.username}', '{self.cv_name}', '{self.email}')"

# @login_manager.user_loader
# def load_user(recruiter_id):
#     return recruiter.query.get(int(recruiter_id))
    
class recruiter(db.Model,UserMixin):
    def get_id(self):
        return self.email
    email = db.Column(db.String(125),primary_key=True)
    fname = db.Column(db.String(25),nullable=False)
    lname = db.Column(db.String(25),nullable=False)
    username = db.Column(db.String(25),nullable=False)
    linkedin = db.Column(db.String(125),nullable=False)
    company   = db.Column(db.String(25),nullable=False)
    industry   = db.Column(db.String(25),nullable=False)
    password = db.Column(db.String(125),nullable=False)
    job_desc = db.relationship('job_description',backref='Recruiter',lazy=True)
    def __repr__(self):
        return f"recruiter('{self.username}', '{self.industry}', '{self.company}')"
    

class job_description(db.Model,UserMixin):
    job_title = db.Column(db.String(125),nullable=False)
    Job_description = db.Column(db.Text,nullable=False)
    recruiter_email = db.Column(db.String(125),db.ForeignKey('recruiter.email'),nullable=False)
    company   = db.Column(db.String(25),nullable=False)
    industry   = db.Column(db.String(25),nullable=False)
    username = db.Column(db.String(25),nullable=False)
    cvs = db.Column(db.Text,nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('job_title', 'Job_description', 'recruiter_email','cvs'),
    )
    def __repr__(self):
        return f"Seekr('{self.email}' , {self.job_title}, '{self.cvs})"
    

