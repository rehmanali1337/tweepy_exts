from .models import Tweet
import json
from tweepy.client import Response
import tweepy
from tweepy.asynchronous import AsyncStreamingClient, AsyncClient
from .logger import logger
from . import static
from .query_builder import QueryBuilder
from typing import Callable, Optional, List, Any


class MonitorState:
    valid_authors_ids: List[str] = []


OnStatusCallback = Optional[Callable[[Tweet], Any]]


class AsyncMainStreamingClient(AsyncStreamingClient):
    def __init__(self, *args: Any, on_status_callback: OnStatusCallback = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._on_status_callback: OnStatusCallback = on_status_callback

    async def on_connect(self) -> None:
        return logger.debug("Connected to twitter streaming API.")

    async def on_closed(self, resp: Any) -> None:
        return logger.debug(f"Stream has been closed by twitter. {resp}")

    async def on_data(self, raw_data: bytes) -> None:
        if self._on_status_callback:
            await self._on_status_callback(Tweet(json.loads(raw_data.decode())))


class AsyncMonitorEssentialAcces:
    def __init__(self, bearer_token: str,
                 on_new_status: OnStatusCallback):
        self.streaming_client = AsyncMainStreamingClient(
            bearer_token, on_status_callback=on_new_status, wait_on_rate_limit=False)
        self.client = AsyncClient(bearer_token=bearer_token)

    async def usernames_to_ids(self, usernames: List[str]) -> None:
        chunks = [usernames[x:x + 100] for x in range(0, len(usernames), 100)]
        for chunk in chunks:
            res = await self.client.get_users(usernames=chunk)
            assert isinstance(res, Response), f"Response from twitter is not of type Response. Type: {type(res)}"
            user_ids = [str(user.id) for user in res.data]
            MonitorState.valid_authors_ids.extend(user_ids)

    async def _start(self) -> None:
        await self.streaming_client.filter(expansions=static.expansions, tweet_fields=static.tweet_fields, user_fields=static.user_fields, media_fields=static.media_fields, place_fields=static.place_fields)

    async def track_keywords(self, keywords_list: List[str]) -> None:
        await self.delete_existing_rules()
        streaming_rules = QueryBuilder.track_keywords(keywords_list)
        await self.add_rules(streaming_rules)
        await self._start()

    async def delete_existing_rules(self) -> None:
        """Delete all existing rules"""
        res = await self.streaming_client.get_rules()
        if res.data is not None:
            existing_rules = res.data
            existing_rules_ids = [rule.id for rule in existing_rules]
            r = await self.streaming_client.delete_rules(existing_rules_ids)
            logger.debug(f"Rules deletion: {r}")

    async def track_users_by_usernames(self, usernames: List[str],
                                       remove_replies: bool = False,
                                       remove_retweets: bool = False,
                                       remove_quotes: bool = False) -> None:
        await self.delete_existing_rules()
        rules = QueryBuilder.tweets_from_users(
            usernames, remove_replies=remove_replies, remove_quoted=remove_quotes, remove_retweets=remove_retweets)
        added = await self.add_rules(rules)
        logger.debug(f"Rules creation: {added}")
        await self.usernames_to_ids(usernames)
        await self._start()

    async def add_rules(self, rules: List[tweepy.StreamRule], delete_existing: bool = True) -> Any:
        if delete_existing:
            await self.delete_existing_rules()
        return await self.streaming_client.add_rules(rules)

    async def run(self, rules: List[tweepy.StreamRule]) -> None:
        await self.add_rules(rules)
        return await self._start()

    async def sample(self) -> None:
        await self.streaming_client.sample()
