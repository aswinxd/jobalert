from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

app = Client("job_scraper_bot", 
             bot_token="7022599037:AAFLJR-NI5vWD_7roOyCdo4RFq9oP8wEKZ8", 
             api_id=7980140, 
             api_hash="db84e318c6894f560a4087c20c33ce0a")

# Function to scrape jobs
def scrape_jobs(keyword, location):
    try:
        url = f"https://www.adzuna.com/search?q={keyword}&l={location}"
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Scraping logic
        jobs = []
        for job in soup.find_all('div', class_='result'):
            title = job.find('h2').text
            link = job.find('a')['href']
            jobs.append(f"Job Title: {title}\nLink: {link}\n\n")
        
        return jobs if jobs else ["No jobs found"]
    except Exception as e:
        logging.error(f"Error scraping jobs: {e}")
        return ["Error fetching jobs"]
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
