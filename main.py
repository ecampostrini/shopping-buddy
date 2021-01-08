from collections import namedtuple, defaultdict
import yaml
import os
import re

from trello import TrelloClient
from config import STORES_PATH, SHOPPING_LIST_PATH
from store import Store
from shopping_list import ShoppingList


def main():
  stores = Store.fromFile(STORES_PATH)
  # print("Stores:\n{}".format(stores))
  shopping_list = ShoppingList.fromFile(SHOPPING_LIST_PATH)
  # print("{}".format(shopping_list))
  currenStore = stores[shopping_list.store]

  for itemName, quantity in shopping_list:
    currenStore.addItem(itemName, quantity)

  print("Shopping list: ")
  for item, qtty in currenStore:
    print("{}: {}".format(item, qtty))

  print("=======")

  trelloClient = TrelloClient()
  cardId = trelloClient.createCard(currenStore.name)
  checklistId = trelloClient.createChecklist(cardId, shopping_list.name)
  trelloClient.addItemsToChecklist(
      checklistId,
      ["{}: {}".format(k, v) for k, v in currenStore.getCart().items()],
  )


if __name__ == "__main__":
  main()
