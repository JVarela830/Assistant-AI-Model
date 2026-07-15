from langchain_community.tools import DuckDuckGoSearchRun


def search_web(query):
    try:
        search = DuckDuckGoSearchRun()
        
        results = search.invoke(query)
        return results
    except Exception as e:
        print(f"Erro ao pesquisar na web: {e}")
        return None