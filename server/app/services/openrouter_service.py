# OpenRouter Service Module
# This module provides an interface to the OpenRouter AI API for personality assessment

import httpx
from app.config import settings
from typing import Dict, List, Any, Optional

class OpenRouterService:
    """Service class for interacting with OpenRouter AI API
    
    This class handles all AI-powered operations including:
    - Generating behavioral interview questions
    - Analyzing candidate responses
    - Creating comprehensive personality profiles
    
    The service uses OpenRouter's API to access advanced language models
    for natural language processing and analysis tasks.
    
    Attributes:
        api_key (str): Authentication key for OpenRouter API
        api_url (str): Base URL for OpenRouter API endpoints
        headers (dict): HTTP headers for API requests
    """
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.api_url = settings.OPENROUTER_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_questions(self, trait_category: str, count: int = 3) -> List[str]:
        """Generate behavioral questions for a specific personality trait."""
        prompt = f"""
        Generate {count} behavioral interview questions that assess a person's {trait_category}.
        These questions should help evaluate their personality traits related to {trait_category}.
        Return only the questions in a numbered list without any additional text.
        """
        
        response = await self._call_openrouter(prompt)
        # Parse the response to extract questions
        questions = self._parse_questions(response)
        return questions[:count]
    
    async def analyze_response(self, question: str, response: str, trait_category: str) -> Dict[str, Any]:
        """Analyze a candidate's response to a behavioral question."""
        prompt = f"""
        Analyze the following response to this behavioral question:
        
        Question: {question}
        Response: {response}
        
        This question is designed to assess the personality trait: {trait_category}
        
        Provide an analysis with the following:
        1. Score (0-100) for how strongly this response indicates the trait
        2. Brief explanation of the score
        3. Key behavioral indicators detected in the response
        
        Format the response as a JSON with keys: 'score', 'explanation', and 'indicators'.
        """
        
        result = await self._call_openrouter(prompt)
        # Parse JSON from the text response
        return self._extract_json(result)
    
    async def generate_personality_profile(self, all_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive personality profile based on all question responses."""
        # Prepare a summary of all the analyses to send to OpenRouter
        analyses_summary = "\n".join([
            f"Trait: {trait}, Score: {analysis['score']}, Explanation: {analysis['explanation']}"
            for trait, analysis in all_analyses.items()
        ])
        
        prompt = f"""
        Based on the following personality trait analyses:
        
        {analyses_summary}
        
        Generate a comprehensive personality profile with:
        1. Big Five personality trait scores (0-100 for each: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
        2. Equivalent MBTI personality type
        3. Top 3 strengths
        4. Top 3 areas for improvement
        5. 3 career fields that might be a good fit
        
        Format the response as a JSON with keys: 'big_five', 'mbti', 'strengths', 'weaknesses', and 'career_recommendations'.
        """
        
        result = await self._call_openrouter(prompt)
        return self._extract_json(result)
    
    async def _call_openrouter(self, prompt: str) -> str:
        """Make a call to the OpenRouter API."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "anthropic/claude-3-opus-20240229",  # Or your preferred model
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.text}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    def _parse_questions(self, text: str) -> List[str]:
        """Parse generated questions from the API response."""
        # Simple parser for numbered list
        lines = text.strip().split("\n")
        questions = []
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                # Remove number/bullet and trim
                question = line.split(".", 1)[-1].strip() if "." in line else line[1:].strip()
                questions.append(question)
        
        return questions
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON data from the API response."""
        import json
        import re
        
        # Try to find JSON in the text
        try:
            # Look for text that appears to be JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # If no JSON format detected, try parsing the entire text
            return json.loads(text)
        except (json.JSONDecodeError, AttributeError):
            # Fallback with a basic structure if JSON parsing fails
            return {
                "error": "Failed to parse JSON response",
                "raw_text": text
            }