import configparser
from os import getenv

config = configparser.ConfigParser()
config.read(getenv("CONFIG_FILE_PATH", "config.ini"))

TRELLO_API_KEY = getenv("TRELLO_API_KEY", config["TRELLO"]["api_key"])

TRELLO_SERVER_TOKEN = getenv("TRELLO_SERVER_TOKEN", config["TRELLO"]["server_token"])

TRELLO_BASE_API_URL = getenv("TRELLO_BASE_API_URL", config["TRELLO"]["base_api_url"])

TRELLO_BOARD_NAME = getenv("TRELLO_BOARD_NAME", config["TRELLO"]["board_name"])

TRELLO_LIST_NAME = getenv("TRELLO_LIST_NAME", config["TRELLO"]["list_name"])

STORES_PATH = getenv("STORES_PATH", "stores.yaml")

SHOPPING_LIST_PATH = getenv("SHOPPING_LIST_PATH", "shopping_lists.yaml")
