import tweepy
import typing
from .basc_rule import BasicRule, BasicMultipleRulesBuilder
from typing import Any

"""https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query"""


class KeywordRule(BasicRule):

    def __init__(self, keywords: typing.List[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.keywords = keywords

    def build(self) -> tweepy.StreamRule:
        """The last method to call to Build the rule"""
        query = ""
        _keywords = self.keywords.copy()
        for keyword in _keywords:
            self.keywords.remove(keyword)

            if len(keyword) + len(query) + len(self.non_negated_query) + len(self.negated_query) >= self.max_query_len:
                print("Max Rules Limit reached.")
                break

            query = f"{query} OR {keyword}".strip()

        if query.startswith("OR"):
            query = query.replace("OR", "", 1).strip()

        final_query = ""
        if self.negated_query.strip() != "" or self.non_negated_query.strip() != "":
            final_query = f"{self.non_negated_query} ({query}) {self.negated_query}"
        else:
            final_query = query

        return tweepy.StreamRule(final_query)


class MultipleKeywordRulesBuilder(BasicMultipleRulesBuilder):

    def _get_basic_rule(self) -> KeywordRule:
        return KeywordRule(self.targets)
