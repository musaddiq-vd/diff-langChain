from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI()

llm = init_chat_model(
    "amazon.nova-pro-v1:0",
    model_provider="bedrock"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant, please answer to user questions"),
    ("user", "question: {question}")
])

chain = prompt | llm | StrOutputParser()

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    response = chain.invoke({"question": query.question})
    return {"answer": response}