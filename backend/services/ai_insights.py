"""
AI Insights Service using Google Gemini
Generates natural language analysis of correlation results
"""

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Check if google-generativeai is available
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai not installed. AI insights will use fallback.")


class AIInsightsService:
    """Generate AI-powered insights using Google Gemini."""
    
    def __init__(self):
        """Initialize Gemini AI if available."""
        self.genai_available = GENAI_AVAILABLE
        
        if self.genai_available:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini AI initialized successfully")
            else:
                self.genai_available = False
                logger.warning("GEMINI_API_KEY not set. Using fallback insights.")
        else:
            self.model = None
    
    def generate_insight(self, correlation_data: Dict) -> Dict[str, str]:
        """
        Generate comprehensive AI analysis of correlation results.
        
        Args:
            correlation_data: Dictionary with correlation analysis results
            
        Returns:
            Dictionary with insight sections
        """
        if self.genai_available and self.model:
            return self._generate_ai_insight(correlation_data)
        else:
            return self._generate_fallback_insight(correlation_data)
    
    def _generate_ai_insight(self, data: Dict) -> Dict[str, str]:
        """Generate insight using Gemini AI."""
        try:
            prompt = self._build_prompt(data)
            
            response = self.model.generate_content(prompt)
            
            # Parse the response into sections
            text = response.text
            sections = self._parse_sections(text)
            
            logger.info("AI insight generated successfully")
            return sections
            
        except Exception as e:
            logger.error(f"Error generating AI insight: {e}")
            return self._generate_fallback_insight(data)
    
    def _build_prompt(self, data: Dict) -> str:
        """Build detailed prompt for Gemini."""
        correlation_value = data.get('correlation_value', 0)
        p_value = data.get('p_value', 1)
        sample_size = data.get('sample_size', 0)
        city = data.get('city', 'Unknown')
        symbol = data.get('symbol', 'Unknown')
        weather_var = data.get('weather_variable', 'temperature')
        stock_var = data.get('stock_variable', 'close_price')
        anomalies = data.get('anomalies_detected', 0)
        
        # Determine correlation strength
        abs_corr = abs(correlation_value)
        if abs_corr > 0.7:
            strength = "strong"
        elif abs_corr > 0.4:
            strength = "moderate"
        elif abs_corr > 0.2:
            strength = "weak"
        else:
            strength = "very weak"
        
        direction = "positive" if correlation_value > 0 else "negative"
        significant = "statistically significant" if p_value < 0.05 else "not statistically significant"
        
        prompt = f"""You are an expert financial and meteorological data analyst. Analyze the following correlation study:

**Study Parameters:**
- Location: {city}
- Stock: {symbol}
- Weather Variable: {weather_var}
- Stock Variable: {stock_var}
- Sample Size: {sample_size} data points
- Anomalies Detected: {anomalies}

**Statistical Results:**
- Correlation Coefficient (r): {correlation_value:.4f}
- This indicates a {strength} {direction} correlation
- P-value: {p_value:.4f}
- Statistical Significance: {significant} at α=0.05

Please provide a comprehensive analysis in exactly 4 sections:

**SECTION 1 - Statistical Interpretation:**
Explain what the correlation coefficient and p-value mean in plain language. Is this relationship meaningful?

**SECTION 2 - Potential Explanations:**
If there's any correlation (even weak), what could be the potential causal mechanisms or confounding factors? Be specific to {city} and {symbol}.

**SECTION 3 - Investment Implications:**
What should investors or analysts take away from this finding? Should they act on it or ignore it?

**SECTION 4 - Recommendations:**
Suggest 2-3 specific follow-up analyses that would provide deeper insights.

Keep each section concise (2-3 sentences). Be professional and data-driven."""

        return prompt
    
    def _parse_sections(self, text: str) -> Dict[str, str]:
        """Parse AI response into sections."""
        sections = {
            'statistical': '',
            'explanations': '',
            'implications': '',
            'recommendations': ''
        }
        
        # Try to parse sections from the response
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if 'statistical' in line_lower and ('interpretation' in line_lower or 'analysis' in line_lower):
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'statistical'
                current_content = []
            elif 'potential' in line_lower and ('explanation' in line_lower or 'mechanism' in line_lower):
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'explanations'
                current_content = []
            elif 'investment' in line_lower or 'implication' in line_lower:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'implications'
                current_content = []
            elif 'recommendation' in line_lower or 'follow-up' in line_lower:
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'recommendations'
                current_content = []
            elif current_section and line.strip() and not line.startswith('#'):
                current_content.append(line.strip())
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Fallback: if parsing failed, put everything in statistical
        if not any(sections.values()):
            sections['statistical'] = text.strip()
        
        return sections
    
    def _generate_fallback_insight(self, data: Dict) -> Dict[str, str]:
        """Generate rule-based insight when AI is unavailable."""
        correlation_value = data.get('correlation_value', 0)
        p_value = data.get('p_value', 1)
        sample_size = data.get('sample_size', 0)
        city = data.get('city', 'Unknown')
        symbol = data.get('symbol', 'Unknown')
        weather_var = data.get('weather_variable', 'temperature')
        stock_var = data.get('stock_variable', 'close_price')
        
        abs_corr = abs(correlation_value)
        
        # Strength classification
        if abs_corr > 0.7:
            strength = "strong"
            strength_desc = "a relationship worth investigating further"
        elif abs_corr > 0.4:
            strength = "moderate"
            strength_desc = "a noteworthy relationship"
        elif abs_corr > 0.2:
            strength = "weak"
            strength_desc = "a slight tendency"
        else:
            strength = "very weak"
            strength_desc = "minimal relationship"
        
        direction = "positive" if correlation_value > 0 else "negative"
        significant = p_value < 0.05
        
        # Statistical section
        statistical = f"The analysis reveals a {strength} {direction} correlation (r={correlation_value:.3f}) between {weather_var} in {city} and {symbol}'s {stock_var}, based on {sample_size} data points. "
        
        if significant:
            statistical += f"With a p-value of {p_value:.4f}, this relationship is statistically significant at the 95% confidence level, meaning there's less than a 5% chance this pattern occurred randomly."
        else:
            statistical += f"However, with a p-value of {p_value:.4f}, this relationship is not statistically significant, suggesting the observed pattern could be due to random chance rather than a true underlying relationship."
        
        # Explanations section
        if abs_corr > 0.3:
            explanations = f"Several factors could explain this correlation: {weather_var} might influence consumer behavior patterns that affect {symbol}'s sales, or both variables could be responding to seasonal trends. Additionally, {city}'s specific economic geography could create unique market dynamics."
        else:
            explanations = f"The weak correlation suggests that {weather_var} has minimal direct impact on {symbol}'s stock performance. Most stock price movements are driven by company fundamentals, market sentiment, and macroeconomic factors rather than local weather conditions."
        
        # Implications section
        if significant and abs_corr > 0.4:
            implications = f"Investors should note this relationship but avoid overweighting it in decision-making. While statistically significant, the correlation of {abs_corr:.2f} explains only {(abs_corr**2)*100:.1f}% of the variance. Consider this as one data point among many fundamental and technical factors."
        else:
            implications = f"From an investment perspective, this weak {('and non-significant' if not significant else '')} correlation should not influence trading decisions. Focus on traditional fundamental analysis, company earnings, and broader market trends rather than weather patterns for {symbol}."
        
        # Recommendations section
        recommendations = f"""For deeper analysis, consider: (1) Extending the study period to multiple years to identify seasonal patterns, (2) Comparing multiple cities to see if the relationship holds geographically, and (3) Analyzing {symbol}'s sector peers to determine if this is industry-wide or company-specific."""
        
        return {
            'statistical': statistical,
            'explanations': explanations,
            'implications': implications,
            'recommendations': recommendations
        }
