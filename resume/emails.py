from resume import mail ,Message
def sent_offer_to_seekers(email,company_name,description,job_title,recruiter_email):
    message = Message('New Job Announcement!', sender='galalamrewida@example.com', recipients=[email])
    message.body = f"""
Subject: New Job Announcement from [{company_name}]

Hi,

A new job opportunity was announced and the CV appeared in the search results:
Job Title: {job_title}

Job Description:
{description}

Please visit [resume Resume] for more details.

Thanks,
The Team at [{company_name}]
email : {recruiter_email}
"""
    mail.send(message)



def apply_to_job(company_name, job_title, recruiter_email, seeker_mail, seeker_name,seeker_phone, seeker_linkden, seeker_skills):

    message = Message('New Job Application: ' + job_title, sender='raniasakr533@example.com', recipients=[recruiter_email])
    message.body = f"""
    Subject: New Job Application: [{job_title}] at [{company_name}]

    Hi,

    You have received a new job application for the position of [{job_title}] at [{company_name}].

    **Seeker Information:**
    - **Name:** {[seeker_name]}
    - **Email:** [{seeker_mail}]
    - **Phone:** {[seeker_phone]}
    - **linkedin Account:** {[seeker_linkden]}
    - **skills:** {[seeker_skills]}



    Please review the candidate's details and consider them for the position.

    Best regards,
    BREAKTHROUGHHIRE TEAM
    """
    try:
        mail.send(message)
        return True  # Email sent successfully
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False  # Email sending failed
