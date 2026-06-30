"""Product management router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Product, FunnelStage, ProductStatus
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.services.scorer import calculate_product_scores

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Calculate initial scores
    score_result = calculate_product_scores(product)
    product.scores = score_result["scores"]
    product.total_score = score_result["total_score"]
    
    db.commit()
    db.refresh(product)
    
    return product


@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    funnel_stage: Optional[FunnelStage] = None,
    status: Optional[ProductStatus] = None,
    min_score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """List products with filters"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    if funnel_stage:
        query = query.filter(Product.funnel_stage == funnel_stage)
    if status:
        query = query.filter(Product.status == status)
    if min_score:
        query = query.filter(Product.total_score >= min_score)
    
    products = query.order_by(Product.total_score.desc()).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    # Recalculate scores if relevant fields changed
    if any(k in update_data for k in ["cost_price_cny", "weight_g", "category", "notes"]):
        score_result = calculate_product_scores(product)
        product.scores = score_result["scores"]
        product.total_score = score_result["total_score"]
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted", "id": product_id}


@router.post("/{product_id}/recalculate-scores", response_model=ProductResponse)
def recalculate_scores(product_id: int, db: Session = Depends(get_db)):
    """Recalculate product scores"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    score_result = calculate_product_scores(product)
    product.scores = score_result["scores"]
    product.total_score = score_result["total_score"]
    
    db.commit()
    db.refresh(product)
    return product


@router.get("/funnel/stats")
def get_funnel_stats(db: Session = Depends(get_db)):
    """Get funnel stage statistics"""
    stats = {}
    for stage in FunnelStage:
        count = db.query(Product).filter(Product.funnel_stage == stage).count()
        stats[stage.value] = count
    
    return {
        "funnel": stats,
        "total": sum(stats.values())
    }
