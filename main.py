from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


import database

#Specify the model
model = OllamaLLM(model="qwen2.5:1.5b")

template = """
You are an assistant model ready to answer questions

Here is the context to make a better answer: {context}

Here is the question to answer: {question}
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

        if(relevant_data):
             result = chain.invoke({"context": relevant_data, "question": question})
        else:
            result = chain.invoke({"question": question})

        database.update_database(question)

        print(result)
        print("\n\n")


    