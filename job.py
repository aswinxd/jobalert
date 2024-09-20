from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
import logging
app = Client("job_scraper_bot", 
             bot_token="7022599037:AAFLJR-NI5vWD_7roOyCdo4RFq9oP8wEKZ8", 
             api_id=7980140, 
             api_hash="db84e318c6894f560a4087c20c33ce0a")

# Function to scrape jobs
def scrape_jobs(keyword, location):
    try:
        url = f"https://www.adzuna.com/search?q={keyword}&l={location}"
        logging.info(f"Fetching jobs from: {url}")
        
        # Send request to Adzuna
        response = requests.get(url)
        response.raise_for_status()  # Check if request is successful

        # Print content for debugging
        logging.info("Page content fetched successfully")

        # Parse HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Check if job listings are found
        jobs = []
        job_listings = soup.find_all('div', class_='result')
        if not job_listings:
            logging.warning("No jobs found in the HTML content.")
            return ["No jobs found"]

        for job in job_listings:
            title = job.find('h2').text if job.find('h2') else "No Title"
            link = job.find('a')['href'] if job.find('a') else "No Link"
            jobs.append(f"Job Title: {title}\nLink: {link}\n\n")

        return jobs if jobs else ["No jobs found"]

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching jobs: {e}")
        return ["Error fetching jobs"]

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return ["An error occurred while processing the data"]

# Command to search jobs
@app.on_message(filters.command("jobs"))
def get_jobs(client, message):
    try:
        query = message.text.split(" ", 2)
        if len(query) < 3:
            message.reply("Usage: /jobs <job_title> <location>")
            return
        keyword, location = query[1], query[2]
        jobs = scrape_jobs(keyword, location)
        message.reply("\n".join(jobs))
    except Exception as e:
        message.reply(f"Error: {str(e)}")

app.run()
