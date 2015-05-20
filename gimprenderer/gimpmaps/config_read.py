'''
Created on May 20, 2015

@author: mucx
'''

import os
import json

config_file = os.getcwd() + "/conf/config_test.json"
print config_file

read_file = open(config_file, "r")

json_config = json.load(read_file)

print json_config["osm_db"]["host"]
print json_config["osm_db"]["user"]
print json_config["osm_db"]["password"]
print json_config["osm_db"]["db_name"]

print json_config["style"]["style_file_path"]