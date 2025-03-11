from bs4 import BeautifulSoup
import requests

def extract_wikipedia_text(url):
    # Send a GET request to the Wikipedia page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text from the main content div (usually has id 'mw-content-text')
    content_div = soup.find(id='mw-content-text')
    
    if content_div is None:
        print("Could not find the main content div.")
        return None
    
    # Remove reference sections (footnotes, citations, etc.)
    for ref in content_div.find_all(class_=lambda x: x and 'cite' in x):
        ref.decompose()  # Remove the element from the HTML tree
    
    # Extract all paragraphs within the content div
    paragraphs = content_div.find_all(['p', 'li'])
    
    # Combine the text from all paragraphs
    text = '\n'.join([p.get_text() for p in paragraphs])
    return text

"""
# Example usage
url = 'https://en.wikipedia.org/wiki/History_of_Pittsburgh'
text = extract_wikipedia_text(url)
if text:
    print(text)
"""

urls = [
    'https://en.wikipedia.org/wiki/Pittsburgh',
    'https://en.wikipedia.org/wiki/History_of_Pittsburgh',
    
]

for url in urls:
    text = extract_wikipedia_text(url)
    title = url.strip('/').split('/')[-1]
    filename = f"web_text/wiki/{title}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)