import streamlit as st
import agents.sales_agent as sales_agent
import agents.service_agent as service_agent
import agents.general_agent as general_agent

import random

st.set_page_config(
    page_title="BrightSpeed",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title('BrightSpeed')

names = ["Ajay", "John", "Jane", "Mary"]  
agent = random.choice(names)

if 'chat' not in st.session_state:
  st.session_state['chat'] = [{
    "content": f"Hi, you've reached {agent}. How can I help you today?",
    "role": "ai"
  }]

user_input = st.chat_input('message:', key= "user_input")
if user_input:
  st.session_state['chat'].append({
    "content": user_input,
    "role": "user"
  })

  # call classifier to get agent
  
  agent = service_agent.get_agent()
  agent_response = agent.invoke({user_input})
  st.session_state['chat'].append({
    "content": agent_response['output'],
    "role": "ai"
  })
if st.session_state['chat']:
  for i in range(0, len(st.session_state['chat'])):
    user_message = st.session_state['chat'][i]
    st.chat_message(user_message["role"]).write(user_message["content"])