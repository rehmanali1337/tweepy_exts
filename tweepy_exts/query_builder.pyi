import tweepy
from typing import List


class QueryBuilder:
    @classmethod
    def tweets_from_user_query(self, username: str, remove_replies: bool = ...,
                               remove_retweets: bool = ..., remove_quoted: bool = ...) -> str: ...

    @classmethod
    def tweets_from_users(self, usernames: List[str],
                          remove_replies: bool = ..., remove_retweets: bool = ..., remove_quoted: bool = ...,
                          max_query_len: int = ..., max_rules_allowed: int = ...) -> List[tweepy.StreamRule]: ...

    @classmethod
    def track_keywords(self, keywords_list: List[str], max_query_len: int = ...,
                       max_rules_allowed: int = ...) -> List[tweepy.StreamRule]: ...


RulesBuilder = QueryBuilder
