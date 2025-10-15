# import os
# import dotenv
# from copy import deepcopy
# from openai import OpenAI
# from .utils import get_chatbot_respnse, double_check_json_output
# import json

# dotenv.load_dotenv()

# class ClassificationAgent():
#     def __init__(self):
#         self.client = OpenAI(
#             api_key=os.getenv("RUNPOD_TOKEN"), 
#             base_url=os.getenv("RUNPOD_CHATBOT_URL")
#         )
#         self.model_name = os.getenv("MODEL_NAME")

#     def get_response(self, messages):
#         messages = deepcopy(messages)

#         system_prompt = """
#             You are a helpful AI assistant for a coffee shop application.
#             Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
#             1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menue items. Or listing items in the menu items. Or by asking what we have.
#             2. order_taking_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
#             3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should be used.

#             Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
#             {
#             "chain of thought": "go over each of the agents above and write some your thoughts about what agent is this input relevant to.",
#             "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those. and only write the word.,
#             "message": leave the message empty
#             }
#         """

#         input_message = [{"role": "system", "content": system_prompt}] 
#         input_message += messages[-3:]

#         chatbot_output = get_chatbot_respnse(self.client, self.model_name, input_message)
#         print("Raw Classification Output:", chatbot_output)
#         chatbot_output = double_check_json_output(self.client, self.model_name, chatbot_output)
#         print("After double-check:", chatbot_output)
#         output = self.postprocess(chatbot_output)

#         return output
#     def postprocess(self, output):
#         #print("Classification Output:" , output)
#         output = json.loads(output)
        
#         dict_output = {
#             "role": "assistant",
#             "content": output['message'],
#             "memory": {
#                 "agent": "classification_agent",
#                 "classification_decision": output['decision']
#             }
#         }

#         return dict_output

import os
import dotenv
from copy import deepcopy
from openai import OpenAI
from .utils import get_chatbot_respnse, double_check_json_output
import json

dotenv.load_dotenv()

class ClassificationAgent():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"), 
            base_url=os.getenv("RUNPOD_CHATBOT_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")

    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """You are a helpful AI assistant for a coffee shop application.
Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
1. details_agent: Answers questions about the coffee shop (location, delivery, hours, menu details, listing items)
2. order_taking_agent: Takes orders and has conversations about orders until complete
3. recommendation_agent: Gives recommendations about what to buy

Output ONLY valid JSON in this exact format:
{
  "chain of thought": "brief reasoning about which agent to use",
  "decision": "details_agent",
  "message": ""
}"""

        input_message = [{"role": "system", "content": system_prompt}] 
        input_message += messages[-3:]

        chatbot_output = get_chatbot_respnse(self.client, self.model_name, input_message, temperature=0, use_json_mode=True)
        # print("Raw Classification Output:", chatbot_output)
        chatbot_output = double_check_json_output(self.client, self.model_name, chatbot_output)
        # print("After double-check:", chatbot_output)
        output = self.postprocess(chatbot_output)

        return output
        
    def postprocess(self, output):
        output = json.loads(output)
        
        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {
                "agent": "classification_agent",
                "classification_decision": output['decision']
            }
        }

        return dict_output