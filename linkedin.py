
import json
# import requests
import openai
import os
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Using OpenAI API
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

with open('C:/Users/RUDRANIL/Desktop/OpenAI/Dealintent/scrapy_project/basic-scrapy-project/company_data.json', 'r') as file:
    data = json.load(file)

    documents = data['all_text']

documents=documents[503:-22000].replace('   ','')
# Get your splitter ready
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

# Split your docs into texts
# texts = text_splitter.split_documents(documents)

# print(documents[:3000])

# def linkedin_details(company):
    
#     prompt1 = f"""
#     Your task is to parse through the dictionary of informion found from linkedin website about {company}/
#     and finding out the details about the {company} like company description, company location/
#     number of employees, industry segments the company operates in, what and how many funding/
#     rounds the company has gone through.  
#     The format of your answer should be
#     Company Description: Description of the company in a summarized manner
#     Company Location: Location of the company
#     Number of employees: Total number of employees in the company
#     Industry of Operation: Industry segments the company operates in
#     Funding details: what and how many funding rounds the company has gone through.
    
#     Get all the details from the given below dictionary within backticks. 
#     Text in webpage: ```{text}```
#     """

#     response1 = get_completion(prompt1)
#     return response1

# ext = linkedin_details(company='microsoft')
# print(ext)

def extract_details(doc):
    # Creating an empty list to store details
    detail = [] 
    # Splitting the entrire into batches so that doesn't exceed openai api limit
    for i in range(1,(len(doc)//3000)+1):
        print(i)
        s1= doc[3000*(i-1):i*3000]
        prompt = f"""
        Your task is to parse through parts of text found from linkedin website about a company/
        and finding out the details about the like company description, company location/
        number of employees, industry segments the company operates in, what they usually post about,
        what and how many funding rounds the company has gone through.
        Please ignore all the texts which are not related to company like job advertisements or
        other information whic are not related to the company.
        Summarize all the relevent information in a paragraph
        Get all the details from the given below within backticks.
        backticks. 
        output as a list
        transcript: ```{s1}```
        """

        response = get_completion(prompt)
        detail.append(response)
    # Secondary prompt for reading all the ideas and summarizing those into final results
    prompt1 = f"""
    Your task is to parse through the summary of informion found from linkedin website about a company
    and finding out the details about the company like company description, company location/
    number of employees, industry segments the company operates in, what they usually post about,
    what and how many funding rounds the company has gone through.  
    The format of your answer should be
    Company Description: Description of the company in a summarized manner
    Company Location: Location of the company
    Number of employees: Total number of employees in the company
    Industry of Operation: Industry segments the company operates in
    Posting details: The company usually posts about
    Funding details: what and how many funding rounds the company has gone through.
    
    Get all the details from the given below dictionary within backticks. 
    Text in webpage: ```{detail}```
    """

    response1 = get_completion(prompt1)
    return response1

company_detail = extract_details(documents)
print(company_detail)