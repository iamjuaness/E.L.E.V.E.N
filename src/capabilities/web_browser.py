import webbrowser
from src.utils.logger import logger

class WebBrowser:
    """
    Controls web browser interactions.
    """
    
    def open_url(self, url):
        """Open a specific URL"""
        if not url.startswith('http'):
            url = 'https://' + url
        logger.info(f"Opening URL: {url}")
        webbrowser.open(url)
        return f"Opening {url}"
        
    def search_google(self, query):
        """Search Google for a query"""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        logger.info(f"Searching Google: {query}")
        webbrowser.open(url)
        return f"Searching Google for {query}"
