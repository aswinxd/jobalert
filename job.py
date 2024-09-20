from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

app = Client("job_scraper_bot", 
             bot_token="7022599037:AAFLJR-NI5vWD_7roOyCdo4RFq9oP8wEKZ8", 
             api_id=7980140, 
             api_hash="db84e318c6894f560a4087c20c33ce0a")

# Function to scrape jobs
def scrape_jobs(keyword, location):
    url = f"https://www.adzuna.com/search?q={keyword}&l={location}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    
    for job in soup.find_all('div', class_='result'):
        title = job.find('h2').text
        link = job.find('a')['href']
        jobs.append(f"Job Title: {title}\nLink: {link}\n\n")
    
    return jobs if jobs else ["No jobs found"]

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
