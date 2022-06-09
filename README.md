# trading_bot

## Prerequisites

- Tested to work on Python 3.7
- Make sure you have python3-dev installed 
`sudo apt install python3-dev`

## Description

 Crypto trading model
 wagmi_Strategy.py file contains a single function that return a string 'Long' if trade taken is a long trade and 'Short' if the trade to be taken is a short trade, else it return 'Pass' to move to next iteration.
 Params:
 
 crypto_asset : Tickr of the asset; default = 'USD-BTC'
 
 p_interval : Interval size of primary candle; default = '15m'
 
 p_period : Period of primary candle data; default = '1mo'
 
 s_interval : Interval size of secondary candle; default = '5m'
 
 s_period : Period of secondary candle data; default = '1mo'
 
