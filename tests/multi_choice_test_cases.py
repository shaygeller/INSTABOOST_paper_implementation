"""
INSTABOOST Multi-Choice Extraction Test Cases

This module provides test cases for evaluating the effectiveness of INSTABOOST
in improving instruction following for multi-choice extraction tasks.
"""

# ============================================================================
# TEST CASE 1: Product Category Classification
# ============================================================================

PRODUCT_CATEGORY_TEST = {
    "name": "Product Category Classification",
    "instruction": """
You are an AI assistant designed to help with product categorization. Your task is to analyze product descriptions and classify them into exactly one of the following categories:

1. Electronics
2. Clothing
3. Home & Kitchen
4. Beauty & Personal Care
5. Sports & Outdoors
6. Books
7. Toys & Games
8. Automotive

IMPORTANT INSTRUCTIONS:
- Read the product description carefully
- Choose EXACTLY ONE category from the list above that best matches the product
- Return ONLY the category name as your answer (e.g., "Electronics")
- Do not include any additional text, explanations, or formatting in your response
- If a product could fit multiple categories, choose the one that is most specific or appropriate

Answer with ONLY the category name.
""",
    "query": """
Product Description:
"The UltraSlim X7 Laptop features a 14-inch 4K display, 16GB RAM, 512GB SSD, and the latest Intel Core i7 processor. With a battery life of up to 12 hours and weighing only 2.5 pounds, it's perfect for professionals on the go. Includes two USB-C ports, HDMI output, and a backlit keyboard."

Answer:
""",
    "description": "A multi-choice extraction task where the model needs to classify a product into exactly one of eight categories. The correct answer is 'Electronics'. This tests the model's ability to follow instructions to return only the category name without additional text."
}

# ============================================================================
# TEST CASE 2: Sentiment Analysis
# ============================================================================

SENTIMENT_ANALYSIS_TEST = {
    "name": "Customer Review Sentiment Analysis",
    "instruction": """
You are an AI assistant designed to help with sentiment analysis of customer reviews. Your task is to analyze the sentiment of a customer review and classify it into exactly one of the following categories:

1. Very Positive
2. Positive
3. Neutral
4. Negative
5. Very Negative

IMPORTANT INSTRUCTIONS:
- Read the customer review carefully
- Choose EXACTLY ONE sentiment category from the list above
- Return ONLY the sentiment category as your answer (e.g., "Positive")
- Do not include any additional text, explanations, or formatting in your response
- Consider the overall tone, specific words used, and context of the review

Answer with ONLY the sentiment category.
""",
    "query": """
Customer Review:
"I've been using this product for about three weeks now. It works as advertised, but nothing special. The price is reasonable for what you get. Setup was straightforward, though the instructions could have been clearer. It does the job, but I wouldn't say I'm particularly impressed or disappointed."

Answer:
""",
    "description": "A multi-choice extraction task where the model needs to classify a customer review into exactly one of five sentiment categories. The correct answer is 'Neutral'. This tests the model's ability to analyze text sentiment and follow instructions to return only the category without additional text."
}

# ============================================================================
# TEST CASE 3: Medical Symptom Urgency
# ============================================================================

MEDICAL_URGENCY_TEST = {
    "name": "Medical Symptom Urgency Classification",
    "instruction": """
You are an AI assistant designed to help with preliminary medical triage. Your task is to analyze a patient's reported symptoms and classify the urgency level into exactly one of the following categories:

1. Emergency (Seek immediate medical attention)
2. Urgent (See a doctor within 24 hours)
3. Semi-Urgent (See a doctor within a few days)
4. Routine (Schedule a regular appointment)
5. Self-Care (Can be managed at home)

IMPORTANT INSTRUCTIONS:
- Read the patient's symptoms carefully
- Choose EXACTLY ONE urgency level from the list above
- Return ONLY the urgency level as your answer (e.g., "Urgent")
- Do not include any additional text, explanations, or formatting in your response
- Do not provide medical advice beyond the urgency classification

Answer with ONLY the urgency level.
""",
    "query": """
Patient Symptoms:
"I've had a mild headache for the past three days that comes and goes. Over-the-counter pain relievers help temporarily. No fever, no visual disturbances, no nausea. I've been able to work and sleep normally, though I do notice the headache gets worse when I'm staring at my computer screen for long periods. I've been drinking water regularly and getting adequate sleep."

Answer:
""",
    "description": "A multi-choice extraction task where the model needs to classify patient symptoms into exactly one of five urgency levels. The correct answer is 'Routine' or 'Self-Care'. This tests the model's ability to analyze medical symptoms and follow instructions to return only the urgency level without additional text or medical advice."
}

