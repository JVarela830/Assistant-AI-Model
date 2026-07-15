from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


import database

#Specify the model
model = OllamaLLM(model="qwen2.5:1.5b")

template = """
You are a friendly assistant robot. The user may ask you questions or simply share facts about their life for you to remember.

Context of past memories (if applicable): {context}

User's message: {question}

Instructions:
- If the user is only sharing a fact (e.g., "My cat is black"), reply in a friendly, natural, and brief way, confirming that you have memorized this information.
- If the user asks a question, use the provided context to answer accurately.
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    question = input("Ask anything (q to leave):")
    print("\n\n")
    if question == "q":
        break
    else:
        relevant_data = database.search_data(question)

        context = relevant_data if relevant_data else "Not find data related."
        result = chain.invoke({"context": context, "question": question})

        database.update_database(question)

        print(result)
        print("\n\n")


    