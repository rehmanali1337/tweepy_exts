"""https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query"""
import tweepy
import typing
from .basc_rule import BasicRule, BasicMultipleRulesBuilder
from typing import Any


class UrlRule(BasicRule):

    def __init__(self, urls: typing.List[str], **kwargs: Any) -> None:
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


class MultipleUrlsRulesBuilder(BasicMultipleRulesBuilder):

    def _get_basic_rule(self) -> UrlRule:
        return UrlRule(self.targets)
