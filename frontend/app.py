
import streamlit as st
import shelve
from utils.api_calls import generate_text_llm
from config import Config


st.title("Amazon Documentacion Chatbot")

USER_AVATAR = "👤"
BOT_AVATAR = "🖥️"

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("sessions", {})

# Save chat history to shelve file
def save_chat_history(sessions):
    with shelve.open("chat_history") as db:
        db["sessions"] = sessions

# Initialize or load chat history
if "sessions" not in st.session_state:
    st.session_state.sessions = load_chat_history()

if "current_chat_session" not in st.session_state:
    st.session_state.current_chat_session = 1

if st.session_state.current_chat_session not in st.session_state.sessions:
    st.session_state.sessions[st.session_state.current_chat_session] = [{'role': 'assistant', 'content': ''}]

if "messages" not in st.session_state:
    st.session_state.messages = st.session_state.sessions[st.session_state.current_chat_session]

# Sidebar with a button to delete chat history
with st.sidebar:

    with open('static/style.css') as f:
        st.sidebar.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown('#')
    st.markdown('#')


    if st.button("Open New Chat"):
        # Save the current chat history
        st.session_state.sessions[st.session_state.current_chat_session] = st.session_state.messages

        # Increment the chat session number
        st.session_state.current_chat_session = max(st.session_state.sessions.keys()) +1

        # Load the new chat history or create an empty list if not exists
        st.session_state.sessions[st.session_state.current_chat_session] = [{'role': 'assistant', 'content': ''}]

        # Load the new chat history
        st.session_state.messages = st.session_state.sessions[st.session_state.current_chat_session]

    
    if st.session_state.sessions[1]:
        auxiliar_list = []
        dict_to_side = {}
        for i,elem in st.session_state.sessions.items():
            if len(elem) > 1:
                auxiliar_list.append(elem[1]['content'])
                dict_to_side[i] = elem[1]['content']
            else :
                auxiliar_list.append(elem[0]['content'])
                dict_to_side[i] = elem[0]['content']

        if auxiliar_list:
            st.markdown('#')
            selected_text = st.sidebar.radio("Select Chat Session", auxiliar_list, key="selected option", index=st.session_state.current_chat_session-1)
            selected_chat_session = next((key for key, value in dict_to_side.items() if value == selected_text), None)

            # Load and display the selected chat session
            if selected_chat_session and selected_chat_session != st.session_state.current_chat_session:
                st.session_state.messages = st.session_state.sessions[selected_chat_session]
                st.session_state.current_chat_session = selected_chat_session
                st.rerun()
    
    st.markdown('#')
    st.markdown('#')
    if st.button("Delete Chat History"):
        st.session_state.sessions[st.session_state.current_chat_session] = [{'role': 'assistant', 'content': ''}]
        st.session_state.messages = st.session_state.sessions[st.session_state.current_chat_session]
        save_chat_history(st.session_state.sessions)



if st.session_state.sessions[st.session_state.current_chat_session]:

    for message in st.session_state.messages[1:]:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
       
        with st.spinner("Generating an answer based on your documentation ..."):
            full_response = generate_text_llm(Config.BACKEND_HOST,
                                              st.session_state["messages"][-1],
                                              Config.TOKEN_API)

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    if st.session_state.messages:
        st.rerun()


# Save chat history after each interaction
st.session_state.sessions[st.session_state.current_chat_session] = st.session_state.messages
save_chat_history(st.session_state.sessions)
