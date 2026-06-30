"""Product scoring service"""
from typing import Dict
from app.models import Product


def calculate_product_scores(product: Product) -> Dict[str, float]:
    """
    Calculate multi-dimensional scores for a product.
    Returns dict with individual scores and total.
    """
    scores = {}
    
    # 1. Video Suitability (0-100)
    # Based on category, visual impact potential, weight
    scores["video_suitability"] = _score_video_suitability(product)
    
    # 2. Profit Potential (0-100)
    # Based on cost, weight (shipping), category margins
    scores["profit_potential"] = _score_profit_potential(product)
    
    # 3. Competition Level (0-100, lower is better but we invert)
    # Based on category saturation, price point
    scores["competition"] = _score_competition(product)
    
    # 4. Trend Score (0-100)
    # Placeholder - would integrate with trend data sources
    scores["trend"] = _score_trend(product)
    
    # 5. Supply Chain (0-100)
    # Based on source platform availability, lead time estimates
    scores["supply_chain"] = _score_supply_chain(product)
    
    # Calculate weighted total
    weights = {
        "video_suitability": 0.25,
        "profit_potential": 0.30,
        "competition": 0.20,
        "trend": 0.15,
        "supply_chain": 0.10
    }
    
    total = sum(scores[k] * weights[k] for k in weights.keys())
    
    return {
        "scores": scores,
        "total_score": round(total, 2),
        "weights": weights
    }


def _score_video_suitability(product: Product) -> float:
    """Score how suitable product is for AI video content"""
    score = 50.0  # Base score
    
    # Category bonuses
    if product.category.value == "beauty_tool":
        score += 20  # Before/after content very effective
    elif product.category.value == "accessory":
        score += 15  # Visual impact from wearing
    
    # Weight bonus (lighter = easier to showcase)
    if product.weight_g <= 50:
        score += 15
    elif product.weight_g <= 200:
        score += 10
    elif product.weight_g <= 500:
        score += 5
    
    # Price point bonus (mid-range performs better in video)
    if 30 <= product.cost_price_cny <= 100:
        score += 10
    elif 10 <= product.cost_price_cny < 30:
        score += 5
    
    return min(100, max(0, score))


def _score_profit_potential(product: Product) -> float:
    """Score profit potential based on cost and margins"""
    score = 50.0
    
    # Cost-based scoring (lower cost = higher potential margin)
    if product.cost_price_cny <= 10:
        score += 30
    elif product.cost_price_cny <= 20:
        score += 20
    elif product.cost_price_cny <= 50:
        score += 10
    elif product.cost_price_cny <= 100:
        score += 0
    else:
        score -= 10
    
    # Weight-based scoring (lighter = lower shipping costs)
    if product.weight_g <= 50:
        score += 20
    elif product.weight_g <= 200:
        score += 15
    elif product.weight_g <= 500:
        score += 5
    
    # Category margin expectations
    if product.category.value == "accessory":
        score += 10  # Higher margins typical
    elif product.category.value == "beauty_tool":
        score += 5
    
    return min(100, max(0, score))


def _score_competition(product: Product) -> float:
    """Score competition level (higher = less competition = better)"""
    score = 50.0
    
    # Category considerations
    if product.category.value == "beauty_tool":
        score += 10  # Slightly less saturated
    elif product.category.value == "accessory":
        score -= 5  # More competitive
    
    # Price point (niche pricing = less direct competition)
    if 50 <= product.cost_price_cny <= 150:
        score += 15  # Mid-range, less price war
    elif 10 <= product.cost_price_cny <= 50:
        score += 5
    
    # Weight (heavier items have fewer competitors due to shipping)
    if product.weight_g > 500:
        score += 10
    
    return min(100, max(0, score))


def _score_trend(product: Product) -> float:
    """Score trend alignment (placeholder - integrate real trend data)"""
    # Base score - would be enhanced with real trend data
    score = 60.0
    
    # Add bonus for trending categories
    # This would integrate with TikTok/Shopee trend APIs
    trending_keywords = ["美妆", "配饰", "收纳", "宠物"]
    
    if product.notes:
        for keyword in trending_keywords:
            if keyword in product.notes:
                score += 10
                break
    
    return min(100, max(0, score))


def _score_supply_chain(product: Product) -> float:
    """Score supply chain reliability"""
    score = 60.0
    
    # 1688 is generally reliable
    if product.source_platform == "1688":
        score += 20
    elif product.source_platform == "拼多多":
        score += 10
    
    # Lighter items have more supplier options
    if product.weight_g <= 100:
        score += 15
    elif product.weight_g <= 300:
        score += 10
    
    # Standard categories have better supply chains
    if product.category.value in ["accessory", "beauty_tool"]:
        score += 10
    
    return min(100, max(0, score))


def get_recommendation(total_score: float) -> Dict[str, str]:
    """Get recommendation based on total score"""
    if total_score >= 80:
        return {
            "level": "A",
            "action": "立即测试",
            "description": "高优先级，建议立即进入L4测品阶段"
        }
    elif total_score >= 65:
        return {
            "level": "B",
            "action": "优先评估",
            "description": "中等优先级，建议深入分析后决定是否测试"
        }
    elif total_score >= 50:
        return {
            "level": "C",
            "action": "持续关注",
            "description": "一般优先级，可放入观察池"
        }
    else:
        return {
            "level": "D",
            "action": "暂时搁置",
            "description": "低优先级，建议寻找更优选项"
        }
