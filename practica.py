import subprocess
import os
import shutil
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pathlib import Path
import re

# Función para descargar un archivo
def download_file(url, dest_folder):
    try:
        # Crear la carpeta "nivel_1" si no existe
        primer_nivel_folder = os.path.join(dest_folder, "nivel_1")
        if not os.path.exists(primer_nivel_folder):
            os.makedirs(primer_nivel_folder)
        
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
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except Exception as e:
        print(f"Invalid URL {url}: {e}")
        return False
    
# Función recursiva para descargar un sitio web
def download_site(url, dest_folder, depth, executor):
    if depth < 0:
        return
    print(dest_folder)
    print(f"Downloading {url}")
    download_file(url, dest_folder)

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

# Función para realizar el reemplazo del enlace en el contenido HTML
def replace_link_in_html(content, old_link, new_link):
    # Crear la expresión regular para encontrar el enlace antiguo
    pattern = re.compile(rf'(?<=["\']){re.escape(old_link)}(?=["\'])')
    # Reemplazar el enlace antiguo con el nuevo enlace
    new_content = re.sub(pattern, lambda x: new_link, content)
    return new_content

# Función principal
def main():
    entrada = input("Enter the URL to download: ")
    dest_folder = "downloaded_site"
    res_folder="recursos_folder"
    max_level = int(input("Enter the level to retrieve: "))
    depth = max_level  # Nivel de profundidad para la descarga
    
    # Verificar si la carpeta "downloaded_site" existe y eliminar su contenido si es así
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
        os.makedirs(dest_folder)
        os.makedirs(os.path.join(dest_folder, res_folder))
    elif not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        os.makedirs(os.path.join(dest_folder, res_folder))
    
    
    #links = get_all_links(url)
    
    
    #Se descargan recursos de primer link
    subprocess.run(["python", "recursos.py", entrada, dest_folder], check=True)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(download_site, entrada, dest_folder, depth, executor)    
    
    levels = get_links_by_levels(entrada, max_level)
    ruta_directorio=os.path.dirname(os.path.abspath(__file__))
    path_html=os.path.join(ruta_directorio,"downloaded_site","index.html")
    count=0
    for level in range(1, max_level + 1):
        print(f"\nLinks del nivel {level}:")
        nivel_folder = os.path.join(dest_folder, "nivel_"+str(level))
        for link in levels[level]:
            count+=1
            subprocess.run(["python", "level_index.py", link, str(count),str(level),str(max_level),nivel_folder], check=True)
            ruta_sublink = f"sublink_{str(count)}"
            ruta_sublink = os.path.join(nivel_folder,ruta_sublink,"index.html")
            # Abrimos el archivo con codificación utf-8 para evitar problemas de decodificación
            
            
            path_usuario=os.path.join(ruta_directorio,ruta_sublink)
            #exit(0)
            with open(path_html, "r", encoding="utf-8") as file:
                contenido_html = file.read()
                nuevo_contenido = replace_link_in_html(contenido_html, link, path_usuario)

            with open(path_html, "w", encoding="utf-8") as file:
                file.write(nuevo_contenido)

            #print(link)
        print(count)
        count=0


if __name__ == "__main__":
    main() 
