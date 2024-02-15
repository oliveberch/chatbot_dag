from langchain.memory import ConversationBufferWindowMemory



memory = ConversationBufferWindowMemory(k=10, memory_key='chat_history', return_messages=True)
