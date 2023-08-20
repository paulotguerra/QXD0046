import re

class RE:
  def __init__(self,regex=None):
    if (regex == None):
      self.regex = None
    elif (re.match("^[a-zA-Z0-9\(\)\|\*]*$", regex)):
      self.regex = regex
    else:
      raise Exception("Invalid pattern")

  def generates(self, input_string):
    if (self.regex == None):
      return False
    else:
      return True if re.match("^"+self.regex+"$",input_string) else False
  
  def __repr__(self):
    return self.regex

class ER(RE):
    def gera(self, input_string=0):
        return self.generates(input_string)