"""
Market data integration with caching and error handling
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class StockQuote:
    """Represents a stock quote"""
    symbol: str
    price: float
    currency: str
    timestamp: datetime
    change: float
    change_percent: float
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None


@dataclass
class MarketTrend:
    """Represents market trends"""
    index: str
    value: float
    change_percent: float
    timestamp: datetime


class MarketDataCache:
    """Cache for market data with TTL"""

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self.cache:
            cached = self.cache[key]
            if datetime.now() - cached['timestamp'] < timedelta(seconds=self.ttl_seconds):
                logger.debug(f"Cache hit for {key}")
                return cached['value']
            else:
                del self.cache[key]
                logger.debug(f"Cache expired for {key}")
        return None

    def set(self, key: str, value: Any) -> None:
        """Set cache value"""
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now()
        }

    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()


class YFinanceProvider:
    """yFinance market data provider"""

    def __init__(self, cache_ttl: int = 3600):
        try:
            import yfinance as yf
            self.yf = yf
            self.cache = MarketDataCache(cache_ttl)
            logger.info("YFinance provider initialized")
        except ImportError:
            raise ImportError("yfinance package required")

    def get_stock_quote(self, symbol: str) -> Optional[StockQuote]:
        """Get stock quote"""
        cache_key = f"stock_{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self.yf.Ticker(symbol)
            data = ticker.history(period='1d')
            info = ticker.info

            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return None

            latest = data.iloc[-1]
            price = float(latest['Close'])
            
            # Calculate change
            prev_close = info.get('previousClose', price)
            change = price - prev_close
            change_percent = (change / prev_close * 100) if prev_close != 0 else 0

            quote = StockQuote(
                symbol=symbol,
                price=price,
                currency=info.get('currency', 'USD'),
                timestamp=datetime.now(),
                change=change,
                change_percent=change_percent,
                high_52w=info.get('fiftyTwoWeekHigh'),
                low_52w=info.get('fiftyTwoWeekLow'),
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE')
            )

            self.cache.set(cache_key, quote)
            return quote
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            return None

    def get_portfolio_performance(self, holdings: Dict[str, float]) -> Dict[str, Any]:
        """Get portfolio performance metrics"""
        try:
            total_value = 0
            performance = []

            for symbol, quantity in holdings.items():
                quote = self.get_stock_quote(symbol)
                if quote:
                    holding_value = quote.price * quantity
                    total_value += holding_value
                    performance.append({
                        'symbol': symbol,
                        'quantity': quantity,
                        'price': quote.price,
                        'value': holding_value,
                        'change_percent': quote.change_percent
                    })

            return {
                'total_value': total_value,
                'holdings': performance,
                'timestamp': datetime.now()
            }
        except Exception as e:
            logger.error(f"Error calculating portfolio performance: {e}")
            return {'total_value': 0, 'holdings': []}

    def get_market_trends(self) -> List[MarketTrend]:
        """Get major market indices"""
        indices = {
            '^GSPC': 'S&P 500',
            '^IXIC': 'NASDAQ',
            '^DJI': 'Dow Jones'
        }
        
        trends = []
        for symbol, name in indices.items():
            try:
                quote = self.get_stock_quote(symbol)
                if quote:
                    trends.append(MarketTrend(
                        index=name,
                        value=quote.price,
                        change_percent=quote.change_percent,
                        timestamp=datetime.now()
                    ))
            except Exception as e:
                logger.warning(f"Could not fetch {name}: {e}")

        return trends


class AlphaVantageProvider:
    """Alpha Vantage market data provider"""

    def __init__(self, api_key: str, cache_ttl: int = 3600):
        try:
            from alpha_vantage.timeseries import TimeSeries
            self.ts = TimeSeries(key=api_key)
            self.cache = MarketDataCache(cache_ttl)
            logger.info("Alpha Vantage provider initialized")
        except ImportError:
            raise ImportError("alpha-vantage package required")

    def get_stock_quote(self, symbol: str) -> Optional[StockQuote]:
        """Get stock quote"""
        cache_key = f"stock_{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            data, meta_data = self.ts.get_quote_endpoint(symbol=symbol)
            if data:
                quote = StockQuote(
                    symbol=symbol,
                    price=float(data['05. price']),
                    currency=meta_data.get('05. price', 'USD'),
                    timestamp=datetime.now(),
                    change=float(data.get('09. change', 0)),
                    change_percent=float(data.get('10. change percent', '0').rstrip('%'))
                )
                self.cache.set(cache_key, quote)
                return quote
        except Exception as e:
            logger.error(f"Error fetching quote from Alpha Vantage for {symbol}: {e}")
        
        return None

    def get_portfolio_performance(self, holdings: Dict[str, float]) -> Dict[str, Any]:
        """Get portfolio performance metrics"""
        total_value = 0
        performance = []

        for symbol, quantity in holdings.items():
            quote = self.get_stock_quote(symbol)
            if quote:
                holding_value = quote.price * quantity
                total_value += holding_value
                performance.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': quote.price,
                    'value': holding_value,
                    'change_percent': quote.change_percent
                })

        return {
            'total_value': total_value,
            'holdings': performance,
            'timestamp': datetime.now()
        }

    def get_market_trends(self) -> List[MarketTrend]:
        """Get market trends (limited with Alpha Vantage)"""
        # Alpha Vantage has limited free tier, return empty for now
        logger.info("Market trends limited with Alpha Vantage free tier")
        return []


class MarketDataProvider:
    """Unified market data provider"""

    def __init__(self, provider: str = "yfinance", **kwargs):
        if provider.lower() == "yfinance":
            self.provider = YFinanceProvider(kwargs.get('cache_ttl', 3600))
        elif provider.lower() == "alpha_vantage":
            api_key = kwargs.get('api_key', '')
            self.provider = AlphaVantageProvider(api_key, kwargs.get('cache_ttl', 3600))
        else:
            raise ValueError(f"Unsupported market data provider: {provider}")

    def get_stock_quote(self, symbol: str) -> Optional[StockQuote]:
        """Get stock quote"""
        return self.provider.get_stock_quote(symbol)

    def get_portfolio_performance(self, holdings: Dict[str, float]) -> Dict[str, Any]:
        """Get portfolio performance"""
        return self.provider.get_portfolio_performance(holdings)

    def get_market_trends(self) -> List[MarketTrend]:
        """Get market trends"""
        return self.provider.get_market_trends()
