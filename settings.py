import re

from rich.theme import Theme

console_theme = Theme({
    "info": "cyan",
    "warning": "magenta",
    "danger": "bold red"
})

requests_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

news_outlets = [
    {
        'name': '15min',
        'url': 'https://www.15min.lt',
        'url_root': 'https://www.15min.lt',
        'all_articles': {
            'tag': 'article',
            'class': 'item',
            'single_article_info': {
                'tag': 'h4',
                'class': 'vl-title'
            },
        },
        'article': [
            {
                'tag': 'div',
                'attributes': {'class': 'text'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': 'text-wrapper'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            }
        ],
    },
    {
        'name': 'Delfi',
        'url': 'https://www.delfi.lt',
        'url_root': 'https://www.delfi.lt',
        'all_articles': {
            'tag': 'div',
            'class': 'headline',
            'single_article_info': {
                'tag': 'h3',
                'class': 'headline-title'
            },
        },
        'article': [
            {
                'tag': 'div',
                'attributes': {'class': 'col-xs-8'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': 'video-article-body'},
                'paragraph': {
                    'tag': 'div',
                    'attributes': {'class': 'video-article-lead'},
                    'recursive': False
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': 'article-body'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': 'article-teaser'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': 'col-xs-12'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            }
        ],
    },
    {
        'name': 'LRytas',
        'url': 'https://www.lrytas.lt',
        'url_root': 'https://www.lrytas.lt',
        'all_articles': {
            'tag': 'article',
            'class': 'LPost',
            'single_article_info': {
                'tag': 'h2',
                'class': 'LPostContent__title'
            },
        },
        'article': [
            {
                'tag': 'div',
                'attributes': {'class': 'LArticleText'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': re.compile('LArticleParagraph')},
                    'recursive': True
                }
            },
        ],
    },
    {
        'name': 'BBC',
        'url': 'https://www.bbc.com/news',
        'url_root': 'https://www.bbc.com',
        'all_articles': {
            'tag': 'div',
            'class': 'gs-c-promo-body',
            'single_article_info': {
                'tag': 'div',
                'class': None
            },
        },
        'article': [
            {
                'tag': 'div',
                'attributes': {'class': 'story-body'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'data-reactid': re.compile('paragraph')},
                    'recursive': True
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': 'body-text-card'},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': None},
                    'recursive': True
                }
            },
            {
                'tag': 'div',
                'attributes': {'class': None},
                'paragraph': {
                    'tag': 'p',
                    'attributes': {'class': re.compile('Paragraph')},
                    'recursive': True
                }
            },
        ],
    }
]
