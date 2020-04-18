[![PyPI version](https://badge.fury.io/py/google-play-reviews-scraper.svg)](https://badge.fury.io/py/google-play-reviews-scraper)
[![CircleCI](https://circleci.com/gh/mohamedali92/google-play-reviews-scraper/tree/master.svg?style=svg)](https://circleci.com/gh/mohamedali92/google-play-reviews-scraper/tree/master)

google-play-reviews-scraper is a python application that scrapes and downloads an app's user reviews from the Google play store.



Install
-------
To install the scraper:
```bash
$ pip install google-play-reviews-scraper
```

To update the scraper:
```bash
$ pip install google-play-reviews-scraper --upgrade
```

Usage
-----

To scape an app's reviews:
```bash
$ google-play-reviews-scraper -id <app_id> -n <number of pages to scrape>
```

OPTIONS
-------
```
--help -h           Show help message and exit.

--app_id  -id       ID of app you need to scaper, for example "com.samsung.android.spay"

--num_pages  -n     Number of review pages to scraper, each page contains 40 reviews.
```
