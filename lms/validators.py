from urllib.parse import urlparse
from rest_framework import serializers


def validate_youtube_url(value):
    allowed_hosts = (
        'youtube.com',
        'www.youtube.com',
        'm.youtube.com',
        'youtu.be',
    )
    host = urlparse(value).netloc.lower()

    if host not in allowed_hosts:
        raise serializers.ValidationError(
            'Ссылки на сторонние ресурсы запрещены. Разрешён только youtube.com'
        )

    return value
