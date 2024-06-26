from solutions.CHK import checkout_solution
import pytest
# TODO check coverage

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


class TestChk():

    def test_checkout_simple_basket(self):
        expected_total_price = 115
        total_price = checkout_solution.checkout("A,B,C,D")
        assert total_price == expected_total_price
    
    def test_checkout_extra_item_basket(self):
        expected_total_price = 115
        total_price = checkout_solution.checkout("A,B,C,D,D")
        assert total_price == expected_total_price

    def test_checkout_invalid_basket(self):
        expected_response = -1
        response = checkout_solution.checkout("A,B,@%@£%,C,D")
        assert response == expected_response

    def test_checkout_special_offer_a(self):
        expected_total_price = 130
        total_price = checkout_solution.checkout("A,A,A")
        assert total_price == expected_total_price
    
    def test_checkout_special_offer_b(self):
        expected_total_price = 75
        total_price = checkout_solution.checkout("B,B,B")
        assert total_price == expected_total_price

