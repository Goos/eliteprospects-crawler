from src.parsers.parser import Parser
import bs4
from datetime import datetime

class PlayerParser(Parser):
  def run(self):
    # Parse the entire data blog with BeautifulSoup, 
    # giving us a tree of tag-objects.
    html = bs4.BeautifulSoup(self.data)
 
    # Pulling out the first span that is used as a header for one of
    # the values we're after, and in turn its closest 'table' parent,
    # in order to avoid iterating through the entire page for each value.
    info_table = html.select('span#fontSmall')[0].find_parent('table')
      
    parsed = {
      'name': self.find_name(html),
      'birthdate': self.find_birthdate(info_table),
      'birthplace': self.find_birthplace(info_table),
      'age': self.find_age(info_table),
      'nationality': self.find_nationality(info_table),
      'position': self.find_position(info_table),
      'shooting_direction': self.find_shooting_direction(info_table),
      'catching_direction': self.find_catching_direction(info_table),
      'height': self.find_height(info_table),
      'weight': self.find_weight(info_table),
      'status': self.find_status(info_table),
      'youth_team': self.find_youth_team(info_table)
    } 

    return parsed 

  def find_name(self, html):
    name_span = html.select('span#fontHeader')[0] 
    return str(name_span.text)

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
    # Finding the text node containing the text we're after,
    # returning None if it doesn't exist.
    text_node = html.find(text=header_text)
    if text_node == None:
      return None

    # Finding the text node's sibling-cell, which contains the
    # value text we're after.
    sibling = text_node.find_parent('td').find_next_sibling('td')

    # Checking if the cell responds to 'children', which
    # then is supposed to return an iterator.
    if hasattr(sibling, 'children'):
      children = sibling.children
      # In certain cases, the cell exists but is empty,
      # causing the iterator to throw an exception upon
      # receiving `next`.
      try:
        first_child = next(children)
      except(StopIteration):
        return None

      # The child element is either a text node or an element
      # containing one, and we want its string value either way.
      if isinstance(first_child, bs4.element.NavigableString):
        return str(first_child)
      else:
        return str(first_child.text)
    else:
      return None

