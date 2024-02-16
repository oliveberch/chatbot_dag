from langchain.agents import Tool

def greet_user_tool(user_name):
    """
    Tool to greet the user.

    Parameters:
    - user_name (str): The name of the user to greet.

    Returns:
    - str: Greeting message.
    """
    greeting_message = f"Hello, {user_name}! Welcome to BrightSpeed. How can I assist you today?"
    return greeting_message

def get_greet_user_tool():
    """
    Returns the LangChain tool for greeting users.

    Returns:
    - Tool: LangChain tool for greeting users.
    """
    tool = Tool(
        func=greet_user_tool,
        name="Greet User",
        description="Tool to greet users when they interact with the chatbot.",
        input_params=["user_name"],
        output_params=["greeting_message"],
    )
    return tool
