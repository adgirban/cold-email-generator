import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model='llama-3.1-70b-versatile')

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from a job posting. Your job is to extract the following keys from the job posting in JSON format: 'role', 'experience', 'skills', 'description'.
            Only return valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={'page_data': cleaned_text})

        try:
            response = JsonOutputParser().parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return response if isinstance(response, list) else [response]
    
    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Heisenberg, a business development executive at Phetamine. Phetamine is an Software consulting company dedicated for seamless integration of business processes through automated tools.
            Over our experience, we have developed a strong portfolio of clients and projects.
            Your job is to write a cold email to the client regarding the job mentioned above descibing the capabilities of fulfilling their needs.
            Also add the most relevant links from the portfolio that you think will be helpful for the client. {link_list}
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        response = chain_email.invoke(input={'job_description': str(job), 'link_list': links})
        return response.content
