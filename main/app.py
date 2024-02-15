import streamlit as st
from  agents import sales_agent, service_agent, general_agent
from classifier import classifier

import random


logo_path = "assets/logo.jpg"

st.set_page_config(
    page_title="brightspeed",
    page_icon = logo_path,
    initial_sidebar_state="auto",
)

st.title('Chatbot')


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
  category = classifier(user_input)

  # make calls based on agent
  if category == 'service':
    # service
    agent = service_agent.get_agent()
    agent_response = agent.invoke({user_input})
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"
    })
  elif category  == 'sales':
    # sales
    agent = sales_agent.get_agent()
    agent_response = agent.invoke({user_input})
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"
    })
  else:
    # general
    agent = general_agent.get_agent()
    agent_response = agent.invoke({user_input})
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"
    })

  

if st.session_state['chat']:
  for i in range(0, len(st.session_state['chat'])):
    user_message = st.session_state['chat'][i]
    st.chat_message(user_message["role"]).write(user_message["content"])


# stream lit theme:

# [theme]
# primaryColor="#ff5d22"
# backgroundColor="#ffca33"
# secondaryBackgroundColor="#ffffff"
# textColor="#000000"
# font="monospace"