# ============================================================================
# TEST CASE 4: Programming Language Identification
# ============================================================================

PROGRAMMING_LANGUAGE_TEST = {
    "name": "Programming Language Identification",
    "instruction": """
You are an AI assistant designed to help with code analysis. Your task is to identify the programming language of a given code snippet and classify it into exactly one of the following languages:

1. Python
2. JavaScript
3. Java
4. C++
5. Ruby
6. PHP
7. Swift
8. Go
9. Rust

IMPORTANT INSTRUCTIONS:
- Analyze the code snippet carefully
- Choose EXACTLY ONE programming language from the list above
- Return ONLY the programming language name as your answer (e.g., "Python")
- Do not include any additional text, explanations, or formatting in your response
- Focus on syntax, keywords, and language-specific patterns

Answer with ONLY the programming language name.
""",
    "query": """
Code Snippet:
```
function calculateTotal(items) {
  return items
    .filter(item => item.price > 0)
    .map(item => item.price * item.quantity)
    .reduce((total, itemTotal) => total + itemTotal, 0);
}

const cart = [
  { name: 'Widget', price: 9.99, quantity: 2 },
  { name: 'Gadget', price: 14.99, quantity: 1 },
  { name: 'Doohickey', price: 4.99, quantity: 3 }
];

console.log(`Total: $${calculateTotal(cart).toFixed(2)}`);
```

Answer:
""",
    "description": "A multi-choice extraction task where the model needs to identify the programming language of a code snippet from nine options. The correct answer is 'JavaScript'. This tests the model's ability to analyze code syntax and follow instructions to return only the language name without additional text."
}

# ============================================================================
# TEST CASE 5: Movie Genre Classification
# ============================================================================

MOVIE_GENRE_TEST = {
    "name": "Movie Genre Classification",
    "instruction": """
You are an AI assistant designed to help with movie classification. Your task is to analyze a movie plot summary and classify it into exactly one of the following primary genres:

1. Action
2. Comedy
3. Drama
4. Horror
5. Science Fiction
6. Fantasy
7. Romance
8. Thriller
9. Documentary

IMPORTANT INSTRUCTIONS:
- Read the movie plot summary carefully
- Choose EXACTLY ONE primary genre from the list above
- Return ONLY the genre name as your answer (e.g., "Comedy")
- Do not include any additional text, explanations, or formatting in your response
- If a movie could fit multiple genres, choose the one that seems most dominant

Answer with ONLY the genre name.
""",
    "query": """
Movie Plot Summary:
"In the year 2157, humanity has established colonies on Mars after Earth became increasingly uninhabitable due to climate change. The story follows Dr. Elena Reyes, a brilliant scientist who discovers an ancient alien artifact buried beneath the Martian surface. As her team investigates the mysterious object, they inadvertently activate it, opening a portal to another dimension. Strange phenomena begin occurring throughout the colony, and crew members start disappearing one by one. Elena races against time to understand the artifact's purpose and close the portal before whatever is coming through can threaten not just the Mars colony, but all of humanity."

Answer:
""",
    "description": "A multi-choice extraction task where the model needs to classify a movie plot into exactly one of nine genre categories. The correct answer is 'Science Fiction'. This tests the model's ability to analyze narrative content and follow instructions to return only the genre name without additional text."
}

# List of all multi-choice extraction test cases
MULTI_CHOICE_TEST_CASES = [
    PRODUCT_CATEGORY_TEST,
    SENTIMENT_ANALYSIS_TEST,
    MEDICAL_URGENCY_TEST,
    PROGRAMMING_LANGUAGE_TEST,
    MOVIE_GENRE_TEST,
]
