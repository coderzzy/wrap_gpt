import pandas as pd
import tiktoken  # for token counting
from docx import Document
import PyPDF2

encoding = tiktoken.get_encoding("cl100k_base")

def content_len(messages):
    count = num_tokens_from_messages(messages)
    print(count+"token in this document")
    return count

def long_content_process(messages):
    123

def content_cost(count):
    return count*0.002/1000

def txt_read(txt_path):
    txt_content=''
    with open(txt_path, 'r') as file:
        txt_content = file.read()
    return txt_content

def excel_read(excel_path):
    df = pd.read_excel(excel_path)
    csv_data = df.to_csv(index=False)
    return csv_data

def word_read(doc_path):
    doc = Document(doc_path)
    text_content = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(text_content)

def pdf_read(pdf_path):
    pdf_content=''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            pdf_content += page.extract_text()
    return pdf_content

def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens