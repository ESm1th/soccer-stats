from soccer_stats.items import (
    CountryItem,
    LeagueItem,
    MatchItem,
    PostMatchStatisticsItem
)
from soccer_stats.db import (
    SessionScope,
    Country,
    League,
    Match,
    MatchStatistics
)


session_scope = SessionScope()


class BaseSqlDbPipeline:

    """Common method across pipelines."""

    def open_spider(self, spider):
        self.scope = session_scope


class CountrySqlDbPipeline(BaseSqlDbPipeline):

    """
    Works with `CountryItem` item. Insert new entry to database.
    """

    def process_item(self, item, spider):
        if isinstance(item, CountryItem):
            with self.scope as session:
                country = Country(**item)
                session.add(country)
                session.commit()
        return item


class LeagueSqlDbPipeline(BaseSqlDbPipeline):

    """
    Works with `LeagueItem` item. Insert new entry to database.
    """

    def process_item(self, item, spider):
        if isinstance(item, LeagueItem):
            with self.scope as session:
                league = League(**item)
                session.add(league)
                session.commit()
        return item


class MatchSqlDbPipeline(BaseSqlDbPipeline):

    """Works with `MatchItem` item. Insert new entry to database."""

    def process_item(self, item, spider):
        if isinstance(item, MatchItem):
            with self.scope as session:
                match = Match(**item)
                session.add(match)
                session.commit()
        return item


class MatchStatisticsSqlDbPipeline(BaseSqlDbPipeline):

    """
    Works with `PostMatchStatisticsItem` item. Insert new entry to database.
    """

    def process_item(self, item, spider):
        if isinstance(item, PostMatchStatisticsItem):
            with self.scope as session:
                statistics = MatchStatistics(**item)
                session.add(statistics)
                session.commit()
        return item
