
import streamlit as st
import requests
from hugchat import hugchat
from hugchat.login import Login

# huggingface credentials required
huggingface_email =  ''
huggingface_password = ''


# User login Area
with st.sidebar:
    st.title("Omdena AI Assistant")
    # User need to login with hugging face credentials  
    st.write("Enter Huggingface Login Credentials")  
    email = st.text_input('Enter email:', type='password')
    passwd = st.text_input('Enter password:', type='password')       
    if (email and passwd):    
        huggingface_email = email
        huggingface_password = passwd        
        st.success("Please procced....")    



# Grant authorization and instantiate the chat
def grant_authorization_for_chat(user_query, huggingface_email, huggingface_password):
    
    sign = Login(huggingface_email, huggingface_password)
    try:
        cookies = sign.login()
    except Exception as e:
        st.error(e)
        return
    # Handle cookies
    cookie_path_dir = "./Cookies"
    sign.saveCookiesToDir(cookie_path_dir)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
    # Check if login credentials are valid
    if not cookies:
        st.warning('Please enter your valid credentials!')
        return
  
    return chatbot.chat(user_query)

    
# Store responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "Omdena assistant", "content": "Welcome! How may I help you today?"}]  

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if user_query := st.chat_input(disabled=not (huggingface_email and huggingface_password)):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)        
               
# Response
if st.session_state.messages[-1]["role"] != "Omdena assistant":
    with st.chat_message("Omdena assistant"):        
            response = grant_authorization_for_chat(user_query, huggingface_email, huggingface_password) 
            st.write(response) 
    message = {"role": "Omdena assistant", "content": response}
    st.session_state.messages.append(message)


