import re

def remove_c_parantheses(text):
  """
  returns: text with the c() surrounding it removed
  """
  return re.sub(r'c\(([^)]+)\)', r'\1', text)