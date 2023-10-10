from bs4 import BeautifulSoup
import requests
import time

#Allows user to input unfamiliar skill(s)
print('Input skill(s) you are not familiar with:')
unfamiliar_skills = input('>')
print(f'Filtering out {unfamiliar_skills}')
unfamiliar_skills = (unfamiliar_skills.replace(',', '')).split()

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

def find_jobs():
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_ = 'sim-posted').span.text
        if 'few' in published_date:

            company_name = job.find('h3', class_="joblist-comp-name").text.replace(' ', '')
            skills = (job.find('span', class_='srp-skills').text.replace(' ','')).replace(',', ', ') #gets rid of whitespace
            more_info = job.header.h2.a['href']
            # the above line uses a bunch of tag attributes to find the link where we can find more info about the job.
            # Since the URL is not text, we need to grab it from the 'href' attribute of the <a> tag through the above technique
           
            for unfamiliar_skill in unfamiliar_skills:
                if unfamiliar_skill not in skills:
                    with open(f'job #{index}.txt', 'w') as f: #writes a file to posts directory at file path "posts/job #index.txt". It's given the variable "f".
                        f.write(f"Company Name: {company_name.strip()} \n") #f.write uses the write attribute to write it to this txt file
                        f.write(f"Required Skills: {skills.strip()} \n")
                        f.write(f"More Info: {more_info} \n")
                        f.write(f"{published_date}")
                    print(f'File saved: job #{index}.txt')

if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10 #seconds
        print(f'Waiting {time_wait} minutes')
        time.sleep(time_wait * 60)
