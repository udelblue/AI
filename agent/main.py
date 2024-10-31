import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools

st.title("Agent")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def generate_response(input_text):
    llm = OpenAI(temperature=0, streaming=True, api_key=openai_api_key)
    tools = load_tools(["ddg-search"])
    agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    response = agent.run(input_text)
    st.info(response)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)