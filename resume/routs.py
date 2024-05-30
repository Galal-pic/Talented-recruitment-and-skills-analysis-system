from resume import app, bcrypt, db
from resume.models import recruiter, seekr, job_description
from resume.forms import RegistrationRecruiter, RegistrationSeeker, LoginForm
from resume.huggingface import preprocessing_pipeline, similarty
from resume.extract_skills_from_cv import append_cvs, retrive_skills_from_data_fortitle
from resume.emails import sent_offer_to_seekers, apply_to_job
from resume.careerjet import client, search_job
from resume.utils import (
    extract_skills_from_pdf,
    sentence_embedding4_similarity_score_test,
)
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import secure_filename
from markupsafe import Markup
import os, json
import pandas as pd
import ast
from itertools import chain


@app.route("/")
def PREHOME():
    return render_template("PREHOME.html")


@app.route("/homeregistered")
def homeregistered():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard/")
def render_dashboard():
    return render_template("dashboard.html")


@app.route("/salaries")
def salaries():
    return render_template("salaries.html")


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    if request.method == "POST":
        # Handle search form submission
        keywords = request.form["keywords"]
        location = request.form["location"]
        user_ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")
        url = request.url_root
        job_results = client.search_jobs(keywords, location, user_ip, user_agent, url)

        return render_template("jobs.html", job_results=job_results.get("jobs", []))

    # Render the index page for GET requests
    return render_template("jobs.html", jobs=[])


@app.route("/job description", methods=["POST", "GET"])
def jobdescription():
    return render_template("jobdescription.html", title="job description")


@app.route("/history", methods=["POST", "GET"])
def history():
    current_recruiter = job_description.query.filter_by(
        recruiter_email=current_user.email
    ).all()

    job_titles = [job.job_title for job in current_recruiter]
    Job_description = [job.Job_description for job in current_recruiter]
    cvs = [job.cvs for job in current_recruiter]
    history_data = []
    for title, dec, cv in zip(job_titles, Job_description, cvs):
        history_data.append((title, dec, cv))

    return render_template("history.html", title="History", data=history_data)


@app.route("/CVs", methods=["POST"])
def cvs():
    if request.method == "POST" and current_user.is_authenticated:
        description = request.form["desc"]
        job_title = request.form["job_title"]
        skills_from_description = preprocessing_pipeline(description)
        cvs = similarty(skills_from_description)
        current_recruiter = recruiter.query.filter_by(email=current_user.email).first()
        all_cvs = []

        for cv in cvs:
            seeker = seekr.query.filter_by(cv_name=cv[0]).first()
            # sent_offer_to_seekers(seeker.email,current_recruiter.company,description,job_title,current_recruiter.email)
            all_cvs.append(
                (
                    cv[0],
                    seeker.skills,
                    seeker.phone,
                    seeker.email,
                    seeker.country,
                    seeker.linkedin,
                    cv[1],
                )
            )

        aready_job_description = job_description.query.filter_by(
            recruiter_email=current_recruiter.email,
            job_title=job_title,
            Job_description=description,
        ).first()
        if current_recruiter and aready_job_description:
            return redirect(url_for("history"))
        elif current_recruiter:
            desc = job_description(
                job_title=job_title,
                Job_description=description,
                cvs=str(cvs),
                recruiter_email=current_user.email,
                company=current_recruiter.company,
                industry=current_recruiter.industry,
                username=current_recruiter.username,
            )

            db.session.add(desc)
            db.session.commit()

    return render_template("outdescription.html", data=all_cvs)


UPLOAD_FOLDER = "cvs/"

