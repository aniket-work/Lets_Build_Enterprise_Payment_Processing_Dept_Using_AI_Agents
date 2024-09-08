import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any
from nodes.constant import GROQ_API_KEY, MODEL_NAME

load_dotenv()


class LLMService:
    def __init__(self):
        api_key = os.getenv(GROQ_API_KEY)
        self.llm = ChatGroq(model=MODEL_NAME, groq_api_key=api_key)
        self.json_parser = JsonOutputParser()

    def generate_response(self, prompt_template: str, input_variables: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=list(input_variables.keys())
        )
        chain = prompt | self.llm | self.json_parser
        return chain.invoke(input_variables)


llm_service = LLMService()
