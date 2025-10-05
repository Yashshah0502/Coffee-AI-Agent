from agents import (GuardAgent, ClassificationAgent, DetailsAgent, AgentProtocol, OrderTakingAgent, 
                    RecommendationAgent)
import os
import sys
import pathlib
from typing import Dict

folder_path = pathlib.Path(__file__).parent.resolve()

def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()

    # ✅ Create one shared recommendation agent instance
    recommendation_agent = RecommendationAgent(
        os.path.join(folder_path, 'recommendation_objects/apriori_recommendations.json'),
        os.path.join(folder_path, 'recommendation_objects/popularity_recommendation.csv')
    )

    # ✅ Pass it properly to OrderTakingAgent
    agent_dict : Dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "recommendation_agent": recommendation_agent,
        "order_taking_agent": OrderTakingAgent(recommendation_agent)
    }

    messages = []

    while True:
        # os.system('clear' if os.name == 'nt' else 'clear')

        print("\n\nPrint Messages ...............")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})

        # Guard agent decision
        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response['memory']['guard_decision'] == 'not allowed':
            messages.append(guard_agent_response)
            continue

        # Classification agent response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent_response['memory']['classification_decision']
        print(f"Chosen Agent: {chosen_agent}")

        # Get the response from the chosen agent
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        print("Agent response : ", response)

        messages.append(response)


# if __name__ == "__main__":
#     recommendation_agent = RecommendationAgent(
#         os.path.join(folder_path, 'recommendation_objects/apriori_recommendations.json'),
#         os.path.join(folder_path, 'recommendation_objects/popularity_recommendation.csv')
#     )

#     print(recommendation_agent.get_apriori_recommendation(['Latte']))

if __name__ == "__main__":
    main()
