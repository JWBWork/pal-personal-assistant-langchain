from dotenv import load_dotenv
load_dotenv()  # noqa

from fire import Fire
from loguru import logger

from src.llm import get_agent
from src.llm.tools.notion import (complete_todo, complete_todos, get_all_todos,
                                  save_sub_todo, save_todo)


def run(verbose: bool = False):
    logger.info("initializing agent ...")
    system_message = """
    Your purpose is to store and track todos for your user

    Use your best judgement when naming and tagging todos
    """
    agent = get_agent(
        system_message,
        get_all_todos,
        save_todo,
        save_sub_todo,
        complete_todo,
        complete_todos,
        verbose=verbose
    )
    logger.info("done!")
    while True:
        try:
            user_input = input("\n💬: ")
            response = agent.run(user_input)
            logger.info(response)
        except KeyboardInterrupt:
            logger.info("\nBye! 👋")
            break


if __name__ == "__main__":
    logger.info("starting Fire")
    Fire(run)
