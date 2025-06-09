from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# Initialize LLM
llm = ChatOpenAI(temperature=0.3, model_name="gpt-4o-mini")

# Define prompt
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["document"],
    template="""
    You are a helpful assistant. Summarize the following document into a short, concise summary:

    DOCUMENT:
    {document}
    """
    )

def summarizer_agent(extracted_text: str) -> str:
    """
    Agent to summarize extracted text using LLM.

    Args:
        extracted_text (str): Text extracted from the PDF.

    Returns:
        str: Summary of the document.
    """
    prompt = SUMMARY_PROMPT.format(document=extracted_text[:3000])  # Truncate to avoid token limits
    messages = [HumanMessage(content=prompt)]
    summary = llm(messages).content
    return summary
