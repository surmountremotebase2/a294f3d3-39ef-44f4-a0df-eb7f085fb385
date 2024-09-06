from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "TSLA"]  # Example tickers
        self.insider_data = [InsiderTrading(i) for i in self.tickers]
        self.sentiment_data = [SocialSentiment(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"  # Using daily data

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # Combine insider trading data and social sentiment data in the data list
        return self.insider_data + self.sentiment_data

    def run(self, data):
        allocation_dict = {}
        
        # Iterate through each stock ticker
        for ticker in self.tickers:
            insider_signal = False
            sentiment_signal = False
            
            # Check the latest insider trading activity
            insider_data_key = ("insider_trading", ticker)
            if insider_data_key in data and data[insider_data_key]:
                latest_insider_activity = data[insider_data_key][-1]
                if latest_insider_activity['transactionType'].startswith('P'):  # Assuming 'P' stands for purchase
                    insider_signal = True
            
            # Check the latest social sentiment
            sentiment_data_key = ("social_sentiment", ticker)
            if sentiment_data_key in data and data[sentiment_data_key]:
                latest_sentiment = data[sentiment_data_key][-1]
                if latest_sentiment['twitterSentiment'] > 0.5:  # Arbitrary threshold for positive sentiment
                    sentiment_signal = True
            
            # If both insider buying activity and positive sentiment are found, allocate investment to this stock
            if insider_signal and sentiment_signal:
                allocation_dict[ticker] = 1 / len([t for t in self.tickers if t in allocation_dict or (insider_signal and sentiment_signal)])
            else:
                allocation_dict[ticker] = 0  # No allocation if signals do not align

        return TargetAllocation(allocation_dict)