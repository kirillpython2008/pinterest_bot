import re
from urllib.parse import urlparse

async def is_link(link: str):
    """
        Проверяет, является ли ссылка валидной ссылкой Pinterest (фото/видео)
        Поддерживает форматы:
        - https://www.pinterest.com/pin/123456/
        - https://ru.pinterest.com/pin/123456/
        - https://pin.it/abc123
        - https://www.pinterest.com/username/board-name-123456/
        """
    try:
        parsed = urlparse(link)

        # Базовые проверки URL
        if not all([parsed.scheme in ('http', 'https'), parsed.netloc]):
            return False

        # Проверка всех возможных доменов Pinterest
        pinterest_domains = [
            'pinterest.com',
            'ru.pinterest.com',
            'www.pinterest.com',
            'pin.it'
        ]

        if not any(domain in parsed.netloc for domain in pinterest_domains):
            return False

        # Проверка пути для разных типов ссылок
        path = parsed.path.rstrip('/')

        # Паттерны для проверки
        patterns = [
            r'^/pin/\d+',  # /pin/123456
            r'^/[^/]+/[\w-]+-\d+',  # /username/board-name-123456
            r'^/[^/]+/[^/]+',  # /username/boardname
            r'^/[a-zA-Z0-9]+'  # Короткие ссылки pin.it/abc123
        ]

        return any(re.match(pattern, path) for pattern in patterns)

    except Exception:
        return False