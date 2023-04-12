
from tweepy_exts.async_monitor import AsyncMonitorEssentialAcces
from tweepy_exts.models import Tweet
import asyncio
import tweepy
from typing import List, Type, Any
from .logger import Console


class BasicMonitor:

    def __init__(self,
                 targets_list: List[str],
                 bearer_token: str,
                 output_queue: asyncio.Queue[Any],
                 *,
                 console: Type[Console] = Console,
                 **kwargs: Any
                 ) -> None:
        self.targets_list = targets_list
        self.output_queue = output_queue
        self.monitor = AsyncMonitorEssentialAcces(bearer_token, self.on_status)
        self.console = console

    async def start(self) -> None:
        try:
            self.console.info("Building the rules for monitoring data ...")
            rules = await self.build_rules()
            await self.monitor.run(rules)

        except tweepy.Unauthorized as e:
            return self.console.error(f"Bearer token is invalid/disabled. {e}")

        except Exception as e:
            self.console.error(f"Monitoring error. {e}", exc_info=True)
            self.console.info("Restarting in 3 seconds ...")
            await asyncio.sleep(3)
            return await self.start()

    async def build_rules(self) -> List[tweepy.StreamRule]:
        return []

    async def on_status(self, tweet: Tweet) -> None:
        asyncio.create_task(self.handle_tweet(tweet))

    async def handle_tweet(self, tweet: Tweet) -> None:
        return await self.output_queue.put(tweet)
