import os
import streamlit as st

from langchain_openai.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from rag import chain

st.title("Agent with RAG")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def generate_response(question):
    chain = chain.invoke(question) 
    st.info(chain)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "I have 500 dollars and want to buy a toy priced at 355 dollars. Please let me know how much money I will have left after purchasing the toy. ",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)





