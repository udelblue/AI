import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent

st.title("Agent with tools")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def generate_response(question):
    llm = OpenAI(temperature=0, streaming=True, api_key=openai_api_key)

    # prompt for reasoning based tool
    word_problem_template = """You are a reasoning agent tasked with solving t he user's logic-based questions. Logically arrive at the solution, and be factual. In your answers, clearly detail the steps involved and give the final answer. Provide the response in bullet points. Question  {question} Answer"""

    math_assistant_prompt = PromptTemplate(
        input_variables=["question"],
        template=word_problem_template
    )
    # chain for reasoning based tool
    word_problem_chain = LLMChain(llm=llm,
                                    prompt=math_assistant_prompt)
    # reasoning based tool                              
    word_problem_tool = Tool.from_function(name="Reasoning Tool",
                                            func=word_problem_chain.run,
                                            description="Useful for when you need to answer logic-based/reasoning questions."
                                            )
    # calculator tool for arithmetics
    problem_chain = LLMMathChain.from_llm(llm=llm)
    math_tool = Tool.from_function(name="Calculator",
                                    func=problem_chain.run,
                                    description="Useful for when you need to answer numeric questions. This tool is only for math questions and nothing else. Only input math expressions, without text",
                                    )

    # Wikipedia Tool
    wikipedia = WikipediaAPIWrapper()
    wikipedia_tool = Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="A useful tool for searching the Internet to find information on world events, issues, dates, "
                    "years, etc. Worth using for general topics. Use precise questions.",
    )
    
    agent = initialize_agent(
     tools=[wikipedia_tool, math_tool, word_problem_tool], llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,handle_parsing_errors=True
    )
    response = agent.run(question)
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