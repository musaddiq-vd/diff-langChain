from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock

# LLM: Calls Amazon Bedrock model
llm = ChatBedrock(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# Parser: Converts AI response to plain string
parser = StrOutputParser()

# Step 1: Generate explanation
prompt1 = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words."
)

# Step 2: Summarize the explanation
prompt2 = ChatPromptTemplate.from_template(
    "Summarize the following in 3 bullet points:\n\n{text}"
)

# Chain 1: Topic -> Explanation
chain1 = prompt1 | llm | parser

# Chain 2: Explanation -> Summary
chain2 = prompt2 | llm | parser

# Run Step 1
explanation = chain1.invoke({
    "topic": "Amazon Bedrock"
})

# Run Step 2
summary = chain2.invoke({
    "text": explanation
})

# Print final summary
print(summary)





"""
Flow of the programm : -----------

Input
  ↓
Prompt 1 (Explain)
  ↓
Bedrock LLM
  ↓
Parser
  ↓
Explanation
  ↓
Prompt 2 (Summarize)
  ↓
Bedrock LLM
  ↓
Parser
  ↓
Final Summary
"""