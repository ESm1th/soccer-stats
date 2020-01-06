import os


BOT_NAME = 'soccer_stats'

SPIDER_MODULES = ['soccer_stats.spiders']
NEWSPIDER_MODULE = 'soccer_stats.spiders'

LOG_FILE = 'soccer.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) snap Chromium/78.0.3904.97 '
    'Chrome/78.0.3904.97 Safari/537.36'
)

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Cookies
COOKIES_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.8

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
AUTOTHROTTLE_TARGET_CONCURRENCY = 4

# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Dupefilter settings
DUPEFILTER_DEBUG = True

# Item pipelines
ITEM_PIPELINES = {
    # 'soccer_stats.pipelines.LeaguePipeline': 100,
    # 'soccer_stats.pipelines.MatchPipeline': 110,
    # 'soccer_stats.pipelines.PostMatchStatisticsPipeline': 120,
    'soccer_stats.pipelines.CountrySqlDbPipeline': 130,
    'soccer_stats.pipelines.LeagueSqlDbPipeline': 140,
    'soccer_stats.pipelines.MatchSqlDbPipeline': 150,
    'soccer_stats.pipelines.MatchStatisticsSqlDbPipeline': 160
}

# Custom project downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'soccer_stats.middlewares.SetProxyMiddleware': 720,
    'soccer_stats.middlewares.Blank200ResponseMiddleware': 1000,
}

# Timeout for blank 200 responses in seconds
BLANK_TIMEOUT = 20

# Postgres settings
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']

# Proxy settings
PROXY = os.environ['PROXY']
PROXY_USERNAME = os.environ['PROXY_USERNAME']
PROXY_PASSWORD = os.environ['PROXY_PASSWORD']