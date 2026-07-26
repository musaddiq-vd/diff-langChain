from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock

# LLM: Calls Amazon Bedrock model
llm = ChatBedrock(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# Prompt Template: Creates dynamic prompt using variables
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words."
)

# Output Parser: Converts AI response to plain string
parser = StrOutputParser()

# Chain: Connects all components into one pipeline
chain = prompt | llm | parser

# Execute chain with input
response = chain.invoke({
    "topic": "Amazon Bedrock"
})

# Print final output
print(response)



"""
Flow of the programm : -----------


Input
  ↓
Prompt 
  ↓
Bedrock LLM
  ↓
Output Parser
  ↓
Final text

"""