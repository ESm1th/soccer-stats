import json
from datetime import datetime
from uuid import uuid4

import scrapy
from scrapy.http import FormRequest, HtmlResponse
from scrapy.loader import ItemLoader

from soccer_stats.items import (
    CountryItem,
    LeagueItem,
    MatchItem,
    PostMatchStatisticsItem
)


class GetSoccerDataSpider(scrapy.Spider):

    """
    Spider that pulls soccer data from web resources.
    Fetched data: leagues and related matches.
    """

    name = 'get_soccer_data'
    allowed_domains = ['footystats.org']
    base_url = 'https://footystats.org'

    def start_requests(self):
        yield scrapy.Request(
            url=self.make_url('leagues/'),
            callback=self.parse_leagues
        )

    def parse_leagues(self, response):
        """
        Parses response and fetches country selectors from content. Gets
        coutry name from selector and than yields requests for all leagues urls
        for each available country.
        """

        # get relative urls pathes for each league
        leagues_urls = response.xpath(
            '//div[@class="team-item info"]/a/@href'
        ).getall()

        countries_ids = {}  # empty dict to gather unique country titles

        for url in leagues_urls:
            country_name = url.strip('/').split('/')[0]

            if country_name not in countries_ids.keys():
                loader = ItemLoader(item=CountryItem(), response=response)
                loader.add_value('title', country_name)
                loader.add_value('id', uuid4())
                country = loader.load_item()
                countries_ids[country_name] = country['id']
                yield country

            yield response.follow(
                url=url,
                callback=self.parse_league,
                cb_kwargs={'country_id': countries_ids[country_name]}
            )

    def parse_league(self, response, **kwargs):
        """Makes requests for each available season for particular league."""
        seasons = response.xpath(
            '//div[@class="detail season"]/'
            'div[contains(@class, "drop-down-parent")]/ul/li/a'
        )

        for season in seasons:
            # parameters for urls query string
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
                cb_kwargs={'country_id': kwargs.get('country_id')}
            )

    def parse_season(self, response, **kwargs):
        """
        Parses page with particular league season. Creates `league` item and
        fills it with data parsed from returned content.
        """
        loader = ItemLoader(
            item=LeagueItem(),
            response=response
        )
        loader.add_value('id', uuid4())
        loader.add_xpath(
            'title',
            '//div[@id="teamSummary"]/h1[contains(@class, "teamName")]/text()'
        )
        loader.add_value('country_id', kwargs.get('country_id'))
        loader.add_xpath(
            'teams_count',
            (
                '//div[@class="league-details"]/div[@class="detail"]'
                '/div[contains(., "Teams")]/following-sibling::div/text()'
            )
        )
        loader.add_xpath(
            'season_start',
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
            'image_url',
            '//div[@id="teamSummary"]/img/@src'
        )
        league = loader.load_item()

        matches = response.xpath(
            '//div[@id="teamSummary"]/ul[contains(@class, "secondary-nav")]/'
            'li[contains(@class, "middle")]/a'
        )  # selector
        href = matches.xpath('@href').get()

        # matches for this league available for premium account
        league['blocked'] = True if href else False
        yield league

        if href == '#':
            # parameters for urls query string
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
                cb_kwargs={'league_id': league['id']}
            )
        elif href and href != '#':
            yield response.follow(
                url=href,
                callback=self.parse_matches,
                cb_kwargs={'league_id': league['id']}
            )

    def parse_matches(self, response, **kwargs):
        """
        Pulls all urls for each match from returned content and
        yields request for each url.
        """
        matches = response.xpath(
            '//table[contains(@class, "matches-table")]/tr/'
            'td[contains(@class, "link")]/a/@href'
        ).getall()

        for match in matches:
            yield response.follow(
                url=match,
                callback=self.parse_match_dates,
                cb_kwargs={'league_id': kwargs.get('league_id')}
            )

    def parse_match_dates(self, response, **kwargs):
        active_match_item = response.xpath(
            '//ul[@class="menu bbox"]/li/'
            'p[contains(@class, "active")]/parent::li'
        )

        params = {
            'z': active_match_item.attrib['data-z'],
            'zz': active_match_item.attrib['data-zz'],
            'zzzz': active_match_item.attrib['data-zzzz']
        }
        
        yield FormRequest(
            url=self.make_url('ajax_h2h.php'),
            method='POST',
            formdata=params,
            callback=self.parse_match,
            cb_kwargs={'league_id': kwargs.get('league_id')}
        )

    def parse_match(self, response, **kwargs):
        """
        Fetches data about particular event from returned content.
        Creates match item and fills with fetched data.
        """
        html_event_part = HtmlResponse(
            url=response.url,
            body=json.loads(response.body)['content1'].encode()
        )

        match_loader = ItemLoader(
            item=MatchItem(),
            response=html_event_part
        )
        match_loader.add_value('id', uuid4())
        match_loader.add_value('league_id', kwargs.get('league_id'))
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

        html_post_match = HtmlResponse(
            url=response.url,
            body=json.loads(response.body)['content2'].encode()
        )

        if html_post_match.xpath('//div[@class="w100 cf ac"]'):
            # if post match statistics data exists
            statistics_loader = ItemLoader(
                item=PostMatchStatisticsItem(),
                response=html_post_match
            )
            statistics_loader.add_value('id', uuid4())
            statistics_loader.add_value('match_id', match['id'])
            statistics_loader.add_xpath(
                'possession_home',
                '//span[contains(@class, "possession")]/text()'
            )
            statistics_loader.add_xpath(
                'possession_away',
                '//span[contains(@class, "possession")]/text()'
            )
            statistics_loader.add_xpath(
                'shots_home',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Shots")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'shots_away',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Shots")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'cards_home',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Cards")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'cards_away',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Cards")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'corners_home',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Corners")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'corners_away',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Corners")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'fouls_home',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Fouls")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'fouls_away',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Fouls")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'offsides_home',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Offsides")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            statistics_loader.add_xpath(
                'offsides_away',
                '//div[@class="w100 m0Auto"]/div/div[contains(text(), "Offsides")]'
                '/following-sibling::div[contains(@class, "bbox")]/span/text()'
            )
            yield statistics_loader.load_item()

    def make_url(self, path):
        """Returns url created from base url and relative path."""
        return '{base}/{relative}'.format(base=self.base_url, relative=path)


