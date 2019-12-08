from time import sleep
from logging import getLogger

from scrapy.http import TextResponse


logger = getLogger(__name__)


class Blank200ResponseMiddleware:

    """
    Pause crawling engine and then retry request if <body> tag in received
    response is empty. 
    """

    def __init__(self, crawler, timeout):
        self.crawler = crawler
        self.timeout = timeout
        self.log_message = 'Engine paused on {time} seconds'.format(
            time=self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        timeout = crawler.settings['BLANK_TIMEOUT']
        return cls(crawler, timeout)

    def process_response(self, request, response, spider):
        text_response = TextResponse(url=response.url, body=response.body)
        if response.status == 200:
            if not bool(text_response.xpath('//body')):
                if not self.crawler.engine.paused:
                    logger.debug(self.log_message)
                    self.crawler.engine.pause()
                    sleep(self.timeout)
                    self.crawler.engine.unpause()
                request.dont_filter = True
                return request
        return response