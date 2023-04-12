import tweepy
from .basc_rule import BasicMultipleRulesBuilder as BasicMultipleRulesBuilder, BasicRule as BasicRule
from _typeshed import Incomplete
from typing import Any, List


class UsersRule(BasicRule):
    usernames: Incomplete
    def __init__(self, usernames: List[str], **kwargs: Any) -> None: ...
    def build(self) -> tweepy.StreamRule: ...


class MultipleUsersRulesBuilder(BasicMultipleRulesBuilder):
    ...
