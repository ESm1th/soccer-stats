from logging import getLogger


logger = getLogger(__name__)


class Blank200ResponseMiddleware:

    """Crawling engine pauses after receiving a blank 200 response."""

    def __init__(self, engine, timeout):
        self.engine = engine
        self.timeout = timeout

    @classmethod
    def from_crawler(cls, crawler):
        timeout = crawler.settings['c']
        return cls(crawler.engine, timeout)

    def process_response(self, request, response, spider):
        if response.status == 200:
            if not bool(response.body):
                if not self.engine.paused:
                    self.engine.pause(self.timeout)
                    logger.debug(
                        'Engine paused on {time} seconds'.format(
                            time=self.timeout
                        )
                    )
                return request
            return response