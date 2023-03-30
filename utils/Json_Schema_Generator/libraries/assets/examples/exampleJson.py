import random
import string
from datetime import datetime
import json

def stringExample():
  return 'string'

def rlshpExample():
  return 'urn:ngsi:DataModel:001'

def numberExample(prop):
  res = 2021

  if ("minimum" in prop) and ("maximum" in prop):
    res = random.randint(prop['minimum'], prop['maximum'])
  elif ("minimum" in prop):
    res = prop['minimum'] + 5
  elif ("maximum" in prop):
    res = random.randint(0, prop['maximum'])

  return res

def booleanExample():
  return True

def datetimeExample():
  date_example = datetime(2021, 7, 5, 18, 00)
  date_example = date_example.isoformat()

  return date_example

def enumExample(prop):
  return prop['enum']

def arrayExample(prop):
  return prop['items']['enum']

def geoProp(prop):
  res = {}

  geo_type = prop['type'].split(":")

  res["type"] = geo_type[1]

  if (geo_type[1] == "Point"):
    res["coordinates"] = [100.0, 0.0]

  if (geo_type[1] == "MultiPoint"):
    res["coordinates"] = [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]]

  if (geo_type[1] == "LineString"):
    res["coordinates"] = [[-170, 10],[170, 11]]

  if (geo_type[1] == "MultiLineString"):
    res["coordinates"] = [[[170.0, 45.0], [180.0, 45.0]], [[-180.0, 45.0], [-170.0, 45.0]]]

  if (geo_type[1] == "Polygon"):
    res["coordinates"] = [[[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, -10.0]]]

  if (geo_type[1] == "MultiPolygon"):
    res["coordinates"] = [[[[180.0, 40.0], [180.0, 50.0], [170.0, 50.0], [170.0, 40.0], [180.0, 40.0]]], [[[-170.0, 40.0], [-170.0, 50.0], [-180.0, 50.0], [-180.0, 40.0], [-170.0, 40.0]]]]

  return res
  
def objectExample(prop):
  del prop['type']
  del prop['description']

  objtProps = prop['properties']
  for key,value in objtProps.items():

    ######### Case property is string ##########
    if ((value['type'] == 'string') and ("format" not in value)):
      res = stringExample()
      objtProps[key] = res

    ######### Case property is relationship ##########
    if (value['type'] == 'relationship'):
      res = rlshpExample()
      objtProps[key] = res

    ####### Case if property is number ########
    if (value['type'] == 'number'):
      prop = value
      res = numberExample(prop)
      objtProps[key] = res

    ######### Case property is boolean #########
    if (value['type'] == 'boolean'):
      res = booleanExample()
      objtProps[key] = res 

    ######## Case property is datetime ########
    if ((value['type'] == 'string') and ("format" in value)):      
      res = datetimeExample()
      objtProps[key] = res 
    
    ######## Case property is enum ######## 
    if ((value['type'] == 'string') and ("enum" in value)):      
      prop = value
      res = enumExample(prop)
      objtProps[key] = res

    ######## Case property is array ########
    if (value['type'] == 'array'):   
      prop = value
      res = arrayExample(prop)
      objtProps[key] = res 

    ######## Case property is geo ########
    if ("geo" in value['type']):   
      prop = value
      res = geoProp(prop)
      objtProps[key] = res   

    ######## Case property is object ########
    if (value['type'] == 'object'):    
      prop = value
      res = objectExample(prop) 
      objtProps[key] = res
    
  return objtProps


def createJsonExample(creationPath, datamodel):
  
  jsonObject = ""
  with open(creationPath+"schema.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

    del jsonObject['required']

  props = jsonObject["allOf"][2]['properties']
  for key,value in props.items():
    
    ######### Case property is string ##########
    if ((value['type'] == 'string') and ("format" not in value)):
      res = stringExample()
      jsonObject["allOf"][2]['properties'][key] = res

    ######### Case property is relationship ##########
    if (value['type'] == 'relationship'):
      res = rlshpExample()
      jsonObject["allOf"][2]['properties'][key] = res

    ####### Case if property is number ########
    if (value['type'] == 'number'):
      prop = value
      res = numberExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######### Case property is boolean #########
    if (value['type'] == 'boolean'):
      res = booleanExample()
      jsonObject["allOf"][2]['properties'][key] = res 

    ######## Case property is datetime ########
    if ((value['type'] == 'string') and ("format" in value)):      
      res = datetimeExample()
      jsonObject["allOf"][2]['properties'][key] = res 
      
    ######## Case property is enum ########
    if ((value['type'] == 'string') and ("enum" in value)):      
      prop = value
      res = enumExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######## Case property is array ########
    if (value['type'] == 'array'):   
      prop = value
      res = arrayExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######## Case property is geo ########
    if ("geo" in value['type']):   
      prop = value
      res = geoProp(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######## Case property is object ########
    if (value['type'] == 'object'):    
      prop = value
      res = objectExample(prop) 
      jsonObject["allOf"][2]['properties'][key] = res
  ############################################    
    

  example = {}
  
  randomId = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
  example['id'] = (datamodel.lower()) + '-' + randomId
  example['type'] = datamodel.lower()

  props = jsonObject["allOf"][2]['properties']
  for key,value in props.items():
    example[key] = value

  return example
