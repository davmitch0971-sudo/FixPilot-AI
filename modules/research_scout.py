import requests
from bs4 import BeautifulSoup

def get_live_trends():
    # Scrapes high-traffic dev forum categories or trending repos
    url = "https://github.com/trending"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract project descriptions as "problems"
    problems = []
    for item in soup.select('.col-9')[:5]:
        problems.append(item.get_text(strip=True))
    return problems

if __name__ == "__main__":
    for p in get_live_trends():
        print(p)
