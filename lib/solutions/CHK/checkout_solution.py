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


# set up dataframe for item price tabular data
# TODO save this dataframe to disk for efficiency, it doesn't change very often
price_df = pd.read_csv('lib/solutions/CHK/item_price.csv', sep="|")
price_df.columns = price_df.columns.str.strip()
price_df = price_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
price_df.set_index('Item', inplace=True)
price_df.columns = ['price', 'discount_rule']
price_df['rule_ranking'] = 0

# top-ranking rule == 2
price_df = price_df.assign(rule_ranking=[2 if " get one " in x else 0 for x in price_df['discount_rule']])
# Sort the discount rules by their ranking
price_df.sort_values('rule_ranking', ascending=False, inplace=True)

# TODO compute this automatically in future
SKUS_IN_3_FOR_45_OFFER = ['S,T,X,Y,Z']

# TODO check if this interferes with the last rule
# price_df = price_df.assign(rule_type=[1 if " for " in x else 0 for x in price_df['discount_rule']])
# import pdb;pdb.set_trace()

def _is_basket_valid(products_in_basket_sku_list):
    for sku in products_in_basket_sku_list:
        if sku not in price_df.index:
            return False
    return True

def _get_sku_price(sku):
    return price_df[sku:sku]['price'].iloc[0]

def _discount_parser(original_price_per_unit: int, discount_rule: str) -> dict:

    discount_rules = discount_rule.split(",")
    if len(discount_rules) == 2:
        # clear up any leading whitespace
        discount_rules[1] = discount_rules[1].lstrip()
        discount_rules = list(reversed(discount_rules))

    parsed_rules_info = []
    for discount_rule in discount_rules:
        if ")" in discount_rule:
            # it's the 3 for 45 deal
            parsed_rules_info.append({
                "type": '3for45',
                "discount_per_trigger": None,
                "number_of_items_required_to_trigger": 3,
                "discount_target_sku": None
            })
        elif "for" in discount_rule:
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
            discount_per_trigger = _get_sku_price(discount_target_sku)
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

def _3_for_45_evaluator(basket_contents_lookup, index, row, discount_info):
    # accumulate the amount spent on S,T,X,Y,Z collectively

    # check how many times triggered
    number_of_this_item_in_basket = basket_contents_lookup[index]
    number_of_discounts_triggered, remainder = divmod(
        number_of_this_item_in_basket, discount_info['number_of_items_required_to_trigger'])
    # enough for a discount?
    import pdb;pdb.set_trace()

    pass


def _calculate_total_price(products_in_basket_sku_list):
    basket_contents_lookup = {sku: 0 for sku in price_df.index}
    for sku in products_in_basket_sku_list:
        basket_contents_lookup[sku] += 1

    basket_sub_total = int(sum([_get_sku_price(sku)
                           for sku in products_in_basket_sku_list]))

    discount_accumulated = 0

    # manage discounts
    for index, row in price_df.iterrows():
        discount_rules_info = _discount_parser(
            row["price"], row["discount_rule"])
        for discount_rule in discount_rules_info:
            # TODO define a proper interface for these
            if discount_rule['type'] == 'multibuy':
                evaluated_discount_details = _multibuy_evaluator(
                    basket_contents_lookup, index, row, discount_rule)
            elif discount_rule['type'] == "bogof":
                evaluated_discount_details = _bogof_evaluator(
                    basket_contents_lookup, index, row, discount_rule)
            elif discount_rule['type'] == "3for45":
                evaluated_discount_details = _3_for_45_evaluator(
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

