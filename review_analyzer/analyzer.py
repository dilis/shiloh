from typing import Dict, List
import json

class ProductAnalyzer:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def analyze_reviews(self, reviews: List[Dict]) -> Dict:
        """
        Analyze product reviews using LLM to extract insights
        """
        # TODO: Implement review analysis
        pass

    def analyze_review(self, review: Dict) -> Dict:
        """
        Analyze a single review using LLM to extract insights
        """
        review_distilled = {
            "title": review["title"],
            "review": review["description"],
            "rating": review["rating"]
        }
        prompt = f"""For the review data enclosed in triple backticks and expressed in JSON do the following:
1. Identify the language
2. Identify the sentiment as positive, neutral, or negative
3. Identify any actionable insights, if there is
The output should be in plain JSON with no display/printing formatting and with the following fields: "language", "sentiment", "actionable_insights" as list of string.
    ```{json.dumps(review_distilled)}```
"""
        response = self.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        resp_json = json.loads(response.choices[0].message.content)
        resp_json["chat_id"] = response.id
        resp_json["prompt_token_count"] = response.usage.prompt_tokens
        resp_json["response_token_count"] = response.usage.completion_tokens
        resp_json["model"] = response.model
        return resp_json