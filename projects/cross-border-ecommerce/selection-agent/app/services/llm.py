"""LLM integration for listing generation and analysis"""
from openai import OpenAI
from typing import List, Dict
from app.models import Product
from app.config import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_api_base
        )
        self.model = settings.llm_model
    
    def generate_listing(
        self,
        product: Product,
        language: str,
        platform: str
    ) -> Dict[str, any]:
        """
        Generate product listing in specified language for platform.
        
        Args:
            product: Product instance
            language: Language code (en, th, vi, etc)
            platform: Platform name
        
        Returns:
            Dict with title, description, keywords
        """
        language_names = {
            "en": "English",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "ms": "Malay",
            "ru": "Russian",
            "zh": "Chinese"
        }
        
        lang_name = language_names.get(language, "English")
        
        # Build prompt based on product info
        prompt = f"""You are an expert e-commerce copywriter specializing in {platform} listings.

Product Information:
- Name: {product.name}
- English Name: {product.name_en or product.name}
- Category: {product.category.value}
- Cost: {product.cost_price_cny} CNY
- Weight: {product.weight_g}g

Generate a compelling {platform} product listing in {lang_name}.

Requirements:
1. Title: Max 80 characters, include key search terms, highlight main benefit
2. Description: 150-300 words, focus on benefits, include specifications, use emojis sparingly
3. Keywords: 10-15 relevant search keywords (in {lang_name})

Target market: {'Southeast Asia' if language in ['th', 'vi', 'id', 'ms'] else 'Russia' if language == 'ru' else 'Global'}

Format your response as JSON:
{{
  "title": "...",
  "description": "...",
  "keywords": ["keyword1", "keyword2", ...]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional e-commerce copywriter. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON from response
            import json
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: extract JSON block
                import re
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    # Last resort: create structured response
                    result = {
                        "title": product.name_en or product.name,
                        "description": content,
                        "keywords": []
                    }
            
            return result
            
        except Exception as e:
            # Return error info
            return {
                "title": product.name_en or product.name,
                "description": f"Error generating listing: {str(e)}",
                "keywords": [],
                "error": str(e)
            }
    
    def analyze_product(self, product: Product) -> str:
        """
        Generate AI analysis and recommendations for a product.
        """
        prompt = f"""Analyze this cross-border e-commerce product and provide strategic recommendations:

Product: {product.name}
Category: {product.category.value}
Cost: {product.cost_price_cny} CNY
Weight: {product.weight_g}g
Source: {product.source_platform or 'Unknown'}
Notes: {product.notes or 'None'}

Scores:
- Video Suitability: {product.scores.get('video_suitability', 0)}/100
- Profit Potential: {product.scores.get('profit_potential', 0)}/100
- Competition: {product.scores.get('competition', 0)}/100
- Trend: {product.scores.get('trend', 0)}/100
- Supply Chain: {product.scores.get('supply_chain', 0)}/100
- Total: {product.total_score}/100

Provide analysis in the following structure:
1. 优势分析 (Strengths)
2. 风险因素 (Risks)
3. 视频内容建议 (Video Content Suggestions) - 3 specific video ideas
4. 定价策略 (Pricing Strategy)
5. 目标市场优先级 (Target Market Priority)
6. 下一步行动 (Next Steps)

Respond in Chinese.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cross-border e-commerce consultant. Provide actionable, specific advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def generate_video_script(
        self,
        product: Product,
        language: str,
        duration_seconds: int = 30
    ) -> str:
        """
        Generate AI video script for product promotion.
        """
        language_names = {
            "en": "English",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "ms": "Malay",
            "ru": "Russian"
        }
        
        lang_name = language_names.get(language, "English")
        
        prompt = f"""Create a {duration_seconds}-second video script for promoting this product on TikTok/short video platforms:

Product: {product.name}
Category: {product.category.value}
Key Features: {product.notes or 'Fashion accessory / Beauty tool'}

Requirements:
1. Language: {lang_name}
2. Hook (first 3 seconds): Attention-grabbing opening
3. Product showcase (10-15 seconds): Key features and benefits
4. Call to action (last 5 seconds): Clear CTA

Format:
[HOOK]
...

[SHOWCASE]
...

[CTA]
...

Keep it natural, engaging, and suitable for AI voice-over.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a video script writer specializing in e-commerce short videos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating script: {str(e)}"


# Singleton instance
llm_service = LLMService()
