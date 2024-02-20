from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory,SQLChatMessageHistory
from datetime import datetime
import os

chat_history = SQLChatMessageHistory(session_id=datetime.now().strftime("%m/%d/%Y, %H:%M"), connection_string=os.getenv('CHAT_SQL_CONNECTION_URL'))

def get_memory():
    return ConversationBufferWindowMemory(k=3, memory_key='chat_history', return_messages=True, chat_memory=chat_history)


