from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
import logging
app = Client("job_scraper_bot", 
             bot_token="7022599037:AAFLJR-NI5vWD_7roOyCdo4RFq9oP8wEKZ8", 
             api_id=7980140, 
             api_hash="db84e318c6894f560a4087c20c33ce0a")

# Function to scrape jobs
rapidapi_key = "f97f646882mshbcc0c1f61a5549ep146823jsn2f8ac04b5bf1"
url = "https://linkedin-jobs-scraper-api.p.rapidapi.com/jobs/trial"

# Function to Get Jobs Using API
def fetch_jobs(job_title, location, rows=25):
    try:
        payload = {
            "title": job_title,
            "location": location,
            "rows": rows
        }

        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "linkedin-jobs-scraper-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()

        # Parse and format the job data
        jobs = []
        if 'data' in data:
            for job in data['data']:
                job_title = job.get('title', 'No Title')
                company = job.get('companyName', 'No Company Name')
                location = job.get('location', 'No Location')
                job_url = job.get('jobUrl', 'No Job URL')
                posted_time = job.get('postedTime', 'No Posted Time')
                applications_count = job.get('applicationsCount', 'No Application Count')
                salary = job.get('salary', 'No Salary Data')
                description = job.get('description', 'No Description')

                jobs.append(f"Job Title: {job_title}\nCompany: {company}\nLocation: {location}\nPosted: {posted_time}\nApplications: {applications_count}\nSalary: {salary}\nDescription: {description}\nLink: {job_url}\n\n")
            return jobs if jobs else ["No jobs found"]
        else:
            return ["No jobs found"]

    except requests.exceptions.RequestException as e:
        return [f"Error fetching jobs: {e}"]

# Telegram Bot Command to Get Jobs
@app.on_message(filters.command("jobs"))
def get_jobs(client, message):
    try:
        query = message.text.split(" ", 2)
        if len(query) < 3:
            message.reply("Usage: /jobs <job_title> <location>")
            return
        job_title, location = query[1], query[2]
        jobs = fetch_jobs(job_title, location)
        message.reply("\n".join(jobs))
    except Exception as e:
        message.reply(f"Error: {str(e)}")

app.run()
