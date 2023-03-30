# Description

With the execution of this script, developed with Python, a document of the Json Schema type corresponding to a determinated data model will be generated together with its assets, using an Exel file as data source.

# Version
The current version of the tool is: ```2```

# Example

For the execution of the script, the following instruction must be used:

```
py json_schema_generator.py -M 0 -st [template_name] -stl [template_location_path] -srl [schema_save_location_path]
```

For a real demostration, staying in this folder, and using the template of the example folder, the instructon will be:


```
py json_schema_generator.py -M 0 -st json_vessel_datamodel.xlsx -stl ./example/ -srl ./example/SaveSchema/
```

# Requisites

For the script to work correctly, the following requirements will be necessary:

* ```Pythonn 3.10.x```
* Python libraries:
    * ```pandas```
    * ```openpyxl```
    * ```json```
    * ```argparse```
    * ```os```
    * ```sys```
    * ```signal```
    * ```shutil```
    * ```datetime```
    * ```random```
    * ```string```
* ```Microsoft Office 2016, 2019 or 2021```

# Resources

This tool contain the next files:

* ```json_schema_generator.py```
* ```schemaV2.py```
* ```createAssets.py```
* ```exampleJson.py```
* ```normalizedJson.py```
* ```json_schema_template.xlsx```
* ```json_schema_multi.xlsx```

This tool contains five files that will be in charge of generating the Json Schema and its assets. 

The main file of the tool is ```json_schema_generator.py```. This will be the script that must be executed to start the generation proccess. The next file that the tool will use is ```schemaV2.py```, which objective is to generate the **schema.json** and store it in the indicated save location. The third file used, called ```createAssets.py``` will be in charge of creating the assets that will be related to the Json Schema. The fourth file that is called ```exampleJson.py```, will generates a json v2 key values example. The last file called ```normalizedJson.py``` will generate a json v2 normalized exmaple.

The order in which the tool files are called is as follows:  
```json_schema_generator.py``` --> ```schemaV2.py``` --> ```createAssets.py``` --> ```exampleJson.py```  ```normalizedJson.py```

For the tool to work properly, these files must be located according to the following structure:
```
Folder:
│   json_schema_generator.py    
│
└───libraries:
    └───schema:    
    │       schemaV2.py
    │
    └───assets:    
        │   createAssets.py
        │   
        └───examples:
            │   exampleJson.py
            │   normalizedJson.py
```

Apart from the Python files, the tool will also contain two Excel files:

The ```json_schema_template.xlsx``` file will be the one that will have to be filled with the properties and the information that the Json Schema will contain. This file will be necessary for the operation of the tool.

The second file, called ```json_schema_multi.xslx```, will be used in case several Json Schemas are to be generated at the same time. This file will be for the optional use.

# Advanced Options

## Python files:

This tool also contains two execution modes. The first one, called ```simple mode```, is used to generate a single Json Schema file together with its assets using a single Excel template. The second mode, called ```multiple mode```, is used to recursively generate various Json Schemas along with their assets. To use this second mode, the use of the ```json_schema_multi.xlsx``` file is neccsary.

An example of the instrucction to use for multiple mode is:

```
py json_schema_generator.py -M 1 -mt [multi_template_name] -mtl [multi_template_location_path]
```

Using the ```--help``` option, the script execution options can be checked.

In the case that save location will contain a Json Schema file, the script will ask user if the old Json Schema should be replaced or not. Until the answer of ther user, the script will be waiting.

In the case that the Json Schema should be replaced, the schema file and all old assets will be removed to generate the new files. In the case that the Json Schema should not be replaced, the generation of the current Json Schema will finish and any old file will not be deleted.

If the script detects an internal error or a problem related to the information read from the excel files, the generation of the Json Schema related with the used template in that moment, will stop and no file be generated or replaced, and at the same time, it will be displayed through the console, the reason why the generation of the files has not been done. Also in the case that in the save folder already exist a generated Json Schema, if and error occurs, the files that have been generated will be deleted and the previous information will be restored.

## Excel files:

The first sheet of each of the Exel files will contain the instructions that the user must follow to fill in each of them.

# Validation

The generated Json Schema/s can be validated using the following tool: https://json-schema-validator.herokuapp.com/syntax.jsp

# IMPORTANT

In the save location ```There should be no more files inside the folder as they can be deleted```. ```Only``` the ```.py files or .xlsx files``` belonging to the tool ```can be putting inside``` if the save location will be the same as the source location.
