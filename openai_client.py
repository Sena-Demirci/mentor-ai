from openai import OpenAI
import os
from dotenv import load_dotenv
from ai_client import AIClient
from mentor_prompts import HINT_PROMPT, QUESTION_PROMPT, SOLUTION_PROMPT
from mentor_prompts import LEARN_PROMPT
from mentor_prompts import FOLLOW_UP_PROMPT
from mentor_prompts import FOLLOW_UP_HINT_PROMPT
from mentor_prompts import DEBUG_PROMPT
from mentor_prompts import FOLLOW_UP_DEBUG_PROMPT
from mentor_prompts import ROUTER_PROMPT
from mentor_prompts import PLANNING_PROMPT


class OpenAIClient(AIClient):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def get_a_hint(self, building, problem, code):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": HINT_PROMPT},
                    {"role": "user", "content": f"What I'm building:\n{building}"},
                    {"role": "user", "content": f"Where I'm stuck:\n{problem}"},
                    {"role": "user", "content": f"My code:\n{code}"}
                ]
            )

            return response.choices[0].message.content

        except Exception:
            return (
                "Demo Hint\n\n"
                "Think about which variable should change every iteration.\n"
                "Try tracing your code step by step instead of changing the syntax."
            )
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


    def get_learning_explanation(self, topic):
        messages = [
            {"role": "system", "content": LEARN_PROMPT},
            {"role": "user", "content": topic}
        ]
        try:
           response = self.client.chat.completions.create(
               model="gpt-4.1-mini",
               messages  =  messages )

           return response.choices[0].message.content

        except Exception:
            return(
                "I couldn't reach the AI right now.\n\n"
                "Please check your internet connection or try again later."
            )


    def get_follow_up_answer(self, topic, explanation, question):
        messages = [
                {"role": "system", "content": FOLLOW_UP_PROMPT},
                {"role": "user", "content": topic},
                {"role": "assistant", "content": explanation},
                {"role": "user", "content": question}
        ]

        try:
           response = self.client.chat.completions.create(
               model="gpt-4.1-mini",
               messages  =  messages )

           return response.choices[0].message.content

        except Exception:
            return(
                "I couldn't reach the AI right now.\n\n"
                "Please check your internet connection or try again later."
            )

    def get_follow_up_hint(
            self,
            building,
            problem,
            code,
            previous_hint,
            follow_up_question
    ):
        messages = [
            {"role": "system", "content": FOLLOW_UP_HINT_PROMPT},
            {"role": "user", "content": f"What I'm building:\n{building}"},
            {"role": "user", "content": f"Where I'm stuck:\n{problem}"},
            {"role": "user", "content": f"My code:\n{code}"},
            {"role": "assistant", "content": previous_hint},
            {"role": "user", "content": follow_up_question}
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages = messages
            )
            return response.choices[0].message.content

        except Exception:
            return(
                "I couldn't reach the AI right now.\n\n"
                "Please try again later."
            )

    def get_debug_help(self, code, error):
        messages = [
            {"role": "system", "content": DEBUG_PROMPT},
            {"role": "user", "content": f"My code: \n{code}"},
            {"role": "user", "content": f"Error: \n{error}"},
        ]
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages = messages
            )

            return response.choices[0].message.content
        except Exception:
            return(
                "I couldn't reach the AI right now.\n\n"
                "Please try again later."
            )

    def get_follow_up_debug(
            self,
            code,
            error,
            previous_debug,
            follow_up_question
    ):
        messages = [
            {"role": "system", "content": FOLLOW_UP_DEBUG_PROMPT},
            {"role": "user", "content": f"My code:\n{code}"},
            {"role": "user", "content": f"Error:\n{error}"},
            {"role": "assistant", "content": previous_debug},
            {"role": "user", "content": follow_up_question}
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            return response.choices[0].message.content



        except Exception:

            return (

                "I couldn't reach the AI right now.\n\n"
                "Please try again later."

            )

    def classify_intent(self, message):

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": ROUTER_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content.strip().upper()

    def get_planning_response(self, history):

        messages = [
            {
                "role": "system",
                "content": PLANNING_PROMPT
            }
        ]

        messages.extend(history)

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        return response.choices[0].message.content.strip()




if __name__ == "__main__":
    client = OpenAIClient()
    answer = client.get_a_hint("How does a for loop work in Python?")
    print(answer)