import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
urls = [
    "https://www.nasa.gov/",
    "https://science.nasa.gov/solar-system/moons/",
    "https://science.nasa.gov/solar-system/asteroids/"
]
def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            if is_valid(link):
                links.add(link)
        return links
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return set()

def is_valid(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except Exception as e:
        print(f"Invalid URL {url}: {e}")
        return False

def get_links_by_levels(url, max_level):
    levels = {i: set() for i in range(1, max_level + 1)}
    visited_links = set()

    current_level_links = {url}

    for current_level in range(1, max_level + 1):
        next_level_links = set()
        for link in current_level_links:
            if link not in visited_links:
                visited_links.add(link)
                #if current_level==1:
                    
                    #links = current_level_links
                #else:
                links = get_all_links(link)
                for l in links:
                    if l not in visited_links:
                        next_level_links.add(l)
        levels[current_level] = next_level_links
        current_level_links = next_level_links

    return levels

def main():
    url = input("Enter the URL to start with: ")
    max_level = int(input("Enter the level to retrieve: "))
    levels = get_links_by_levels(url, max_level)
    count=0
    for level in range(1, max_level + 1):
        print(f"\nLinks of level {level}:")
        for link in levels[level]:
            count+=1
            #print(link)
        print(count)
        count=0
if __name__ == "__main__":
    main()
