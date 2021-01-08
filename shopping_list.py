import yaml
from collections import namedtuple

from units import BaseQuantity


class ShoppingList:
  Item = namedtuple("ShoppingListItem", "name quantity")

  @classmethod
  def fromFile(cls, filename):
    with open(filename, "r") as shopping_list:
      return cls(yaml.safe_load(shopping_list))

  def __init__(self, sl_yaml):
    assert sl_yaml["kind"] == "shopping_list"
    self.name = sl_yaml["name"]
    self.store = sl_yaml["store"]
    self.items = {}
    for item in sl_yaml["items"]:
      name = item["name"]
      # TODO add repeated items based on their store instead of complaining
      if name in self.items:
        self.items[name] = self.items[name] + BaseQuantity.fromText(item["quantity"])
      else:
        self.items[name] = BaseQuantity.fromText(item["quantity"])

  def __repr__(self):
    return "{}:\n{}\n".format(self.name, repr(self.items))

  def __iter__(self):
    self.iterator = iter(self.items.items())
    return self

  def __next__(self):
    return next(self.iterator)
