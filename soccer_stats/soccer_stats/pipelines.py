from soccer_stats.mongo import StatsMongoClient
from soccer_stats.settings import (
    MONGO_URI,
    MONGO_DATABASE,
    MONGO_COLLECTION
)
from soccer_stats.items import (
    League,
    Match,
    PostMatchStatistics
)


class BaseSoccerStatsPipline:

    def __init__(self, *args, **kwargs):
        self.client = StatsMongoClient(
            MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION
        )


class LeaguePipeline:

    def process_item(self, item, spider):
        
        if isinstance(item, League):
            league = self.client.find_one({'_id': item['_id']})
            if not league:
                self.client.insert_one(dict(item))
