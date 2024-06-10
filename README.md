# Computer-Networks-WGET
Implementation of a Custom Wget in Python: This project is a custom implementation of wget in Python to download websites recursively. It uses requests, BeautifulSoup, and concurrent.futures to handle downloading and parsing HTML content, and replaces links to maintain site integrity. Ideal for learning and testing.

# Implementation of a Custom Wget in Python

This project is a custom implementation of `wget` in Python. It recursively downloads websites, replaces links to maintain site integrity, and saves the content locally. The project uses `requests`, `BeautifulSoup`, and `concurrent.futures` for downloading and parsing HTML content.

## Features

- Recursively download websites up to a specified depth.
- Replace links in HTML to maintain site integrity.
- Concurrent downloading using `ThreadPoolExecutor`.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `lxml` library

You can install the required libraries using:
```bash
pip install requests beautifulsoup4 lxml

In my case I used
py -m pip install requests beautifulsoup4 lxml
