import openai
import streamlit as st
from utils import ChatSession

def main():
    st.title('Financial Bank Advisor Chatbot')

    # Load the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["api_key"]

    # Initialize the AdvisorGPT. (Move this outside of the button click handler)
    sessionAdvisor = ChatSession(gpt_name='Advisor')

    # Instruct GPT to become a financial advisor.
    sessionAdvisor.inject(
        line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
        role="user"
    )
    sessionAdvisor.inject(line="Ok.", role="assistant")

    # Create a Streamlit text input for user input with a unique key
    user_input = st.text_input("User:", key="user_input")

    # Create a Streamlit button with a unique key
    if st.button("Send", key="send_button"):
        # Update the chat session with the user's input
        sessionAdvisor.chat(user_input=user_input, verbose=False)

        # Get the chat history, which includes the chatbot's response
        chat_history = sessionAdvisor.messages

        # Extract the chatbot's response from the last message in the history
        advisor_response = chat_history[-1]['content'] if chat_history else ""

        # Display the chatbot's response with text wrapping
        st.markdown(f'**Advisor:** {advisor_response}', unsafe_allow_html=True)

    # Create a new chat button with a unique key
    if st.button("New Chat", key="new_chat_button"):
        # Clear the chat session
        sessionAdvisor = ChatSession(gpt_name='Advisor')
        sessionAdvisor.inject(
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
            role="user"
        )
        sessionAdvisor.inject(line="Ok.", role="assistant")

        # Clear the user input
        user_input = ""

        # Clear the chat history
        st.session_state.messages = []

    # Create an exit chat button with a unique key
    if st.button("Exit Chat", key="exit_chat_button"):
        # Clear the user input
        user_input = ""

        # Clear the chat history
        st.session_state.messages = []

    # Add the user input and chatbot response to the chat history
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": advisor_response})

    # Display the chat history
    st.chat(st.session_state.messages)

if __name__ == "__main__":
    main()
