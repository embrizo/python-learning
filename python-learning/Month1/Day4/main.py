import temperature as temp 
import utils.finance as finance
import utils.converter as converter
import utils.math_untils as math_untils
import os
import json

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "student.json")

with open(DATA_FILE) as file:  
    student = json.load(file)
    
print(student)   


