import json
import os

def propType(prop_name, prop_type, enumAttributes):
  result = ""

  # Checks if the property is enum, date-time or anothe. If not enum or date-time, the type used is in the properties dataframe.
  if prop_type != 'enum' and prop_type != 'date-time' and prop_type != 'geo':    
    result += """ 
        \"""" + str(prop_name) + """\": { 
          "type": \"""" + str(prop_type) + """\","""

  # If is date-time, the type will be string
  if prop_type == 'date-time':
    result += """ 
        \"""" + str(prop_name) + """\": { 
          "type": \"string\","""

  # If is enum, the type used is in the enumAttributes dataframe
  if prop_type == 'enum': 

    enum_prop_type = enumAttributes.loc[enumAttributes['property_name'] == prop_name]

    # Check if the attributes of the propierty of the current loop are empty or repeated
    if enum_prop_type.empty: 
      print("\n Ups. Something goes wrong:\n")
      print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are not defiend.')      
      #sys.exit('\nExecution terminated with error\s')
      return -1
    if len(enum_prop_type) > 1:
      print("\n Ups. Something goes wrong:\n")
      print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are repeated.')
      #sys.exit('\nExecution terminated with error\s')
      return -1

    enumType = enum_prop_type.iloc[0]['enum_type']
    result += """ 
        \"""" + str(prop_name) + """\": { 
          "type": \"""" + enumType + """\","""     

  if prop_type == 'geo':
    result += """ 
        \"""" + str(prop_name) + """\": {"""          

  return result

