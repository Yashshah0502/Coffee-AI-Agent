import os
import dotenv
from copy import deepcopy
from openai import OpenAI
from .utils import get_chatbot_respnse, double_check_json_output
import json

dotenv.load_dotenv()

class GuardAgent():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"), 
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")

    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
        You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
        Your task is to determine whether the user is asking something relevant to the coffee shop or not.
        The user is allowed to:
        1. Ask questions about the coffee shop, like location, working hours, menue items and coffee shop related questions.
        2. Ask questions about menue items, they can ask for ingredients in an item and more details about the item.
        3. Make an order.
        4. Ask about recommendations of what to buy.

        The user is NOT allowed to:
        1. Ask questions about anything else other than our coffee shop.
        2. Ask questions about the staff or how to make a certain menue item.

        Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
        {
          "chain of thought": "...",
          "decision": "allowed" or "not allowed",
          "message": ""
        }
        """

        input_message = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output = get_chatbot_respnse(self.client, self.model_name, input_message)
        chatbot_output = double_check_json_output(self.client, self.model_name, chatbot_output)

        output = self.postprocess(chatbot_output)
        return output

    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {
                "agent": "guard_agent",
                "guard_decision": output['decision']
            }
        }

        return dict_output
