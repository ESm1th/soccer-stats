import os

from dotenv import load_dotenv


load_dotenv()

BOT_NAME = 'soccer_stats'

SPIDER_MODULES = ['soccer_stats.spiders']
NEWSPIDER_MODULE = 'soccer_stats.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) snap Chromium/78.0.3904.97 '
    'Chrome/78.0.3904.97 Safari/537.36'
)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Dupefilter settings
DUPEFILTER_DEBUG = True

# Mongo settings
MONGO_URI = os.environ['MONGO_URI']
MONGO_DATABASE = os.environ['MONGO_DATABASE']
MONGO_COLLECTION = os.environ['MONGO_COLLECTION']