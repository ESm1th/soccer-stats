import scrapy
from scrapy.loader.processors import TakeFirst

from soccer_stats.processors import (
    process_league_title,
    strip_string,
    convert_to_integer,
    process_season_start,
    process_season_end,
    process_all_matches,
    process_timestamp,
    process_home_result,
    process_away_result,
    process_post_match_data_home,
    process_post_match_data_away
)


class Country(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())


class League(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=process_league_title)
    country_id = scrapy.Field(output_processor=TakeFirst())
    teams_count = scrapy.Field(output_processor=convert_to_integer)
    season_start = scrapy.Field(output_processor=process_season_start)
    season_end = scrapy.Field(output_processor=process_season_end)
    all_matches_count = scrapy.Field(output_processor=process_all_matches)
    completed = scrapy.Field()
    image_url = scrapy.Field(output_processor=TakeFirst())
    blocked = scrapy.Field()


class Match(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    league_id = scrapy.Field(output_processor=TakeFirst())
    timestamp = scrapy.Field(output_processor=process_timestamp)
    home_team = scrapy.Field(output_processor=TakeFirst())
    away_team = scrapy.Field(output_processor=TakeFirst())
    stadium = scrapy.Field(output_processor=TakeFirst())
    home_result = scrapy.Field(output_processor=process_home_result)
    away_result = scrapy.Field(output_processor=process_away_result)
    home_image = scrapy.Field()
    away_image = scrapy.Field()


class PostMatchStatistics(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    match_id = scrapy.Field(output_processor=TakeFirst())
    possession_home = scrapy.Field(output_processor=process_post_match_data_home)
    possession_away = scrapy.Field(output_processor=process_post_match_data_away)
    shots_home = scrapy.Field(output_processor=process_post_match_data_home)
    shots_away = scrapy.Field(output_processor=process_post_match_data_away)
    cards_home = scrapy.Field(output_processor=process_post_match_data_home)
    cards_away = scrapy.Field(output_processor=process_post_match_data_away)
    corners_home = scrapy.Field(output_processor=process_post_match_data_home)
    corners_away = scrapy.Field(output_processor=process_post_match_data_away)
    fouls_home = scrapy.Field(output_processor=process_post_match_data_home)
    fouls_away = scrapy.Field(output_processor=process_post_match_data_away)
    offsides_home = scrapy.Field(output_processor=process_post_match_data_home)
    offsides_away = scrapy.Field(output_processor=process_post_match_data_away)