app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(["pdf"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/UPLOAD", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        path = UPLOAD_FOLDER + filename
        skills = extract_skills_from_pdf(path)
        job_title, similarity = sentence_embedding4_similarity_score_test(skills)

        job_results = search_job(job_title)
        # Remove the uploaded file after processing
        os.remove(path)
        df = pd.read_csv("cvs\data_with_vector_technology.csv")
        df["technology"] = df["technology"].apply(ast.literal_eval)
        nested_list = df[df["job_title"] == "data analyst"]["technology"].tolist()
        skills = list(chain.from_iterable(nested_list))
        return render_template(
            "skills.html",
            filename=filename,
            skills=skills,
            job_title=job_title,
            similarity=similarity,
            job_results=job_results,
        )

    else:
        flash("Only PDF file format are allowed!")
        return redirect(request.url)


@app.route("/seekerregister", methods=["GET", "POST"])
def seekerregister():
    if current_user.is_authenticated:
        return redirect(url_for("uploadcv"))
    form = RegistrationSeeker()
    if form.validate_on_submit():
        file = form.cv.data
        filename = file.filename
        file.save("cvs/" + filename)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        jobs, skills_list, embedding = append_cvs(
            filename, "cvs/" + filename, name="seekerregister"
        )
        new_seeker = seekr(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            linkedin=form.linkedin.data,
            country=form.country.data,
            phone=form.phone.data,
            seniority_level=form.seniority_level.data,
            current_position=form.current_position.data,
            password=hashed_password,
            cv_name=filename,
            skills=str(skills_list),
            jobs=str(jobs),
            embedding=str(embedding),
        )
        db.session.add(new_seeker)
        db.session.commit()
        db.session.close()

        # flash(f"Account created successfully for {form.fname.data}", "success")
        return redirect(url_for("login"))

    return render_template("seekerregister.html", title="seekerregister", form=form)


@app.route("/recruiterregister", methods=["POST", "GET"])
def recruiterregister():
    if current_user.is_authenticated:
        return redirect(url_for("jobdescription"))
    form = RegistrationRecruiter()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_recruiter = recruiter(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            linkedin=form.linkedin.data,
            company=form.company.data,
            industry=form.industry.data,
            password=hashed_password,
        )
        db.session.add(new_recruiter)
        db.session.commit()
        db.session.close()
        flash(f"Account created successfully for {form.fname.data}", "success")
        return redirect(url_for("login"))

    return render_template(
        "recruiterregister.html", title="recruiterregister", form=form
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        new_seeker = seekr.query.filter_by(email=form.email.data).first()
        new_recruiter = recruiter.query.filter_by(email=form.email.data).first()

        if new_seeker and bcrypt.check_password_hash(
            new_seeker.password, form.password.data
        ):
            login_user(new_seeker, remember=form.remember)
            # flash('You have been logged in','success')
            return redirect(url_for("uploadcv"))
        elif new_recruiter and bcrypt.check_password_hash(
            new_recruiter.password, form.password.data
        ):
            login_user(new_recruiter, remember=form.remember)
            # flash('You have been logged in','success')
            return redirect(url_for("jobdescription"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")

    return render_template("login.html", title="home", form=form)


@app.route("/registeration")
def registeration():
    return render_template("registeration.html", title="registeration")


@app.route("/upload", methods=["POST", "GET"])
def uploadcv():
    return render_template("uploadcv.html", title="uploadcv")


@app.route("/pdf", methods=["POST", "GET"])
def pdf():
    if request.method == "POST":
        if "pdfFile" not in request.files:
            return "No file part"
        else:
            input_pdf = request.files["pdfFile"]
            input_pdf.save("cvs/" + input_pdf.filename)
            jobs, _, _ = append_cvs(
                input_pdf.filename, "cvs/" + input_pdf.filename, name="pdf"
            )
            skill = retrive_skills_from_data_fortitle(jobs)
            compined = list(zip(jobs, skill))
    return render_template("outpdf.html", data=compined)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("PREHOME"))


@app.route("/jobfeed")
def jobfeed():
    job_feed = job_description.query.all()
    for job in job_feed:
        job.Job_description = job.Job_description.replace("\r", "")
        job.Job_description = job.Job_description.replace(
            "\n", "<br>"
        )  # Replace newlines with HTML line breaks
        job.Job_description = json.dumps(job.Job_description)  # Convert to JSON string
        job.Job_description = Markup(
            job.Job_description
        )  # Mark as safe for HTML rendering
    return render_template("jobfeed.html", job_feed=job_feed)


@app.route("/applyjob", methods=["POST"])
def applyjob():
    if current_user.is_authenticated:
        seeker = seekr.query.filter_by(email=current_user.email).first()
        if seeker:
            company_name = request.form.get("company_name")
            job_title = request.form.get("job_title")
            recruiter_email = request.form.get("recruiter_email")
            if apply_to_job(
                company_name,
                job_title,
                recruiter_email,
                seeker.email,
                seeker.fname,
                seeker.phone,
                seeker.linkedin,
                seeker.skills,
            ):
                flash("Job application sent successfully", "success")
            else:
                flash("Failed to send job application", "error")
        else:
            flash("Seeker not found", "error")
    else:
        flash("User not authenticated", "error")
    return redirect(url_for("jobfeed"))


@app.route("/open_url", methods=["POST"])
def open_url():
    if current_user.is_authenticated:
        url = request.form.get("linkedin_link")
        return redirect(url)
