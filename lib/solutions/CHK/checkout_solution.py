

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


def _is_basket_valid(products_in_basket_sku_list):
    for sku in products_in_basket_sku_list:
        if sku not in PRICE_LIST:
            return False
    return True


def _calculate_total_price(products_in_basket_sku_list):
    number_of_each_item = {sku: 0 for sku in PRICE_LIST}
    for sku in products_in_basket_sku_list:
        number_of_each_item[sku] += 1

    # check special offers
    number_of_a_discounts = int(number_of_each_item['A'] / 3)
    number_of_b_discounts = int(number_of_each_item['B'] / 2)

    basket_sub_total = sum([PRICE_LIST[sku]
                           for sku in products_in_basket_sku_list])

    basket_total_post_discounts = basket_sub_total - \
        (number_of_a_discounts * 20) - (number_of_b_discounts * 15)

    return basket_total_post_discounts


def checkout(skus: str) -> int:
    if not skus:
        return -1

    # SKUs come in as a simple list of chars, no seperator
    products_in_basket_sku_list = list(skus)

    basket_valid = _is_basket_valid(products_in_basket_sku_list)
    # TODO fallback plan if not comma seperated
    # countA = skus.count("A")
    # countB = skus.count("B")
    # countC = skus.count("C")
    # countD = skus.count("D")

    if basket_valid:
        return _calculate_total_price(products_in_basket_sku_list)
    else:
        return -1





