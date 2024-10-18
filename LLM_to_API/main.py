from dotenv import load_dotenv
import os
from langchain import Langchain


load_dotenv()  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 



# Initialize Langchain with the Gemini API key
lc = Langchain(api_key=GEMINI_API_KEY)

# Confirm connection
status = lc.check_connection()
print("Connection to Gemini:", status)

prompt = "Summarize the key points of artificial intelligence in bullet points."
response = lc.generate(prompt)
print(response)

structured_prompt = """
# Task
Provide an overview of natural language processing (NLP).

# Requirements
- Use bullet points.
- Keep it concise (no more than five points).
- Use a professional tone.
"""

response = lc.generate(structured_prompt)
print(response)



"""
# Create an APITool instance:
   api_tool = APITool(
    name="My API",
    description="A tool that interacts with a specific API.",
    api_key="YOUR_API_KEY",  # Replace with your actual API key
    endpoint="https://api.example.com/v1",  # Replace with the API endpoint
)


#Create an LLM instance:
llm = OpenAI(temperature=0.7)

# Combine the LLM and API tool into a chain:
from langchain.chains import ToolChain
chain = ToolChain(llm=llm, tools=[api_tool])

# Call the chain with a prompt:
response = chain.run("Use the API to get the weather in New York City.")
print(response)

"""