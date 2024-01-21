import os
from nltk.tokenize import sent_tokenize
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import StringIO, BufferedReader
import re
from openai import OpenAI

class gptManager:
  def __init__(self, api_key:str,assistant_id_notes:str,assistant_id_quiz:str):
    self.api_key = api_key
    self.assistant_id_notes = assistant_id_notes
    self.assistant_id_quiz = assistant_id_quiz
    self.limit_pages = 5

  def forward(self,file_name:str, mode:str):
    if file_name.endswith('.pdf'):
      pages = self._process_pdf(file_name)

    pages_generator = self._pagesGenerator(pages)

    if mode == 'notes':
      result = self._askChat(next(pages_generator),mode)
      for page in pages_generator:
        response = self._askChat(page,mode)
        result = self._concatenateReponses(result,response)
      result += '\n\end\{document\}'
      self._save(result)
      return result
    
    elif mode == 'quiz':
      result = self._askChat(next(pages_generator),mode)
      result = self._processQuiz(result)
      for page in pages_generator:
        response = self._askChat(page,mode)
        response_processed = self._processQuiz(response)
        result = self._concatenateQuizes(result,response_processed)
      return result
    
    else:
      raise Exception(f"Error, mode can only be set to either 'quiz' or 'notes'")
  
  def forward_read(self,data:BufferedReader, mode:str):
    # if file_name.endswith('.pdf'):
    pages = self._process_pdf_data(data)
    pages_generator = self._pagesGenerator(pages)

    if mode == 'notes':
      result = self._askChat(next(pages_generator),mode)
      for page in pages_generator:
        response = self._askChat(page,mode)
        result = self._concatenateReponses(result,response)
      result += '\n\end\{document\}'
      self._save(result)
      return result
    
    elif mode == 'quiz':
      result = self._askChat(next(pages_generator),mode)
      result = self._processQuiz(result)
      for page in pages_generator:
        response = self._askChat(page,mode)
        response_processed = self._processQuiz(response)
        result = self._concatenateQuizes(result,response_processed)
      return result
    
    else:
      raise Exception(f"Error, mode can only be set to either 'quiz' or 'notes'")
    
  def _process_pdf(self,file_name: str) -> list[str]:
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    pages = []
    with open(file_name, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            pages.append(text.replace('\n',''))
            fake_file_handle.truncate(0)
            fake_file_handle.seek(0)

    converter.close()
    fake_file_handle.close()
    return pages
  
  def _process_pdf_data(self,data:BufferedReader) -> list[str]:
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    pages = []
    # with open(file_name, 'rb') as fh:
    for page in PDFPage.get_pages(data, caching=True, check_extractable=True):
        page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        pages.append(text.replace('\n',''))
        fake_file_handle.truncate(0)
        fake_file_handle.seek(0)

    converter.close()
    fake_file_handle.close()
    return pages
  
  def _processQuiz(self,quiz:str):
    result = {'question':[],'answers':[],'correct':[]}
    questions = quiz.split('\n\n')
    for question in questions:
        lines = question.split('\n')
        result['question'].append(lines[0])
        result['answers'].append(lines[1:4])
        result['correct'].append(lines[-1].replace("Poprawna: ",''))
    return result
  
  def _concatenateQuizes(self,quiz_main,quiz_to_add):
    quiz_main['question'].extend(quiz_to_add['question'])
    quiz_main['answers'].extend(quiz_to_add['answers'])
    quiz_main['correct'].extend(quiz_to_add['correct'])
    return quiz_main

  def _pagesGenerator(self,pages, limit = 1000):
    text =''
    sum_signs = 0
    for page in pages[:self.limit_pages]:
      if sum_signs+len(page)<limit:
        text+=page
        sum_signs+=len(page)
      else:
        yield text
        text =page
        sum_signs = len(page)
    else:
      yield text
      
  def _askChat(self,content:str,mode = 'notes'):
    client = OpenAI(api_key=self.api_key)
    thread = client.beta.threads.create(
    messages=[
            {
            "role": "user",
            "content": content
            }
        ]
    )
    if mode == 'notes':
      run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=self.assistant_id_notes
      )
    elif mode == 'quiz':
      run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=self.assistant_id_quiz
      )

    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if keep_retrieving_run.status == "completed":
            break
        elif keep_retrieving_run.status == "failed" or keep_retrieving_run.status == "canceled":
            raise Exception(f"Error, API conection has {keep_retrieving_run.status}")
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    return all_messages.data[0].content[0].text.value
  
  def _concatenateReponses(self,response_main:str,response_to_add:str):
    pattern = r'\\usepackage\{.*?\}'
    pattern_remove = r'\\title\{.*?\}|\\date\{\\today\}|\\maketitle|\\documentclass\{.*?\}|\\begin{document}'
    pattern_to_place_packages = r'\\documentclass\{.*?\}'

    matches = re.findall(pattern, response_to_add)
    response_to_add = re.sub(pattern, '', response_to_add)
    response_to_add = re.sub(pattern_remove, '', response_to_add)

    new_text = ''
    for m in matches:
        new_text+=m
        new_text+='\n'

    response_main = re.sub(pattern_to_place_packages, lambda x: x.group() + new_text, response_main)
    response_main = response_main.replace("\\end{document}", response_to_add)
    return response_main
  
  def _save(self, text:str):
     print(text,file=open('main.tex','w'))

if __name__ == '__main__':
  print(os.listdir('../'))
  gpt = gptManager('TOUPDATE','asst_1hmFCTKpuOC3WmmRzbL78Yte','asst_Lb3RWc77sIsdunncnkgKZtfX' )
  print(gpt.forward('FPP-wyklad.pdf',mode = 'quiz'))
