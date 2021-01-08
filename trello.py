import requests
from config import (
    TRELLO_API_KEY,
    TRELLO_SERVER_TOKEN,
    TRELLO_BASE_API_URL,
    TRELLO_BOARD_NAME,
    TRELLO_LIST_NAME,
)


class TrelloClient:

  def __init__(self):
    self.auth = {"key": TRELLO_API_KEY, "token": TRELLO_SERVER_TOKEN}

    print("Retrieving ID for board {}...".format(TRELLO_BOARD_NAME))
    boards = requests.request("GET", TRELLO_BASE_API_URL + "/members/me/boards", params=self.auth)

    self.boardId = next(
        (board["id"] for board in boards.json() if board["name"] == TRELLO_BOARD_NAME),
        None,
    )

    if not self.boardId:
      print("Couldn't find a board with the name {}. Will create it".format(TRELLO_BOARD_NAME))
      # TODO create the board and the lists
      self.boardId = self.createBoard(TRELLO_BOARD_NAME)
      self.listId = self.createList(self.boardId, TRELLO_LIST_NAME)
    else:
      print("Done:", self.boardId)
      print("Retrieving ID for list {}...".format(TRELLO_LIST_NAME))
      lists = requests.request(
          "GET",
          TRELLO_BASE_API_URL + "/boards/" + self.boardId + "/lists",
          params=self.auth,
      )

      self.listId = next(
          (lista["id"] for lista in lists.json() if lista["name"] == TRELLO_LIST_NAME),
          None,
      )

      if not self.listId:
        print(
            "Couldn't find a list with the name {}. Will create it".format(TRELLO_TODO_LIST_NAME))
        self.listId = self.createList(self.boardId, TRELLO_LIST_NAME)
      else:
        print("Done:", self.listId)

  def createBoard(self, boardName):
    # TODO implement
    pass

  def createList(self, boardId, listName):
    # TODO implement
    pass

  def createCard(self, cardName):
    """ Create a new card on a board's list """
    url = TRELLO_BASE_API_URL + "/cards"
    query = self.auth.copy()
    query["idList"] = self.listId
    query["name"] = cardName

    response = requests.request("POST", url, params=query)
    response.raise_for_status()

    return response.json()["id"]

  def createChecklist(self, cardId, checklistName):
    """ Create a new check list inside a card"""
    url = TRELLO_BASE_API_URL + "/checklists"

    query = self.auth.copy()
    query["idCard"] = cardId
    query["name"] = checklistName
    query["pos"] = "bottom"

    response = requests.request("POST", url, params=query)
    response.raise_for_status()

    return response.json()["id"]

  def addItemsToChecklist(self, checklistId, items=[]):
    """ Add items to a given checklist """
    url = TRELLO_BASE_API_URL + "/".join(["checklists", checklistId, "checkitems"])

    query = self.auth.copy()
    for item in items:
      query["name"] = item
      response = requests.request("POST", url, params=query)
      response.raise_for_status()
      print("Response: {}".format(response.text))


if __name__ == "__main__":
  trelloClient = TrelloClient()

  print("Creating a card: ")
  cardId = trelloClient.createCard("Test card")
  print("CardId:", cardId)

  print("Creating check list: ")
  checklistId = trelloClient.createChecklist(cardId, "Test checklist!")
  print(checklistId)

  print("Adding items to the checklist: ")
  trelloClient.addItemsToChecklist(checklistId, [str(i) for i in range(10)])
