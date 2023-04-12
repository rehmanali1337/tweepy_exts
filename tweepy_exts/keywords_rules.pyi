import tweepy
import typing
from .basc_rule import BasicMultipleRulesBuilder as BasicMultipleRulesBuilder, BasicRule as BasicRule
from _typeshed import Incomplete
from typing import Any

class KeywordRule(BasicRule):
    keywords: Incomplete
    def __init__(self, keywords: typing.List[str], **kwargs: Any) -> None: ...
    def build(self) -> tweepy.StreamRule: ...

class MultipleKeywordRulesBuilder(BasicMultipleRulesBuilder): ...
