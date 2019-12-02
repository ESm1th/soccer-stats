from time import sleep
from logging import getLogger

from scrapy.http import TextResponse
from scrapy_splash import SplashRequest


logger = getLogger(__name__)


class Blank200ResponseMiddleware:

    """Crawling engine pauses after receiving a blank 200 response."""

    def __init__(self, crawler, timeout):
        self.crawler = crawler
        self.timeout = timeout

    @classmethod
    def from_crawler(cls, crawler):
        timeout = crawler.settings['BLANK_TIMEOUT']
        return cls(crawler, timeout)

    def process_response(self, request, response, spider):
        text_response = TextResponse(url=response.url, body=response.body)
        if response.status == 200:
            if not bool(text_response.xpath('//body')):
                if not self.crawler.engine.paused:
                    logger.debug(
                        'Engine paused on {time} seconds'.format(
                            time=self.timeout
                        )
                    )
                    self.crawler.engine.pause()
                    sleep(self.timeout)
                request.dont_filter = True
                return request
        return response