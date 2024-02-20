import streamlit as st
from  bs_agents.general_agent import agent_execution as general
from  bs_agents.sales_agent import agent_execution as sales
from  bs_agents.service_agent import agent_execution as service
from classifier import classifier_gopika, classifier_azaan
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGSMITH_KEY')
os.environ["LANGCHAIN_PROJECT"] = "genai_chatbot"

logo_path = "main\static\logo.jpg"

st.set_page_config(
    page_title="brightspeed",
    page_icon = logo_path,
    initial_sidebar_state="auto",
)

st.title('Chatbot')

if 'chat' not in st.session_state:
  st.session_state['chat'] = [{
    "content": "Hi, you've reached Brightspeed chat support. How can I help you today?",
    "role": "ai"
  }]

user_input = st.chat_input('Message', key= "user_input")

if user_input:
  st.session_state['chat'].append({
    "content": user_input,
    "role": "user"
  })

  # call classifier model to get agent for query
  # category = classifier_gopika(user_input)
  category = classifier_azaan(user_input)
  
  # make calls based on agent
  if category == 'service':
    # service
    agent = service
    agent_response = agent.invoke({'input':user_input})
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"
    })
  elif category  == 'sales':
    # sales
    agent = sales
    agent_response = agent.invoke({'input':user_input})
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"
    })
  else:
    # general
    agent = general
    agent_response = agent.invoke({'input':user_input})
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"
    })

  
if st.session_state['chat']:
  for i in range(0, len(st.session_state['chat'])):
    user_message = st.session_state['chat'][i]
    st.chat_message(user_message["role"]).write(user_message["content"])
