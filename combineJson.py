"""
Purpose: combine the assignment and calendar assignments into a single json file for google
to integrate with
"""
import json

def start(a,b):
    finalJson = "final.json"
    a.update(b)
    with open(finalJson,'w') as f:
        json.dump(a,f,indent = 2)
