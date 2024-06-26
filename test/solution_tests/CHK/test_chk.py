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
    # def test_chk_1(self):
    #     # Just an initial test to ensure it can find the module
    #     with pytest.raises(NotImplementedError):
    #         checkout_solution.checkout(None)
    #     # assert sum_solution.compute(1, 2) == 3

    def test_chk_1(self):
        # Just an initial test to ensure it can find the module
        with pytest.raises(NotImplementedError):
            checkout_solution.checkout(None)
        # assert sum_solution.compute(1, 2) == 3


