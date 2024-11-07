from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()  # Assuming your API key is set in the environment variables

# Initialize Flask app
app = Flask(__name__)

def ai_chatbot():
    try:
        # Load the training data from the file and create a vector store
        file = client.files.create(file=open("training_data.txt", "rb"), purpose='assistants')
        vector_store = client.beta.vector_stores.create(
            name="Training Data",
            file_ids=[file.id]
        )
        assistant = client.beta.assistants.create(
            model="gpt-4o-mini",
            instructions="You are a helpful assistant for Morgan State University computer science students. You have access to a file to answer student questions about the computer science program.",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            temperature=0.7,
            top_p=1
        )
        return assistant
    except Exception as e:
        return f"Error: {str(e)}"

# Create assistant instance once and reuse
assistant = ai_chatbot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def message():
    try:
        user_input = request.json.get("message")
        
        if not user_input:
            return jsonify({"error": "No input provided."}), 400

        # Creating a thread and sending user input
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=user_input,
        )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        messages = client.beta.threads.messages.list(run.thread_id)
        response_text = messages.data[0].content[0].text.value

        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
