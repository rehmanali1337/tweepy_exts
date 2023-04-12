"""https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query"""
import tweepy
from .basc_rule import BasicRule, BasicMultipleRulesBuilder
from typing import Any, List


class UsersRule(BasicRule):

    def __init__(self, usernames: List[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.usernames = usernames

    def build(self) -> tweepy.StreamRule:
        """The last method to call to Build the rule"""
        query = ""
        _usernames = self.usernames.copy()
        for username in _usernames:
            self.usernames.remove(username)

            if len(username) + len(query) + len(self.non_negated_query) + len(self.negated_query) >= self.max_query_len:
                break

            query = f"{query} OR from:{username}".strip()

        if query.startswith("OR"):
            query = query.replace("OR", "", 1).strip()

        final_query = ""
        if self.negated_query.strip() != "" or self.non_negated_query.strip() != "":
            final_query = f"{self.non_negated_query} ({query}) {self.negated_query}"
        else:
            final_query = query

        return tweepy.StreamRule(final_query)


class MultipleUsersRulesBuilder(BasicMultipleRulesBuilder):

    def _get_basic_rule(self) -> UsersRule:
        return UsersRule(self.targets)
