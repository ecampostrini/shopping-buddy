# Shopping buddy
Shoping buddy takes as input a list of items you need from the grocery shop and turns it into a Trello card where each item is a `checkitem` inside a `checklist`,
allowing you to create a fresh and easy to read Trello card for every grocery shopping you have to do, ready to be shared with family or friends and ease the
grocery shop organization.

# Usage
1. Create a `yaml` file containing the `stores` where you get the groceries from:
```yaml
kind: store
name: lidl
items:
  - name: queso parmesano
    category: diary
    sold_in:
      - 250 grams unit

  - name: hasselnuts
    category: grains
    sold_by_the: bag

  - name: peras sueltas
    category: fruits and vegetables
    sold_by_the: unit

```

2. Create a `yaml` file containing the list of the groceries you need:
```yaml
kind: shopping_list
name: compras para la semana
store: lidl
items:
  - name: queso parmesano
    quantity: 150 grams
    
  - name: hasselnuts
    quantity: 2 bags
```

3. Create a `config.ini` file with the required `Trello` config:
```ini
[TRELLO]
api_key=<Trello api key>
server_token=<Trello server token>
base_api_url=https://api.trello.com/1/
# Name of the board where you want the shopping list card to be created
board_name=compras 
# Name of the list within the board where you want the shopping list to be created
list_name=Por hacer
```

4. Run the script setting the environment variables `STORES_PATH` and `SHOPPING_LIST_PATH` to the files created in points `1` and `2`. Assuming these are
called `stores.yaml` and `shopping_list.yaml` this would look like:
```bash
STORES_PATH=stores.yaml SHOPPING_LIST_PATH=shopping_list.yaml python main.py
```

5. Check the `board` in Trello, the new card containing the checklist should be there.
