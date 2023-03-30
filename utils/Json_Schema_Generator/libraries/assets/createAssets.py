import os
import shutil
import json

from .examples.exampleJson import *
from .examples.normalizedJson import *

def readmeText(subject, datamodel, dataMDescription):
  # Define the text of the Readme.md file
  readme = '''# ''' + datamodel + '''
  This section will contains the description of the Data Model

  ## ''' + dataMDescription + '''
  This section will contains the description of the Type of the Data Model

  ### Specification

  Link to the [specification in English](https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/'''+subject+'''/'''+datamodel+'''/doc/spec_EN.md")

  Enlace a la [especificación en Español](https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/'''+subject+'''/'''+datamodel+'''/doc/spec_ES.md")

  ### Examples

  Link to the [example](https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/'''+subject+'''/'''+datamodel+'''/examples/example.json) (keyvalues) for NGSI v2

  Link to the [example](https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/'''+subject+'''/'''+datamodel+'''/examples/example.jsonld) (keyvalues) for NGSI-LD - TBD

  Link to the [example](https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/'''+subject+'''/'''+datamodel+'''/examples/example-normalized.json) (normalized) for NGSI-V2

  Link to the [example](https://egitlab.iti.es/dataports/data_processing/datamodel/-/tree/master/'''+subject+'''/'''+datamodel+'''/examples/example-normalized.jsonld) (normalized) for NGSI-LD - TBD'''
  
  return readme


def createAssets(creationPath, subject, datamodel, dataMDescription):

  # Check if the assets already exist in the folder. If they exist, they will be eliminated
  try:    
    if os.path.isdir(creationPath+'examples'):      
      print("\n  Removing the examples folder ...")
      shutil.rmtree(creationPath+'examples')
      print("  examples folder removed!")
  except:
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the deletion of the examples folder.")
    return -1

  try:    
    if os.path.isdir(creationPath+'doc'):
      print("\n  Removing the doc folder ...")
      shutil.rmtree(creationPath+'doc')
      print("  doc folder removed!")
  except:
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the deletion of the doc folder.")
    return -1
  
  try:    
    if os.path.isfile(creationPath+'README.md'):
      print("\n  Removing the README.md file ...")
      os.remove(creationPath+'README.md')
      print("  README.md file removed!")
  except:
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the deletion of the README.md file.")
    return -1



  # Get the text for the README 
  readme = ""
  readmeError = 0
  try:  
    readme = readmeText(subject, datamodel, dataMDescription)
  except:
    readmeError = 1
  #############################

  # Generate a json keyvalues example based on the json schema    
  jsonExampleError = 0
  jsonExample = ""
  try:
    jsonExample = createJsonExample(creationPath, datamodel)
  except:
    jsonExampleError = 1
  ############################################

  # Generate a json normalized example based on the json schema    
  normalizedJsonError = 0
  normalizedJsonExample = ""
  try:
    normalizedJsonExample = createNormalizedJsonExample(creationPath, datamodel)
  except:
    normalizedJsonError = 1
  ############################################

  # Generate a json-ld keyvalues example based on the json schema    
  jsonldExampleError = 0
  jsonldExample = ""
  try:
    jsonldExample = ""
  except:
    jsonldExampleError = 1
  ############################################

  # Generate a jsonld normalized example based on the json schema    
  normalizedldJsonError = 0
  normalizedldJsonExample = ""
  try:
    normalizedldJsonExample = ""
  except:
    normalizedldJsonError = 1
  ############################################




  # Generate the english spec file    
  enSpecError = 0
  enSpecDescription = ""
  try:
    enSpecDescription = ""
  except:
    enSpecError = 1
  ############################################

  # Generate the spanish spec file    
  esSpecError = 0
  esSpecDescription = ""
  try:
    esSpecDescription = ""
  except:
    esSpecError = 1
  ############################################




  ## Creates the necessary folders ##  
  try:
    print("\n  Creating the examples and doc folders ...")
    os.mkdir(creationPath+'examples')
    os.mkdir(creationPath+'doc')
    print("  examples and doc folders created!")
  except:
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the examples and doc folders creation.")
    return -1
  ##################################





  ###### Creates README.md ######  
  try:
    print("\n  Creating the README.md ...")
    with open(creationPath+'README.md', 'w', encoding='utf-8') as f:
      f.write(readme)
      f.close()
    print("  README.md created!")
  except:
    readmeError = 1
  if (readmeError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the README.md file generation.")
    return -1
  ###############################

  ###### Creates the example files using the previous generated json examples ######  
  try:
    print("\n  Creating the example.json ...")
    with open(creationPath+'examples\example.json', 'w', encoding='utf-8') as f:
      f.write(json.dumps(jsonExample, indent = 2))
      f.close()
    print("  example.json created!")
  except:
    jsonExampleError = 1  
  if (jsonExampleError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the example.json file generation.")
    return -1

  try:  
    print("\n  Creating the example.jsonld ...")
    with open(creationPath+'examples\example.jsonld', 'w', encoding='utf-8') as f:
      f.write(json.dumps(jsonldExample, indent = 2))
      f.close()
    print("  example.jsonld created!")
  except:
    jsonldExampleError = 1
  if (jsonldExampleError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the example.jsonld file generation.")
    return -1

  try:
    print("\n  Creating the example-normalized.json ...")
    with open(creationPath+'examples\example-normalized.json', 'w', encoding='utf-8') as f:    
      f.write(json.dumps(normalizedJsonExample, indent = 2))
      f.close()
    print("  example-normalized.json created!")
  except:
    normalizedJsonError = 1
  if (normalizedJsonError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the example.json file generation.")
    return -1

  try:
    print("\n  Creating the example-normalized.jsonld ...")
    with open(creationPath+'examples\example-normalized.jsonld', 'w', encoding='utf-8') as f:
      f.write(json.dumps(normalizedldJsonExample, indent = 2))
      f.close()
    print("  example-normalized.jsonld created!")
  except:
    normalizedldJsonError = 1
  if (normalizedldJsonError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the example-normalized.jsonld file generation.")
    return -1
  ##################################

  ###### Creates de spec files in doc folder using the previous generated spec descriptions ######
  try:  
    print("\n  Creating the spec_EN.md ...")
    with open(creationPath+'doc\spec_EN.md', 'w', encoding='utf-8') as f:      
      f.write(enSpecDescription)
      f.close()
    print("  spec_EN.md created!")
  except:
    enSpecError = 1
  if (enSpecError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the spec_EN.md file generation.")
    return -1

  try:  
    print("\n  Creating the spec_ES.md ...")
    with open(creationPath+'doc\spec_ES.md', 'w', encoding='utf-8') as f:
      f.write(esSpecDescription)
      f.close()
    print("  spec_ES.md created!")
  except:
    esSpecError = 1
  if (esSpecError == 1):
    print("\n  Ups. Something goes wrong:")
    print ("     An error occurred during the spec_ES.md file generation.")
    return -1
  #################################################

  return 1
