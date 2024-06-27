from solutions.CHK import checkout_solution
import pytest
# TODO check coverage

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
# | G    | 20    |                        | 
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

class TestChk():
    # def test_checkout_empty_basket(self):
    #     expected_total_price = 0
    #     total_price = checkout_solution.checkout("")
    #     assert total_price == expected_total_price

    # def test_checkout_simple_basket(self):
    #     expected_total_price = 115
    #     total_price = checkout_solution.checkout("ABCD")
    #     assert total_price == expected_total_price

    # def test_checkout_extra_item_basket(self):
    #     expected_total_price = 130
    #     total_price = checkout_solution.checkout("ABCDD")
    #     assert total_price == expected_total_price

    # def test_checkout_invalid_basket(self):
    #     expected_response = -1
    #     response = checkout_solution.checkout("AB@%@£%CD")
    #     assert response == expected_response

    # def test_checkout_special_offer_a(self):
    #     expected_total_price = 130
    #     total_price = checkout_solution.checkout("AAA")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_b(self):
    #     expected_total_price = 75
    #     total_price = checkout_solution.checkout("BBB")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_4e_for_b(self):
    #     # the free Bs removed
    #     expected_total_price = 40+40+40+40
    #     total_price = checkout_solution.checkout("EEEEBB")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_3e_for_b_extra_b(self):
    #     # the free Bs removed
    #     expected_total_price = 40+40+40+40+30
    #     total_price = checkout_solution.checkout("EEEEBBB")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_3e_for_b_extra_2bs(self):
    #     # the free Bs removed
    #     expected_total_price = 40+40+40+40+45
    #     total_price = checkout_solution.checkout("EEEEBBBB")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_5a_for_200(self):
    #     expected_total_price = 200
    #     total_price = checkout_solution.checkout("AAAAA")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_5a_for_200_extra_a(self):
    #     expected_total_price = 250
    #     total_price = checkout_solution.checkout("AAAAAA")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_5a_for_200_extra_a_again(self):
    #     expected_total_price = 300
    #     total_price = checkout_solution.checkout("AAAAAAA")
    #     assert total_price == expected_total_price

    # def test_checkout_special_offer_buy_2f_get_1_free(self):
    #     expected_total_price = 20
    #     total_price = checkout_solution.checkout("FFF")
    #     assert total_price == expected_total_price

    # def test_checkout_no_special_offer_f(self):
    #     expected_total_price = 20
    #     total_price = checkout_solution.checkout("FF")
    #     assert total_price == expected_total_price

    # def test_checkout_no_special_extra_f(self):
    #     expected_total_price = 30
    #     total_price = checkout_solution.checkout("FFFF")
    #     assert total_price == expected_total_price

    # def test_checkout_h_only(self):
    #     expected_total_price = 10
    #     total_price = checkout_solution.checkout("H")
    #     assert total_price == expected_total_price

    # def test_checkout_alphabet(self):
    #     expected_total_price = 965
    #     total_price = checkout_solution.checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    #     assert total_price == expected_total_price

    # def test_ee(self):
    #     expected_total_price = 80
    #     total_price = checkout_solution.checkout("EE")
    #     assert total_price == expected_total_price

    # def test_hhhhhhhhhh(self):
    #     expected_total_price = 80
    #     total_price = checkout_solution.checkout("HHHHHHHHHH")
    #     assert total_price == expected_total_price

    # def test_hhhhhhhhhhh(self):
    #     expected_total_price = 90
    #     total_price = checkout_solution.checkout("HHHHHHHHHHH")
    #     assert total_price == expected_total_price

    def test_sss(self):
        expected_total_price = 90
        total_price = checkout_solution.checkout("SSS")
        assert total_price == expected_total_price
