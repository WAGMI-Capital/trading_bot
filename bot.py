#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import dydx3.constants as consts
import traceback

from strategies.zeno import Zeno
from utils.dydx import setup_dydx, go_long, check_if_pending, go_short
from utils.discord_api import notify_discord


process_throttle_secs = 30

def start_bot(dydx_client, strategy):
    current_orders = {}
    while(True):
        # Run the strat every x seconds
        time.sleep(process_throttle_secs)

        # If there pending open orders, no trades will be placed
        if check_if_pending(current_orders, dydx_client):
            continue
        # We can reset order here
        current_orders = {}

        # Get market data and analyze it
        strategy.crunch_data()

        # Run our strategy
        if (strategy.should_long()):
            current_orders = go_long(
                dydx_client, amount=3.5, stop_loss=1, roi=1)
            notify_discord("Going long!")
            notify_discord(current_orders)
            continue
        
        if (strategy.should_short()):
            current_orders = go_short(
                dydx_client, amount=3.5, stop_loss=1, roi=1)
            notify_discord("Going short!")
            notify_discord(current_orders)
            continue

if __name__ == "__main__":
    client = setup_dydx()
    strat = Zeno(client, consts.MARKET_ETH_USD)
    try:
        start_bot(client, strat)
    except Exception:
        traceback.print_exc()
        notify_discord(traceback.format_exc())
