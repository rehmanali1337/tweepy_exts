
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
                "attachments",
                'author_id']
user_fields = [
    "created_at",
    "description",
    "entities",
    "username",
    "verified_type",
    "verified",
    "public_metrics",
    "url",
    "pinned_tweet_id",
    "location",
    "name",
    "id"
]

media_fields = [
    "duration_ms",
    "height",
    "media_key",
    "preview_image_url",
    "type",
    "url",
    "width",
    "public_metrics",
    "non_public_metrics",
    "organic_metrics",
    "promoted_metrics",
    "alt_text",
    "variants"
]

place_fields = [
    "contained_within",
    "country",
    "country_code",
    "full_name",
    "geo",
    "id",
    "name",
    "place_type"
]

expansions = [
    "referenced_tweets.id",
    "referenced_tweets.id.author_id",
    "geo.place_id",
    "attachments.media_keys",
    "in_reply_to_user_id",
    "entities.mentions.username",
    "attachments.poll_ids"
]
