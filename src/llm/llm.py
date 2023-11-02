from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import HumanInputRun
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder


def get_agent(system_message, *tools, **kwargs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    memory_key = "chat_history"
    chat_history = MessagesPlaceholder(variable_name=memory_key)
    memory = ConversationBufferMemory(
        memory_key=memory_key, return_messages=True)

    agent = initialize_agent(
        llm=llm,
        tools=[HumanInputRun(), *tools],
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        agent_kwargs={
            "system_message": system_message,
            "memory_prompts": [chat_history],
            "input_variables": [
                "input", "agent_scratchpad", memory_key
            ]
        },
        **kwargs
    )
    return agent
