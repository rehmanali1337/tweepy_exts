

class BasicRule:

    def __init__(self,
                 max_query_len: int = 510,
                 *args, **kwargs) -> None:
        self.max_query_len = max_query_len
        self.query = ""

    def _add_operator(self, operator: str, negated=False):
        if negated:
            operator = f"-{operator}"
        self.query = f"{self.query} {operator}".strip()

    def has_links(self, negated=False):
        return self._add_operator("has:links", negated=negated)

    def has_media(self, negated=False):
        return self._add_operator("has:media", negated=negated)

    def has_images(self, negated=False):
        return self._add_operator("has:images", negated=negated)

    def is_reply(self, negated=False):
        return self._add_operator("is:reply", negated=negated)

    def is_retweet(self, negated=False):
        return self._add_operator("is:retweet", negated=negated)

    def is_quote(self, negated=False):
        return self._add_operator("is:quote", negated=negated)

    def is_verified(self, negated=False):
        return self._add_operator("is:verified", negated=negated)

    def has_mentions(self, negated=False):
        return self._add_operator("has:mentions", negated=negated)

    def has_video_link(self, negated=False):
        return self._add_operator("has:video_link", negated=negated)

    def has_geo(self, negated=False):
        return self._add_operator("has:geo", negated=negated)

    def lang(self, lang: str):
        return self._add_operator(f"lang:{lang}", negated=False)

    def has_hashtags(self, negated=False):
        return self._add_operator("has:hashtags", negated=negated)
