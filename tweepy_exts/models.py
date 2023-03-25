

class User:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.id = data.get("id")
        self.name = data.get("name")
        self.username = data.get("username")
        self.verified = data.get("verified", False)
        self.verified_type = data.get("verified_type", None)
        self.created_at = data.get("created_at", "")
        self.description = data.get("description", "")
        self.location = data.get("location", "")
        self.pinned_tweet_id = data.get("pinned_tweet_id")
        self.public_matrics = data.get("public_matrics", {})
        self.followers_count = self.public_matrics.get("followers_count")
        self.following_count = self.public_matrics.get("following_count")
        self.tweet_count = self.public_matrics.get("tweet_count")
        self.listed_count = self.public_matrics.get("listed_count")


class Media:
    def __init__(self, data: dict) -> None:
        self.data = data


class Annotation:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.start = data.get("start", 0)
        self.end = data.get("end", 0)
        self.probability = data.get("probability", 0)
        self.type = data.get("type", "")
        self.normalized_text = data.get("normalized_text", "")


class Image:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.url = data.get("url")
        self.width = data.get("width", 0)
        self.height = data.get("height", 0)

    def __repr__(self) -> str:
        return f"[{self.width}x{self.height}]({self.url})"

    def __str__(self) -> str:
        return f"[{self.width}x{self.height}]({self.url})"


class Url:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.start = data.get("start")
        self.end = data.get("end")
        self.url = data.get("url")
        self.expanded_url = data.get("expanded_url", self.url)
        self.display_url = data.get("display_url", self.url)
        self.images = [Image(i) for i in data.get("images", [])]
        self.status = data.get("status", 0)
        self.title = data.get("title", "")
        self.description = data.get("description", "")
        self.unwound_url = data.get("unwound_url", "")
        self.media_key = data.get("media_key")


class Tweet:

    def __init__(self, data: dict, from_alt=False) -> None:
        if data == {}:
            return
        self.full_data = data

        _includes = self.full_data.get("includes", {})
        self.users = [User(d) for d in _includes.get("users", [])]
        self.tweets = [self._alt_init(t) for t in _includes.get("tweets", [])]

        if not from_alt:
            data = self.full_data.get("data")

        self.tweet_data = data
        self.id = data.get("id")
        self.author_id = data.get("author_id")

        self.author = None
        if len(self.users) > 0:
            for user in self.users:
                if user.id == self.author_id:
                    self.author = user
                    break

        self.attachments = data.get("attachments", {})
        self.created_at = data.get("created_at")
        self.edit_hisotry_tweet_ids = data.get("edit_history_tweet_ids", [])
        self.public_matrics = data.get("public_matrics", {})
        self.retweet_count = self.public_matrics.get("retweet_count", None)
        self.reply_count = self.public_matrics.get("reply_count", None)
        self.like_count = self.public_matrics.get("like_count", None)
        self.impression_count = self.public_matrics.get("impression_count", None)
        self.quote_count = self.public_matrics.get("quote_count", None)
        self.referenced_tweets = data.get("referenced_tweets", [])
        self.text = data.get("text", "")

        self.entities = data.get("entities", {})
        self.annotations = [Annotation(a) for a in self.entities.get("annotations", [])]

        self.hashtags = [tag["tag"] for tag in self.entities.get("hashtags", [])]

        self.mentions = [mention["username"] for mention in self.entities.get("mentions", [])]

        self.urls = [Url(u) for u in self.entities.get("urls", [])]

        self.geo = data.get("geo", {})

        self.is_retweet = False
        self.fix_text()

    @classmethod
    def _alt_init(cls, data: dict) -> "Tweet":
        return cls(data, from_alt=True)

    @property
    def url(self):
        author_username = "i" if self.author is None else self.author.username
        return f"https://twitter.com/{author_username}/status/{self.id}"

    def __str__(self) -> str:
        return f"{self.text} || {self.url}"

    def __repr__(self) -> str:
        return self.__str__()

    def fix_text(self):
        """If tweet is a retweet then get complete text from retweeted tweet"""

        if len(self.referenced_tweets) > 0:
            for t in self.referenced_tweets:
                if t["type"] == "retweeted":
                    self.is_retweet = True
                    original_id = t["id"]
                    for tweet in self.tweets:
                        if tweet.id == original_id:
                            self.text = tweet.text
                            break
