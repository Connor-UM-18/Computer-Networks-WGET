import os
import sys
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse, urlsplit
from bs4 import BeautifulSoup
from pathlib import Path

# Función para descargar un archivo
def download_file(url, dest_folder):
    try:
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        
        local_filename = os.path.join(dest_folder, os.path.basename(urlsplit(url).path) or 'index.html')
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        #print(f"Downloaded: {url}")
        return local_filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

# Función para obtener todas las URLs de una página web
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

# Función para obtener todos los recursos de una página web
def get_all_resources(url, soup):
    resources = set()
    tags = {'img': 'src', 'script': 'src', 'link': 'href'}
    for tag, attr in tags.items():
        for resource in soup.find_all(tag, **{attr: True}):
            resource_url = urljoin(url, resource[attr])
            if is_valid(resource_url):
                resources.add(resource_url)
    return resources

# Función para validar URLs
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Función recursiva para descargar un sitio web
def download_site(url, dest_folder, executor):
    #print(f"Downloading {url} at depth {depth}")
    html_path = download_file(url, dest_folder)
    if html_path:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')

        resources = get_all_resources(url, soup)
        for resource_url in resources:
            resource_path = download_file(resource_url, os.path.join(dest_folder, os.path.dirname(urlparse(resource_url).path.lstrip('/'))))
            if resource_path:
                resource_tag = soup.find(src=resource_url) or soup.find(href=resource_url)
                if resource_tag:
                    if resource_tag.has_attr('src'):
                        resource_tag['src'] = resource_path
                    if resource_tag.has_attr('href'):
                        resource_tag['href'] = resource_path

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())


# Función principal
def main(url,dest_folder):
    dest_folder =os.path.join(dest_folder,"recursos_folder")
    #depth = 1  # Nivel de profundidad para la descarga
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(download_site, url, dest_folder, executor)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python recursos.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    dest_folder=sys.argv[2]
    #print(url)
    main(url,dest_folder)