def number(prop_name, num_attrs):
  result = ""

  # Check if the attributes of the propierty of the current loop are empty or repeated
  #if num_attrs.empty: 
    #sys.exit('\nProperty ' + prop_name + ' has a problem:\n     - The attributes of the property are not defiend.\n')


  # Check if the attributes of the propierty of the current loop are empty
  if num_attrs.empty == False:

    # Check if the attributes of the propierty of the current loop are repeated
    if len(num_attrs) > 1:
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are repeated.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
      
    minAttr = str(num_attrs.iloc[0]['minimum'])
    maxAttr = str(num_attrs.iloc[0]['maximum'])

    # Checks if both or any of the minimum and/or maximum values is/are integer/s
    min_int = True
    max_int = True

    try:
      int(minAttr)
    except:
      min_int = False

    try:
      int(maxAttr)
    except:
      max_int = False

    if (minAttr != 'nan' and maxAttr != 'nan') and (min_int == False and max_int == False):
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      Minimum and Maximum values must be integer.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
    elif minAttr != 'nan' and min_int == False:
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      Minimum value must be integer.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
    elif maxAttr != 'nan' and max_int == False:
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      Maximum value must be integer.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    # Checks if both or any of the minimum and/or maximum values is/are greater than 0    
    elif (minAttr != 'nan' and maxAttr != 'nan') and (int(minAttr) < 0 and int(maxAttr) < 0):
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      Minimum and Maximum values must be greater than 0.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
    elif  minAttr != 'nan' and int(minAttr) < 0:
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      Minimum value must be greater than 0.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
    elif maxAttr != 'nan' and int(maxAttr) < 0:
      print("\n Ups. Something goes wrong:")
      print('    Property ' + str(prop_name) + ' has a problem:\n      Maximum value must be greater than 0.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    # Checks if the maximum value if greater than the minimum value
    elif (minAttr != 'nan' and maxAttr != 'nan') and (int(minAttr) > int(maxAttr)):
      print("\n Ups. Something goes wrong:")
      print('    Property' + str(prop_name) + ' has a problem:\n      Maximum must be greater than Minimum.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    # If all the controls have been passed, the values are written
    else:
      # Checks if exists a minimum value specified
      if minAttr != 'nan':        
        result += """
            "minimum": """ + minAttr + ""","""
      
      # Checks if exists a maximum value specified
      if maxAttr != 'nan':        
        result += """
            "maximum": """ + maxAttr + ""","""

  return result

def enum(prop_name, enum_attrs):
  result = ""

  enumType = enum_attrs.iloc[0]['enum_type']
  enumVals = str(enum_attrs.iloc[0]['enumeration_values'])
  enumVals = enumVals.replace(".", ",")
  enumVals = enumVals.split(',')

  # Check if there are repeated values ​​in the enumeration_values ​​attribute
  if len(set(enumVals)) < len(enumVals):
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The enumeration values has repeated values.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  if (str(enumVals[0]) != 'nan'):
    result += """
            "enum": ["""

    if enumType == 'number':
      for i in enumVals:

        # Checks if the values of the list are integers
        isInt = True
        try:
          int(i)
        except:
          isInt = False

        if isInt == False:
          print("\n Ups. Something goes wrong:")
          print('    Property ' + str(prop_name) + ' has a problem:\n      All values from enumeration_values must be integers.')
          #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
          return -1
        else:
          result += str(i) + ","

    if enumType == 'string':
      for s in enumVals:
        result += "\"" + str(s) + "\"," 

    result = result[:-1]
    result += '],'   
  
  else:
    result += """
            "enum": \"\","""

  return result    

def array(prop_name, array_attrs):
  result = ""

  # Check if the attributes of the propierty of the current loop are empty or repeated
  if array_attrs.empty: 
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are not defiend.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  if len(array_attrs) > 1:
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are repeated.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  arrayVals = str(array_attrs.iloc[0]['array_values'])
  arrayVals = arrayVals.replace(".", ",")
  arrayVals = arrayVals.split(',')

  # Check if the minimum_items is integer
  try:
    int(array_attrs.iloc[0]['minimum_items'])
  except:
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The minimum items values must be integer.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  # Check if the quanty of array_values is equal or greater than minimum_items attribute
  if ((len(arrayVals) < int(array_attrs.iloc[0]['minimum_items'])) and (arrayVals[0] != 'nan')):
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The array values length is under the minimum items value.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  # Check if the quanty of array_values is equal to 0
  if int(array_attrs.iloc[0]['minimum_items']) == 0 and arrayVals[0] != 'nan':
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The minimum_items is 0, but there are values in array_values attribute.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  # Check if there are repeated values ​​in the array_values ​​attribute
  if len(set(arrayVals)) < len(arrayVals):
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The array values has repeated values.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
    

  result += """
          "items": {
            "type": \"""" + array_attrs.iloc[0]['array_type'] + """\","""

  if (str(arrayVals[0]) != 'nan'):
    result += """
            "enum": ["""

    if str(array_attrs.iloc[0]['array_type']) == 'number':
      for i in arrayVals:          
        # Checks if the values of the list are integers
        isInt = True
        try:
          int(i)
        except:
          isInt = False

        if isInt == False:
          print("\n Ups. Something goes wrong:")
          print('    Property ' + str(prop_name) + ' has a problem:\n      Because the type of the array is number, all values from array_values must be integers.')
          #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
          return -1

        else:
          result += str(i) + ","

    if str(array_attrs.iloc[0]['array_type']) == 'string':
      for s in arrayVals:
        result += "\"" + str(s) + "\"," 

    result = result[:-1]
    result += '],'

  else:
    result += """
            "enum": \"\","""

  result += """
            "minItems": """ + str(array_attrs.iloc[0]['minimum_items']) + """
          },"""
  
  return result     

def datetime():
  result = ""

  result += """
          "format": \"date-time\","""
  
  return result

def geoProp(prop_name, geo_attrs):
  result = ""

  # Check if the attributes of the propierty of the current loop are empty or repeated
  if geo_attrs.empty:
    print("\n Ups. Something goes wrong:\n")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are not defiend.')      
    #sys.exit('\nExecution terminated with error\s')
    return -1

  if len(geo_attrs) > 1:
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The attributes of the property are repeated.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  geoType = geo_attrs.iloc[0]['geo_type']

  geoOptions = ['Point', 'MultiPoint', 'LineString', 'MultiLineString', 'Polygon', 'MultiPolygon']

  if geoType in geoOptions:
    result += """
          "type": \"geo:""" + geoType + """\","""

    return result

  else:
    print("\n Ups. Something goes wrong:")
    print('    Property ' + str(prop_name) + ' has a problem:\n      The selected geo_type value is not in the list of allowed value types.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

def objt(objtProps, properties, numberAttributes, enumAttributes, arrayAttributes, geoAttributes, objectAttributes):
  
  result = ""

  result += """
          "properties": {"""

  if objtProps.empty == True:
    result += '},'      
  
  else:
    for p in objtProps.itertuples():
      prop = properties.loc[properties['property_name'] == p.property_name]

      prop_name = prop.iloc[0]['property_name']
      prop_type = prop.iloc[0]['data_type']
      prop_desc = prop.iloc[0]['description']
      


      ############ Add property type ############ 
      nestedResult = propType(prop_name, prop_type, enumAttributes)    
      if nestedResult == -1:
        return -1
      else:
        result += nestedResult        
      ###########################################

      ####### Case if property is number ########
      if prop_type == 'number':
        nestedResult = number(prop_name, numberAttributes.loc[numberAttributes['property_name'] == prop_name])
        if nestedResult == -1:
          return -1
        else:
          result += nestedResult 
      ###########################################

      ########## Case property is enum ##########
      if prop_type == 'enum':
        nestedResult = enum(prop_name, enumAttributes.loc[enumAttributes['property_name'] == prop_name])
        if nestedResult == -1:
          return -1
        else:
          result += nestedResult 
      ###########################################

      ########## Case property is array #########
      if prop_type == 'array':
        nestedResult = array(prop_name, arrayAttributes.loc[arrayAttributes['property_name'] == prop_name])
        if nestedResult == -1:
          return -1
        else:
          result += nestedResult 
      ###########################################

      ######## Case property is datetime ########
      if prop_type == 'date-time':
        nestedResult = datetime() 
        if nestedResult == -1:
          return -1
        else:
          result += nestedResult 
      ###########################################

      ######## Case property is geo ########
      if prop_type == 'geo':
        nestedResult = geoProp(prop_name, geoAttributes.loc[geoAttributes['property_name'] == prop_name]) 
        if nestedResult == -1:
          return -1
        else:
          result += nestedResult 
      ###########################################

      ######### Case property is object #########
      if prop_type == 'object':
        nestedResult = objt(prop_name, arrayAttributes.loc[arrayAttributes['property_name'] == prop_name])    
        if nestedResult == -1:
          return -1
        else:
          result += nestedResult 
      ###########################################

      ############# Add Description #############   
      result += description(prop_desc)
      ###########################################

    result = result[:-1]
    result += '\n          },'

  return result

def description(desc):
  result = ""

  result += """
          "description": \"""" + desc + """\"
        },"""
  
  return result


    

def generationV2(model_book, properties, numberAttributes, enumAttributes, arrayAttributes, geoAttributes, objectAttributes, save_location):

  print(" Processing information ...")

  ################# Treatment of properties dataframe ################
  properties_subset = properties[['property_name', 'data_type', 'data_type_ld', 'description', 'required']]
 
  # Checks for empty values   
  if properties_subset.isnull().sum().sum() > 0:
    print("\n Ups. Something goes wrong:")
    print ("    Some field in propierties sheet is empty.")
    print('    Please, check the list of properties and fill in the empty fields.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  else:
    # Transform include_in_object values from string to int
    properties[properties.columns[4]] = properties[properties.columns[4]].replace(['No'],0)
    properties[properties.columns[4]] = properties[properties.columns[4]].replace(['Yes'],1)

    # Transform required values from string to int
    properties['required'] = properties['required'].replace(['No'],0)
    properties['required'] = properties['required'].replace(['Yes'],1)

    # Checks if include_in_object column in properties sheet has permitted values
    nullV = properties['include_in_object'].isnull().sum().sum()
    yesV = len(properties[properties['include_in_object'] == 1])
    noV = len(properties[properties['include_in_object'] == 0])

    if ((yesV + noV + nullV) != len(properties)):
      print("\n Some value/s in required column of the properties sheet has a not allowed value.")
      print(" Please check the instructions sheet.")
      return -1

    # Checks if required column in properties sheet has permitted values  
    yesV = len(properties[properties['required'] == 1])
    noV = len(properties[properties['required'] == 0])

    if ((yesV + noV) != len(properties)):
      print("\n Some value/s in required column of the properties sheet has a not allowed value.")
      print(" Please check the instructions sheet.")
      return -1
  ####################################################################
  


  ############# Treatment of numberAttributes dataframe ##############
  # Checks for empty values in the property_name column, non-referenced values
  # or if the property is in the wrong sheet because of his data type
  if numberAttributes['property_name'].isnull().sum().sum() > 0:
    print("\n Ups. Something goes wrong:")
    print ("    Some field in number_attributes sheet is empty.")
    print('    Please, check the list of number_attributes and fill in the empty fields.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
  
  for nu in numberAttributes.itertuples():  
    prop = properties.loc[properties['property_name'] == nu.property_name]

    if len(prop) == 0:
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(nu.property_name) + ' in the number_attributes sheet not exist in the properties sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
    
    if (prop.iloc[0]['data_type'] != 'number'):
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(nu.property_name) + ' is not a number. Remove the property from the number_attributes sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
  ####################################################################



  ############### Treatment of enumAttributes dataframe ##############
  # Checks for empty values in the property_name column, non-referenced values
  # or if the property is in the wrong sheet because of his data type
  if enumAttributes.isnull().sum().sum() > 0:
    print("\n Ups. Something goes wrong:")
    print ("    Some field in enum_attributes sheet is empty.")
    print('    Please, check the list of enum_attributes and fill in the empty fields.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
  
  for en in enumAttributes.itertuples():  
    prop = properties.loc[properties['property_name'] == en.property_name]

    if len(prop) == 0:
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(en.property_name) + ' in the enum_attributes sheet not exist in the properties sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    if (prop.iloc[0]['data_type'] != 'enum'):
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(en.property_name) + ' is not a enum. Remove the property from the enum_attributes sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
  
  # Checks if enum_type column in enum_attributes sheet has permitted values  
  numberV = len(enumAttributes[enumAttributes['enum_type'] == 'number'])
  stringV = len(enumAttributes[enumAttributes['enum_type'] == 'string'])

  if ((numberV + stringV) != len(enumAttributes)):
    print("\n Some value/s in enum_type column of the enum_attributes sheet has a not allowed value.")
    print(" Please check the instructions sheet.")
    return -1
  ####################################################################



  ############### Treatment of arrayAttributes dataframe ##############
  # Checks for empty values in the property_name column, non-referenced values
  # or if the property is in the wrong sheet because of his data type 
  arrayAttrs_subset = arrayAttributes[['property_name', 'array_type', 'minimum_items']]
  if arrayAttrs_subset.isnull().sum().sum() > 0:
    print("\n Ups. Something goes wrong:")
    print ("    Excepting the array_values column, some field in array_attributes sheet is empty.")
    print('    Please, check the list of array_attributes and fill in the empty fields excepting the array_values column.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
  
  for ar in arrayAttributes.itertuples():  
    prop = properties.loc[properties['property_name'] == ar.property_name]

    if len(prop) == 0:
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(ar.property_name) + ' in the array_attributes sheet not exist in the properties sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
      
    if (prop.iloc[0]['data_type'] != 'array'):
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(ar.property_name) + ' is not a array. Remove the property from the array_attributes sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
  
  # Checks if array_type column in array_attributes sheet has permitted values  
  numberV = len(arrayAttributes[arrayAttributes['array_type'] == 'number'])
  stringV = len(arrayAttributes[arrayAttributes['array_type'] == 'string'])

  if ((numberV + stringV) != len(arrayAttributes)):
    print("\n Some value/s in array_type column of the array_attributes sheet has a not allowed value.")
    print(" Please check the instructions sheet.")
    return -1
  ####################################################################


############### Treatment of geoAttributes dataframe ##############
  # Checks for empty values in the property_name column, non-referenced values
  # or if the property is in the wrong sheet because of his data type 
  if geoAttributes.isnull().sum().sum() > 0:
    print("\n Ups. Something goes wrong:")
    print ("    Some field in geo_attributes sheet is empty.")
    print('    Please, check the list of geo_attributes and fill in the empty fields.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
  
  for geo in geoAttributes.itertuples():  
    prop = properties.loc[properties['property_name'] == geo.property_name]

    if len(prop) == 0:
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(geo.property_name) + ' in the geo_attributes sheet not exist in the properties sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
      
    if (prop.iloc[0]['data_type'] != 'geo'):
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(geo.property_name) + ' is not a geo. Remove the property from the geo_attributes sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
  ####################################################################


  ############### Treatment of objectAttributes dataframe ##############
  # Checks for empty values in the property_name column, non-referenced values
  # or if the property is in the wrong sheet because of his data type
  if objectAttributes.isnull().sum().sum() > 0:
    print("\n Ups. Something goes wrong:")
    print ("    Some field in object_attributes sheet is empty.")
    print('    Please, check the list of object_attributes and fill in the empty fields.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
  
  for ob in objectAttributes.itertuples():
    parent = properties.loc[properties['property_name'] == ob.parent_object]
    prop = properties.loc[properties['property_name'] == ob.property_name]

    if len(prop) == 0:
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(ob.property_name) + ' in the objects_attributes sheet not exist in the properties sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    if len(parent) == 0:
      print("\n Ups. Something goes wrong:")
      print('    The parent ' + str(ob.parent_object) + ' in the objects_attributes sheet not exist in the properties sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    if (parent.iloc[0]['data_type'] != 'object'):
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(ob.parent_object) + ' is not a object. Remove the property from the objects_attributes sheet.')
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
  ####################################################################




  ############### Checking for repeated properties ##############  
  duplicated_props = properties[properties.duplicated(['property_name'], keep=False)]
  dpl_visited = {}
  for dpl in duplicated_props.itertuples():
    if dpl.property_name not in dpl_visited:
      isObjt = len(objectAttributes.loc[objectAttributes['property_name'] == dpl.property_name])
      dpl_visited[dpl.property_name] = isObjt
  
  for key, value in dpl_visited.items():
    if value == 0:
      print("\n Ups. Something goes wrong:")
      print('    The property ' + str(key) + ' is repeated in the first level.')
      print('    Remember: At the same level, no two properties can exist with the same name.') 
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1

    if value > 0:
      error = 0

      repProp = duplicated_props.loc[duplicated_props['property_name'] == str(key)]
      if repProp.isnull().sum().sum() > 0:
        error = 1
      
      else:
        if len(repProp.loc[repProp[repProp.columns[4]] == 0]) > 1:
          error = 1
        
        else:
          dplParents = objectAttributes.loc[objectAttributes['property_name'] == key]
          dplParents = len(dplParents[dplParents.duplicated(['parent_object'], keep=False)])

          if dplParents > 1:
            error = 1
      
      if error == 1:
        print("\n Ups. Something goes wrong:")
        print('    There are two properties with the same name.')
        print('    One property or some of them are inside another property of type object.')
        print('    Please indicate the level at which each property is located selecting the correct parent.')
        print('    Remember: At the same level, no two properties can exist with the same name.') 
        #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
        return -1
  ###############################################################
  
  print(" Information processed!\n")

  print(" Generating Json Schema ...")

  schemaBody = ""


  # Read the Title and the Global Description from excel template
  subdmtitdesc = model_book['properties']

  subject = str(subdmtitdesc['B1'].value)
  data_model = str(subdmtitdesc['B2'].value)
  title = str(subdmtitdesc['B3'].value)
  global_description = str(subdmtitdesc['B4'].value)

  # Checks if Subject, DataModel, Title or Global Description are empty or not.
  if subject == 'None':
    print("\n Ups. Something goes wrong:")
    print('    The Subject cannot be empty.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  if data_model == 'None':
    print("\n Ups. Something goes wrong:")
    print('    The DataModel cannot be empty.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1
  
  if title == 'None':
    print("\n Ups. Something goes wrong:")
    print('    The Title cannot be empty.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1

  if global_description == 'None':
    print("\n Ups. Something goes wrong:")
    print('    The Global Description cannot be empty.')
    #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
    return -1


  ################ Add header ###############

  schemaHeaderBase = """{
  "$schema": "http://json-schema.org/schema#",
  "$id": "https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/"""+subject+"""/"""+data_model+"""/schema.json",
  "title": \"DataPorts - """ + title + """ schema\",
  "description": \"""" + global_description + """\",
  "type": "object",
  "allOf": [
    {
      "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/GSMA-Commons"
    },
    {
      "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/Location-Commons"
    },
    {
      "properties" : {"""

  schemaBody = schemaHeaderBase
  ###########################################


  schemaProperties = ""
  ngsiV2_propType = ["string", "number", "boolean", "array", "object", "date-time", "enum"]  

  # Iterating the list of properties specified in the read excel template
  for row in properties.itertuples():
    equivalent = 0

    if ((row.data_type in ngsiV2_propType) and (row[3] == 'property')):
      equivalent = 1
    if ((row.data_type == "relationship") and (row[3] == 'relationship')):
      equivalent = 1
    if ((row.data_type == "geo") and (row[3] == 'geoproperty')):
      equivalent = 1

    if equivalent == 1:
      idObj = objectAttributes.loc[objectAttributes['property_name'] == row.property_name]
      if (row[5] == 0 or str(row[5]) == 'nan') and (len(idObj) == 0):

        ############ Add property type ############  
        result = propType(row.property_name, row.data_type, enumAttributes)
        if result == -1:
          return -1
        else:
          schemaProperties += result
        ###########################################

        ####### Case if property is number ########
        if row.data_type == 'number':
          result = number(row.property_name, numberAttributes.loc[numberAttributes['property_name'] == row.property_name])
          if result == -1:
            return -1
          else:
            schemaProperties += result
        ###########################################

        ########## Case property is enum ##########
        if row.data_type == 'enum':
          result = enum(row.property_name, enumAttributes.loc[enumAttributes['property_name'] == row.property_name])
          if result == -1:
            return -1
          else:
            schemaProperties += result
        ###########################################

        ########## Case property is array #########
        if row.data_type == 'array':
          result = array(row.property_name, arrayAttributes.loc[arrayAttributes['property_name'] == row.property_name])
          if result == -1:
            return -1
          else:
            schemaProperties += result
        ###########################################

        ######## Case property is datetime ########
        if row.data_type == 'date-time':
          result = datetime() 
          if result == -1:
            return -1
          else:
            schemaProperties += result
        ###########################################

        ######## Case property is geo ########
        if row.data_type == 'geo':
          result = geoProp(row.property_name, geoAttributes.loc[geoAttributes['property_name'] == row.property_name]) 
          if result == -1:
            return -1
          else:
            schemaProperties += result
        ###########################################

        ######### Case property is object #########
        if row.data_type == 'object':
          result = objt(objectAttributes.loc[objectAttributes['parent_object'] == row.property_name], properties, numberAttributes, enumAttributes, arrayAttributes, geoAttributes, objectAttributes)
          if result == -1:
            return -1
          else:
            schemaProperties += result
        ###########################################

        ############# Add Description #############   
        result = description(row.description)
        if result == -1:
          return -1
        else:
          schemaProperties += result
        ###########################################
    
    else:
      valueV2 = 0
      valueLD = 0

      if ((row.data_type in ngsiV2_propType) or (row.data_type == 'relationship') or (row.data_type == 'geo')):
        valueV2 = 0
      else:
        valueV2 = 1
      if ((row[3] == 'property') or (row[3] == 'relationship') or (row[3] == 'geo')):
        valueLD = 0
      else:
        valueLD = 1
   
      if (valueV2 == 0) and (valueLD == 1):
        print("\n Ups. Something goes wrong:")
        print('    Property ' + str(row.property_name) + ' has a problem:\n      The selected data_type_ld value is not in the list of allowed value types.')

      elif (valueV2 == 1) and (valueLD == 0):
        print("\n Ups. Something goes wrong:")
        print('    Property ' + str(row.property_name) + ' has a problem:\n      The selected data_type value is not in the list of allowed value types.')
      
      elif (valueV2 == 1) and (valueLD == 1):
        print("\n Ups. Something goes wrong:")
        print('    Property ' + str(row.property_name) + ' some a problems:\n      The selected data_type value is not in the list of allowed value types.\n      The selected data_type_ld value is not in the list of allowed value types.')    

      else:
        print("\n Ups. Something goes wrong:")
        print('    Property ' + str(row.property_name) + ' has a problem:\n      The selected data_type value and the selected data_type_ld value are not equivalent')
        
      return -1

  schemaProperties = schemaProperties[:-1]

  schemaBody += schemaProperties
  schemaBody += """
      }
    }
  ],"""



  ############ Add required values ############
  requiredVals = properties.loc[properties['required'] == 1]

  required = """
  \"required\": [
    \"id\",
    \"type\","""

  if requiredVals.empty:
    required = required[:-1]
    required += '\n  ]'

  else:
    for req in requiredVals.itertuples():
      required += '\n    \"' + req.property_name + '\",'

    required = required[:-1]
    required += '\n  ]'

  #############################################
  
  schemaBody += required + '\n}'
  schemaBody = json.loads(schemaBody)
  

  #### Generation of the Json Schema file #####
  if save_location == ".":
      save_location = ""

  replace = -1

  if os.path.isfile(save_location+'schema.json'):
    while (replace == -1):
      print('\n A Json Schema file already exists in ' + save_location + ' location.')
      print(' Do you want to replace it? (yes=1/no=0): ', end="")

      rplc = str(input())

      if rplc != "0" and rplc != "1":
        print("\n Please insert a valid value")

      else:
        replace = int(rplc)


     

  if replace == -1 or replace == 1:
    try:        
      with open(save_location+'schema.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(schemaBody, indent = 2))
        f.close()

      if save_location == "":
        save_location = "."

      print(" Json Schema generated!")  
      print(" Json Schema saved in " + save_location)        
    
    except:
      print("\n Ups. Something goes wrong:")
      print("    Location " + save_location + " for save the " + data_model + " schema is unrreachable.")
      #sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')
      return -1
  
  else:
    print(" \nJson Schema not generated!")  
 
  #############################################
