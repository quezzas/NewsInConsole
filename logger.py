import logging

logging.basicConfig(filename='main.log', filemode='a',
                    format='[%(asctime)s] [%(levelname)s] %(name)s %(message)s', level=logging.DEBUG)

app_logger = logging.getLogger('NewsInConsole')

