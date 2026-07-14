from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#Specify the model
model = OllamaLLM(model="qwen2.5:1.5b")

template = """
You are an assistant model ready to answer questions

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    question = input("Ask anything (q to leave):")
    if question == "q":
        break
    else:
        result = chain.invoke({"question": question})