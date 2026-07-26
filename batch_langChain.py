from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

questions = [
    "What is RAG?",
    "What is Amazon Bedrock?",
    "What is OpenSearch?"
]

responses = llm.batch(questions)

for res in responses:
    print(res.content)