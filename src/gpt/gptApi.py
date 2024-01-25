import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import StringIO, BufferedReader
import re
from openai import OpenAI

class gptManager:
  def __init__(self, api_key:str,assistant_id_notes:str,assistant_id_quiz:str,assistant_id_notes_markdown:str):
    self.api_key = api_key
    self.assistant_id_notes = assistant_id_notes
    self.assistant_id_quiz = assistant_id_quiz
    self.assistant_id_notes_markdown = assistant_id_notes_markdown
    self.limit_pages = 20
    self.quiz_map = {'a':0,'b':1,'c':2,'d':3}

  def forward(self,data:BufferedReader, mode:str, callback=None):
    if callback:
      callback(0)
    pages = self._process_pdf_data(data)
    pages_generator = self._pagesGenerator(pages)
    if callback:
      pages_generator_copy = self._pagesGenerator(pages)
      gen_size = len(list(pages_generator_copy))+1
    
    if mode == 'notes_latex':
      result = self._askChat(next(pages_generator),mode)
      if callback:
        num_pages = 1
        callback(num_pages/gen_size)
      for page in pages_generator:
        if callback:
          num_pages += 1
          callback(num_pages/gen_size)
        response = self._askChat(page,mode)
        result = self._concatenateReponses(result,response)
      result += '\n\end\{document\}'
      self._save(result)
      if callback:
        callback((num_pages+1)/gen_size)
      return result
    
    elif mode == 'notes_markdown':
      result = self._askChat(next(pages_generator),mode)
      if callback:
        num_pages = 1
        callback(num_pages/gen_size)
      for page in pages_generator:
        if callback:
          num_pages += 1
          callback(num_pages/gen_size)
        result += self._askChat(page,mode)
      if callback:
        callback((num_pages+1)/gen_size)
      return result
    
    elif mode == 'quiz':
      result = self._askChat(next(pages_generator),mode)
      result = self._processQuiz(result)
      if callback:
        num_pages = 1
        callback(num_pages/gen_size)
      for page in pages_generator:
        if callback:
          num_pages += 1
          callback(num_pages/gen_size)
        response = self._askChat(page,mode)
        response_processed = self._processQuiz(response)
        result = self._concatenateQuizes(result,response_processed)
      if callback:
        callback((num_pages+1)/gen_size)
      return result
    
    else:
      raise Exception(f"Error, mode can only be set to either 'quiz' or 'notes'")
    
  def _process_pdf_data(self,data:BufferedReader, callback=None) -> list[str]:
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle,codec='utf-8', laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    pages = []
    if callback:
      num_pages = sum(1 for _ in PDFPage.get_pages(data, caching=True, check_extractable=True))
      cur_num_pages = 0
    for page in PDFPage.get_pages(data, caching=True, check_extractable=True):
        if callback:
          cur_num_pages +=1
          callback(cur_num_pages/num_pages)
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
        pattern = r'Poprawna: (\w)'
        ans = re.search(pattern, lines[-1])
        answers = [lines[1].replace('a. ',''),lines[2].replace('b. ',''),lines[3].replace('c. ',''),lines[4].replace('d. ','')]
        if ans:
            result['question'].append(lines[0])
            result['answers'].append(answers)
            result['correct'].append(answers[self.quiz_map[ans.group(1)]])
        else:
            continue
    return result
  
  def _concatenateQuizes(self,quiz_main,quiz_to_add):
    quiz_main['question'].extend(quiz_to_add['question'])
    quiz_main['answers'].extend(quiz_to_add['answers'])
    quiz_main['correct'].extend(quiz_to_add['correct'])
    return quiz_main

  def _pagesGenerator(self,pages, limit=4000):
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
    if mode == 'notes_latex':
      run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=self.assistant_id_notes
      )
    elif mode == 'notes_markdown':
      run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=self.assistant_id_notes_markdown
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
  gpt = gptManager('TODO','asst_1hmFCTKpuOC3WmmRzbL78Yte','asst_gWFzDPwpOqJ8xgfnPlE2wTZ9','asst_Ovdhi8eA6BQIx3NqpiQj3TMM' )
  print(gpt.forward('FPP-wyklad.pdf',mode = 'notes_markdown'),file=open('wyklad.md','w'))
  print('DONE')
