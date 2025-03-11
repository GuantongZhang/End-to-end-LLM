from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def extract_subpage_links(url, include_external=False):
    """
    Extracts links to subpages from a given URL.
    """
    try:
        # Send a GET request to the page
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags and extract href attributes
    subpage_links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Convert relative URLs to absolute URLs
        full_url = urljoin(url, href)
        # Filter out (external links) and non-HTML resources
        if not full_url.endswith(('.pdf', '.jpg', '.png', '.zip')):
            if full_url.startswith(url) or include_external:
                subpage_links.add(full_url)

    return list(subpage_links)


def extract_text_from_page(url):
    """
    Extracts text from a given URL.
    """
    try:
        # Send a GET request to the page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove unwanted elements (e.g., scripts, styles, navbars, footers)
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        element.decompose()

    # Extract text from the main content
    text = soup.get_text(separator='\n', strip=True)
    return text


subpages = extract_subpage_links('https://www.visitpittsburgh.com')

for subpage in subpages:
    text = extract_text_from_page(subpage)
    title = subpage.strip('/').split('/')[-1]
    filename = f"web_text/visit_pit/{title}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)