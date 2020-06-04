"""
Greenblatt's Magic Formula
==========================

We closely follow the procedure described in the Little Book.

1. Construct the universe of stocks: we require market capitalisations of more than $100m and remove stocks in the Financials or Utilities sectors (since they have slightly different accounting).
2. Calculate the ROC and the earnings yield.
3. Rank each company in the stock universe by ROC 
4. Rank each company in the stock universe by Earnings Yield
5. Add the two ranks to get a combined score
6. Each month, buy the top 2 stocks by ranking (that we don't already own)
7. Hold each position for one year.

This version of the algorithm does not include tax optimisation
"""

from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.factset import RBICSFocus, Fundamentals
from quantopian.pipeline.filters import QTradableStocksUS
        

def initialize(context):
    context.min_mcap = 100e6  # 100m min market cap
    context.holding_period = 12  # months
    context.stocks_per_month = 2  # number of stocks to buy each month
    context.stocks = []  # will hold the list of stocks in portfolio
    context.top_stocks = []  # will hold the top ranked stocks in each period
    
    # Monthly rebalance
    schedule_function(
        rebalance,
        date_rules.month_start(),
        time_rules.market_close(hours=2)
    )

    # Create our pipeline and attach it to our algorithm.
    my_pipe = make_pipeline(context)
    attach_pipeline(my_pipe, 'pipe')

    
def make_pipeline(context):
    sector = RBICSFocus.l1_name.latest
    sector_mask = (sector != "Finance") & (sector != "Utilities")
    mask = QTradableStocksUS() & (Fundamentals.mkt_val_public.latest > context.min_mcap) & sector_mask
    
    # Quality
    ebit = Fundamentals.ebit_oper_ltm.latest
    ev = Fundamentals.entrpr_val_qf.latest
    earnings_yield = ebit / ev
    
    # Cheapness
    net_fixed_assets = Fundamentals.ppe_net.latest
    working_capital = Fundamentals.wkcap_qf.latest
    roc = ebit / (net_fixed_assets + working_capital)
    
    # Rank and combine
    ey_rank = earnings_yield.rank(mask=mask)
    roc_rank = roc.rank(mask=mask)
    combined_score = ey_rank + roc_rank
    
    # In the worst case we will need 26 (assuming top 24 are already held)
    top_stocks = combined_score.top(30, mask=mask)
    
    return Pipeline(
      columns={"top_stocks": top_stocks,
               "score": combined_score},
      screen=(mask & combined_score.notnull() & top_stocks)
    )


def before_trading_start(context, data):
    # Gets our pipeline output everyday
    pipe_results = pipeline_output('pipe')

    # Sort stocks by score
    context.top_stocks = []
    for sec in pipe_results.sort_values(by=["score"],ascending=False).index.tolist():
        if data.can_trade(sec):
            context.top_stocks.append(sec)

             
def rebalance(context, data):
    n = context.holding_period * context.stocks_per_month
    
    # Get top stocks that aren't already held
    new_stocks = [s for s in context.top_stocks if s not in context.stocks][:context.stocks_per_month]  
    # For the first year of the backtest, just accumulate
    if len(context.stocks) < n:
        order_stocks(new_stocks, context, data)
    else:
        # Sell first two
        stocks_to_sell = context.stocks[:context.stocks_per_month]
        sell_stocks(stocks_to_sell, context, data)
        order_stocks(new_stocks, context, data)
    
    log.info("Portfolio size after rebalance: " + str(len(context.stocks)))
    
    
def order_stocks(new_stocks, context, data):
    # Helper method to buy stocks
    n = context.holding_period * context.stocks_per_month
    target_weight = 1.0 / n

    # Order and add to list
    for s in new_stocks:
        order_target_percent(s, target_weight)
        context.stocks.append(s)

    
def sell_stocks(stocks_to_sell, context, data):
    # Liquidate and remove from list
    for s in stocks_to_sell:
        order_target_percent(s, 0)
        context.stocks.remove(s)