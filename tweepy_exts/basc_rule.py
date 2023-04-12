from typing import Any
import tweepy
from typing import Optional, List


class BasicRule:

    def __init__(self,
                 max_query_len: int = 510,
                 *args: Any, **kwargs: Any) -> None:
        self.max_query_len = max_query_len
        self.negated_query = ""
        self.non_negated_query = ""

    def _add_operator(self, operator: str, negated: bool = False) -> None:
        if negated:
            operator = f"-{operator}"
            self.negated_query = f"{self.negated_query} {operator}".strip()
        else:
            self.non_negated_query = f"{self.non_negated_query} {operator}".strip()

    def has_links(self, negated: bool = False) -> None:
        return self._add_operator("has:links", negated=negated)

    def has_media(self, negated: bool = False) -> None:
        return self._add_operator("has:media", negated=negated)

    def has_images(self, negated: bool = False) -> None:
        return self._add_operator("has:images", negated=negated)

    def is_reply(self, negated: bool = False) -> None:
        return self._add_operator("is:reply", negated=negated)

    def is_retweet(self, negated: bool = False) -> None:
        return self._add_operator("is:retweet", negated=negated)

    def is_quote(self, negated: bool = False) -> None:
        return self._add_operator("is:quote", negated=negated)

    def is_verified(self, negated: bool = False) -> None:
        return self._add_operator("is:verified", negated=negated)

    def has_mentions(self, negated: bool = False) -> None:
        return self._add_operator("has:mentions", negated=negated)

    def has_video_link(self, negated: bool = False) -> None:
        return self._add_operator("has:video_link", negated=negated)

    def has_geo(self, negated: bool = False) -> None:
        return self._add_operator("has:geo", negated=negated)

    def lang(self, lang: str) -> None:
        return self._add_operator(f"lang:{lang}", negated=False)

    def has_hashtags(self, negated: bool = False) -> None:
        return self._add_operator("has:hashtags", negated=negated)

    def build(self) -> tweepy.StreamRule:
        return tweepy.StreamRule()


class BasicMultipleRulesBuilder:

    def __init__(self, targets: List[str],
                 max_rules: int = 25,
                 max_query_len: int = 510,
                 is_retweet: Optional[bool] = None,
                 is_reply: Optional[bool] = None,
                 is_quote: Optional[bool] = None,
                 is_verified: Optional[bool] = None,
                 is_nullcast: Optional[bool] = None,
                 has_hashtags: Optional[bool] = None,
                 has_cashtags: Optional[bool] = None,
                 has_links: Optional[bool] = None,
                 has_mentions: Optional[bool] = None,
                 has_media: Optional[bool] = None,
                 has_images: Optional[bool] = None,
                 has_video_links: Optional[bool] = None,
                 has_geo: Optional[bool] = None,
                 lang: Optional[str] = None
                 ) -> None:
        self.targets = targets
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

        self.rules: List[tweepy.StreamRule] = []

    def _get_basic_rule(self) -> BasicRule:
        assert False, "Override this method to return specific rule class"

    def build(self) -> List[tweepy.StreamRule]:
        while True:
            if len(self.rules) == self.max_rules:
                break

            rule = self._get_basic_rule()

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
            if len(self.targets) > 0:
                continue

            break

        return self.rules
