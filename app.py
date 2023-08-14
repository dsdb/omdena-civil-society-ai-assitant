import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="Omdena Civil Society Online Assitant")

# Set Credentials
user = st.secrets['USER']
token = st.secrets['PASS']

# Store responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "Omdena assistant", "content": "Welcome! How may I help you today?"}]  
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def get_response(usr_input, usr_email, usr_passwd):    
    sign = Login(user, token)
    cookies = sign.login()                      
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(usr_input)  

# User query
if user_query := st.chat_input(disabled=not (user and token)):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)        
               
# Response
if st.session_state.messages[-1]["role"] != "Omdena assistant":
    with st.chat_message("Omdena assistant"):        
            response = get_response(user_query, user, token) 
            st.write(response) 
    message = {"role": "Omdena assistant", "content": response}
    st.session_state.messages.append(message)