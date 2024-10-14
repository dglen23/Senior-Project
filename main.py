from openai import OpenAI

# Initialize the OpenAI API key (replace with your actual API key)
client = OpenAI()
def message(user_input):
    assistant = ai_chatbot()
    assistantId=assistant.id
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
  thread.id,
  role="user",
  content=user_input,
    )
    run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id= assistantId,
    )
    messages = client.beta.threads.messages.list(run.thread_id)
    response = messages.data[0].content[0].text.value
    return response

def ai_chatbot():
    try:
        # Make a request to OpenAI's API using the `gpt-4o-mini` model
        file = client.files.create(file=open("training_data.txt", "rb"), purpose = 'assistants')
        vector_store = client.beta.vector_stores.create(
            name="Training Data",
            file_ids=[file.id]
            )
        assistant = client.beta.assistants.create(
            model="gpt-4o-mini",
            instructions="You are a helpful assistant for Morgan State University computer science students. You have access to a file to answer student questions about the computer science program.",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = more random)
            top_p=1,  # Controls diversity via nucleus sampling
        )

        # Extract and return the response from the model
        #return response.choices[0].messages
        return assistant

    except Exception as e:
        return f"Error: {str(e)}"


def chat():
    print("AI Chatbot: Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        # Call the chatbot function to get the AI response
        response = message(user_input)
        print(f"AI: {response}")


if __name__ == "__main__":
    chat()

