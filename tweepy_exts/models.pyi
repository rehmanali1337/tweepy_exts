from _typeshed import Incomplete
from typing import Any, Dict

class User:
    data: Incomplete
    id: Incomplete
    name: Incomplete
    username: Incomplete
    verified: Incomplete
    verified_type: Incomplete
    created_at: Incomplete
    description: Incomplete
    location: Incomplete
    pinned_tweet_id: Incomplete
    public_matrics: Incomplete
    followers_count: Incomplete
    following_count: Incomplete
    tweet_count: Incomplete
    listed_count: Incomplete
    def __init__(self, data: Dict[str, Any]) -> None: ...

class Media:
    data: Incomplete
    def __init__(self, data: Dict[str, Any]) -> None: ...

class Annotation:
    data: Incomplete
    start: Incomplete
    end: Incomplete
    probability: Incomplete
    type: Incomplete
    normalized_text: Incomplete
    def __init__(self, data: Dict[str, Any]) -> None: ...

class Image:
    data: Incomplete
    url: Incomplete
    width: Incomplete
    height: Incomplete
    def __init__(self, data: Dict[str, Any]) -> None: ...

class Url:
    data: Incomplete
    start: Incomplete
    end: Incomplete
    url: Incomplete
    expanded_url: Incomplete
    display_url: Incomplete
    images: Incomplete
    status: Incomplete
    title: Incomplete
    description: Incomplete
    unwound_url: Incomplete
    media_key: Incomplete
    def __init__(self, data: Dict[str, Any]) -> None: ...

class Tweet:
    full_data: Incomplete
    users: Incomplete
    tweets: Incomplete
    tweet_data: Incomplete
    id: Incomplete
    author_id: Incomplete
    author: Incomplete
    attachments: Incomplete
    created_at: Incomplete
    created_at_dt: Incomplete
    edit_hisotry_tweet_ids: Incomplete
    public_matrics: Incomplete
    retweet_count: Incomplete
    reply_count: Incomplete
    like_count: Incomplete
    impression_count: Incomplete
    quote_count: Incomplete
    referenced_tweets: Incomplete
    text: Incomplete
    entities: Incomplete
    annotations: Incomplete
    hashtags: Incomplete
    mentions: Incomplete
    urls: Incomplete
    geo: Incomplete
    is_retweet: bool
    def __init__(self, data: dict[str, Any], from_alt: bool = ...) -> None: ...
    @property
    def url(self) -> str: ...
    def fix_text(self) -> None: ...
