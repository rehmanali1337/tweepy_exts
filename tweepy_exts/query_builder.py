import tweepy
from typing import List


class QueryBuilder:

    @classmethod
    def tweets_from_user_query(self, username: str, remove_replies: bool = False, remove_retweets: bool = False,
                               remove_quoted: bool = False) -> str:
        query = f"from:{username}"
        if remove_retweets:
            query = f"{query} -is:retweet"

        if remove_replies:
            query = f"{query} -is:reply"

        if remove_quoted:
            query = f"{query} -is:quote"

        return f"({query})"

    @classmethod
    def tweets_from_users(self, usernames: List[str],
                          remove_replies: bool = False,
                          remove_retweets: bool = False,
                          remove_quoted: bool = False,
                          max_query_len: int = 510,
                          max_rules_allowed: int = 25
                          ) -> List[tweepy.StreamRule]:
        rules: List[tweepy.StreamRule] = []
        query = ""
        for i, username in enumerate(usernames):
            if len(rules) == max_rules_allowed:
                # Maximum allowed rules created.
                break

            user_query = self.tweets_from_user_query(username=username,
                                                     remove_replies=remove_replies,
                                                     remove_quoted=remove_quoted,
                                                     remove_retweets=remove_retweets)

            if query == "" and len(usernames) == 1:
                # First username in the list and only username in the list.
                query = user_query
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                return rules

            elif query == "":
                # First username in the list
                query = user_query
                continue

            if len(query) + len(user_query) > max_query_len and i + 1 == len(usernames):
                # We are the max character allowed in query and the username is last one
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                query = user_query
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                return rules

            elif len(query) + len(user_query) > max_query_len and i + 1 != len(usernames):
                # At max characters allowed in the query  and NOT the last username
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                query = user_query
                continue

            elif len(query) + len(user_query) < max_query_len and i + 1 != len(usernames):
                # NOT at max allowed characters and NOT the last username.
                query = f"{query} OR {user_query}"
                continue

            elif len(query) + len(user_query) < max_query_len and i + 1 == len(usernames):
                # Not at the max query len but last username
                query = f"{query} OR {user_query}"
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                return rules

        return rules

    @classmethod
    def track_keywords(self, keywords_list: List[str],
                       max_query_len: int = 510,
                       max_rules_allowed: int = 25
                       ) -> List[tweepy.StreamRule]:
        rules = []
        query = ""
        for keyword in keywords_list:

            if query == "":
                query = f"{keyword}"

            else:
                if len(keyword) + len(query) >= max_query_len:
                    rules.append(tweepy.StreamRule(query))

                    if len(rules) == max_rules_allowed:
                        return rules

                    query = f"{keyword}"
                    continue
                query = f"{query} OR {keyword}"

        if query.strip() != "":
            rules.append(tweepy.StreamRule(query))

        return rules


RulesBuilder = QueryBuilder
