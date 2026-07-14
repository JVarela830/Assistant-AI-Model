from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#Specify the model
model = OllamaLLM(model="qwen2.5:1.5b")