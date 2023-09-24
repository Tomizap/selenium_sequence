from pprint import pprint


class Item:

  def __init__(self, fields={}) -> None:
    self.set_item(fields)

  def set_item(self, fields={}, prefix=''):

    # print('--- set fields ----')
    # print(fields)
    
    for field in dict(fields):
      value = fields.get(field) if fields.get(field) is not None else ''
      self.__setattr__(f"{f'{prefix}_' if prefix != '' else ''}{field}", value)

  # def update_item(self, name=None, value=None):
  #   if name is None or value is None:
  #     return
  #   if self.__getattribute__(name) is None:
  #     return
  #   self.__setattr__(name, value)

  def get(self, name):
    try:
      return self.__getattribute__(name)
    except:
      return None
    
  def update(self, name=None, value=None):
    if name is None or value is None:
      return
    if self.__getattribute__(name) is None:
      return
    self.__setattr__(name, value)


class Thing(Item):
  def __init__(self, fields={
      "URL": '',
      # "TITLE": '',
      "DESCRIPTION": '',
      "NAME": '',
      "LOCATION": 'France',
      # "WEBSITE": '',
      # "PHONE": '',
      # "EMAIL": '',
    }):

    self.set_item(fields=fields)


class ContactItem(Item):
  def __init__(self, fields={}, prefix=''):

    self.set_item(fields={
      "PHONE": '',
      "EMAIL": '',
    }, prefix=prefix)
    self.set_item(fields=fields, prefix=prefix)

class UrlsItem(Item):
  def __init__(self, fields={}, prefix=''):

    self.set_item(fields={
      "LINKEDIN_URL": "",
      "TWITTER_URL": "",
      "FACEBOOK_URL": "",
      "YOUTUBE_URL": "",
      "WEBSITE_URL": "",
      "INSTAGRAM_URL": "",
    }, prefix=prefix)
    self.set_item(fields=fields, prefix=prefix)
# th = Thing()
# pprint(vars(th))


# RATING





# CONTACTS


class CompanyItem(Item):
  def __init__(self, fields={}, prefix='COMPANY'):
    
    self.set_item(fields=Thing().__dict__, prefix=prefix)
    self.set_item(fields={
      "HIRING": False,
      "HIRING_EXPERIENCE": "Positive",
      "HIRING_DIFFICULTY": "Moyenne",
      "HIRING_TIME": "",
      "HIRING_STATUS": "",

      "JOBS_COUNT": "",

      "RATING": "5",
      "RATING_COUNT": "0",

      # "WEBSITE": "",
      "CREATION_DATE": "",
      "EMPLOYEES_COUNT": "1+",
      "REVENUE": "",
      "SECTOR": "",

      "INDEED_URL": ""
    }, prefix=prefix)
    self.set_item(fields=ContactItem().__dict__, prefix=prefix)
    self.set_item(fields=UrlsItem().__dict__, prefix=prefix)
    self.set_item(fields=fields, prefix=prefix)


class PeopleItem(Item):
  def __init__(self, fields={}, prefix=''):

    self.set_item(fields=Thing().__dict__, prefix=prefix)
    self.set_item(fields={
      "BIRTHDAY": "",
      "AGE": "",
      "GENDER": "",
      "JOB": ""
    }, prefix=prefix)
    self.set_item(fields=ContactItem().__dict__, prefix=prefix)
    self.set_item(fields=UrlsItem().__dict__, prefix='')
    self.set_item(fields=fields, prefix=prefix)


# JOBS


class JobItem(Item):
  def __init__(self, fields={}, prefix='JOB'):

    self.set_item(fields=Thing().__dict__, prefix=prefix)
    self.set_item(fields={
      "TIME": "Il y a moins d'un mois",
      "SPECIFICATIONS": "",
      "REVENUE": "",
      "APPLICATION_COUNT": "",
      "REVENUE": "",
      "ADVANTAGES": "",
      "REQUIREMENTS": "",

      "WORKTIME": "",
      "WORKSPACE": "Sur site",
      "WORKHOURS": "7h / jour",

      "INDEED_URL": "",
      "LINKEDIN_URL": "",
      "HELLOWORK_URL": "",
      "WELCOME_TO_THE_JUNLGE_URL": "",
    }, prefix=prefix)
    
    # self.set_item(fields=UrlsItem().__dict__, prefix=prefix)
    self.set_item(fields=CompanyItem({
      "HIRING_STATUS": "hiring",
      "HIRING": True,
      "JOBS_COUNT": "1+",
      "HIRING_TIME": "Il y a moins d'un mois"
    }).__dict__)
    # self.set_item(fields=PeopleItem().__dict__, prefix='RECRUITER')

    self.set_item(fields=fields, prefix=prefix)


# job = JobItem(fields={
#   'JOB_URL': 'test url'
# })
# pprint(vars(job))

