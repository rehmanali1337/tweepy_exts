import asyncio
import tweepy
from .logger import Console as Console
from _typeshed import Incomplete
from tweepy_exts.async_monitor import AsyncMonitorEssentialAcces as AsyncMonitorEssentialAcces
from tweepy_exts.models import Tweet as Tweet
from typing import Any, List, Type

class BasicMonitor:
    targets_list: Incomplete
    output_queue: Incomplete
    monitor: Incomplete
    console: Incomplete
    def __init__(self, targets_list: List[str], bearer_token: str, output_queue: asyncio.Queue[Any], *, console: Type[Console] = ..., **kwargs: Any) -> None: ...
    async def start(self) -> None: ...
    async def build_rules(self) -> List[tweepy.StreamRule]: ...
    async def on_status(self, tweet: Tweet) -> None: ...
    async def handle_tweet(self, tweet: Tweet) -> None: ...
