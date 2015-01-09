from lib.parsers.parser import Parser
import bs4
from datetime import datetime
import logging

class PlayerParser(Parser):
  def run(self):
    html = bs4.BeautifulSoup(self.data)

    name_header = html.select('span#fontHeader')[0] 
    logging.getLogger(__name__).info(name_header.find_parent('table').find_next_sibling('table'))
    info_table = name_header.find_parent('table').find_next_sibling('table')
    info_subtable = info_table.find('table')
    
    name = name_header.text 
    birthdate = self.find_birthdate(info_subtable)
  
    parsed = {
      'name': name_header.text,
      'birthdate': self.find_birthdate(info_subtable),
      'birthplace': self.find_birthplace(info_subtable),
      'age': self.find_age(info_subtable),
      'nationality': self.find_nationality(info_subtable),
      'position': self.find_position(info_subtable),
      'shooting_direction': self.find_shooting_direction(info_subtable),
      'catching_direction': self.find_catching_direction(info_subtable),
      'height': self.find_height(info_subtable),
      'weight': self.find_weight(info_subtable),
      'status': self.find_status(info_subtable),
      'youth_team': self.find_youth_team(info_subtable)
    }

    logging.getLogger(__name__).info(parsed)

    return parsed 

  def find_birthdate(self, html):
    datestring = self.find_value_for_cell_header(html, 'BIRTHYEAR') 
    birthdate = None
    if datestring:
      birthdate = datetime.strptime(datestring, '%Y-%m-%d')
    return birthdate
    
  def find_birthplace(self, html):
    return self.find_value_for_cell_header(html, 'BIRTHPLACE') 

  def find_age(self, html):
    age = self.find_value_for_cell_header(html, 'AGE') 
    try:
      return int(age)
    except(ValueError):
      return None

  def find_nationality(self, html):
    return self.find_value_for_cell_header(html, 'NATION') 

  def find_position(self, html):
    return self.find_value_for_cell_header(html, 'POSITION') 

  def find_shooting_direction(self, html):
    return self.find_value_for_cell_header(html, 'SHOOTS') 

  def find_catching_direction(self, html):
    return self.find_value_for_cell_header(html, 'CATCHES')
    
  def find_height(self, html):
    height = self.find_value_for_cell_header(html, 'HEIGHT') 
    try:
      return float(height.split(' ')[0])
    except(ValueError):
      return None

  def find_weight(self, html):
    weight = self.find_value_for_cell_header(html, 'WEIGHT') 
    try:
      return float(weight.split(' ')[0])
    except(ValueError):
      return None

  def find_status(self, html):
    return self.find_value_for_cell_header(html, 'STATUS') 

  def find_youth_team(self, html):
    return self.find_value_for_cell_header(html, 'YOUTH TEAM') 
 
  def find_value_for_cell_header(self, html, header_text):
    header = html.find(text=header_text)
    if header == None:
      return None

    sibling = header.find_parent('td').find_next_sibling('td')

    if hasattr(sibling, 'children'):
      children = sibling.children
      try:
        first_child = next(children)
      except(StopIteration):
        return None

      if isinstance(first_child, bs4.element.NavigableString):
        return str(first_child)
      else:
        return str(first_child.text)
    else:
      return None

