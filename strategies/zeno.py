#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 02:25:44 2022

@author: pranav.atulya
"""

# Basic Initial strat
# Indicators used: Bollinger bands, MACD, Simple moving average, OLS regression channel
# Data feed: Close price, period: last 1 month, interval: 5min(primary), 1min(confirmation) (May change later based on backtest results)
# Entry condition; BUY/GoLong: (50SMA > UBB) and (MACD_FastLine < MACD_FastLine_mean - MACD_FastLine_stdev)
# Entry condition cofirmation; BUY/GoLong: (Close_1min > 50SMA_1min)
# Entry condition; SELL/GoShort: *exact opposite of the buy conditions.

# strat1 takes two dataframes, one for each interval(primary and confirmation);
# It requires the dataframes to have the close price and all the indicator values as separate columns
from .strategy import Strategy
from utils.getData import getFromDydx
from utils.getIndicators import getBollingerBands, getMACD



class Zeno(Strategy):
    def __init__(self, client, market) -> None:
        self.client = client
        self.market = market

    def _get_market_data(self):
        self.price_primary = getFromDydx(self.client, self.market, '5MINS')
        self.price_confirmation = getFromDydx(self.client, self.market, '1MIN')

    def _populate_indicators(self):
        # Turning these indicator functions into in-memory operations will be more
        # Effcient performance-wise
        # Readable in terms of code
        self.price_primary = getBollingerBands(self.price_primary)
        self.price_primary = getMACD(self.price_primary)
        self.price_primary['SMA50'] = self.price_primary['close'].rolling(
            window=50).mean()

        self.price_confirmation = getBollingerBands(self.price_confirmation)
        self.price_confirmation = getMACD(self.price_confirmation)
        self.price_confirmation['SMA50'] = self.price_confirmation['close'].rolling(
            window=50).mean()
    
    def crunch_data(self):
        self._get_market_data()
        self._populate_indicators()
    
    def should_long(self):
        return self._long_filters()
    
    def should_short(self):
        return self._short_filters()

    def _long_filters(self):
        macd_mean = self.price_primary['signal_line'].mean()
        macd_dev = self.price_primary['signal_line'].std()

        last_candle_primary = self.price_primary.iloc[-1]
        last_candle_confirmation = self.price_confirmation.iloc[-1]

        if(last_candle_primary['SMA50'] > last_candle_primary['Upper Band'] and last_candle_primary['signal_line'] < macd_mean-1*macd_dev):
            return bool(last_candle_confirmation['SMA50'] < float(last_candle_confirmation['close']))
        else:
            return False
    
    def _short_filters(self):
        macd_mean = self.price_primary['signal_line'].mean()
        macd_dev = self.price_primary['signal_line'].std()

        last_candle_primary = self.price_primary.iloc[-1]
        last_candle_confirmation = self.price_confirmation.iloc[-1]
    
        if(last_candle_primary['SMA50'] < last_candle_primary['Lower Band'] and last_candle_primary['signal_line'] > macd_mean + 1 * macd_dev):        
            return bool(last_candle_confirmation['SMA50'] > float(last_candle_confirmation['close']))
        else:
            return False
