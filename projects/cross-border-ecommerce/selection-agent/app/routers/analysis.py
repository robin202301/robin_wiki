"""Analysis and profit calculation router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product, ProfitAnalysis
from app.schemas import ProfitAnalysisCreate, ProfitAnalysisResponse
from app.services.profit import calculate_profit, suggest_price_range
from app.services.scorer import get_recommendation

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/profit", response_model=ProfitAnalysisResponse)
def analyze_profit(data: ProfitAnalysisCreate, db: Session = Depends(get_db)):
    """Calculate profit for a product on specific platform/market"""
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    result = calculate_profit(
        product=product,
        selling_price_usd=data.selling_price_usd,
        platform=data.platform,
        market=data.market,
        exchange_rate=data.exchange_rate,
        shipping_cost_usd=data.shipping_cost_usd,
        platform_fee_pct=data.platform_fee_pct,
        ad_cost_pct=data.ad_cost_pct
    )
    
    # Save to database
    profit_analysis = ProfitAnalysis(
        product_id=data.product_id,
        platform=data.platform,
        market=data.market,
        selling_price_usd=data.selling_price_usd,
        cost_price_cny=product.cost_price_cny,
        exchange_rate=data.exchange_rate,
        cost_price_usd=result["cost_price_usd"],
        shipping_cost_usd=data.shipping_cost_usd,
        platform_fee_pct=data.platform_fee_pct,
        platform_fee_usd=result["platform_fee_usd"],
        ad_cost_pct=data.ad_cost_pct,
        ad_cost_usd=result["ad_cost_usd"],
        gross_profit_usd=result["gross_profit_usd"],
        gross_margin_pct=result["gross_margin_pct"],
        notes=data.notes
    )
    
    db.add(profit_analysis)
    db.commit()
    db.refresh(profit_analysis)
    
    return profit_analysis


@router.get("/profit/product/{product_id}", response_model=List[ProfitAnalysisResponse])
def get_profit_history(product_id: int, db: Session = Depends(get_db)):
    """Get profit analysis history for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    analyses = db.query(ProfitAnalysis).filter(
        ProfitAnalysis.product_id == product_id
    ).order_by(ProfitAnalysis.created_at.desc()).all()
    
    return analyses


@router.get("/price-suggestion/{product_id}")
def suggest_price(
    product_id: int,
    platform: str = "TikTok Shop",
    market: str = "泰国",
    target_margin: float = 0.50,
    db: Session = Depends(get_db)
):
    """Suggest optimal price range for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    result = suggest_price_range(
        product=product,
        platform=platform,
        market=market,
        target_margin_pct=target_margin
    )
    
    return result


@router.get("/recommendation/{product_id}")
def get_recommendation_for_product(product_id: int, db: Session = Depends(get_db)):
    """Get recommendation based on product scores"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    recommendation = get_recommendation(product.total_score)
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_score": product.total_score,
        "recommendation": recommendation,
        "scores": product.scores
    }


@router.get("/top-products")
def get_top_products(
    limit: int = 10,
    min_score: float = 60,
    db: Session = Depends(get_db)
):
    """Get top-scoring products"""
    products = db.query(Product).filter(
        Product.total_score >= min_score,
        Product.status != "rejected"
    ).order_by(Product.total_score.desc()).limit(limit).all()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category.value,
            "total_score": p.total_score,
            "funnel_stage": p.funnel_stage.value,
            "status": p.status.value,
            "scores": p.scores
        }
        for p in products
    ]
