# def get_chatbot_respnse(client, model_name, messages,temprature =0 ):
#     input_messages = []
#     for message in messages:
#         input_messages.append({"role": message['role'],"content": message['content']})
    
#     response = client.chat.completions.create(
#         model= model_name,
#         messages=input_messages,
#         temperature= temprature,
#         top_p= 0.8,
#         max_tokens=2000
#     ).choices[0].message.content

#     return response

# def get_embedding(embedding_client,model_name,text_input):
#     output = embedding_client.embeddings.create(input = text_input,model=model_name)
    
#     embedings = []
#     for embedding_object in output.data:
#         embedings.append(embedding_object.embedding)

#     return embedings


# def double_check_json_output(client,model_name,json_string):
#     prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
#     If the Json is correct just return it.

#     If there is any text before or after the json string, remove it.
#     Do NOT return a single letter outside of the json string.
#     Make sure that each key is enclosed in double quotes.
#      The first thing you write should be open curly brace of the json string and the last thing you write should be the closing curly brace of the json string.

#     You should check the JSON string for the following text between triple backticks:
#     ```
#     {json_string}

#     ```
#     """

#     messages = [{"role": "user", "content": prompt}]
#     response = get_chatbot_respnse(client,model_name,messages)
#     response = response.replace("```","" )

#     return response
import json
import re

def get_chatbot_respnse(client, model_name, messages, temperature=0, use_json_mode=False):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message['role'], "content": message['content']})
    
    params = {
        "model": model_name,
        "messages": input_messages,
        "temperature": temperature,
        "top_p": 0.8,
        "max_tokens": 2000
    }
    
    # Add JSON mode if requested
    if use_json_mode:
        params["response_format"] = {"type": "json_object"}
    
    response = client.chat.completions.create(**params).choices[0].message.content
    return response


def get_embedding(embedding_client, model_name, text_input):
    output = embedding_client.embeddings.create(input=text_input, model=model_name)
    
    embeddings = []
    for embedding_object in output.data:
        embeddings.append(embedding_object.embedding)
    
    return embeddings


def extract_json_from_text(text):
    """Extract JSON object from text that might contain extra content"""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Find the first { and last }
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    
    return text


def double_check_json_output(client, model_name, json_string):
    """Validate and clean JSON output"""
    # First, try to extract JSON from the text
    cleaned = extract_json_from_text(json_string)
    
    # Try to parse it
    try:
        json.loads(cleaned)
        return cleaned  # It's valid, return it
    except json.JSONDecodeError:
        # If parsing fails, ask LLM to fix it
        prompt = f"""Fix this JSON and return ONLY the valid JSON object. No explanations, no text before or after.

JSON to fix:
```
{cleaned}
```

Return ONLY the corrected JSON starting with {{ and ending with }}."""

        messages = [{"role": "user", "content": prompt}]
        response = get_chatbot_respnse(client, model_name, messages, temperature=0, use_json_mode=True)
        response = extract_json_from_text(response)
        
        return response