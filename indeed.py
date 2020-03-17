import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find("div", {"class":"pagination"})
  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page
  
def extract_jobs(html):
    title = html.find("div", {"class":"title"}).find("a")["title"]
    location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
    company = html.find("span", {"class":"company"})
    job_id = html["data-jk"]
    company_anchor = company.find("a")
    if company.find("a") is not None:
     company = str(company_anchor.string)
    else:
     # print(title)
     company = str(company.string)
    company = company.strip() # strip = 없애는 용도
    return {
      'company' : company , 
      'title' : title , 
      'location' : location , 
      'link' : f"https://kr.indeed.com/viewjob?jk={job_id}" 
      }


def get_jobs(last_page):
  jobs = []
  for page in range(last_page) :
    print(f"Scrapping page I0: page:{page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results : 
      job = extract_jobs(result)
      jobs.append(job)
  return jobs

def get_job():
  last_page = get_last_page()
  jobs = get_jobs(last_page)
  return jobs
