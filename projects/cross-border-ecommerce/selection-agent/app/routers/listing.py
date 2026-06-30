"""Listing generation router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product, Listing
from app.schemas import ListingCreate, ListingResponse
from app.services.llm import llm_service

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post("/generate", response_model=ListingResponse)
def generate_listing(data: ListingCreate, db: Session = Depends(get_db)):
    """Generate product listing using LLM"""
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Generate listing with LLM
    result = llm_service.generate_listing(
        product=product,
        language=data.language,
        platform=data.platform
    )
    
    # Check for errors
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Save to database
    listing = Listing(
        product_id=data.product_id,
        language=data.language,
        platform=data.platform,
        title=result["title"],
        description=result["description"],
        keywords=result.get("keywords", [])
    )
    
    db.add(listing)
    db.commit()
    db.refresh(listing)
    
    return listing


@router.get("/product/{product_id}", response_model=List[ListingResponse])
def get_product_listings(product_id: int, db: Session = Depends(get_db)):
    """Get all listings for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    listings = db.query(Listing).filter(
        Listing.product_id == product_id
    ).order_by(Listing.created_at.desc()).all()
    
    return listings


@router.post("/analyze/{product_id}")
def analyze_product(product_id: int, db: Session = Depends(get_db)):
    """Generate AI analysis for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    analysis = llm_service.analyze_product(product)
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "analysis": analysis
    }


@router.post("/video-script/{product_id}")
def generate_video_script(
    product_id: int,
    language: str = "en",
    duration: int = 30,
    db: Session = Depends(get_db)
):
    """Generate video script for product promotion"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    script = llm_service.generate_video_script(
        product=product,
        language=language,
        duration_seconds=duration
    )
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "language": language,
        "duration_seconds": duration,
        "script": script
    }


@router.post("/batch-generate")
def batch_generate_listings(
    product_ids: List[int],
    languages: List[str],
    platform: str,
    db: Session = Depends(get_db)
):
    """Generate listings for multiple products and languages"""
    results = []
    
    for product_id in product_ids:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            continue
        
        for language in languages:
            try:
                result = llm_service.generate_listing(
                    product=product,
                    language=language,
                    platform=platform
                )
                
                if "error" not in result:
                    listing = Listing(
                        product_id=product_id,
                        language=language,
                        platform=platform,
                        title=result["title"],
                        description=result["description"],
                        keywords=result.get("keywords", [])
                    )
                    db.add(listing)
                    results.append({
                        "product_id": product_id,
                        "language": language,
                        "status": "success"
                    })
                else:
                    results.append({
                        "product_id": product_id,
                        "language": language,
                        "status": "error",
                        "error": result["error"]
                    })
            except Exception as e:
                results.append({
                    "product_id": product_id,
                    "language": language,
                    "status": "error",
                    "error": str(e)
                })
    
    db.commit()
    
    return {
        "total": len(results),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "error"]),
        "results": results
    }
