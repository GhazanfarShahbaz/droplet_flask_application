from apps.personal_website.requests import app as personal_website_app
from apps.tool_repository.endpoints import app as tool_app
from apps.knowledge_graph.app import app as knowledge_graph_app
from apps.projects.the_mouseion.app import app as mouseion_app


from typing import Dict
from flask import Flask

# Define a dictionary of Flask apps, where each key is an app number and each value is the corresponding app dictionary containing the applications name and module
app_list: Dict[int, dict] = {
    1: {
        "app_name"      : "Personal Website",
        "app_module"    : personal_website_app
    },
    2: {
        "app_name"      : "Tools Application",
        "app_module"    : tool_app
    },
    3: {
        "app_name"      : "Knowledge Graph",
        "app_module"    : knowledge_graph_app
    },
    4: {
        "app_name"      : "The Mouseion",
        "app_module"    : mouseion_app 
    }
}


print("Available Applications: ")

for app_index, app_dict in app_list.items():
    print(app_index, app_dict["app_name"])

print()

# Get the app number from the user
app_number_temp = input("Please Enter the number of the application you want to run: ")
app_number: int or None = None 

# Try converting app number string to a number
try:
    app_number = int(app_number_temp)
except TypeError:
    print("This is not a number")
    exit()

# If the app number is in the app_list dictionary, run the corresponding app
if app_number in app_list.keys():
    app_list[app_number]["app_module"].run()
# If the app number is not in the app_list dictionary, print an error message
else:
    print("That application number you entered does not exist]")