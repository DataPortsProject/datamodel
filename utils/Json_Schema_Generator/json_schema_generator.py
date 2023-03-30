import pandas as pd

import openpyxl

import argparse
import os
import sys
import signal
import shutil

sys.dont_write_bytecode = True

from libraries.schema.schemaV2 import *
from libraries.assets.createAssets import *

import warnings
warnings.filterwarnings('ignore')

args = argparse.ArgumentParser(description = 'Description: Generates a Json Schema of a Data Model using the data from the Excel Template')
args.add_argument('-M', '--Multiple', type=int, metavar='', nargs=1, required=True, help='Indicates if only one schema will be generated or multiple of schemas wil be generated')
args.add_argument('-st', '--stemplate', type=str, metavar='', nargs=1, required=False, help='Template for obtain the necessary data. Only for Multiple = 0')
args.add_argument('-mt', '--mtemplate', type=str, metavar='', nargs=1, required=False, help='Template for obtain the paths of the excel data sources templates and locations where save the generated schemas. Only for Multiple = 1')
args.add_argument('-mtl', '--mtlocation', type=str, metavar='', nargs=1, required=False, help='Location of the template for obtain the paths of the excel data sources templates and locations where save the generated schemas ended with \ character. Use . without \ for local location or the full path for a specific location. Only for Multiple = 1')
args.add_argument('-stl', '--stlocation', type=str, metavar='', nargs=1, required=False, help='Location of the excel data source template ended with \ character. Use . without \ for local location or the full path for a specific location. Only for Multiple = 0')
args.add_argument('-srl', '--srlocation', type=str, metavar='', nargs=1, required=False, help='Location where save the generated schema ended with \ character. Use . without \ for local location or the full path for a specific location. Only for Multiple = 0')
args = args.parse_args()

if int(args.Multiple[0]) == 0:
  if (str(args.stemplate) == 'None' or str(args.stlocation) == 'None' or str(args.srlocation) == 'None'):
    print('\nFor the selected mode, the script needs:')
    print('    - The name of the data source information excel template. Specified by the command: -st or --stemplate')
    print('    - The location of the data source information excel template ended with \ character. Specified by the command: -stl or --stlocation')
    print('    - The location where the generated schema will be saved eneded with \ character. Specified by the command: -srl or --srlocation')
    sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')

if int(args.Multiple[0]) == 1:
  if (str(args.mtemplate) == 'None' and str(args.mtlocation) == 'None'):
    print('\nFor the selected mode, the script needs:')
    print('    - The name of the excel template that contains the paths of the source data excel templates and the save location for the schemas that will be generated ended with \ character. Specified by the command: -mt or --mtemplate')
    print('    - The location of the excel template that contains the paths of the source data excel templates and the save location for the schemas that will be generated. Specified by the command: -mtl or --mtlocation')
    sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')

signal.signal(signal.SIGINT, lambda x, y: sys.exit("\n\nExecution terminated by User\nReturning to the previous state"))


