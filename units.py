from collections import namedtuple
import re

Quantity = namedtuple(
    "Quantity", ["quantity", "unit", "containerName"], defaults=(None, None, None))


def convertQuantity(mappingDict, toUnit, quantity):
  fromFactor = mappingDict[quantity.unit]
  toFactor = mappingDict[toUnit]

  return Quantity(quantity.quantity * fromFactor / toFactor, toUnit, quantity.containerName)


class BaseQuantity(object):

  @classmethod
  def fromText(cls, rawQuantity):
    for subclass in cls.__subclasses__():
      match = subclass.formatRegex.match(rawQuantity)
      if match:
        return subclass(*match.groups())
    else:
      raise RuntimeError(
          "BaseQuantity.fromText called with invalid arguments: {}".format(rawQuantity))

  def __init__(self, amount, unit, containerName=None):
    pass

  def __repr__(self):
    originalQuantity = self.originalQuantity
    return " ".join([
        ("%f" % originalQuantity.quantity).rstrip("0").rstrip("."),
        originalQuantity.unit,
        originalQuantity.containerName or "",
    ]).strip()

  def __add__(self, other):
    myQuantity, myUnit, _ = self.normalizedQuantity
    theirQuantity, theirUnit, _ = other.normalizedQuantity
    cls = type(self)

    assert type(myUnit) == type(
        theirUnit), "Tried to sum elements of mismatching types {}: {} vs {}".format(
            cls.__name__, myUnit, theirUnit)

    return cls(myQuantity + theirQuantity, myUnit)

  def __sub__(self, other):
    myQuantity, myUnit, _ = self.normalizedQuantity
    theirQuantity, theirUnit, _ = other.normalizedQuantity
    cls = type(self)

    assert type(myUnit) == type(theirUnit), "Mismatching units during substraction of {}!".format(
        cls.__name__)

    return cls(myQuantity - theirQuantity, myUnit)

  def __le__(self, other):
    # TODO implement a better version of these comparissons
    return self.normalizedQuantity.quantity <= other

  def __lt__(self, other):
    # TODO implement a better version of these comparissons
    return self.normalizedQuantity.quantity < other

  def __gt__(self, other):
    # TODO implement a better version of these comparissons
    return self.normalizedQuantity.quantity > other

  def __ge__(self, other):
    # TODO implement a better version of these comparissons
    return self.normalizedQuantity.quantity >= other


class Kilograms(BaseQuantity):
  conversionTable = {
      "grams": 0.001,
      "kilos": 1,
  }

  unitMappings = {
      "grams": set(["grams", "gm", "gms"]),
      "kilos": set(["kilo", "kilos", "kilogram", "kilograms", "kg", "kgs"]),
  }

  aliases = [alias for mapping in unitMappings.values() for alias in mapping]

  formatRegex = re.compile("([0-9][0-9]*(?:.[0-9]+)?)\s*({})(?:\s+(\w+(?:\s+\w+)*))?".format(
      "|".join([val for subset in unitMappings.values() for val in subset])))

  @staticmethod
  def toNormalUnit(unit, isPlural=False):
    if unit in Kilograms.unitMappings["grams"]:
      return "grams"
    elif unit in Kilograms.unitMappings["kilos"]:
      return "kilos"

    raise RuntimeError("Invalid unit ({}). This should've been caught earlier".format(unit))

  def __init__(self, qtty, unit="grams", containerName=None):
    self.originalQuantity = Quantity(
        float(qtty), Kilograms.toNormalUnit(unit,
                                            float(qtty) > 1), containerName)
    # Internally handle everything as grams
    self.normalizedQuantity = convertQuantity(Kilograms.conversionTable, "grams",
                                              self.originalQuantity)


class Units(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(units?)(?:\s+(\w+(?:\s+\w+)*))?")

  aliases = ["unit", "units"]

  def __init__(self, qtty, unit="units", containerName=None):
    self.originalQuantity = Quantity(float(qtty), unit, containerName)
    self.normalizedQuantity = self.originalQuantity


class Pots(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(pots?)")

  aliases = ["pot", "pots"]

  def __init__(self, qtty, unit="pots"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity


class Bags(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(bags?)")

  aliases = ["bag", "bags"]

  def __init__(self, qtty, unit="bags"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity


class Pack(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(packs?)")

  aliases = ["pack", "packs"]

  def __init__(self, qtty, unit="packs"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity


class Bottle(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(bottles?)")

  aliases = ["bottle", "bottles"]

  def __init__(self, qtty, unit="bottles"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity


class Box(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(box(?:es)?)")

  aliases = ["box", "boxes"]

  def __init__(self, qtty, unit="boxes"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity


class Jar(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(jar(?:s)?)")

  aliases = ["jar", "jars"]

  def __init__(self, qtty, unit="jars"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity

class Bundle(BaseQuantity):
  formatRegex = re.compile("([0-9][0-9]*)\s(bundle(?:s)?)")

  aliases = ["bundle", "bundles"]

  def __init__(self, qtty, unit="bundle"):
    self.originalQuantity = Quantity(float(qtty), unit)
    self.normalizedQuantity = self.originalQuantity

availableUnits = [subclass.__name__.lower() for subclass in BaseQuantity.__subclasses__()]


def optimizeQuantity(targetQuantity, availableQuantities):
  minQuantity = type(targetQuantity)(9999999)
  minCombination = []
  for quantity in availableQuantities:
    if targetQuantity <= quantity:
      minQtty = type(targetQuantity)(0)
      minComb = []
    else:
      minQtty, minComb = optimizeQuantity(targetQuantity - quantity, availableQuantities)

    if minQuantity >= minQtty + quantity:
      minQuantity = minQtty + quantity
      minCombination = minComb
      minCombination.append(quantity)

  return minQuantity, minCombination
