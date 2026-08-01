from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 

import streamlit as st

load_dotenv()

llm = init_chat_model(
    "amazon.nova-pro-v1:0",
    model_provider="bedrock"
)

prompt = ChatPromptTemplate.from_messages([
    ("system","you are a helpful assistant, please answer to usre questions"),
    ("user","question: {question}")
])

st.title("langchain-demo")
input_txt = st.text_input("search the topic u want")

chain = prompt | llm | StrOutputParser()

if input_txt:
    st.write(chain.invoke({"question":input_txt}))
