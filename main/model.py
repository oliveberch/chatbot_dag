from langchain.llms.deepinfra import DeepInfra
from langchain_experimental.chat_models import Llama2Chat
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI
from dotenv import load_dotenv
import os

def get_chat_model(model:str):
    load_dotenv()
    if(model == "llama2"):
        llm = DeepInfra(
        model_id="meta-llama/Llama-2-70b-chat-hf"
        )
        model = Llama2Chat(llm=llm)
    if(model=="openai"):
        model = ChatOpenAI(temperature=0.6)
    
    return model

def get_llm(llm:str):
    load_dotenv()
    if(llm == "llama2"):
        llm = DeepInfra(
        model_id="meta-llama/Llama-2-70b-chat-hf"
        )
    if(llm=="openai"):
        llm = ChatOpenAI(temperature=0.6)
    
    return llm


    
