

# noinspection PyUnusedLocal
# skus = unicode string

# TODO
# total price of a number of items
# things are identified using Stock Keeping Units, or SKUs
# some items are multi-priced: buy n of them, and they'll cost you y pounds

# Our price table and offers:
# +------+-------+------------------------+
# | Item | Price | Special offers         |
# +------+-------+------------------------+
# | A    | 50    | 3A for 130, 5A for 200 |
# | B    | 30    | 2B for 45              |
# | C    | 20    |                        |
# | D    | 15    |                        |
# | E    | 40    | 2E get one B free      |
# | F    | 10    | 2F get one F free      |
# | G    | 20    |                        | <---- new starting here
# | H    | 10    | 5H for 45, 10H for 80  |
# | I    | 35    |                        |
# | J    | 60    |                        |
# | K    | 80    | 2K for 150             |
# | L    | 90    |                        |
# | M    | 15    |                        |
# | N    | 40    | 3N get one M free      |
# | O    | 10    |                        |
# | P    | 50    | 5P for 200             |
# | Q    | 30    | 3Q for 80              |
# | R    | 50    | 3R get one Q free      |
# | S    | 30    |                        |
# | T    | 20    |                        |
# | U    | 40    | 3U get one U free      |
# | V    | 50    | 2V for 90, 3V for 130  |
# | W    | 20    |                        |
# | X    | 90    |                        |
# | Y    | 10    |                        |
# | Z    | 50    |                        |
# +------+-------+------------------------+

# TODO convert to (data)class if requirements change
PRICE_LIST = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
}


def _is_basket_valid(products_in_basket_sku_list):
    for sku in products_in_basket_sku_list:
        if sku not in PRICE_LIST:
            return False
    return True


def same_product_multibuy_discount():


def _calculate_total_price(products_in_basket_sku_list):
    number_of_each_item = {sku: 0 for sku in PRICE_LIST}
    for sku in products_in_basket_sku_list:
        number_of_each_item[sku] += 1

    # check special offers
    number_of_5a_discounts, a_remainder = divmod(number_of_each_item['A'], 5)
    number_of_3a_discounts = int(a_remainder / 3)
    potential_number_of_free_b_products = int(number_of_each_item['E'] / 2)

    temp_b_count = number_of_each_item['B']
    temp_b_count -= potential_number_of_free_b_products

    if temp_b_count < 0:
        potential_number_of_free_b_products = 0

    number_of_b_discounts = int(temp_b_count / 2)

    number_of_f_free = int(number_of_each_item['F'] / 3)

    basket_sub_total = sum([PRICE_LIST[sku]
                           for sku in products_in_basket_sku_list])

    basket_total_post_discounts = basket_sub_total - (number_of_5a_discounts * 50) - (number_of_3a_discounts * 20) - (
        number_of_b_discounts * 15) - (potential_number_of_free_b_products * 30) - (number_of_f_free * 10)

    return basket_total_post_discounts


def checkout(skus: str) -> int:

    if not skus:
        # empty basket, total cost is 0
        return 0

    # SKUs come in as a simple list of chars, no seperator
    products_in_basket_sku_list = list(skus)

    basket_valid = _is_basket_valid(products_in_basket_sku_list)

    if basket_valid:
        return _calculate_total_price(products_in_basket_sku_list)
    else:
        return -1

