import logging
import feedparser
import re
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup

from app.models.domain import CandidateTopic

logger = logging.getLogger("abtalks.discovery")

# Using reliable AI/Tech RSS feeds
SOURCES = [
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "MIT Tech Review - AI", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/"},
    {"name": "VentureBeat AI", "url": "https://feeds.feedburner.com/venturebeat/SZYF"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml"}
]

def clean_html(raw_html: str) -> str:
    """Removes HTML tags from content snippets."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # limit length to avoid massive context
    return text[:1000]

def normalize_title(title: str) -> str:
    """Create a basic fingerprint for duplicate detection."""
    if not title:
        return ""
    # Lowercase, remove non-alphanumeric
    norm = re.sub(r'[^a-z0-9]', '', title.lower())
    return norm

def discover_candidates() -> List[CandidateTopic]:
    """
    Fetches live information from configured RSS sources.
    Handles individual source failures gracefully.
    """
    candidates = []
    
    for source in SOURCES:
        logger.info(f"[DISCOVERY] Fetching from {source['name']} ({source['url']})")
        try:
            feed = feedparser.parse(source['url'])
            
            # Check for fetch errors inside feedparser
            if feed.bozo and hasattr(feed.bozo_exception, 'getMessage'):
                logger.warning(f"[DISCOVERY] Error parsing {source['name']}: {feed.bozo_exception}")
                continue
                
            entries = feed.entries[:5] # Grab up to 5 latest from each
            
            for entry in entries:
                title = entry.get('title', '')
                link = entry.get('link', '')
                description = entry.get('description', '') or entry.get('summary', '')
                
                if not title or not link:
                    continue
                    
                snippet = clean_html(description)
                fingerprint = normalize_title(title)
                
                candidates.append(CandidateTopic(
                    title=title,
                    content_snippet=snippet,
                    source_url=link,
                    source_name=source['name'],
                    fingerprint=fingerprint
                ))
        except Exception as e:
            logger.error(f"[DISCOVERY] Failed to fetch {source['name']}: {e}")
            
    logger.info(f"[DISCOVERY] Found {len(candidates)} total candidates.")
    return candidates
