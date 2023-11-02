from langchain.utilities import GoogleSearchAPIWrapper
from langchain.tools import Tool

_search = GoogleSearchAPIWrapper()
search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=_search.run,
)