def getData():
  print("\nReading indicated template ...")

  ################# Read Data Section ################

  # Create a dataframe for fill it with the name and the locations of the template and the save location of the schema that will be generated
  templates_locations = ""

  # If mode multiple == 0
  if int(args.Multiple[0]) == 0:

    # Get the input parameters
    template_name = str(args.stemplate[0])
    template_location = str(args.stlocation[0])
    save_location = str(args.srlocation[0])

    if template_location == ".":
      template_location = ""
    
    if save_location == ".":
      save_location = ""

    # Add the name and the location of the template to the dicctionary
    templates_locations = {'template_name':  [template_name], 'template_location': [template_location], 'save_location': [save_location]}
    templates_locations = pd.DataFrame(templates_locations)

  # If mode multiple == 1
  if int(args.Multiple[0]) == 1:

    # Get the input parameters
    template_name = str(args.mtemplate[0])
    template_location = str(args.mtlocation[0])

    if template_location == ".":
      template_location = ""

    # Read the data from the multiple template
    try:
      locations_multiple = pd.read_excel(template_location+template_name, 'paths')

      model_book = openpyxl.load_workbook(template_location+template_name)

      tplte = model_book['instructions']
      check_valid_template = str(tplte['D1'].value)
    
    except:
      print("\n Ups. Something goes wrong:")
      print("    " + template_name + " file not found or location " + template_location + " is unrreachable.")
      sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')

    if check_valid_template == "/$mtfjsg$/":
      templates_locations = locations_multiple

    else:
      print("\nThe multiple paths excel template " + template_name + " located in " + template_location + " is not valid!")
      sys.exit()

  print("Indicated template readed!")

  # Iterate the dicctionary 
  for tl in templates_locations.itertuples():

    # Checks if the template and the script are in the current location. If not, the script ends
    try:
      template_name = str(tl.template_name)
      template_location = str(tl.template_location)

      if template_location == ".":
        template_location = ""

      model_book = openpyxl.load_workbook(template_location+template_name)

    except:
      print("\n Ups. Something goes wrong:")
      print("    " + template_name + " file not found or location " + template_location + " is unrreachable.")
      sys.exit('\nJson Schema not generated.\nExecution terminated with error\s.\n')

    tplte = model_book['instructions']
    check_valid_template = str(tplte['D1'].value)


    if check_valid_template == "/$stfjsg$/":

      # Transforms the template sheets to dataframes 

      # NGSI-V2 data
      properties = pd.read_excel(template_location+template_name, 'properties', skiprows = 7)
      numberAttributes = pd.read_excel(template_location+template_name, 'number_attributes')
      enumAttributes = pd.read_excel(template_location+template_name, 'enum_attributes')
      arrayAttributes = pd.read_excel(template_location+template_name, 'array_attributes')
      geoAttributes = pd.read_excel(template_location+template_name, 'geo_attributes')
      objectAttributes = pd.read_excel(template_location+template_name, 'object_attributes')

      # NGSI-LD data

      #################################################

      print('\n###########################')
      print("Template " + template_location+template_name + " readed!")
      print("Processing " + template_location+template_name + "template ...\n")

      open = 0
      exitsTmp = 0

      fullPath = os.path.abspath(str(tl.save_location)) + "\\"

      # Checks if folder tmpSv exists before execution
      if os.path.isdir(fullPath+'tmpSv'):
        exitsTmp = 1

        print('Temporary folder tmpSv exists before execution in the save location.')
        print('Please remove the temporary folder located at ' + tl.save_location)

        print('\nTemplate ' + template_location+template_name + ' not processed correctly.')
        print('###########################')

      if exitsTmp == 0:
        # Create a temporary folder to save the files and folders of the save folder of the json schema, if they already exist      
        if os.path.isfile(fullPath+'schema.json'):
          try:
            exitsTmp = 1
            shutil.copytree(fullPath, fullPath+'tmpSv', ignore=shutil.ignore_patterns('*.xlsx', '.py'))
          except shutil.Error as err:
            open = 1

        if open == 0:
          # NGSI-V2 Json Schema Generation
          result = generationV2(model_book, properties, numberAttributes, enumAttributes, arrayAttributes, geoAttributes, objectAttributes, str(tl.save_location))
          assetsError = 0

          # If the NGSI-V2 and NGSI-LD Json Schema generation finish without problems, the Assets will be generated
          if (result != -1):

            subdmtitdesc = model_book['properties']

            subject = str(subdmtitdesc['B1'].value)
            data_model = str(subdmtitdesc['B2'].value)
            global_description = str(subdmtitdesc['B4'].value)

            print("\n Creating Assets ...")
            result = createAssets(save_location, subject, data_model, global_description)
            if result == -1:
              assetsError = 1

          if (result == -1): 
            # If exists a temporary folder, in case of an error, the previous elements that are in that temporary folder
            if (exitsTmp == 1) or (exitsTmp == 0 and assetsError == 1):
              if os.path.isdir(fullPath+'examples'):
                  shutil.rmtree(fullPath+'examples')

              if os.path.isdir(fullPath+'doc'):
                shutil.rmtree(fullPath+'doc')
              
              if os.path.isfile(fullPath+'README.md'):
                os.remove(fullPath+'README.md')

              if os.path.isfile(fullPath+'schema.json'):
                os.remove(fullPath+'schema.json')

            if exitsTmp == 1:
              filesExcpt = os.listdir(fullPath+'tmpSv')
              files = []
              for fi in filesExcpt:
                ext = fi.split('.')              
                if (len(ext) < 2):
                  files.append(fi)                
                else:
                  if (ext[1] != 'py' and ext[1] != 'xlsx'):
                    files.append(fi)

              for fi in files:             
                if os.path.isfile(fullPath+'tmpSv\\'+fi):
                  shutil.copy2(fullPath+'tmpSv\\'+fi, fullPath)
                if os.path.isdir(fullPath+'tmpSv\\'+fi):
                  shutil.move(fullPath+'tmpSv\\'+fi, fullPath) 

            print('\nTemplate ' + template_location+template_name + ' not processed correctly.')
            print('###########################')       
          
          else:
            print("\n Assets created!")

            print("\n" + template_location+template_name + "template processed!")
            print('###########################')

        # Checks that the excel template is not open or that there were no errors during the creation of the temporary folder
        if open == 1:
          print('\n Ups. Something goes wrong:')
          print('    ' + template_name + 'template cannot be open during the generation process or the necessary temporary files could not be generated')
          
          print('\nJson Schema not generated.')
          print('###########################')

        # If it exists, after the generation process the temporary folder will be deleted
        if exitsTmp == 1:
          shutil.rmtree(fullPath+'tmpSv')

    else:
      if template_location == "":
        template_location = "."

      print("\nThe data source excel template " + template_name + " located in " + template_location + " is not valid!")

  print("\nExecution terminated!\n")








# Starting the Json Schema generation
if __name__ == '__main__':
  getData()

