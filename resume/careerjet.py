import requests
from flask import request


class CareerjetAPIClient(object):

    def __init__(self, affiliate_id, locale_code="en_GB"):
        self.affiliate_id = affiliate_id
        self.locale_code = locale_code

    def search_jobs(self, keywords, location, user_ip, user_agent, url):
        base_url = "http://public.api.careerjet.net/search"

        search_params = {
            'affid': self.affiliate_id,
            'keywords': keywords,
            'location': location,
            'user_ip': user_ip,
            'user_agent': user_agent,
            'url': url,
        }

        response = requests.get(base_url, params=search_params)
        response.raise_for_status()  # Check for errors in the response

        return response.json()


affiliate_id = "ddcfeb742ec45305b3858196016bc43b"
client = CareerjetAPIClient(affiliate_id)


def search_job(job_title):
    location = "Egypt"  # Default location
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    url = request.url_root

    # Perform job search using Careerjet API
    job_results = client.search_jobs(job_title, location, user_ip, user_agent, url)

    return job_results.get('jobs', [])


 
