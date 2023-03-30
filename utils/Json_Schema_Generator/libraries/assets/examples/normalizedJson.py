import random
import string
from datetime import datetime
import json

def stringNormalizedExample():
  txt = {}
  txt['type'] = "Text"
  txt['value'] = "string"

  return txt

def rlshpNormalizedExample():
  relsp = {}
  relsp['type'] = "Relationship"
  relsp['value'] = "urn:ngsi:DataModel:001"

  return relsp

def numberNormalizedExample(prop):
  num = {}

  res = 2021

  if ("minimum" in prop) and ("maximum" in prop):
    res = random.randint(prop['minimum'], prop['maximum'])
  elif ("minimum" in prop):
    res = prop['minimum'] + 5
  elif ("maximum" in prop):
    res = random.randint(0, prop['maximum'])

  num['type'] = "Number"
  num['value'] = res

  return num

def booleanNormalizedExample():
  bl = {}
  bl['type'] = "Boolean"
  bl['value'] = True
  
  return bl

def datetimeNormalizedExample():
  dt = {}

  date_example = datetime(2021, 7, 5, 18, 00)
  date_example = date_example.isoformat()

  dt['type'] = "DateTime"
  dt['value'] = date_example

  return dt

def enumNormalizedExample(prop):
  enm = {}
  enm['type'] = "Enum"
  enm['value'] = prop['enum']

  return enm

def arrayNormalizedExample(prop):
  arr = {}
  arr['type'] = "array"
  arr['value'] = prop['items']['enum']

  return arr

def geoNormalizedExample(prop):
  geo = {}
  val = {}

  geo_type = prop['type'].split(":")

  val['type'] = geo_type[1]  

  if (geo_type[1] == "Point"):
    val["coordinates"] = [100.0, 0.0]

  if (geo_type[1] == "MultiPoint"):
    val["coordinates"] = [[-155.5, 19.6], [-156.2, 20.7], [-157.9, 21.4]]

  if (geo_type[1] == "LineString"):
    val["coordinates"] = [[-170, 10],[170, 11]]

  if (geo_type[1] == "MultiLineString"):
    val["coordinates"] = [[[170.0, 45.0], [180.0, 45.0]], [[-180.0, 45.0], [-170.0, 45.0]]]

  if (geo_type[1] == "Polygon"):
    val["coordinates"] = [[[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, -10.0]]]

  if (geo_type[1] == "MultiPolygon"):
    val["coordinates"] = [[[[180.0, 40.0], [180.0, 50.0], [170.0, 50.0], [170.0, 40.0], [180.0, 40.0]]], [[[-170.0, 40.0], [-170.0, 50.0], [-180.0, 50.0], [-180.0, 40.0], [-170.0, 40.0]]]]

  geo['type'] = 'GeoProperty'
  geo['value'] = val

  return geo

def objectNormalizedExample(prop):
  objt = {}

  del prop['type']
  del prop['description']

  objtProps = prop['properties']
  for key,value in objtProps.items():

    ######### Case property is string ##########
    if ((value['type'] == 'string') and ("format" not in value)):
      res = stringNormalizedExample()
      objtProps[key] = res

    ######### Case property is relationship ##########
    if (value['type'] == 'relationship'):
      res = rlshpNormalizedExample()
      objtProps[key] = res

    ####### Case if property is number ########
    if (value['type'] == 'number'):
      prop = value
      res = numberNormalizedExample(prop)
      objtProps[key] = res

    ######### Case property is boolean #########
    if (value['type'] == 'boolean'):
      res = booleanNormalizedExample()
      objtProps[key] = res 

    ######## Case property is datetime ########
    if ((value['type'] == 'string') and ("format" in value)):      
      res = datetimeNormalizedExample()
      objtProps[key] = res 
    
    ######## Case property is enum ######## 
    if ((value['type'] == 'string') and ("enum" in value)):      
      prop = value
      res = enumNormalizedExample(prop)
      objtProps[key] = res

    ######## Case property is array ########
    if (value['type'] == 'array'):   
      prop = value
      res = arrayNormalizedExample(prop)
      objtProps[key] = res   

    ######## Case property is geo ########
    if ("geo" in value['type']):   
      prop = value
      res = geoNormalizedExample(prop)
      objtProps[key] = res     

    ######## Case property is object ########
    if (value['type'] == 'object'):    
      prop = value
      res = objectNormalizedExample(prop) 
      objtProps[key] = res
    
  objt['type'] = "StructuredValue"
  objt['value'] = objtProps

  return objt


def createNormalizedJsonExample(creationPath, datamodel):
  jsonObject = ""
  with open(creationPath+"schema.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

    del jsonObject['required']

  props = jsonObject["allOf"][2]['properties']
  for key,value in props.items():
    
    ######### Case property is string ##########
    if ((value['type'] == 'string') and ("format" not in value)):
      res = stringNormalizedExample()
      jsonObject["allOf"][2]['properties'][key] = res

    ######### Case property is relationship ##########
    if (value['type'] == 'relationship'):
      res = rlshpNormalizedExample()
      jsonObject["allOf"][2]['properties'][key] = res

    ####### Case if property is number ########
    if (value['type'] == 'number'):
      prop = value
      res = numberNormalizedExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######### Case property is boolean #########
    if (value['type'] == 'boolean'):
      res = booleanNormalizedExample()
      jsonObject["allOf"][2]['properties'][key] = res 

    ######## Case property is datetime ########
    if ((value['type'] == 'string') and ("format" in value)):      
      res = datetimeNormalizedExample()
      jsonObject["allOf"][2]['properties'][key] = res 
      
    ######## Case property is enum ########
    if ((value['type'] == 'string') and ("enum" in value)):      
      prop = value
      res = enumNormalizedExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######## Case property is array ########
    if (value['type'] == 'array'):   
      prop = value
      res = arrayNormalizedExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######## Case property is geo ########
    if ("geo" in value['type']):      
      prop = value
      res = geoNormalizedExample(prop)
      jsonObject["allOf"][2]['properties'][key] = res

    ######## Case property is object ########
    if (value['type'] == 'object'):    
      prop = value
      res = objectNormalizedExample(prop) 
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
