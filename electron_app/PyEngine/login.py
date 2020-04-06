import sys
import json
from SakaiPy import SakaiPy
import json




url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

# this is the script the javascript executes importing another python file for turing machines
def input():
    info = {
        'username': username,
        'password': password,
        'baseurl': url
    }

    sak = SakaiPy.SakaiPy(info)
    validate = sak.session.get_current_user_info()
    if validate["displayId"].lower() == username.lower():
        print("true")
    else:
        print("false")


input()
sys.stdout.flush()