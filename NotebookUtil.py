TOKEN = b"REPLACE_WITH_YOUR_OWN"
WORKSPACE_DOMAIN = "westus2.azuredatabricks.net"

import base64
import requests
import json
import sys
import os

def import_notebook(local_file_path, workspace_notebook_path):
    try:
        with open(local_file_path, "rb") as f:
            local_file_content = base64.b64encode(f.read()).decode('ascii')
        response = requests.post(
        "https://%s/api/2.0/workspace/import" % (WORKSPACE_DOMAIN),
            headers = {"Authorization": b"Basic " + base64.standard_b64encode(b"token:" + TOKEN)},
            json = {
                "content": local_file_content,
                "path": workspace_notebook_path,
                "language": "PYTHON",
                "overwrite": "true",
                "format": "SOURCE"
            }
        )
        return response
    except Exception as ex:
        print(ex)

def list_all_notebook(workspace_path):
    try:
        response = requests.get(
        'https://%s/api/2.0/workspace/list' % (WORKSPACE_DOMAIN),
            headers={"Authorization": b"Basic " + base64.standard_b64encode(b"token:" + TOKEN)},
            json = {
                "path": workspace_path,
            }
        )
        return response
    except Exception as ex:
        print(ex)

def print_response(response):
    print("[Status Code]: " + str(response.status_code))
    print("[Response Content]: " + str(response.content))

def main():
    # print command line arguments
    if TOKEN == b"REPLACE_WITH_YOUR_OWN":
        print("Replace TOKEN with personal access token") 
        exit(1)  

    if (len(sys.argv) < 2):
        print("No action specified") 
        exit(1)

    action = sys.argv[1].upper()

    if action == "DEPLOY":
        local_file_path_arg = sys.argv[2]
        workspace_notebook_path_arg = sys.argv[3]
        response = import_notebook(local_file_path_arg, workspace_notebook_path_arg)
        print_response(response)
    elif action == "DEPLOYALL":
        local_notebook_register_path_arg = sys.argv[2]
        if local_notebook_register_path_arg is None:
            print("Specify a comma-separated list [NOTEBOOK_LOCAL_PATH],[NOTEBOOK_REMOTE_PATH] to deploy all")
        with open(local_notebook_register_path_arg, "r") as f:
            for line in f:
                fields = line.split(",")
                notebook_path_local = fields[0]
                notebook_path_remote = fields[1]
                print(("Deploy from local: {} to remote: {}").format(notebook_path_local, notebook_path_remote))
                response = import_notebook(notebook_path_local, notebook_path_remote)
                print_response(response)
    elif action == "LISTALL":
        response = list_all_notebook("/")
        print_response(response)
    else:
        print("Action not recognized")
        print("Example1: python NotebookUtil.py Deploy ./LOCAL_NOTEBOOK.py /Users/YOUR_ALIAS@ame.gbl/XIXI")
        print("Example2: python NotebookUtil.py LISTALL")
        print("Example3: python NotebookUtil.py DEPLOYALL ./NOTEBOOK_PATH_CONFIG.csv")
    
if __name__ == "__main__":
    main()