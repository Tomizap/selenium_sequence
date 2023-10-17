from pprint import pprint
import re
import time
from colorama import Fore, Style
from selenium_driver import SeleniumDriver
# from selenium_sequence import print
from tzmongo import mongo
# from selenium_sequence.automnation import get_automnation

from selenium_sequence.data import get_element_data, get_elements_data
from selenium_sequence.finder import Finder
from selenium_sequence.items import *
from selenium_sequence.models import find_model


class Sequence:
  
  def __init__(self, driver=None, model={}, steps=None, source_url="", data=[], item=None, automnation_id=None) -> None:
    print('init Sequence')
    
    self.source_url = source_url
    self.driver = driver if driver is not None else SeleniumDriver()
    self.model = model if len(model) > 0 else find_model(url=source_url)
    if steps is not None:
        self.model['steps'] = steps
    # self.steps = model.get('steps', steps)
    self.automnation_id = automnation_id
    self.item = item if item is not None else find_model(url=source_url).get('fields', Item)()
    # pprint(item.__dict__)
    self.data = data

  def update_item(self, name, value):
      self.item.__setattr__(name, value)

  def get_data(self):
      if self.automnation_id is not None:
          # ga = get_automnation(_id=self.automnation_id)
          ga = mongo({
                'collection': 'automnations',
                "selector": {'_id': self.automnation_id}
            })
          if ga['ok'] == True:
              automnation = ga['data'][0]
              return automnation.get('data')
      
      return []

  def add_item(self, item={}):
      # print('adding item to data')

      # if self.filename is not None:
      #     add_data_to_csv(data=[item], filename=self.filename)
          # add_data_to_json(data=[item], filename=self.filename)

      item_exist = False
      data = self.get_data()
      # print(data)
      for key in item:
          if 'EMAIL' in key or 'PHONE' in key:
              if item[key] != '' and item[key] in str(data):
                  # print(Fore.WHITE + f"data: {self.data}")
                  # print(Fore.WHITE + f"item[key]: {item[key]}")
                  item_exist = True
                  # item_exist_dict = item
                  break

      if item_exist:
          # print(Fore.WHITE + f"data: {self.data}")
          print(Fore.RED + f"item already exist")
          print(Style.RESET_ALL)
          return

      if self.automnation_id is not None:
          
          # print('adding item to mongo')
          adding = mongo({
              "collection": "automnations",
              "selector": {'_id': self.automnation_id},
              "action": "edit",
              "updator": {
                  "$push": {
                      "data": item
                  }
              }
          })
          # print(adding)

          if adding.get('ok', False) is False:
              print(Fore.RED + str(adding.get('message')))
          # else:
          #     print(f"item successfully added to mongo")
          print(Style.RESET_ALL)

      # self.data.append(item)

  # -------------- INTERACTIONS ------------------

  def play(self):
    sequence = self.model.get('steps', {})
    original_url = self.source_url

    for step in sequence:
                
      print(Fore.WHITE + 'step: ' + str(step))
      value = sequence[step]
      
      # ---------------- ACTION ---------------------

      if ':click' in step:
          if type(value) == str:
              self.driver.click(value)
          elif type(value) == list:
              for e in value:
                  self.driver.click(e)
          continue

      elif ":execute_script" in step:
          if type(value) == str:
              self.driver.execute_script(value)
          elif type(value) == list:
              for script in value:
                  self.driver.execute_script(script)
          continue

      elif ":wait" in step:
          time.sleep(value)
          continue

      elif ":goto" in step:

          if ":original_url" in value:
              # print(Fore.WHITE + 'go back to original_url')
              self.driver.get(original_url)
              continue

          url = ""

          if type(value) == str:
              if "http" in value:
                  url = value
              else:
                  url = get_element_data(
                      driver=self.driver,
                      selector=value, prop="href")
                  
          elif type(value) == dict:
              url = get_element_data(
                  driver=self.driver,
                  selector=value['selector'],
                  prop=value['property'])
              
          if url.strip() != "" and url is not None:
              self.driver.get(url.strip())
              if '404' in self.driver.current_url() or 'unavailable' in self.driver.current_url():
                  print(Fore.RED + 'error')
                  print(Style.RESET_ALL)
                  self.driver.get(
                      "/".join(self.driver.current_url().split('/')[:3]))
                  self.driver.get(url.strip())

          continue

      # elif ':sequence' in step:
      #     seq = Automnation(
      #         driver=self.driver, 
      #         item=self.item, 
      #         data=[], 
      #         sequence=value,
      #         depth= self.depth + 1)
      #     seq.play()
      #     if len(seq.data) == 1:
      #         for prop in seq.data[0]:
      #             if self.item.get(prop) is not None:
      #                 self.item.__setattr__(prop, seq.data[0][prop])
      #                 # self.item[prop] = seq.data[0][prop]
      #     continue
          

      # ---------------- LOOPING ---------------------

      if ':loop' in step:
          
          listing = []
          i_loop = 0
          pagination = value.get('pagination')

          page = 99
          if type(value.get('page')) is str:
              page = int(get_element_data(self.driver, value.get('page')))
          elif type(value.get('page')) is int:
              page = value.get('page')
          # print(f"page: {page}")

          if not self.driver.is_attached(str(pagination)):
              for _ in range(5):
                  if not self.driver.is_attached(str(pagination)):
                      time.sleep(1)
              print(Fore.RED + 'pagination is not attached')
              print(Style.RESET_ALL)
              continue

          while i_loop < page and self.driver.is_attached(str(pagination)):
              i_loop = i_loop + 1

              print(f'page: {i_loop}/{page}')
              if not self.driver.is_attached(str(pagination)):
                  # print('pagination is not attached')
                  for _ in range(5):
                      if not self.driver.is_attached(str(pagination)):
                          time.sleep(1)
                  print(Fore.RED + 'pagination is not attached')
                  print(Style.RESET_ALL)
              
              listing_sequence = Sequence(
                  item=self.item,
                  driver=self.driver,
                  automnation_id=self.automnation_id,
                  steps=value['listing'])
              listing_sequence.play()
              
              if value.get('replace') == True:
                  listing = listing_sequence.data.copy()
              else:
                  for data_url in listing_sequence.data:
                      if data_url not in listing:
                          listing.append(data_url)
              
              self.driver.click(value['pagination'])

              print(Fore.GREEN + f'+{len(listing_sequence.data)} urls of {len(listing)} to scrap')
              # print(Fore.WHITE + f'TOTAL: {len(listing)}')

          # print(Fore.GREEN + f"listing ended: {str(len(listing))} urls founded")
          print(Style.RESET_ALL)

          # for i in range(len(listing)):
          #     listing[i] = str(listing[i]).split('?')[0]
              
          if value.get('deep') is False:
              self.data = listing
              continue

          for u in range(len(listing)):
              
              url = listing[u]

              # print(listing)
              # print(url)

              if url in str(self.get_data()):
                  print(Fore.RED + f"item already exist")
                  print(Style.RESET_ALL)
                  continue

              if type(url) == str:

                  self.driver.get(url)
                  time.sleep(1)
                  url = self.driver.current_url()

                  for attr in self.item.__dict__:
                      self.update_item(attr, "")
                      
                  loop_sequence = Sequence(
                      source_url=url,
                      driver=self.driver, 
                      item=self.item,
                      automnation_id=self.automnation_id)
                  loop_sequence.play()
                  
                  loop_sequence.update_item("SOURCE_URL", url)
                  item = loop_sequence.item.__dict__

                  pprint(item)
                  print(Fore.GREEN + f"+1 item scrapped ({u + 1}/{len(listing)})")
                  print(Style.RESET_ALL)
                  
                  self.add_item(item)

              print(Style.RESET_ALL)
              
          print(Style.RESET_ALL)
          continue
          
      # ---------------- GET DATA ---------------------

      step_property = str(step).split(':')[0]

      if step_property != '':
          if self.item.get(step_property) is None:
              print(Fore.RED + f'{step_property} is an incorrect attribute')
              continue
          elif self.item.get(step_property) != '':
              print(Fore.RED + f'property {step_property} is already set')
              continue

      if ":find" in step:
          result = ''

          if type(value) == dict:

              name = self.item.get('COMPANY_NAME')
              if value.get('name') is not None:
                  name = get_element_data(driver=self.driver, selector=value.get('name'))
              # print(name)

              location = self.item.get('COMPANY_LOCATION')
              if value.get('location') is not None:
                  location = get_element_data(driver=self.driver, selector=value.get('location'))
              # print(location)

              finder = Finder(
                  driver=self.driver,
                  name=name,
                  location=location,
              )

              # if ":contact" in step:
              #     result = str(finder.email())
              #     result = str(finder.phone())
              #     result = str(finder.website())
              #     result = str(finder.linkedin())
              #     result = str(finder.indeed())
              #     result = str(finder.facebook())
              #     result = str(finder.youtube())

              if ":email" in step:
                  result = str(finder.email())
              elif ":phone" in step:
                  result = str(finder.phone())
              elif ':website' in step:
                  result = str(finder.website())
              # elif ':linkedin' in step:
              #     result = str(finder.linkedin())
              # elif ':indeed' in step:
              #     result = str(finder.indeed())
              # elif ':facebook' in step:
              #     result = str(finder.facebook())
              # elif ':facebook' in step:
              #     result = str(finder.youtube())
              else:
                  continue

              self.update_item(step_property, result)

          self.driver.get(original_url)

      elif ':get' in step:

          if step_property == "":
              if ":all" in step:
                  v = {}
                  if type(value) == str:
                      v = get_elements_data(
                          driver=self.driver, selector=value, prop="innerText")
                  elif type(value) == dict:
                      v = get_elements_data(
                          driver=self.driver,
                          selector=value['selector'],
                          prop=value['property'])
                      
                  self.data.extend(v.copy())
                  continue
              else:
                  print(Fore.RED + 'Nothing to get all')

          else:

              if ":current_url" in step:
                  self.update_item(
                      step_property, 
                      self.driver.current_url())
                  continue

              if type(value) == str:
                  self.update_item(
                      step_property, 
                      get_element_data(driver=self.driver, selector=value, prop="innerText"))
                  
              elif type(value) == dict or value.get('selector') is not None:
                  self.update_item(step_property, get_element_data(
                      driver=self.driver,
                      selector=value.get('selector'),
                      prop=value.get('property') if value.get('property') is not None else 'innerText'))
                  if value.get('replace') == str:
                      self.update_item(
                          step_property, 
                          re.sub(value.get('replace', ''), '', self.item.__getattribute__(step_property)))
                  # print(Fore.GREEN + self.item.__getattribute__(step_property))
              else:
                  print(Fore.RED + 'Nothing to get')

    print(Style.RESET_ALL)