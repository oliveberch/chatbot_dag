from langchain.agents import ConversationalChatAgent, AgentExecutor
from bs_agents.vectordb_tool import get_vectordb_tool
from bs_agents.greetuser_tool import get_greet_user_tool
from bs_agents.general_tool import  get_general_tool
from model import get_chat_model
from bs_agents.agent_chat_memory import get_memory
from bs_agents.general_agent_prompt import general_agent_prompt
from langchain.agents import load_tools
from model import get_llm


def get_tools():
    tools = load_tools([], llm = get_llm('llama2'))
    tools.append(get_vectordb_tool()) 
    tools.append(get_greet_user_tool())
    tools.append(get_general_tool())
    return tools

# def get_agent():
model = get_chat_model('llama2')
system_message = general_agent_prompt

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
    memory = get_memory(),
    handle_parsing_errors=True
)
    # return agent_execution


