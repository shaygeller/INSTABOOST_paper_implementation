"""
INSTABOOST Tokens Per Second Test

This module provides test cases for measuring the tokens per second (TPS)
performance of the three model variants:
1. Original model (without INSTABOOST)
2. INSTABOOST with all layers
3. INSTABOOST with middle layers only

The test uses random prompts to evaluate generation speed.
"""

import time
from typing import Dict, Any, List

# ============================================================================
# Random Test Prompts
# ============================================================================

RANDOM_PROMPT_1 = {
    "name": "Technical Documentation",
    "instruction": """
You are a technical documentation writer. Your task is to create clear, concise, and accurate documentation for software products. Follow these guidelines:

1. Use simple, direct language
2. Include code examples where appropriate
3. Organize content with clear headings and subheadings
4. Explain technical concepts in accessible terms
5. Focus on practical use cases and examples

Your documentation should be comprehensive enough for technical users but accessible to those with less technical background.
""",
    "query": """
Write documentation for a REST API endpoint that allows users to upload images to a cloud storage service. Include details about request parameters, authentication requirements, response formats, and error handling.
"""
}

RANDOM_PROMPT_2 = {
    "name": "Creative Storytelling",
    "instruction": """
You are a creative fiction writer specializing in short stories. Your writing should be engaging, evocative, and character-driven. When crafting stories, consider:

1. Creating memorable, three-dimensional characters
2. Establishing a clear setting and atmosphere
3. Developing a compelling conflict or tension
4. Using vivid, sensory language
5. Crafting dialogue that reveals character and advances the plot

Your stories should have a clear beginning, middle, and end, even in a short format. Focus on creating an emotional impact and a satisfying conclusion.
""",
    "query": """
Write a short story about someone who discovers an unusual ability on their 30th birthday. The story should take place in a small coastal town and include an encounter with a mysterious stranger.
"""
}

RANDOM_PROMPT_3 = {
    "name": "Data Analysis",
    "instruction": """
You are a data analyst providing insights based on statistical analysis. When analyzing data and presenting findings, you should:

1. Begin with a clear summary of key findings
2. Present data in a structured, logical manner
3. Explain your methodology and analytical approach
4. Highlight patterns, trends, and anomalies
5. Provide actionable recommendations based on the data

Your analysis should be objective, thorough, and accessible to non-technical stakeholders while maintaining analytical rigor.
""",
    "query": """
Analyze the following e-commerce data and provide insights:
- Monthly sales have increased by 15% year-over-year
- Customer acquisition cost has decreased by 8%
- Mobile purchases now account for 65% of all transactions
- Average order value is $42 for new customers and $67 for returning customers
- Cart abandonment rate is 28%, down from 35% last quarter

What trends do you observe, and what recommendations would you make to the business?
"""
}

# List of all tokens per second test prompts
TOKENS_PER_SECOND_TEST_PROMPTS = [
    RANDOM_PROMPT_1,
    RANDOM_PROMPT_2,
    RANDOM_PROMPT_3,
]

def calculate_tokens_per_second(
    tokens_generated: int,
    generation_time: float
) -> float:
    """
    Calculate tokens per second.
    
    Args:
        tokens_generated: Number of tokens generated
        generation_time: Time taken for generation in seconds
        
    Returns:
        Tokens per second
    """
    return tokens_generated / generation_time if generation_time > 0 else 0

def estimate_token_count(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    This is a rough approximation - actual token count depends on the specific tokenizer.
    
    Args:
        text: The text to estimate token count for
        
    Returns:
        Estimated token count
    """
    # A very rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4
