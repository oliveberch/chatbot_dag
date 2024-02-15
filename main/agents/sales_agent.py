from langchain.agents import ConversationalChatAgent, AgentExecutor
from agents.vectordb_tool import get_vectordb_tool
from model import get_chat_model
from agents.agent_chat_memory import get_memory
from agents.sales_agent_prompt import sales_agent_prompt
from langchain.agents import load_tools
from model import get_llm



def get_tools():
    tools = load_tools([], llm = get_llm('openai'))
    tools.append(get_vectordb_tool())
    return tools

def get_agent():
    model = get_chat_model('openai')
    memory = get_memory()
    system_message = sales_agent_prompt

    agent_definition = ConversationalChatAgent.from_llm_and_tools(
        llm = model,
        tools  = get_tools(),
        system_message = system_message
    )

    agent_execution = AgentExecutor.from_agent_and_tools(
        agent=agent_definition,
        llm=model,
        tools= get_tools(),
        handle_parsing_erros= True,
        verbose = True,
        max_iterations=3,
        memory = memory,
        handle_parsing_errors=True
    )
    return agent_execution



