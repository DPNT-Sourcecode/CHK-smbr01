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
# sorted by BOGOF first (NOTE a python version should be used which retains dictionary order)
# ITEM_PRICE_DISCOUNT_LOOKUP = {
#     "E": [40, "2E get one B free"],
#     "F": [10, "2F get one F free"],
#     "N": [40, "3N get one M free"],
#     "R": [50, "3R get one Q free"],
#     "U": [40, "3U get one U free"],
#     "A": [50, "3A for 130, 5A for 200"],
#     "B": [30, "2B for 45"],
#     "C": [20, ""],
#     "D": [15, ""],
#     "G": [20, ""],
#     "H": [10, "5H for 45, 10H for 80"],
#     "I": [35, ""],
#     "J": [60, ""],
#     "K": [80, "2K for 150"],
#     "L": [90, ""],
#     "M": [15, ""],
#     "O": [10, ""],
#     "P": [50, "5P for 200"],
#     "Q": [30, "3Q for 80"],
#     "S": [30, ""],
#     "T": [20, ""],
#     "V": [50, "2V for 90, 3V for 130"],
#     "W": [20, ""],
#     "X": [90, ""],
#     "Y": [10, ""],
#     "Z": [50, ""],
# }

# set up dataframe for item price tabular data
price_df = pd.DataFrame.from_dict(ITEM_PRICE_DISCOUNT_LOOKUP, orient='index')
price_df.rename(columns={0: "price", 1: "discount_rule"})
price_df.rename(columns={0: "price", 1: "discount_rule"}, inplace=True)



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
        discount_rules = list(reversed(discount_rules))

    parsed_rules_info = []
    for discount_rule in discount_rules:
        if "for" in discount_rule:
            # it's a multibuy discount
            discount_details = discount_rule.split(" for ")
            # TODO increase robustness & clarity when splitting these strings
            number_of_items_required_to_trigger = int(discount_details[0][0:-1])
            discounted_price = int(discount_details[1])
            potential_full_price = number_of_items_required_to_trigger * original_price_per_unit
            discount_per_trigger = potential_full_price - discounted_price
            discount_type = 'multibuy'
            discount_target_sku = discount_details[0][-1]
            # TODO refactor these parts into a class or other data structure
            parsed_rules_info.append({
                "type": discount_type,
                "discount_per_trigger": discount_per_trigger,
                "number_of_items_required_to_trigger": number_of_items_required_to_trigger,
                "discount_target_sku": discount_target_sku
            })
        elif "get one" in discount_rule:
            # it's a buy one get something free discount
            # e.g. "2E get one B free"
            discount_details = discount_rule.split(" get one ")
            number_of_items_required_to_trigger = int(discount_details[0][0])
            discount_type = 'bogof'
            discount_target_sku = discount_details[1][0]
            discount_per_trigger = ITEM_PRICE_DISCOUNT_LOOKUP[discount_target_sku][0]
            parsed_rules_info.append({
                "type": discount_type,
                "discount_per_trigger": discount_per_trigger,
                "number_of_items_required_to_trigger": number_of_items_required_to_trigger,
                "discount_target_sku": discount_target_sku
            })

    return parsed_rules_info


def _multibuy_evaluator(basket_contents_lookup, index, row, discount_info):
    # check how many times triggered
    number_of_this_item_in_basket = basket_contents_lookup[index]
    # calculate total discount
    number_of_discounts_triggered, remainder = divmod(number_of_this_item_in_basket, discount_info['number_of_items_required_to_trigger'])
    # add it to the target row
    total_discount_for_rule = discount_info['discount_per_trigger'] * \
        number_of_discounts_triggered

    return {
        'total_discount': total_discount_for_rule,
        'remaining_items_for_future_discounts': remainder
    }


def _bogof_evaluator(basket_contents_lookup, index, row, discount_info):
    # check how many times triggered
    number_of_this_item_in_basket = basket_contents_lookup[index]
    # calculate total discount
    number_of_discounts_triggered, remainder = divmod(
        number_of_this_item_in_basket, discount_info['number_of_items_required_to_trigger'])

    number_in_discount_target_basket = basket_contents_lookup[discount_info['discount_target_sku']]

    # If the free product isn't in the basket, we won't award the discount
    if discount_info['discount_target_sku'] == index and number_of_discounts_triggered and not remainder:
        number_of_discounts_triggered -= 1
    elif number_in_discount_target_basket != index:
        if number_in_discount_target_basket < number_of_discounts_triggered:
            number_of_discounts_triggered  = number_in_discount_target_basket


    # tally up the discount
    total_discount_for_rule = discount_info['discount_per_trigger'] * \
        number_of_discounts_triggered

    return {
        'total_discount': total_discount_for_rule,
        'remaining_items_for_future_discounts': number_in_discount_target_basket - number_of_discounts_triggered
    }


def _calculate_total_price(products_in_basket_sku_list):
    basket_contents_lookup = {sku: 0 for sku in ITEM_PRICE_DISCOUNT_LOOKUP}
    for sku in products_in_basket_sku_list:
        basket_contents_lookup[sku] += 1

    basket_sub_total = sum([ITEM_PRICE_DISCOUNT_LOOKUP[sku][0]
                           for sku in products_in_basket_sku_list])

    discount_accumulated = 0

    # manage discounts
    for index, row in price_df.iterrows():
        discount_rules_info = _discount_parser(
            row["price"], row["discount_rule"])
        for discount_rule in discount_rules_info:
            if discount_rule['type'] == 'multibuy':
                evaluated_discount_details = _multibuy_evaluator(
                    basket_contents_lookup, index, row, discount_rule)
            else:
                evaluated_discount_details = _bogof_evaluator(
                    basket_contents_lookup, index, row, discount_rule)

            # update discount total, and amount of items left for discount
            discount_accumulated += evaluated_discount_details['total_discount']
            basket_contents_lookup[discount_rule['discount_target_sku']
                                   ] = evaluated_discount_details['remaining_items_for_future_discounts']

    basket_total_post_discounts = basket_sub_total - discount_accumulated

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



