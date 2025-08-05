def get_chatbot_respnse(client, model_name, messages,temprature =0 ):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message['role'],"content": message['content']})
    
    response = client.chat.completions.create(
        model= model_name,
        messages=input_messages,
        temperature= temprature,
        top_p= 0.8,
        max_tokens=2000
    ).choices[0].message.content

    return response

def get_embedding(embedding_client,model_name,text_input):
    output = embedding_client.embeddings.create(input = text_input,model=model_name)
    
    embedings = []
    for embedding_object in output.data:
        embedings.append(embedding_object.embedding)

    return embedings
