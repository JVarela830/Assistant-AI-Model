#External libraries
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

#Local Files
import database
import websearch

def fast_model(model, tokens):
    return model.bind(
        options={
            "temperature": 0.0, 
            "num_predict": tokens
            }
        )

def generate_search_query(user_question, model):
    """Specify the parameters to do a search in DuckDuckGo"""

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
    
    query = fast_model(model, 20).invoke(prompt).strip().replace('"', '')

    return query


def determine_search_type(query, model):
    """Identify what type of data the model needs to process"""

    prompt = f"""
    Analyze the user query and classify its intent.
    You must answer with exactly one word: "INTERNET", "DATABASE", or "CASUAL".

    Rules:
    - "INTERNET": The query is a factual question about world events, history, sports, weather, celebrities, or general knowledge (e.g., "Who played Euro 2004 final?", "What is the capital of France?", "What is the name of the president of Portugal?").
    - "DATABASE": The query is asking about the user, their personal life, pets, family, or things they said before (e.g., "What is the name of my dog?", "Where do I live?", "What is my favorite color?").
    - "CASUAL": Simple greetings, thank yous, or casual chat (e.g., "hello", "how are you", "thanks", "ok").

    Query: {query}
    Class:"""
    
    decision = fast_model(model, 5).invoke(prompt).strip().replace('"', '').upper()

    return decision


def model_template(model):
    """Define the template of the model"""

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
    
    return chain


def internet_search(query, model):
    """Execute the DuckDuckGo search"""

    optimized_query = generate_search_query(query, model)
    #print(f"[INFO] Optimized Query: '{optimized_query}'")
    
    result_web = websearch.search_web(optimized_query)

    return result_web or ""
    

def database_search(query):
    """Execute the Database search"""

    relevant_data = database.search_data(query)
    #print(f"[DEBUG BD] Content from DB: '{relevant_data}'")
    
    if relevant_data and str(relevant_data).strip() not in ["", "None", "[]"]:
        return relevant_data
    else:
        print("[INFO] There's no data to this question\n")
        return ""


def save_database_data(query):
    """TODO: Check if the query is a question. If not, save it in database - Possible bug here (check later)"""

    if not query.strip().endswith("?"):
        database.add_document(query)
        print("[INFO] New personal data saved in DB!")


def process_query(search_type, query, model):
    """Identify the type of search (INTERNET OR DATABASE)"""

    context = ""

    if search_type == "INTERNET":
        context = internet_search(query, model)

    elif search_type == "DATABASE":
        context = database_search(query)

        save_database_data(query)

    else:
        print("[INFO] Casual Talk...\n")

    return context


def print_result(chain, query, result):
    """Print the result in streaming option"""
    print("AI: ", end="")
    
    #streaming option
    for chunk in chain.stream({"context": result, "question": query}):
        print(chunk, end="", flush=True)
    
    print("\n\n" + "-"*50 + "\n")


def menu(model, chain):
    """Waits the user input to process. Have an exit option"""
    while True:
        query = input("Ask anything (q to leave): ")

        print("\n")
        if query == "q":
            break
        else:
            search_type = determine_search_type(query, model)

            result = process_query(search_type, query, model)

            print_result(chain, query, result)            


def main():
    model = OllamaLLM(model="qwen2.5:3b")

    chain = model_template(model)

    menu(model, chain)



if __name__ == "__main__":
    main()