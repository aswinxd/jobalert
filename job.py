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
url = "https://jsearch.p.rapidapi.com/estimated-salary"

# Function to Get Jobs Using API
def fetch_jobs(job_title, location):
    try:
        querystring = {
            "query": job_title,
            "location": location,
            "num_pages": "1"
        }

        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "jsearch.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()

        # Parse and format the job data
        jobs = []
        if 'data' in data and data['data']:
            for job in data['data']:
                title = job.get('job_title', 'No Title')
                company = job.get('employer_name', 'No Company Data')
                location = job.get('location', {}).get('display_name', 'No Location Data')
                description = job.get('job_description', 'No Description Available')
                job_url = job.get('job_apply_link', 'No Link')
                posted_date = job.get('posted_at', 'No Posted Date')

                jobs.append(f"Job Title: {title}\nCompany: {company}\nLocation: {location}\nDescription: {description}\nPosted: {posted_date}\nLink: {job_url}\n\n")
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
