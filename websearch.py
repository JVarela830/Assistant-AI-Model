from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def search_web(query):
    try:
        wrapper = DuckDuckGoSearchAPIWrapper()

        raw_results = wrapper.results(query, max_results=6)
        
        if not raw_results:
            return None

        cleaned_context = ""
        for i, result in enumerate(raw_results, 1):
            title = result.get('title', 'No Title')
            snippet = result.get('snippet', 'No Summary')
            
            cleaned_context += f"Result {i}:\nTitle: {title}\nSummary: {snippet}\n\n"
            
        return cleaned_context.strip()
        
    except Exception as e:
        print(f"Erro ao pesquisar na web: {e}")
        return None