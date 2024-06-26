

# noinspection PyUnusedLocal
# skus = unicode string

# TODO
# total price of a number of items
# things are identified using Stock Keeping Units, or SKUs
# some items are multi-priced: buy n of them, and they'll cost you y pounds

# Our price table and offers:
# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+

# TODO convert to (data)class if requirements change
PRICE_LIST = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15
}

def checkout(skus: str) -> int:
    # assuming SKUs are comma seperated, won't know until run
    products_in_basket_sku_list = skus.split(",")
    return sum([PRICE_LIST[x] for x in products_in_basket_sku_list])






