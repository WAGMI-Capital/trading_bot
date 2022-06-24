import unittest

import dydx3.constants as consts

from utils.dydx import get_stop_limit_price, go_short, setup_dydx
import math


class TestGoShort(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop_loss = 1
        cls.client = setup_dydx()
        cls.position = go_short(
            cls.client, amount=0.01, stop_loss=cls.stop_loss, roi=1)

    def test_market_sell_order_placed(self):
        # Go short with a stop loss of 1 and a take profit of 1
        market_sell_order = self.client.private.get_order_by_id(
            self.position['market_buy_order']['order']['id']).data
        self.assertNotEqual(
            market_sell_order['order']['status'], consts.ORDER_STATUS_CANCELED)
        self.assertTrue(
            market_sell_order['order']['status'] == consts.ORDER_STATUS_FILLED
            or market_sell_order['order']['status'] == consts.ORDER_STATUS_PENDING)

    def test_stop_loss_order_placed(self):
        stop_loss_order = self.client.private.get_order_by_id(
            self.position['stop_loss_order']['order']['id']).data
        self.assertNotEqual(
            stop_loss_order['order']['status'], consts.ORDER_STATUS_CANCELED)

    def test_take_profit_order_placed(self):
        take_profit_order = self.client.private.get_order_by_id(
            self.position['take_profit_order']['order']['id']).data
        self.assertNotEqual(
            take_profit_order['order']['status'], consts.ORDER_STATUS_CANCELED)

    def test_stop_loss_price_value(self):
        stop_loss_order = self.client.private.get_order_by_id(
            self.position['stop_loss_order']['order']['id']).data
        market_sell_order = self.client.private.get_order_by_id(
            self.position['market_buy_order']['order']['id']).data

        self.assertTrue(
            math.isclose(float(stop_loss_order['order']['price']),
                         get_stop_limit_price(
                             market_sell_order['order']['price'], self.stop_loss),
                         rel_tol=(self.stop_loss / 100) * 2) # Tolerance is double the stop_Loss%
        )

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            # TODO: Cancelling is not enough. You need to close positions too
            cls.client.private.cancel_order(
                order_id=cls.position['stop_loss_order']['order']['id'])
            cls.client.private.cancel_order(
                order_id=cls.position['take_profit_order']['order']['id'])
            # clear out the long position too
            cls.client.private.cancel_order(
                order_id=cls.position['market_buy_order']['order']['id'])
        except:
            print("One order was already canceled")


if __name__ == '__main__':
    unittest.main()
