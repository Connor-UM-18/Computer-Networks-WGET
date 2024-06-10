import os
import shutil
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from pathlib import Path
import sys

# Función para descargar un archivo
def download_file(url, dest_folder,nivel_actual):
    try:
        # Crear la carpeta "primer_nivel" si no existe
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        
        local_filename = os.path.join(dest_folder, url.split('/')[-1] or 'index.html')
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        #print(f"Downloaded: {url}")
        return local_filename
    except Exception as e:
        #print(f"Error downloading {url}: {e}")
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

# Función para validar URLs
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Función recursiva para descargar un sitio web
def download_site(url, dest_folder, depth, executor,nivel_actual):
    if depth < 0:
        return
    
    #print(f"Downloading {url}")
    download_file(url, dest_folder,nivel_actual)
# Función principal
def main(url, sublink_index,nivel_actual,depth_faltante,nivel_folder):
    
    dest_folder = f"sublink_{sublink_index}"
    dest_folder = os.path.join(nivel_folder,dest_folder)
    #print(dest_folder)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(download_site, url, dest_folder, 1, executor,nivel_actual)
    
    

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python level_index.py <url> <index>")
        sys.exit(1)
    url = sys.argv[1]
    sublink_index = int(sys.argv[2])
    nivel_actual=int(sys.argv[3])
    depth=int(sys.argv[4])
    nivel_folder=sys.argv[5]
    #print("parametros recibidos")
    #print(url)
    #print(str(sublink_index))
    #print(str(nivel_actual))
    #print(str(depth))
    main(url, sublink_index,nivel_actual,depth,nivel_folder)
