from abc import ABCMeta, abstractmethod

class Parser(object):
  def __init__(self, data):
    self.data = data
  
  @abstractmethod
  def run(self):
    pass
