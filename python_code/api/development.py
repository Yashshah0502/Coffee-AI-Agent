from agents import (GuardAgent, ClassificationAgent, DetailsAgent)
import os

def main():
    pass

if __name__ == "__main__":
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    

    messages = []

    while True:
        os.system('clear' if os.name == 'nt' else 'clear')

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
