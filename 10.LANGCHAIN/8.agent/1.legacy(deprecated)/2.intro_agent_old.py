from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')