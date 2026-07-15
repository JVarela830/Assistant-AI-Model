from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime, timedelta
import sys  
import json
import os

import database
import websearch


def generate_search_query(user_question, model):
    current_date = datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""
    You are an expert search query generator for a search engine.
    Convert the user's question into 2 to 5 highly effective search keywords.
    
    Rules:
    1. Convert relative dates (today, yesterday, etc.) using the reference: Today is {current_date}.
    2. Remove conversational words ("tell me", "who was", "what is", "please", etc.).
    3. If the question asks about a past event, tournament, battle, or competition, ALWAYS append one highly relevant search modifier (e.g., "winner", "result", "date", "summary", "finalists" or "history") to get factual pages.
    
    Examples:
    - "Who won Euro 2004?" -> "Euro 2004 final winner"
    - "Which teams were in the 2010 final?" -> "World Cup 2010 final"
    - "What happened in the Treaty of Windsor?" -> "Treaty of Windsor history summary"
    
    User Question: {user_question}
    Search Query (Output ONLY the keywords, nothing else):"""
    
    fast_model = model.bind(options={"temperature": 0.0, "num_predict": 20})
    query = fast_model.invoke(prompt).strip().replace('"', '')
    return query


def type_of_search(query, model):
    prompt = f"""
    Analyze the user query and classify its intent.
    You must answer with exactly one word: "INTERNET", "MEMORY", or "CASUAL".

    Rules:
    - "INTERNET": The query is a factual question about world events, history, sports, weather, celebrities, or general knowledge (e.g., "Who played Euro 2004 final?", "What is the capital of France?", "What is the name of the president of Portugal?").
    - "MEMORY": The query is asking about the user, their personal life, pets, family, or things they said before (e.g., "What is the name of my dog?", "Where do I live?", "What is my favorite color?").
    - "CASUAL": Simple greetings, thank yous, or casual chat (e.g., "hello", "how are you", "thanks", "ok").

    Query: {query}
    Class:"""
    
    # Usamos o modelo rápido com temperatura 0 para decidir
    fast_model = model.bind(options={"temperature": 0.0, "num_predict": 5})
    decision = fast_model.invoke(prompt).strip().upper()
    return decision


def main():
    model = OllamaLLM(model="qwen2.5:3b")
    current_date = datetime.now().strftime("%B %d, %Y")

    template = f"""
    You are a friendly assistant robot. 
    Today's date is: {current_date}

    Rely strictly on the provided context below to answer. 
    Pay extreme attention to dates! Match the exact date requested by the user with the facts in the context.
    If the context does not have information for the exact date requested, say you don't know.

    Context: {{context}}

    User: {{question}}
    Assistant:"""

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    while True:
        question = input("Ask anything (q to leave): ")
        print("\n")
        if question == "q":
            break
        else:

            intent = type_of_search(question, model)
            print(f"[DEBUG INTENT] A intenção detetada foi: {intent}")

            context = ""

            if intent == "INTERNET":
                # Força a pesquisa web!
                optimized_query = generate_search_query(question, model)
                print(f"[INFO] Query otimizada: '{optimized_query}'")
                print("[INFO] A pesquisar na internet...\n")
                
                result_web = websearch.search_web(optimized_query)
                if result_web:
                    context = result_web

            elif intent == "MEMORY":
                # Procura apenas na Base de Dados Local!
                relevant_data = database.search_data(question)
                print(f"[DEBUG BD] Conteúdo retornado da BD: '{relevant_data}'")
                
                if relevant_data and str(relevant_data).strip() not in ["", "None", "[]"]:
                    context = relevant_data
                    print("[INFO] Usando memória local...\n")
                else:
                    print("[INFO] Memória vazia para esta pergunta...\n")

            else:
                # CASUAL (Conversa normal, sem contexto)
                print("[INFO] Conversa informal...\n")

            print("Robot: ", end="")
            
            #streaming option
            for chunk in chain.stream({"context": context, "question": question}):
                print(chunk, end="", flush=True)
            
            print("\n\n" + "-"*50 + "\n")

            database.update_database(question)


if __name__ == "__main__":
    main()