from src.llm.llm import get_agent


def get_default_agent():
    from src.llm.tools.notion import save_todo, find_similar_todo, save_sub_todo
    return get_agent(
        save_todo, find_similar_todo, save_sub_todo
        # verbose=True
    )


agent = get_default_agent()
