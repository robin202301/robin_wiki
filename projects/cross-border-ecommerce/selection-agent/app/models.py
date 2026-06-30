"""Database models"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


class FunnelStage(str, enum.Enum):
    L1 = "L1"  # 数据海选
    L2 = "L2"  # 数据筛选
    L3 = "L3"  # AI评估
    L4 = "L4"  # 小批量测品
    L5 = "L5"  # 爆品放大


class ProductStatus(str, enum.Enum):
    CANDIDATE = "candidate"
    TESTING = "testing"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCALING = "scaling"


class Category(str, enum.Enum):
    ACCESSORY = "accessory"  # 精品配饰
    BEAUTY_TOOL = "beauty_tool"  # 美妆工具


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    name_en = Column(String(200))
    category = Column(SQLEnum(Category), nullable=False)
    
    # Source info
    source_url = Column(String(500))
    image_url = Column(String(500))
    source_platform = Column(String(50))  # 1688, 拼多多, etc
    
    # Pricing
    cost_price_cny = Column(Float, nullable=False)
    weight_g = Column(Integer, default=0)
    
    # Funnel tracking
    funnel_stage = Column(SQLEnum(FunnelStage), default=FunnelStage.L1)
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.CANDIDATE)
    
    # Target markets and platforms (JSON arrays)
    target_markets = Column(JSON, default=list)
    target_platforms = Column(JSON, default=list)
    
    # Scoring (JSON with breakdown)
    scores = Column(JSON, default=dict)
    total_score = Column(Float, default=0)
    
    # Metadata
    notes = Column(Text)
    tags = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProfitAnalysis(Base):
    __tablename__ = "profit_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True, nullable=False)
    
    # Market & Platform
    platform = Column(String(50), nullable=False)
    market = Column(String(50), nullable=False)
    
    # Pricing (all in USD except where noted)
    selling_price_usd = Column(Float, nullable=False)
    cost_price_cny = Column(Float, nullable=False)
    exchange_rate = Column(Float, default=7.2)
    cost_price_usd = Column(Float, nullable=False)
    
    # Costs
    shipping_cost_usd = Column(Float, default=0)
    platform_fee_pct = Column(Float, default=0.06)
    platform_fee_usd = Column(Float, default=0)
    ad_cost_pct = Column(Float, default=0.20)
    ad_cost_usd = Column(Float, default=0)
    
    # Results
    gross_profit_usd = Column(Float, nullable=False)
    gross_margin_pct = Column(Float, nullable=False)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True, nullable=False)
    
    language = Column(String(10), nullable=False)  # zh, en, th, vi, etc
    platform = Column(String(50), nullable=False)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    keywords = Column(JSON, default=list)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
