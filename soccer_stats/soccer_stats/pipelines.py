from soccer_stats.mongo import mongo_client
from soccer_stats.settings import (
    MONGO_LEAGUES_COLLECTION,
    MONGO_MATCHES_COLLECTION
)
from soccer_stats.items import (
    League,
    Match,
    PostMatchStatistics
)


class BaseSoccerStatsPipline:

    def open_spider(self, spider):
        self.client = mongo_client

    def close_spider(self, spider):
        self.client.close()

class LeaguePipeline(BaseSoccerStatsPipline):

    def process_item(self, item, spider):

        if isinstance(item, League):
            self.client.collection = MONGO_LEAGUES_COLLECTION

            league = self.client.collection.find_one({'hash': item['hash']})
            if not league:
                self.client.collection.insert_one(dict(item))

        return item


class MatchPipeline(BaseSoccerStatsPipline):

    def process_item(self, item, spider):

        if isinstance(item, Match):
            self.client.collection = MONGO_MATCHES_COLLECTION
            match = self.client.collection.find_one({'hash': item['hash']})

            if match:
                self.client.collection.update_one(
                    {'hash': item['hash']},
                    {'$set': dict(item)}
                )
            else:
                self.client.collection.insert_one(dict(item))

        return item


class PostMatchStatisticsPipeline(BaseSoccerStatsPipline):

    def process_item(self, item, spider):

        if isinstance(item, PostMatchStatistics):
            self.client.collection = MONGO_MATCHES_COLLECTION

            match_hash = item.pop('match_hash')
            self.client.collection.update_one(
                {'hash': match_hash},
                {'$set': {'post_match_statistics': dict(item)}}
            )

        return item
