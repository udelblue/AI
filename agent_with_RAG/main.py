import os
import streamlit as st

from langchain_openai.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent

from langchain.retrievers import GoogleVertexAISearchRetriever
from langchain_community.chat_models import ChatVertexAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


st.title("Agent with RAG")

# Get project, data store, and model type from env variables
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
data_store_id = os.environ.get("DATA_STORE_ID")
model_type = os.environ.get("MODEL_TYPE")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


def generate_response(question):
    if not data_store_id:
        raise ValueError(
            "No value provided in env variable 'DATA_STORE_ID'. "
            "A  data store is required to run this application."
        )

    # Set LLM and embeddings
    model = ChatVertexAI(model_name=model_type, temperature=0.0)

    # Create Vertex AI retriever
    retriever = GoogleVertexAISearchRetriever(
        project_id=project_id, search_engine_id=data_store_id
    )

    # RAG prompt
    template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # RAG
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | model
        | StrOutputParser()
    )

    # Add typing for input
    class Question(BaseModel):
        __root__: str

    chain = chain.with_types(input_type=Question)
    
    st.info(response)

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





