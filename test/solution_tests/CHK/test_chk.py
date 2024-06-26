from solutions.CHK import checkout_solution
import pytest
# TODO check coverage

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
# +------+-------+------------------------+


class TestChk():
    def test_checkout_empty_basket(self):
        expected_total_price = 0
        total_price = checkout_solution.checkout("")
        assert total_price == expected_total_price

    def test_checkout_simple_basket(self):
        expected_total_price = 115
        total_price = checkout_solution.checkout("ABCD")
        assert total_price == expected_total_price

    def test_checkout_extra_item_basket(self):
        expected_total_price = 130
        total_price = checkout_solution.checkout("ABCDD")
        assert total_price == expected_total_price

    def test_checkout_invalid_basket(self):
        expected_response = -1
        response = checkout_solution.checkout("AB@%@£%CD")
        assert response == expected_response

    def test_checkout_special_offer_a(self):
        expected_total_price = 130
        total_price = checkout_solution.checkout("AAA")
        assert total_price == expected_total_price

    def test_checkout_special_offer_b(self):
        expected_total_price = 75
        total_price = checkout_solution.checkout("BBB")
        assert total_price == expected_total_price

    def test_checkout_special_offer_3e_for_b(self):
        # the free Bs removed
        expected_total_price = 40+40+40+40
        total_price = checkout_solution.checkout("EEEEBB")
        assert total_price == expected_total_price

    def test_checkout_special_offer_3e_for_b_extra_b(self):
        # the free Bs removed
        expected_total_price = 40+40+40+40+30
        total_price = checkout_solution.checkout("EEEEBBB")
        assert total_price == expected_total_price

    def test_checkout_special_offer_3e_for_b_extra_2bs(self):
        # the free Bs removed
        expected_total_price = 40+40+40+40+45
        total_price = checkout_solution.checkout("EEEEBBBB")
        assert total_price == expected_total_price

    def test_checkout_special_offer_5a_for_200(self):
        expected_total_price = 200
        total_price = checkout_solution.checkout("AAAAA")
        assert total_price == expected_total_price

    def test_checkout_special_offer_5a_for_200_extra_a(self):
        expected_total_price = 250
        total_price = checkout_solution.checkout("AAAAAA")
        assert total_price == expected_total_price

    def test_checkout_special_offer_5a_for_200_extra_a_again(self):
        expected_total_price = 300
        total_price = checkout_solution.checkout("AAAAAAA")
        assert total_price == expected_total_price

