'''
Created on Jul 18, 2015

@author: mucx

This module test whether a style or config JSON is valid. Works only with files
stored in the default directories.
'''

import json, os, inspect
from jsonschema import validate

def get_filepath():
    filepath = os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()
            )
        )
    )
    return filepath

def validate_config(file_in):

    read_file = open(get_filepath() + "/div/schema_config.json", "r")              
    schema = json.load(read_file)
    
    read_file = open(get_filepath() + "/conf/" + file_in, "r")            
    json_data = json.load(read_file)
    
    validate(json_data, schema)
    
    print "Valid :)"
    
def validate_style(style_name):

    read_file = open(get_filepath() + "/div/schema_style_0.json", "r")              
    schema = json.load(read_file)
    
    read_file = open(get_filepath() + "/styles/" + style_name + "/style.json", "r")            
    json_data = json.load(read_file)
    
    validate(json_data, schema)
    
    print "Valid :)"
    
validate_config("config_dd_embroid_map.json")
validate_style("embroid")