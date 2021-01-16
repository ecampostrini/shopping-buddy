#!/usr/bin/env python3

import yaml
from collections import namedtuple, defaultdict
import os
import re
import argparse

from trello import TrelloClient
from config import STORES_PATH, SHOPPING_LIST_PATH
from store import Store
from shopping_list import ShoppingList


def main():
  parser = argparse.ArgumentParser(
      description="A minimalist grocery shopping organizer that creates Trello cards based " +
      "on shopping lists")
  parser.add_argument(
      "--stores",
      "-s",
      dest="stores",
      nargs="+",
      help="Space separated paths to the files containing the stores",
      required=True)
  parser.add_argument(
      "--lists",
      "-l",
      dest="shoppingLists",
      action="append",
      help="Space separated paths to the target shopping lists",
      required=True)
  args = parser.parse_args()

  stores = {}
  for storePath in args.stores:
    stores.update(Store.fromFile(storePath))

  # TODO support per-item store
  for shoppingListPath in args.shoppingLists:
    shoppingList = ShoppingList.fromFile(shoppingListPath)
    for itemName, quantity in shoppingList:
      stores[shoppingList.store].addItem(itemName, quantity)

  # shoppingList = ShoppingList.fromFile(args.shoppingLists[0])
  # # print("{}".format(shoppingList))
  # currenStore = stores[shoppingList.store]

  # for itemName, quantity in shoppingList:
  # currenStore.addItem(itemName, quantity)

  # print("Shopping list: ")
  # for item, qtty in currenStore:
  # print("{}: {}".format(item, qtty))

  # print("=======")

  trelloClient = TrelloClient()
  for storeName, store in stores.items():
    if not len(store.targetItems):
      # Don't create cards for stores that have no items
      continue

    cardId = trelloClient.createCard(storeName)
    checklistId = trelloClient.createChecklist(cardId, "Cosas a traer")
    trelloClient.addItemsToChecklist(
        checklistId,
        ["{}: {}".format(k, v) for k, v in store.getCart().items()],
    )


if __name__ == "__main__":
  main()
