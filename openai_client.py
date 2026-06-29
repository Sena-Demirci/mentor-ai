from openai import OpenAI
import os
from dotenv import load_dotenv
from ai_client import AIClient
from mentor_prompts import HINT_PROMPT, QUESTION_PROMPT, SOLUTION_PROMPT


class OpenAIClient(AIClient):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def get_a_hint(self, question, code=""):
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": question},
                {"role": "system", "content": HINT_PROMPT}
            ]
        )
        return response.choices[0].message.content

    def get_a_question(self, question, code=""):
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": question},
                {"role": "system", "content": QUESTION_PROMPT}
            ]
        )
        return response.choices[0].message.content

    def get_a_solution(self, question, code=""):
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": question},
                {"role": "system", "content": SOLUTION_PROMPT}
            ]
        )
        return response.choices[0].message.content

    def get_a_direct_answer(self, question, code=""):
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    client = OpenAIClient()
    answer = client.get_a_hint("How does a for loop work in Python?")
    print(answer)