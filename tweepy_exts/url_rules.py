"""https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query"""
import tweepy
import typing
from .basc_rule import BasicRule


class UrlRule(BasicRule):

    def __init__(self, urls: typing.List[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.urls = urls

    def build(self) -> tweepy.StreamRule:
        """The last method to call to Build the rule"""
        query = ""
        _urls = self.urls.copy()
        for url in _urls:
            self.urls.remove(url)

            if len(url) + len(query) + len(self.non_negated_query) + len(self.negated_query) >= self.max_query_len:
                break

            query = f"{query} OR url:{url}".strip()

        if query.startswith("OR"):
            query = query.replace("OR", "", 1).strip()

        final_query = ""
        if self.negated_query.strip() != "" or self.non_negated_query.strip() != "":
            final_query = f"{self.non_negated_query} ({query}) {self.negated_query}"
        else:
            final_query = query

        return tweepy.StreamRule(final_query)


class MultipleUrlsRulesBuilder:

    def __init__(self, urls: typing.List[str],
                 max_rules=25,
                 max_query_len=510,
                 is_retweet=None,
                 is_reply=None,
                 is_quote=None,
                 is_verified=None,
                 is_nullcast=None,
                 has_hashtags=None,
                 has_cashtags=None,
                 has_links=None,
                 has_mentions=None,
                 has_media=None,
                 has_images=None,
                 has_video_links=None,
                 has_geo=None,
                 lang: str = None
                 ) -> None:
        self.urls = urls
        self.max_rules = max_rules
        self.max_query_len = max_query_len
        self.is_retweet = is_retweet
        self.is_reply = is_reply
        self.is_quote = is_quote
        self.is_verified = is_verified
        self.is_nullcast = is_nullcast
        self.has_hashtags = has_hashtags
        self.has_cashtags = has_cashtags
        self.has_links = has_links
        self.has_mentions = has_mentions
        self.has_media = has_media
        self.has_images = has_images
        self.has_video_links = has_video_links
        self.has_geo = has_geo
        self.lang = lang

        self.rules = []

    def build(self) -> typing.List[tweepy.StreamRule]:
        while True:
            if len(self.rules) == self.max_rules:
                if len(self.urls) > 0:
                    print(f"Extra urls not being monitored: {len(self.usernames)}")
                break

            rule = UrlRule(self.urls)
            if self.is_retweet is not None:
                rule.is_retweet(negated=not self.is_retweet)

            if self.is_quote is not None:
                rule.is_quote(negated=not self.is_quote)

            if self.is_reply is not None:
                rule.is_reply(negated=not self.is_reply)

            if self.is_verified is not None:
                rule.is_verified(negated=not self.is_verified)

            if self.is_nullcast is not None:
                pass
                # rule.is_nullcast(negated=not self.is_nullcast)

            if self.has_hashtags is not None:
                rule.has_hashtags(negated=not self.has_hashtags)

            if self.has_cashtags is not None:
                pass
                # rule.has_cashtags(negated=not self.has_hashtags)

            if self.has_links is not None:
                rule.has_links(negated=not self.has_links)

            if self.has_mentions is not None:
                rule.has_mentions(negated=not self.has_mentions)

            if self.has_media is not None:
                rule.has_media(negated=not self.has_media)

            if self.has_video_links is not None:
                rule.has_video_link(negated=not self.has_video_links)

            if self.has_images is not None:
                rule.has_images(negated=not self.has_images)

            if self.has_geo is not None:
                rule.has_geo(negated=not self.has_geo)

            if self.lang is not None:
                rule.lang(self.lang)

            _build_rule = rule.build()
            self.rules.append(_build_rule)
            if len(self.urls) > 0:
                continue

            break

        return self.rules
