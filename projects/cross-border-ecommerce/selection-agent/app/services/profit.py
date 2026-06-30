"""Profit calculation service"""
from typing import Dict
from app.models import Product


def calculate_profit(
    product: Product,
    selling_price_usd: float,
    platform: str,
    market: str,
    exchange_rate: float = 7.2,
    shipping_cost_usd: float = None,
    platform_fee_pct: float = None,
    ad_cost_pct: float = None
) -> Dict:
    """
    Calculate profit for a product on a specific platform/market.
    
    Args:
        product: Product instance
        selling_price_usd: Selling price in USD
        platform: Platform name
        market: Market name
        exchange_rate: CNY to USD exchange rate
        shipping_cost_usd: Shipping cost in USD (auto-calculated if None)
        platform_fee_pct: Platform fee percentage (default by platform)
        ad_cost_pct: Ad cost percentage (default 20%)
    
    Returns:
        Dict with all cost breakdowns and profit metrics
    """
    # Convert cost to USD
    cost_price_usd = product.cost_price_cny / exchange_rate
    
    # Calculate shipping if not provided
    if shipping_cost_usd is None:
        shipping_cost_usd = _estimate_shipping(product.weight_g, market)
    
    # Platform fees
    if platform_fee_pct is None:
        platform_fee_pct = _get_platform_fee(platform)
    platform_fee_usd = selling_price_usd * platform_fee_pct
    
    # Ad costs
    if ad_cost_pct is None:
        ad_cost_pct = 0.20  # Default 20%
    ad_cost_usd = selling_price_usd * ad_cost_pct
    
    # Calculate profit
    gross_profit_usd = (
        selling_price_usd
        - cost_price_usd
        - shipping_cost_usd
        - platform_fee_usd
        - ad_cost_usd
    )
    
    gross_margin_pct = (gross_profit_usd / selling_price_usd * 100) if selling_price_usd > 0 else 0
    
    return {
        "selling_price_usd": round(selling_price_usd, 2),
        "cost_price_cny": product.cost_price_cny,
        "cost_price_usd": round(cost_price_usd, 2),
        "exchange_rate": exchange_rate,
        "shipping_cost_usd": round(shipping_cost_usd, 2),
        "platform_fee_pct": round(platform_fee_pct * 100, 1),
        "platform_fee_usd": round(platform_fee_usd, 2),
        "ad_cost_pct": round(ad_cost_pct * 100, 1),
        "ad_cost_usd": round(ad_cost_usd, 2),
        "gross_profit_usd": round(gross_profit_usd, 2),
        "gross_margin_pct": round(gross_margin_pct, 1),
        "platform": platform,
        "market": market
    }


def _estimate_shipping(weight_g: int, market: str) -> float:
    """
    Estimate shipping cost based on weight and market.
    These are rough estimates - actual costs vary by logistics provider.
    """
    # Base rate per 100g
    weight_kg = weight_g / 1000
    
    # Regional shipping estimates (USD)
    shipping_rates = {
        "东南亚": 3.0 + weight_kg * 8,  # ~30 RMB base + 8 RMB/100g
        "泰国": 3.0 + weight_kg * 8,
        "越南": 3.0 + weight_kg * 8,
        "菲律宾": 3.5 + weight_kg * 9,
        "马来西亚": 3.0 + weight_kg * 8,
        "印尼": 3.5 + weight_kg * 9,
        "俄罗斯": 4.5 + weight_kg * 12,  # Higher shipping
    }
    
    base_cost = shipping_rates.get(market, 4.0 + weight_kg * 10)
    return base_cost


def _get_platform_fee(platform: str) -> float:
    """Get default platform fee percentage"""
    platform_fees = {
        "TikTok Shop": 0.05,  # 5%
        "Shopee": 0.06,  # 6%
        "Lazada": 0.06,  # 6%
        "速卖通": 0.08,  # 8%
    }
    return platform_fees.get(platform, 0.06)


def suggest_price_range(
    product: Product,
    platform: str,
    market: str,
    target_margin_pct: float = 0.50,
    exchange_rate: float = 7.2
) -> Dict:
    """
    Suggest optimal price range for a product.
    
    Args:
        product: Product instance
        platform: Platform name
        market: Market name
        target_margin_pct: Target profit margin (default 50%)
        exchange_rate: Exchange rate
    
    Returns:
        Dict with suggested price range
    """
    cost_usd = product.cost_price_cny / exchange_rate
    shipping_usd = _estimate_shipping(product.weight_g, market)
    platform_fee_pct = _get_platform_fee(platform)
    ad_cost_pct = 0.20
    
    # Total costs excluding selling price
    fixed_costs = cost_usd + shipping_usd
    
    # Calculate minimum price for target margin
    # selling_price - fixed_costs - (platform_fee_pct * selling_price) - (ad_cost_pct * selling_price) = target_margin * selling_price
    # selling_price * (1 - platform_fee_pct - ad_cost_pct - target_margin) = fixed_costs
    # selling_price = fixed_costs / (1 - platform_fee_pct - ad_cost_pct - target_margin)
    
    denominator = 1 - platform_fee_pct - ad_cost_pct - target_margin_pct
    
    if denominator <= 0:
        # Target margin too high for this cost structure
        min_price = fixed_costs / (1 - platform_fee_pct - ad_cost_pct) * 1.1  # Minimal margin
    else:
        min_price = fixed_costs / denominator
    
    # Suggest price range
    suggested_low = min_price
    suggested_mid = min_price * 1.2
    suggested_high = min_price * 1.5
    
    # Market adjustments
    if market == "俄罗斯":
        # Russian market can support higher prices
        suggested_low *= 1.1
        suggested_mid *= 1.1
        suggested_high *= 1.1
    
    return {
        "suggested_low_usd": round(suggested_low, 2),
        "suggested_mid_usd": round(suggested_mid, 2),
        "suggested_high_usd": round(suggested_high, 2),
        "cost_breakdown": {
            "cost_usd": round(cost_usd, 2),
            "shipping_usd": round(shipping_usd, 2),
            "platform_fee_pct": round(platform_fee_pct * 100, 1),
            "ad_cost_pct": round(ad_cost_pct * 100, 1)
        },
        "market": market,
        "platform": platform
    }
