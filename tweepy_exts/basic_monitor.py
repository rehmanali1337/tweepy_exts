

import typing
from tweepy_exts.async_monitor import AsyncMonitorEssentialAcces
import asyncio
import tweepy
import colorama

colorama.init(autoreset=True)


class Console:

    @classmethod
    def j_args(cls, args):
        j = [str(arg) for arg in args]
        return " ".join(j)

    @staticmethod
    def wait_for_shutdown():
        input(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\n[#] Press Enter <- ")

    @staticmethod
    def error(*args, exc_info=False, shutdown=False):
        message = Console.j_args(args)
        print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[-] {message}")
        if shutdown:
            return Console.wait_for_shutdown()

    @staticmethod
    def warn(*args, exc_info=False, shutdown=False):
        message = Console.j_args(args)
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"[*] {message}")
        if shutdown:
            return Console.wait_for_shutdown()

    @staticmethod
    def info(*args, exc_info=False, shutdown=False):
        message = Console.j_args(args)
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"[+] {message}")
        if shutdown:
            return Console.wait_for_shutdown()


class BasicMonitor:

    def __init__(self,
                 targets_list: typing.List[str],
                 bearer_token: str,
                 output_queue: asyncio.Queue,
                 console: Console = Console,
                 remove_duplicates=True,
                 raw_tweet=False
                 ) -> None:
        self.targets_list = targets_list
        self.output_queue = output_queue
        self.remove_duplicates = remove_duplicates
        self.raw_tweet = raw_tweet
        self.monitor = AsyncMonitorEssentialAcces(bearer_token, self.on_status)
        self.ecl = []
        self.console = console

    async def start(self):
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

    async def build_rules(self):
        return []

    async def on_status(self, tweet):
        if self.raw_tweet:
            return await self.output_queue.put(tweet)
        tweet_id = tweet.id
        if self.remove_duplicates and tweet_id in self.ecl:
            return
        self.ecl.append(tweet_id)
        asyncio.create_task(self.handle_tweet(tweet_id))

    async def handle_tweet(self, tweet_id: str):
        self.console.info("New Tweet:", self.tweet_id_to_url(tweet_id))
        return await self.output_queue.put(tweet_id)

    def tweet_id_to_url(self, tweet_id: str) -> str:
        return f"https://twitter.com/i/status/{tweet_id}"
