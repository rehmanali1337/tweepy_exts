import tweepy

tweet_fields = ['id',
                'in_reply_to_user_id',
                'referenced_tweets',
                'context_annotations',
                'source',
                'created_at',
                'entities',
                'geo',
                'withheld',
                'public_metrics',
                'text',
                'author_id']


class QueryBuilder:

    @classmethod
    def tweets_from_user_query(self, username: str, remove_replies=False, remove_retweets=False, remove_quoted=False):
        query = f"from:{username}"
        if remove_retweets:
            query = f"{query} -is:retweet"

        if remove_replies:
            query = f"{query} -is:reply"

        if remove_quoted:
            query = f"{query} -is:quote"

        return f"({query})"

    @classmethod
    def tweets_from_users(self, usernames: str,
                          remove_replies=False,
                          remove_retweets=False,
                          remove_quoted=False):
        max_query_len = 510
        max_rules_allowed = 25
        rules = []
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

            if len(query) + len(user_query) > max_query_len and i+1 == len(usernames):
                # We are the max character allowed in query and the username is last one
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                query = user_query
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                return rules

            elif len(query) + len(user_query) > max_query_len and i+1 != len(usernames):
                # At max characters allowed in the query  and NOT the last username
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                query = user_query
                continue

            elif len(query) + len(user_query) < max_query_len and i+1 != len(usernames):
                # NOT at max allowed characters and NOT the last username.
                query = f"{query} OR {user_query}"
                continue

            elif len(query) + len(user_query) < max_query_len and i+1 == len(usernames):
                # Not at the max query len but last username
                query = f"{query} OR {user_query}"
                rule = tweepy.StreamRule(value=query.strip(), id=str(i))
                rules.append(rule)
                return rules

        return rules
