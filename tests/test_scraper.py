import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import GooglePlayReviewScraper


@pytest.fixture
def scrape_reviews():
    appId = "com.samsung.android.spay"
    gs = GooglePlayReviewScraper(appId)
    scraped = gs.scrape(pageNumbers=1)
    return scraped

def test_scraper_1(scrape_reviews):
    assert len(scrape_reviews) == 40

def test_scraper_2(scrape_reviews):
    assert len(scrape_reviews[0].to_JSON()) > 0