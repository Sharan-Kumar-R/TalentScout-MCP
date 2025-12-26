import os
from linkedin_api import Linkedin
from dotenv import load_dotenv
import logging
from requests.cookies import RequestsCookieJar
from ddgs import DDGS

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInClient:
    def __init__(self):
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        self.li_at = os.getenv("LINKEDIN_LI_AT")
        self.jsessionid = os.getenv("LINKEDIN_JSESSIONID")
        self.api = None

    def authenticate(self):
        """Authenticates with LinkedIn using cookies or credentials."""
        try:
            if self.li_at and self.jsessionid:
                logger.info("Authenticating with cookies...")
                jar = RequestsCookieJar()
                jar.set("li_at", self.li_at)
                jar.set("JSESSIONID", self.jsessionid)
                self.api = Linkedin("", "", cookies=jar)
            elif self.email and self.password:
                 logger.info("Authenticating with email/password...")
                 self.api = Linkedin(self.email, self.password)
            else:
                raise ValueError("No credentials found. Please set LINKEDIN_LI_AT and LINKEDIN_JSESSIONID in .env")
            
            logger.info("Successfully authenticated with LinkedIn.")
            return True
        except Exception as e:
            logger.error(f"Failed to authenticate: {e}")
            raise e

    def search_people(self, keywords, location=None, limit=5):
        """
        Searches for people on LinkedIn using DuckDuckGo X-Ray search.
        This bypasses LinkedIn's internal API restrictions for cleaner results.
        """
        results = []
        try:
            query = f"site:linkedin.com/in/ {keywords}"
            if location:
                query += f" {location}"
            
            logger.info(f"Searching via DuckDuckGo: {query}")
            
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, max_results=limit))
                
            for r in ddg_results:
                # Extract clean data from DDG result
                title = r.get('title', '').split(" - ")[0] # Name | Title often in title
                link = r.get('href', '')
                snippet = r.get('body', '')
                
                results.append({
                    "name": title,
                    "profile_url": link,
                    "snippet": snippet,
                    "source": "duckduckgo_xray"
                })
                
            return results
        except Exception as e:
             logger.error(f"Error searching people via DDG: {e}")
             return []

    def search_jobs(self, keywords, location=None, limit=5):
        """Searches for jobs on LinkedIn."""
        if not self.api:
            self.authenticate()
        
        try:
            results = self.api.search_jobs(keywords=keywords, location_name=location, limit=limit)
            return results
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
            return []

    def get_profile(self, urn_id):
        """Retrieves profile details."""
        if not self.api:
            self.authenticate()
        
        try:
            profile = self.api.get_profile(urn_id)
            return profile
        except Exception as e:
            logger.error(f"Error retrieving profile {urn_id}: {e}")
            return None
