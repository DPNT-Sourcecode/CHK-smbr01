from dataclasses import dataclass
import pandas as pd
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
basket_discount_tracker = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0,
    "E": 0,
    "F": 0,
    "G": 0,
    "H": 0,
    "I": 0,
    "J": 0,
    "K": 0,
    "L": 0,
    "M": 0,
    "N": 0,
    "O": 0,
    "P": 0,
    "Q": 0,
    "R": 0,
    "S": 0,
    "T": 0,
    "U": 0,
    "V": 0,
    "W": 0,
    "X": 0,
    "Y": 0,
    "Z": 0,
}

ITEM_PRICE_DISCOUNT_LOOKUP = {
    "A": [50, "3A for 130, 5A for 200"],
    "B": [30, "2B for 45"],             
    "C": [20, ""],                      
    "D": [15, ""],                      
    "E": [40, "2E get one B free"],     
    "F": [10, "2F get one F free"],     
    "G": [20, ""],                      
    "H": [10, "5H for 45, 10H for 80"], 
    "I": [35, ""],                      
    "J": [60, ""],                      
    "K": [80, "2K for 150"],            
    "L": [90, ""],                      
    "M": [15, ""],                      
    "N": [40, "3N get one M free"],     
    "O": [10, ""],                      
    "P": [50, "5P for 200"],            
    "Q": [30, "3Q for 80"],             
    "R": [50, "3R get one Q free"],     
    "S": [30, ""],                      
    "T": [20, ""],                      
    "U": [40, "3U get one U free"],     
    "V": [50, "2V for 90, 3V for 130"], 
    "W": [20, ""],                      
    "X": [90, ""],                      
    "Y": [10, ""],                      
    "Z": [50, ""],                      
}

# PRICE_LIST = ITEM_PRICE_DISCOUNT_LOOKUP.keys()

# set up dataframe for item price tabular data
price_df = pd.DataFrame.from_dict(ITEM_PRICE_DISCOUNT_LOOKUP, orient='index')
price_df.rename(columns={0: "price", 1: "discount_rule"})
price_df.rename(columns={0: "price", 1: "discount_rule"}, inplace=True)
price_df['row_discount'] = 0

def _is_basket_valid(products_in_basket_sku_list):
    for sku in products_in_basket_sku_list:
        if sku not in ITEM_PRICE_DISCOUNT_LOOKUP:
            return False
    return True


def _discount_parser(original_price_per_unit: int, discount_rule: str) -> dict:

    discount_rules = discount_rule.split(",")
    if len(discount_rules) == 2:
        # clear up any leading whitespace
        discount_rules[1] = discount_rules[1].lstrip()

    for discount_rule in discount_rules:
        if "for" in discount_rule:
            # it's a multibuy discount
            discount_details = discount_rule.split(" for ")
            number_of_items_required_to_trigger = int(discount_details[0][0])
            discounted_price = int(discount_details[1])
            potential_full_price = number_of_items_required_to_trigger * original_price_per_unit
            discount_per_trigger = potential_full_price - discounted_price
            discount_type = 'multibuy'
            discount_target_sku = discount_details[0][1]
    # TODO handle those with 2 rules
    return {
        "type": discount_type,
        "discount_per_trigger": discount_per_trigger,
        "number_of_items_required_to_trigger": number_of_items_required_to_trigger,
        "discount_target_sku": discount_target_sku
    }


def _multibuy_evaluator(basket_contents_lookup, index, row, discount_info):
    # check how many times triggered
    number_of_this_item_in_basket = basket_contents_lookup[index]
    # calculate total discount
    number_of_discounts_triggered, remainder = divmod(number_of_this_item_in_basket, discount_info['number_of_items_required_to_trigger'])
    # add it to the target row
    total_discount_for_rule = discount_info['discount_per_trigger'] *  number_of_discounts_triggered
    # return remaining items
    return {
        'total_discount': total_discount_for_rule,
        'remaining_items_for_future_discounts': remainder
    }




# def same_product_multibuy_discount(number_of_items, price):
#     # (number_of_5a_discounts * 50)
#     # (number_of_3a_discounts * 20)
#     return number_of_items * price



def _calculate_total_price(products_in_basket_sku_list):
    basket_contents_lookup = {sku: 0 for sku in ITEM_PRICE_DISCOUNT_LOOKUP}
    for sku in products_in_basket_sku_list:
        basket_contents_lookup[sku] += 1

    # check special offers
    # number_of_5a_discounts, a_remainder = divmod(basket_contents_lookup['A'], 5)
    # number_of_3a_discounts = int(a_remainder / 3)
    # potential_number_of_free_b_products = int(basket_contents_lookup['E'] / 2)

    # temp_b_count = basket_contents_lookup['B']
    # temp_b_count -= potential_number_of_free_b_products

    # if temp_b_count < 0:
    #     potential_number_of_free_b_products = 0

    # number_of_b_discounts = int(temp_b_count / 2)

    # number_of_f_free = int(basket_contents_lookup['F'] / 3)
    # import pdb;pdb.set_trace()
    basket_sub_total = sum([ITEM_PRICE_DISCOUNT_LOOKUP[sku][0]
                           for sku in products_in_basket_sku_list])

    discount_accumulated = 0

    # manage discounts
    for index, row in price_df.iterrows():
        discount_info = _discount_parser(row["price"], row["discount_rule"])
        evaluated_discount_details = _multibuy_evaluator(basket_contents_lookup, index, row, discount_info)
        # update discount total, and amount of items left for discount
        discount_accumulated += evaluated_discount_details['total_discount']
        basket_contents_lookup[index] = evaluated_discount_details['remaining_items_for_future_discounts']

    basket_total_post_discounts = basket_sub_total - discount_accumulated

    # basket_total_post_discounts = basket_sub_total - (number_of_5a_discounts * 50) - (number_of_3a_discounts * 20) - (
    #     number_of_b_discounts * 15) - (potential_number_of_free_b_products * 30) - (number_of_f_free * 10)

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




