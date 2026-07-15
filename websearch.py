from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


def clean_context(raw_results):
    """Clean and returns only the Title and Summary of each raw result"""
    cleaned_context = []

    for i, result in enumerate(raw_results, start=1):

        title = result.get('title', 'No Title') 
        snippet = result.get('snippet', 'No Summary')

        cleaned_context.append(
            f"Result {i}:\n"
            f"Title: {title}\n"
            f"Summary: {snippet}"
        )

    return "\n\n".join(cleaned_context)


def search_web(query):
    """Search the best 6 results via DuckDuckGo to the query"""
    try:
        wrapper = DuckDuckGoSearchAPIWrapper()

        raw_results = wrapper.results(query, max_results=6)
        
        if not raw_results:
            return None

        context = clean_context(raw_results)

        return context
        
    except Exception as e:
        print(f"Error searching in web: {e}")
        return None