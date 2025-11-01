from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
import wikipedia

@tool
def web_search(query: str) -> str:
    """Search the web for current information and news.
    
    Args:
        query: The search query string
    """
    try:
        search = DuckDuckGoSearchRun()
        return search.run(query)
    except Exception as e:
        return f"Search error: {str(e)}"

@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for detailed encyclopedic information about topics.
    
    Args:
        query: The topic to search for on Wikipedia
    """
    try:
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=5, auto_suggest=True)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        # Return first option if multiple results
        return wikipedia.summary(e.options[0], sentences=5)
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for: {query}"
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

@tool
def save_text_to_file(data: str) -> str:
    """Saves structured research data to a text file.
    
    Args:
        data: The research content to save
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"research_output_{timestamp}.txt"
        formatted_text = f"--- Research Output ---\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{data}\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted_text)
        
        return f"✅ Data successfully saved to {filename}"
    except Exception as e:
        return f"❌ Save error: {str(e)}"

# Export tools for main.py
search_tool = web_search
wiki_tool = wikipedia_search
save_tool = save_text_to_file
