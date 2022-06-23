import unittest

import dydx3.constants as consts

from utils.dydx import go_short, setup_dydx


class TestGoShort(unittest.TestCase):
    def setUp(self) -> None:
        self.client = setup_dydx()
        self.position = go_short(self.client, amount=0.01, stop_loss=1, roi=1)

    def test_market_sell_order_placed(self):
        # Go short with a stop loss of 1 and a take profit of 1
        market_sell_order = self.client.private.get_order_by_id(
            self.position['market_buy_order']['order']['id']).data
        self.assertNotEqual(
            market_sell_order['order']['status'], consts.ORDER_STATUS_CANCELED)
        self.assertEqual(
            market_sell_order['order']['status'], consts.ORDER_STATUS_FILLED)
    
    # TODO: Add tests for stop limit and tak eprofit orders

    def tearDown(self) -> None:
        try:
            # TODO: Cancelling is not enough. You need to close positions too
            self.client.private.cancel_order(
                    order_id=self.position['stop_loss_order']['order']['id'])
            self.client.private.cancel_order(
                    order_id=self.position['take_profit_order']['order']['id'])
            # clear out the long position too
            self.client.private.cancel_order(
                    order_id=self.position['market_buy_order']['order']['id'])
        except:
            print("One order was already canceled")

if __name__ == '__main__':
    unittest.main()
