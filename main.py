from rich.console import Console
from bs4 import BeautifulSoup
from logger import app_logger
import settings
import requests
import re
import os


console = Console(width=100, theme=settings.console_theme)


def print_header(text):
    os.system('cls||clear')
    console.rule(f'[bold red1]-=ㅇ {text} ㅇ=-[/]')
    console.print('\n')


def add_choice(function_name: str, max_index: int = None):
    while True:
        try:
            console.print('\n')
            if function_name == 'start_window':
                choice = console.input(f'\n[bold]Choose news outlet (or [info]exit[/]): [/]').strip()
                if choice.lower() in ['exit', 'e', 'back', 'b', 'main', 'm']:
                    return choice
                else:
                    choice = int(choice)

            elif function_name == 'all_articles_window':
                choice = console.input(f'\n[bold]Choose article to read ([info]back/exit[/]): [/]').strip()
                if choice.lower() in ['exit', 'e', 'back', 'b']:
                    return choice
                else:
                    choice = int(choice)

            elif function_name == 'article_window':
                while True:
                    choice = console.input(f'\n[bold]What to do next? ([info]main/back/exit[/]): [/]').strip()
                    if choice.lower() not in ['exit', 'e', 'back', 'b', 'main', 'm']:
                        console.print('[danger]You cant choose from main(m), back(b), exit(e).[/]')
                        continue
                    else:
                        return choice

        except ValueError:
            console.print('[danger]Input value should be integer.[/]')
            app_logger.debug(f'ValueError in choice for {function_name}, input {choice}')
            continue
        if max_index and choice > max_index:
            console.print('[danger]Not an appropriate choice.[/]')
            continue
        else:
            return choice


def read_available_news_outlets():
    outlets = []
    for index, outlet in enumerate(settings.news_outlets):
        outlets.append({'index': index, 'name': outlet['name']})

    return outlets


def article_window(outlet_configurations, article_info):
    print_header(outlet_configurations['name'])
    with console.status('Loading ', spinner='aesthetic'):
        try:
            result = requests.get(article_info['url'], headers=settings.requests_header)
        except requests.exceptions.RequestException as e:
            app_logger.exception(f'Exception raised while sending request to {article_info["url"]}, {e}')
            raise

        if not result.status_code == requests.codes.ok:
            console.print(f'[warning]Couldn\'t reach the article, status code: {result.status_code}[/]')
            app_logger.exception(f'Couldn\'t reach the article, status code: {result.status_code}, '
                                 f'URL: {article_info["url"]}')
            raise

        soup = BeautifulSoup(result.text, 'html.parser')

        for index in range(len(outlet_configurations['article'])):
            article_text = soup.find(
                outlet_configurations['article'][index]['tag'],
                attrs=outlet_configurations['article'][index]['attributes']
            )
            if article_text:
                article_paragraphs = article_text.find_all(
                    outlet_configurations['article'][index]['paragraph']['tag'],
                    attrs=outlet_configurations['article'][index]['paragraph']['attributes'],
                    recursive=outlet_configurations['article'][index]['paragraph']['recursive']
                )

                break
        else:
            console.print(f'[warning]Error while parsing article, check logs[/]')
            app_logger.exception(f'Error while parsing article in article_window, article_info: {article_info}')
            raise

        printable_article = '\n'.join([paragraph.text for paragraph in article_paragraphs])

    console.print(f'[bold purple]{article_info["title"]}[/]')
    console.print('\n', printable_article)

    choice = add_choice('article_window')

    if choice in ['exit', 'e']:
        return
    elif choice in ['back', 'b']:
        all_articles_window(None, outlet_configurations)
    elif choice in ['main', 'm']:
        start_window()


def all_articles_window(index, outlet_configurations=None):
    if not outlet_configurations:
        outlet_configurations = settings.news_outlets[index]

    print_header(outlet_configurations['name'])

    articles_info = []
    with console.status('Loading ', spinner='aesthetic'):
        try:
            result = requests.get(outlet_configurations['url'], headers=settings.requests_header)
        except requests.exceptions.RequestException as e:
            app_logger.exception(f'Exception raised while sending request to {outlet_configurations["url"]}, {e}')
            raise

        if not result.status_code == requests.codes.ok:
            console.print(f'[warning]Couldn\'t reach the website, status code: {result.status_code}[/]')
            app_logger.exception(f'Couldn\'t reach the website, status code: {result.status_code}, '
                                 f'URL: {outlet_configurations["url"]}')
            raise

        soup = BeautifulSoup(result.text, 'html.parser')

        all_articles = soup.find_all(
            outlet_configurations['all_articles']['tag'],
            class_=outlet_configurations['all_articles']['class'],
            limit=100
        )

        article_index = 0
        for article in all_articles:
            if article_index >= 50:
                # Show only 50 newest stories
                break
            try:
                try:
                    article_title = article.find(
                        outlet_configurations['all_articles']['single_article_info']['tag'],
                        class_=outlet_configurations['all_articles']['single_article_info']['class']
                    ).find('a').text.replace('\n', '').replace('\t', '').strip()
                except AttributeError:
                    app_logger.info(f'Couldn\'t parse article title, article: {article}')
                    continue

                article_url = article.find('a', attrs={'href': re.compile("^.+")}).get('href')

                if not (article_url.startswith('https') or article_url.startswith('http')):
                    article_url = outlet_configurations['url_root'] + article_url

                if 'comments/' in article_url:
                    article_url = article_url.replace('comments/', '')

                if articles_info and any([arti['url'] == article_url for arti in articles_info]):
                    #If article already exists do not include it in list
                    continue

                articles_info.append({
                    'index': article_index,
                    'title': article_title,
                    'url': article_url,
                })
                article_index += 1

            except Exception:
                console.print(f'[warning]Error while parsing all articles, check logs[/]')
                app_logger.exception(f'Exception raised while parsing article_info, article data: {article}')
                raise

    for article_info in articles_info:
        console.print(f'[[red1]{article_info["index"]}[/]]\t{article_info["title"]}')

    console.print('[info]Only first 50 shown.[/]')
    choice = add_choice('all_articles_window', len(articles_info) - 1)

    if choice in ['exit', 'e']:
        return
    elif choice in ['back', 'b', 'main', 'm']:
        start_window()
    else:
        article_window(outlet_configurations, articles_info[choice])


def start_window():
    app_logger.info('NewsInConsole app started')

    try:
        print_header('News In Console')
        outlets = read_available_news_outlets()
        for outlet in outlets:
            console.print(f'[[red1]{outlet["index"]}[/]]\t{outlet["name"]}')
        choice = add_choice('start_window', len(outlets) - 1)

        if choice in ['exit', 'e']:
            return

        all_articles_window(choice)
    except Exception as e:
        app_logger.exception(e)
    finally:
        app_logger.info('NewsInConsole app finished')


if __name__ == '__main__':
    start_window()
