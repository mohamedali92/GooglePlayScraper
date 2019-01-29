from bs4 import BeautifulSoup
import json
import sys
from json import dumps, loads, JSONEncoder, JSONDecoder
from time import sleep
from datetime import datetime
import re
from random import randint
import requests

# Max number of pages to click through when scraping reviews
MAX_PAGES_TO_SCRAPE = 500

# Google Play Reviews API base URL
# Give it a try:
# curl --data \
#   "reviewType=0&pageNum=15&id=com.inxile.BardTale&reviewSortOrder=2&xhr=1" \
#   https://play.google.com/store/getreviews
GOOGLE_PLAY_REVIEWS_URL = "https://play.google.com/store/getreviews"


class GooglePlayScrapedReview:
    '''
    Object returned from scraping Google Play reviews.
    '''

    def __init__(self, title, reviewText, date, author, rank):
        self.title = title.strip()
        self.reviewText = reviewText.strip()
        self.date = date.strip()
        self.author = author.strip()
        self.rank = rank.strip()

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class GooglePlayReviewScraperException(Exception):
    pass


class GooglePlayReviewScraper:
    '''
    Essentially, fires off a number of POST requests to the Google Play
    to simulate client requests.

    These requests (as of Sept 8, 2013) are in the format:

      reviewType:0            [???]
      pageNum:11              [pagination]
      id:com.inxile.BardTale  [package name]
      reviewSortOrder:0       [order reviews are retrieved in, 0 will return the newest reviews first, 1 will return based on ratings and 2 will return the most helpful reviews first]
      xhr:1                   [???]

    [???] means I don't know what the param is for.

    '''

    def __init__(self, packageName, maxNumberOfPages=MAX_PAGES_TO_SCRAPE):
        self.packageName = packageName
        self.maxNumberOfPages = maxNumberOfPages
        self.postParams = \
            {
                'reviewType': 0,
                'pageNum': 0,
                'id': packageName,
                'reviewSortOrder': 0,
                'xhr': 1
            }

    def scrapePageNumberUsingRequests(self, pageNum=0):
        # Modify POST params to use required pageNum param
        pagedPostParams = self.postParams.copy()
        pagedPostParams['pageNum'] = pageNum

        r = requests.post(GOOGLE_PLAY_REVIEWS_URL, data=pagedPostParams)
        return r.content

    def parseResult(self, postResults):
        # Magic indices required for parsing Google API results
        contentIdx = 0
        apiJsonStartIndex = 6
        htmlStartIndex = 2

        # Classes for parsing
        reviewBodyClass = "single-review"

        # Read in the API Request
        postResultsString = postResults

        # Attempt to parse result
        try:
            result = \
                json.loads(
                    postResultsString[apiJsonStartIndex:]
                )[contentIdx][htmlStartIndex]
            htmlResult = BeautifulSoup(result, "html.parser")

            parsedResults = \
                [self.generateScrapedObject(reviewBody) for
                    reviewBody in htmlResult.find_all(class_=reviewBodyClass)]
            return parsedResults

        except:
            raise \
                GooglePlayReviewScraperException(
                    "Exception: %s. Bad parse: %s" %
                    (sys.exc_info()[0], postResults)
                )

    @classmethod
    def generateScrapedObject(cls, review):
        # Extract the review title
        reviewTitleClass = "review-title"
        reviewTitle = review.find(class_=reviewTitleClass).get_text() if review.find(
            class_=reviewTitleClass).get_text() != "" else "Unavailable"

        # Extract the review body
        reviewBodyClass = "review-body"
        reviewBody = review.find(class_=reviewBodyClass).get_text() if review.find(
            class_=reviewBodyClass).get_text() != "" else "Unavailable"

        # Extract the review date
        reviewDateClass = "review-date"
        reviewDate = review.find(class_=reviewDateClass).get_text() if review.find(
            class_=reviewDateClass).get_text() != "" else "Unavailable"

        # Extract the review author
        reviewAuthorClass = "author-name"
        reviewAuthor = review.find(class_=reviewAuthorClass).get_text() if review.find(
            class_=reviewAuthorClass).get_text() != "" else "Unavailable"

        # Extract the review rank
        reviewRankClass = "review-info-star-rating"
        reviewRank = review.find("div", attrs={
                                 "class": "tiny-star star-rating-non-editable-container"})["aria-label"]
        reviewRank = reviewRank.split("Rated ")[1].split(" stars")[0] if reviewRank.split(
            "Rated ")[1].split(" stars")[0] != "" else "Unavailable"

        s = reviewTitle.encode('utf8')
        search = re.escape(s)
        reviewBodyFixed = reviewBody.split("Full Review")[0]

        return {'reviewDate': reviewDate, 'reviewAuthor': reviewAuthor, 'reviewRank': reviewRank, 'reviewBody': reviewBodyFixed}

    def scrape(self, pageNumbers=None):
        parsedResults = []
        scrapePageNums = pageNumbers or self.maxNumberOfPages

        try:
            for pageNum in range(scrapePageNums):
                results = self.parseResult(self.scrapePageNumberUsingRequests(pageNum))
                sleep(randint(2, 5))
                for result in results:
                    parsedResults.append(result)
        except GooglePlayReviewScraperException as e:
            print("Bad Parse: %s" % e)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        finally:
            return parsedResults


# Main method
# Play around to get a feel for this
if (__name__ == '__main__'):
         appId = "com.samsung.android.spay"
         try:
             gs = GooglePlayReviewScraper(appId)
             scraped = gs.scrape(pageNumbers=1)
             print (len(scraped))
             print (scraped)
         except:
            print ("error")
