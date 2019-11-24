from datetime import datetime
from bson.objectid import ObjectId

import scrapy
from scrapy.http import FormRequest
from scrapy.loader import ItemLoader

from soccer_stats.items import (
    League,
    Match,
    PostMatchStatistics
)


class FootyStatsSpider(scrapy.Spider):
    name = 'footy_stats_spider'
    allowed_domains = ['footystats.org']
    base_url = 'https://footystats.org'

    custom_settings = {'LOG_STDOUT': True, }

    def start_requests(self):
        yield scrapy.Request(
            url=self.make_url('/leagues/'),
            callback=self.parse_leagues
        )

    def parse_leagues(self, response):
        country_selectors = response.xpath('//div[@class="pt2e"]')

        for selector in country_selectors:
            country = selector.attrib['id']
            leagues_urls = selector.xpath('div/table/tr/td/a/@href').getall()

            for url in leagues_urls:

                yield response.follow(
                    url=url,
                    callback=self.parse_league,
                    cb_kwargs={'country': country}
                )

    def parse_league(self, response, **kwargs):

        seasons = response.xpath(
            '//div[@class="detail season"]/'
            'div[contains(@class, "drop-down-parent")]/ul/li/a'
        )

        for season in seasons:

            params = {
                'hash': season.attrib['data-hash'],
                'zzz': season.attrib['data-zzz'],
                'zzzz': season.attrib['data-zzzz'],
                'cur': season.attrib['data-z']
            }

            yield FormRequest(
                url=self.make_url('ajax_league.php'),
                method='POST',
                formdata=params,
                callback=self.parse_season,
                cb_kwargs={'country': kwargs.get('country')}
            )

    def parse_season(self, response, **kwargs):

        loader = ItemLoader(
            item=League(),
            response=response
        )

        loader.add_value('_id', ObjectId())
        loader.add_value('country', kwargs.get('country'))
        loader.add_xpath(
            'title',
            '//div[@id="teamSummary"]/h1[@class="teamName long"]/text()'
        )
        loader.add_xpath(
            'nation',
            (
                '//div[@class="league-details"]/div[@class="detail"]'
                '/div[contains(., "Nation")]/following-sibling::div/a/text()'
            )
        )
        loader.add_xpath(
            'division',
            (
                '//div[@class="league-details"]/div[@class="detail"]'
                '/div[contains(., "Division")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'league_type',
            (
                '//div[@class="league-details"]/div[@class="detail"]'
                '/div[contains(., "Type")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'teams_count',
            (
                '//div[@class="league-details"]/div[@class="detail"]'
                '/div[contains(., "Teams")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'season',
            (
                '//div[@class="league-details"]/div[@class="detail season"]'
                '/div[contains(., "Season")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'season_end',
            (
                '//div[@class="league-details"]/div[@class="detail season"]'
                '/div[contains(., "Season")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'all_matches_count',
            (
                '//div[@class="league-details"]/div[@class="detail season"]'
                '/div[contains(., "Matches")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'all_matches_count',
            (
                '//div[@class="league-details"]/div[@class="detail season"]'
                '/div[contains(., "Matches")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'image_url',
            '//div[@id="teamSummary"]/img/@src'
        )

        league = loader.load_item()
        yield league

        matches = response.xpath(
            '//div[@id="teamSummary"]/ul[contains(@class, "secondary-nav")]/'
            'li[contains(@class, "middle")]/a'
        )  # selector

        href = matches.xpath('@href').get()
        if href == '#':

            params = {
                'hash': matches.attrib['data-hash'],
                'zzz': matches.attrib['data-zzz'],
                'cur': matches.attrib['data-z']
            }

            yield FormRequest(
                url=self.make_url('ajax_league.php'),
                method='POST',
                formdata=params,
                callback=self.parse_matches,
                cb_kwargs={'league_id': league['_id']}
            )

        elif not href:  # to do what if recursion?
            response.request.dont_filter = True
            yield response.request

        else:

            yield response.follow(
                url=href,
                callback=self.parse_matches,
                cb_kwargs={'league_id': league['_id']}
            )

    def parse_matches(self, response, **kwargs):

        matches = response.xpath(
            '//table[contains(@class, "matches-table")]/tr/'
            'td[contains(@class, "link")]/a/@href'
        ).getall()

        for match in matches:

            yield response.follow(
                url=match,
                callback=self.parse_match,
                cb_kwargs={'league_id': kwargs.get('league_id')}
            )
        
    def parse_match(self, response, **kwargs):

        match_loader = ItemLoader(item=Match(), response=response)

        match_loader.add_value('_id', ObjectId())
        match_loader.add_value(
            'league_id',
            kwargs.get('league_id')
        )
        match_loader.add_xpath(
            'timestamp',
            '//p[@data-time]/@data-time'
        )
        match_loader.add_xpath(
            'home_team',
            '//span[@itemprop="homeTeam"]/span[@itemprop="name"]/@content'
        )
        match_loader.add_xpath(
            'away_team',
            '//span[@itemprop="awayTeam"]/span[@itemprop="name"]/@content'
        )
        match_loader.add_xpath(
            'stadium',
            '//small/span[@itemprop="name"]/text()'
        )
        match_loader.add_xpath(
            'home_result',
            '//div[contains(@class, "h2h-final-score")]/'
            'div[@class="widget-content"]/h2/text()'
        )
        match_loader.add_xpath(
            'away_result',
            '//div[contains(@class, "h2h-final-score")]/'
            'div[@class="widget-content"]/h2/text()'
        )

        match = match_loader.load_item()
        yield match

        if response.xpath('//div[@class="w100 cf ac"]'):

            statistics_loader = ItemLoader(
                item=PostMatchStatistics(),
                response=response
            )

            statistics_loader.add_value('match_id', match['_id'])
            statistics_loader.add_xpath(
                'possession',
                '//span[contains(@class, "possession")]/text()'
            )
            statistics_loader.add_xpath(
                'shots',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Shots")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'cards',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Cards")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'corners',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Corners")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'fouls',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Fouls")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'offsides',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Offsides")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )

            yield statistics_loader.load_item()

    def make_url(self, path):
        return '{base}/{relative}'.format(base=self.base_url, relative=path)


