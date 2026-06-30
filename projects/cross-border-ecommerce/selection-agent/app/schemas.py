"""Pydantic schemas for API"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models import FunnelStage, ProductStatus, Category


class ProductBase(BaseModel):
    name: str = Field(..., description="产品名称（中文）")
    name_en: Optional[str] = Field(None, description="英文名称")
    category: Category = Field(..., description="品类")
    
    source_url: Optional[str] = None
    image_url: Optional[str] = None
    source_platform: Optional[str] = Field(None, description="来源平台（1688等）")
    
    cost_price_cny: float = Field(..., description="采购成本（元）")
    weight_g: int = Field(0, description="重量（克）")
    
    target_markets: List[str] = Field(default=[], description="目标市场")
    target_platforms: List[str] = Field(default=[], description="目标平台")
    
    notes: Optional[str] = None
    tags: List[str] = Field(default=[], description="标签")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    category: Optional[Category] = None
    source_url: Optional[str] = None
    image_url: Optional[str] = None
    source_platform: Optional[str] = None
    cost_price_cny: Optional[float] = None
    weight_g: Optional[int] = None
    funnel_stage: Optional[FunnelStage] = None
    status: Optional[ProductStatus] = None
    target_markets: Optional[List[str]] = None
    target_platforms: Optional[List[str]] = None
    scores: Optional[dict] = None
    total_score: Optional[float] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class ProductResponse(ProductBase):
    id: int
    funnel_stage: FunnelStage
    status: ProductStatus
    scores: dict
    total_score: float
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProfitAnalysisCreate(BaseModel):
    product_id: int
    platform: str = Field(..., description="平台")
    market: str = Field(..., description="市场")
    selling_price_usd: float = Field(..., description="售价（美元）")
    cost_price_cny: Optional[float] = Field(None, description="成本（元），不填则用产品成本")
    exchange_rate: float = Field(7.2, description="汇率")
    shipping_cost_usd: float = Field(0, description="物流成本（美元）")
    platform_fee_pct: float = Field(0.06, description="平台佣金比例")
    ad_cost_pct: float = Field(0.20, description="广告成本比例")
    notes: Optional[str] = None


class ProfitAnalysisResponse(BaseModel):
    id: int
    product_id: int
    platform: str
    market: str
    selling_price_usd: float
    cost_price_cny: float
    cost_price_usd: float
    shipping_cost_usd: float
    platform_fee_usd: float
    ad_cost_usd: float
    gross_profit_usd: float
    gross_margin_pct: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class ListingCreate(BaseModel):
    product_id: int
    language: str = Field(..., description="语言代码（en, th, vi等）")
    platform: str = Field(..., description="平台")


class ListingResponse(BaseModel):
    id: int
    product_id: int
    language: str
    platform: str
    title: str
    description: str
    keywords: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
