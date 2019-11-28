import scrapy
from scrapy.loader.processors import TakeFirst

from soccer_stats.processors import (
    process_league_title,
    strip_string,
    convert_to_integer,
    process_season,
    process_all_matches,
    process_timestamp,
    process_home_result,
    process_away_result,
    process_post_match_data
)


class League(scrapy.Item):
    title = scrapy.Field(output_processor=process_league_title)
    country = scrapy.Field(output_processor=TakeFirst())
    nation = scrapy.Field(output_processor=strip_string)
    division = scrapy.Field(output_processor=strip_string)
    league_type = scrapy.Field(output_processor=strip_string)
    teams_count = scrapy.Field(output_processor=convert_to_integer)
    season = scrapy.Field(output_processor=process_season)
    all_matches_count = scrapy.Field(output_processor=process_all_matches)
    completed = scrapy.Field()
    image_url = scrapy.Field(output_processor=TakeFirst())
    hash = scrapy.Field()
    blocked = scrapy.Field()


class Match(scrapy.Item):
    league_hash = scrapy.Field(output_processor=TakeFirst())
    timestamp = scrapy.Field(output_processor=process_timestamp)
    home_team = scrapy.Field(output_processor=TakeFirst())
    away_team = scrapy.Field(output_processor=TakeFirst())
    stadium = scrapy.Field(output_processor=TakeFirst())
    home_result = scrapy.Field(output_processor=process_home_result)
    away_result = scrapy.Field(output_processor=process_away_result)
    home_image = scrapy.Field()
    away_image = scrapy.Field()
    hash = scrapy.Field()
    post_match_statistics = scrapy.Field()


class PostMatchStatistics(scrapy.Item):
    match_hash = scrapy.Field(output_processor=TakeFirst())
    possession = scrapy.Field(output_processor=process_post_match_data)
    shots = scrapy.Field(output_processor=process_post_match_data)
    cards = scrapy.Field(output_processor=process_post_match_data)
    corners = scrapy.Field(output_processor=process_post_match_data)
    fouls = scrapy.Field(output_processor=process_post_match_data)
    offsides = scrapy.Field(output_processor=process_post_match_data)
