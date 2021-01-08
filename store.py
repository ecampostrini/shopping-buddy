import yaml
from collections import namedtuple, defaultdict
from units import BaseQuantity, optimizeQuantity


class Store:
  Item = namedtuple("StoreItem", "category availableQuantities measurementUnit")

  @classmethod
  def fromFile(cls, filename):
    with open(filename, "r") as stores:
      return {store_yaml["name"]: cls(store_yaml) for store_yaml in yaml.safe_load_all(stores)}

  def __init__(self, store_yaml):
    assert store_yaml["kind"] == "store"
    self.name = store_yaml["name"]
    self.targetItems = {}
    # TODO rename to availableItems
    self.items = {}
    for item in store_yaml["items"]:
      itemName = item["name"]

      if itemName in self.items:
        raise RuntimeError("Found repeated item in {} store: {}".format(self.name, itemName))

      self.items[itemName] = Store.Item(
          category=item["category"],
          availableQuantities=[
              BaseQuantity.fromText(quantity) for quantity in item.get("sold_in", [])
          ],
          # TODO validate/normalize unit
          measurementUnit=item.get("sold_by_the", "").lower())

      if self.items[itemName].availableQuantities and self.items[itemName].measurementUnit:
        raise RuntimeError(
            ("'{}' in '{}' store is misconfigured: only one of 'sold_in' or 'sold_by_the' "
             "can be specified").format(itemName, self.name))

  def __repr__(self):
    return "Store {}: {}".format(self.name, repr(self.items))

  def __iter__(self):
    self.iterator = iter(self.targetItems.items())
    return self

  def __next__(self):
    return next(self.iterator)

  def addItem(self, name, quantity):
    if name in self.targetItems:
      self.targetItems[name] = self.targetItems[name] + quantity
    else:
      self.targetItems[name] = quantity

  def getCart(self):
    cart = {}
    for itemName, quantity in self.targetItems.items():
      if len(self.items[itemName].availableQuantities):
        minQuantity, minCombination = optimizeQuantity(quantity,
                                                       self.items[itemName].availableQuantities)
        count = defaultdict(int)
        for quantity in minCombination:
          count[str(quantity)] += 1
        cart[itemName] = ", ".join(["{} x {}".format(k, v) for k, v in count.items()])
      elif len(self.items[itemName].measurementUnit):
        # TODO enable lookup of class by name of measurement unit and perform this check
        # properly, i.e.:
        # if type(quantity).__name__ not in lookupQuantity(self.items[itemName].measurementUnit).aliases:
        if self.items[itemName].measurementUnit not in type(quantity).aliases:
          raise RuntimeError("{} quantity must be expressed in {}".format(
              itemName,
              type(quantity).__name__))
        # TODO format quantity
        cart[itemName] = repr(quantity)
      else:
        cart[itemName] = repr(quantity)
    return cart
